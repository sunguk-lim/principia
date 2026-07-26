---
id: nccl
title: NCCL
summary: NCCL (NVIDIA Collective Communications Library) is the software library that implements multi-GPU collective-operations — above all all-reduce, where every GPU contributes a value…
type: concept
tags: [gpu]
prereqs: [all-reduce, nvlink, collective-operation, reduce-scatter, all-gather]
sources:
  - "linux-internals-complete.html — NCCL — the choreographer for collective operations; NCCL vs NVLink — they're not alternatives, they're layers; NCCL — ring all-reduce"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# NCCL

## Summary

**NCCL** (NVIDIA Collective Communications Library) is the **software library that
implements multi-GPU [[collective-operation]]s** — above all [[all-reduce]], where every
GPU contributes a value (its gradient), the values are summed, and the identical total
is handed back to every GPU. NCCL is *not* a wire and not a faster version of one: it is
the **algorithm and orchestration layer** that decides *who sends which bytes to whom,
and in what order*, then drives that traffic over whatever fast interconnect is
available — [[nvlink]] between GPUs in one box, or a network link between separate
machines. Its signature contribution is the **ring all-reduce** algorithm, a way of
performing an all-reduce so that every link is loaded evenly and works in parallel,
making the cost of combining the data roughly independent of how many GPUs participate.

## Grounded explanation

### What NCCL is, and the layer it occupies

The [[nvlink]] node ended on a problem-shaped note: when a model is split across many
GPUs, those GPUs must continuously recombine their pieces, and a wide, CPU-bypassing wire
keeps that recombination from throttling the machine. But a wire only moves bytes between
two endpoints; it has no notion of "sum these eight gradients and give everyone the
total." Something has to *decide* that — to break a collective operation into a precise
schedule of point-to-point sends and receives, issue them in the right order, and combine
the numbers as they arrive. That something is **NCCL**.

So NCCL and [[nvlink]] are **layers, not alternatives**. [[nvlink]] is the physical
transport: the wire carrying raw bytes. NCCL is the library running on the CPU that, given
a request like [[all-reduce]] across all the GPUs, plans the data movement and launches
the small GPU programs (helper *kernels* — short routines a GPU runs) that actually read
from local GPU memory, push bytes across the wire to a neighbor, and add what arrives. The
CPU itself never touches the bulk data; it is a **dispatcher**, writing launch and
synchronization commands. The bytes flow GPU-to-GPU over the wire. A useful way to hold
the distinction: NVLink alone is *just bytes* — it does not know what they mean; NCCL is
what knows the bytes are eight gradients that should become one sum, and orchestrates the
sends and receives that make it so.

This separation is also why NCCL is portable. The *same* request — combine the gradients —
runs unchanged whether the GPUs sit in one server wired by [[nvlink]], or share only the
ordinary host bus (commonly PCIe, an order of magnitude slower), or live in *different
machines* connected by a data-center network such as InfiniBand. NCCL probes the hardware
at startup, picks the fastest transport each pair of GPUs can reach, and runs the identical
algorithm over it. The training code says "all-reduce the gradients"; NCCL silently routes
that over [[nvlink]] when it can, and the program is none the wiser — only faster or slower.

### Why a naive all-reduce wastes the wire

The defining question for NCCL is *how* to perform the [[all-reduce]] well. Recall from
[[all-reduce]] that, *as a meaning*, it is reduce-then-broadcast: combine every GPU's value
into one result, then deliver that result to all of them. The obvious implementation makes
that literal: pick one GPU as the gatherer, have all the others send it their data, sum it
there, then send the total back out to everyone.

This is correct but squanders the hardware. Every byte funnels through the one gatherer's
single link, so that link is the bottleneck while every *other* link sits idle. With many
GPUs and large gradients this serializes the whole operation onto one wire — exactly the
kind of single-pipe bottleneck [[nvlink]] was introduced to escape, now reintroduced by a
bad *algorithm* even though the wire is fast. The fast transport is wasted if only one of
its links is busy at a time. The real engineering problem is therefore: schedule the sends
so that **every** link carries data **at once**, and none is a chokepoint.

### Ring all-reduce: the algorithm

NCCL's answer is **ring all-reduce**. Arrange the `N` participating GPUs in a logical
**ring** — `GPU 0 → GPU 1 → GPU 2 → … → GPU (N−1) → GPU 0` — where each GPU has exactly one
*successor* it sends to and one *predecessor* it receives from. Split each GPU's data into
`N` equal **chunks**, one per position in the ring. The operation then runs in two phases.

**Phase 1 — [[reduce-scatter]].** This phase ends with each GPU holding the *complete sum* of
**one** chunk (a different chunk per GPU), rather than the whole result. It takes `N−1`
steps. At each step, every GPU simultaneously sends one chunk to its successor and receives
a chunk from its predecessor, and **adds** the received chunk into the matching chunk it
already holds. Because the GPUs are staggered — each starts by sending a different chunk
index — the partial sums accumulate as they travel: a chunk picks up one more GPU's
contribution at every hop. After `N−1` hops, each chunk has visited all `N` GPUs and been
summed at each, so the GPU where that chunk's accumulation comes to rest holds its
**fully-summed** value. The key invariant: *at every step, all `N` links are carrying a
chunk and all `N` GPUs are adding* — no link idles, nothing funnels through one node.

**Phase 2 — [[all-gather]].** Now the fully-summed chunks are scattered one-per-GPU; everyone
needs *all* of them. This is the broadcast half of [[all-reduce]], done as another `N−1`
steps around the same ring. Each GPU sends the finished chunk it owns to its successor,
which stores it and forwards it on; after `N−1` hops every finished chunk has circulated to
every GPU. No addition happens here — the chunks are already complete; they are merely
copied around. At the end, **every GPU holds every fully-summed chunk** — i.e. the entire
summed result — which is precisely the [[all-reduce]] outcome: the same combined value
sitting on every GPU.

### Why it is bandwidth-optimal

Two properties make ring all-reduce the efficient choice, and both trace back to the
"keep every link busy" goal.

First, **even loading and parallelism.** In every step of both phases, each GPU sends one
chunk and receives one chunk, and all links act at the same time. There is no central
gatherer, so no single link is a bottleneck; the work is spread uniformly around the ring.

Second, and the reason it *scales*: count the bytes each GPU moves. Let one GPU's full data
be of size `S`, so each chunk is `S/N`. Each GPU sends one chunk per step, over `N−1` steps
of reduce-scatter and `N−1` steps of all-gather — `2 × (N−1)` chunks of size `S/N` each.
That is `2 × (N−1)/N × S` bytes per GPU. As `N` grows, the factor `(N−1)/N` climbs toward 1,
so each GPU moves at most about `2S` — *roughly twice its own data, no matter how many GPUs
join.* This is the non-obvious, "magic-looking" payoff that deserves its justification: a
naive scheme makes the gatherer move on the order of `N × S` bytes (growing with the
cluster), whereas the ring caps per-GPU traffic near `2S` regardless of `N`, because the
data is sliced into `N` chunks and the work is shared all the way around the ring instead of
piling onto one node. Combine that with running over [[nvlink]]'s hundreds-of-gigabytes-
per-second links instead of the slow host bus, and the gradient combine that data-parallel
training must perform *every single step* stops being the thing that throttles the run.

### Worked instance: 4 GPUs combining gradients

Take **`N = 4` GPUs**, each holding a gradient vector of four numbers (one chunk per GPU,
so chunk = one number here, kept tiny to make every add visible). Label chunks `a,b,c,d` by
position:

- `GPU0 = [a0, b0, c0, d0] = [1, 2, 3, 4]`
- `GPU1 = [a1, b1, c1, d1] = [5, 6, 7, 8]`
- `GPU2 = [a2, b2, c2, d2] = [9, 10, 11, 12]`
- `GPU3 = [a3, b3, c3, d3] = [13, 14, 15, 16]`

The correct all-reduce result is the per-position sum on **every** GPU:
`a = 1+5+9+13 = 28`, `b = 2+6+10+14 = 32`, `c = 3+7+11+15 = 36`, `d = 4+8+12+16 = 40`, i.e.
every GPU should end at `[28, 32, 36, 40]`. The ring is `0 → 1 → 2 → 3 → 0`. Total steps:
`2 × (4−1) = 6` — three reduce-scatter, three all-gather. Follow chunk `a`, which is destined
to come to rest fully summed on GPU1.

**Reduce-scatter, step 1.** GPU0 sends `a0 = 1` to GPU1; GPU1 adds it to its own `a1 = 5`,
getting `a = 1+5 = 6`. (In parallel GPU1 sends `b1` to GPU2, GPU2 sends `c2` to GPU3, GPU3
sends `d3` to GPU0 — every link busy, every GPU adding.)

**Reduce-scatter, step 2.** GPU1 sends its running `a = 6` onward to GPU2; GPU2 adds its
`a2 = 9`, getting `a = 6+9 = 15`.

**Reduce-scatter, step 3.** GPU2 sends `a = 15` to GPU3; GPU3 adds its `a3 = 13`, getting
`a = 15+13 = 28`. Chunk `a` has now visited all four GPUs and been summed at each. By the
staggered schedule it has come to rest where the algorithm intends, and GPU3 forwards it one
more hop in the handoff so that **GPU1 owns the finished `a = 28`** — exactly matching the
hand-derived `28` above. By the same staggered process, simultaneously, GPU2 ends holding
the finished `b = 32`, GPU3 the finished `c = 36`, and GPU0 the finished `d = 40`. Each GPU
now owns exactly **one** completed chunk — the reduce-scatter invariant.

**All-gather, steps 4–6.** Now circulate those four finished numbers around the same ring so
everyone gets all four. Step 4: each owner sends its finished chunk to its successor (GPU1
sends `a = 28` onward, GPU2 sends `b = 32`, etc.); the receiver stores it. Steps 5 and 6
forward each chunk one more hop apiece. After three hops, `a = 28`, `b = 32`, `c = 36`,
`d = 40` have each reached all four GPUs. Every GPU now holds `[28, 32, 36, 40]` — the
identical summed gradient.

This instance is non-degenerate: all four GPUs participate, every chunk index is exercised,
both phases run their full `N−1 = 3` steps (no phase collapses to zero), and the additions
actually accumulate across hops rather than any term staying at its starting value. Run over
[[nvlink]], each of the four links carries one chunk per step in parallel — none idle, none a
bottleneck — which is exactly the even-loading property that makes the scheme efficient.

### The takeaway

NCCL is the **library and algorithm layer** for multi-GPU collectives. Its central job is to
turn a request like [[all-reduce]] into a concrete, evenly balanced schedule of sends,
receives, and additions, then drive that schedule over a fast transport. Its signature method,
**ring all-reduce**, keeps every link of the interconnect busy at once and caps each GPU's
traffic near twice its own data regardless of cluster size — so combining gradients does not
grow more expensive as GPUs are added. NCCL supplies the *what to do*; [[nvlink]] supplies the
*wire it runs on*. Together — "NCCL over NVLink" — they make the gradient combine that
data-parallel training repeats every step fast enough that the many-GPU machine stays busy
instead of stalling on communication.

## Prerequisites

- [[all-reduce]]
- [[nvlink]]
- [[collective-operation]]
- [[reduce-scatter]]
- [[all-gather]]

## Sources

- linux-internals-complete.html, *NCCL — the choreographer for collective operations* — NCCL as a userspace CPU library that plans the collective, launches helper kernels on each GPU, and synchronizes, while the CPU dispatches rather than moves bytes; *NCCL vs NVLink — they're not alternatives, they're layers* — software-vs-hardware layering and transport selection (NVLink / PCIe / InfiniBand) for the same `all_reduce` call; *NCCL — ring all-reduce* — the ring arrangement, reduce-scatter and all-gather phases, and the `2 × (N−1)/N × gradient_size` bandwidth-optimality argument.
