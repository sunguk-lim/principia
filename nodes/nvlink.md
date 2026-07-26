---
id: nvlink
title: NVLink
summary: NVLink is a dedicated, high-bandwidth, low-latency wire that connects GPUs directly to each other (and, in some packages, a GPU directly to a CPU), so that data living in one…
type: concept
tags: [gpu]
prereqs: [cpu-vs-gpu]
sources:
  - "linux-internals-complete.html — Multi-GPU: how GPUs talk to each other (three mechanisms, increasingly direct); What NVLink looks like in practice (UVA, a load that routes over NVLink); NVLink C2C and NVL72 (chip-to-chip coherence; rack-scale fabric)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# NVLink

## Summary

**NVLink** is a dedicated, high-bandwidth, low-latency wire that connects GPUs
**directly to each other** (and, in some packages, a GPU directly to a CPU), so that
data living in one GPU's memory can move into another's without detouring through the
slow general-purpose bus that normally links a GPU to its host computer. It exists
because of a limit baked into the [[cpu-vs-gpu]] story: a single GPU wins on
**throughput** by feeding thousands of arithmetic lanes from its own on-board memory, but
that memory and that lane count are *finite*. A model too big for one GPU must be split
across many — which turns one chip's throughput bet into a many-chip bet, and that only
pays off if the chips can **exchange** their pieces of the work fast enough. Run that
exchange over the ordinary host bus (tens of gigabytes per second) and it becomes the
bottleneck: the expensive lanes sit idle waiting for data. NVLink widens that pipe by
roughly an order of magnitude (hundreds of gigabytes per second), so the exchange stops
being the limiter and the GPUs stay busy. At rack scale, NVLink switches knit dozens of
GPUs into one fabric so they behave almost like a single, enormous GPU.

## Grounded explanation

### The limit that forces many GPUs

The [[cpu-vs-gpu]] node established the GPU's bet: instead of a few latency-optimized
cores, fill the chip with thousands of simple arithmetic **lanes** (each lane does one
multiply or add per cycle) and feed them from **high-bandwidth on-board memory**, hiding
the slow memory rungs behind a flood of resident threads. That bet wins on
**throughput** — total useful work per second — for regular, data-parallel jobs.

But the bet is bounded by physical capacity. One GPU has a fixed amount of on-board
memory (tens of gigabytes) and a fixed lane count. A large neural network — its weights,
plus the intermediate values produced during a training step — can simply be too big to
fit in one GPU's memory, or too slow to finish on one GPU's lanes in acceptable time. The
only way forward is to **split the work across many GPUs**: give each GPU a slice of the
model (or a slice of the data), and let them run in parallel. This extends the GPU's
throughput scaling from *one chip* to *many chips* — in principle, eight GPUs do eight
times the work.

### Why splitting the work creates a communication problem

"In principle" hides the catch. The slices are not independent. To produce a correct
result, the GPUs must constantly **exchange data** with each other. Three terms make this
concrete (each is just a chunk of numbers a GPU holds):

- **Activations** — the intermediate values a network computes as data flows through it.
  If GPU 0 holds the first half of the model and GPU 1 the second, GPU 0's output
  activations must be *handed to* GPU 1 to continue.
- **Gradients** — the correction signals computed during training that say how to adjust
  the model. If each GPU sees different training examples, each computes a *different*
  gradient for the *same* shared weights, and those gradients must be **combined** (summed,
  then shared back) so every GPU updates its copy identically.
- **Sharded tensors** — pieces of one large array deliberately spread across GPUs; using
  the whole array means gathering the pieces from their owners.

So splitting the model buys parallel compute but **incurs a recurring bill**: at every
step, large blocks of numbers must travel from one GPU's memory to another's. Whether the
many-GPU bet actually beats the one-GPU baseline depends entirely on how fast that travel
is — because while a GPU waits for data it cannot have yet, its thousands of lanes do
nothing. Idle lanes are exactly the throughput the GPU was bought to provide, thrown away.

### The bottleneck: the ordinary host bus

How does data normally leave a GPU? A GPU is a peripheral card plugged into the host
computer over a general-purpose expansion bus — the same kind of bus that connects disks
and network cards to the CPU. (Its common name is PCIe; the details belong to a separate
topic. What matters here is its role and its speed.) That bus was designed to move data
between the CPU and *its* peripherals, not to be a fast highway *between two GPUs*.

To send a block from GPU A to GPU B over this bus, in the basic case the bytes travel up
from A's memory, across the bus into the host's main memory, then back across the bus down
into B's memory — the CPU staging the transfer. Even the better arrangement, where the two
GPUs hand bytes directly to each other across the bus without the host copy, is still
**capped by the bus's bandwidth**: on the order of tens of gigabytes per second
(roughly 30–60 GB/s in practice).

Compare that to the rate at which a single GPU reads its *own* on-board memory — measured
in **thousands** of gigabytes per second. The instant work spans two GPUs, the link
between them is the slowest part of the whole system by a wide margin. The recurring
exchange bill is paid over the narrowest pipe, and so the exchange dominates: the GPUs
spend more time waiting for each other than computing. The many-GPU machine, full of
throughput-optimized lanes, is throttled down to bus speed.

### NVLink: a dedicated wire that bypasses the host bus

NVLink is the answer to that bottleneck. It is a **separate physical interconnect** —
dedicated copper links wired directly between GPUs — that exists *only* to carry
GPU-to-GPU traffic and *bypasses the general-purpose host bus entirely*. Two properties
make it the fix:

- **High bandwidth.** An NVLink connection runs at hundreds of gigabytes per second — on
  a typical data-center GPU around **900 GB/s**, roughly an **order of magnitude** above
  the host bus's tens of GB/s. The pipe that was the limiter is widened until it no longer
  is.
- **Low latency and CPU-bypass.** The CPU is not in the data path. Once the link is
  configured at startup, a thread running on GPU 0 can read an address that physically
  lives in GPU 1's memory, and the GPU's memory system *routes that single read over
  NVLink automatically* — it looks no different in the code from reading local memory. The
  hardware decides, per address, whether the bytes are local or live on a peer GPU. The
  CPU's job shrinks to *setup and orchestration* ("tell the GPUs to exchange"), never
  *moving the bytes itself*.

The key insight is the same throughput logic from [[cpu-vs-gpu]], now applied to the wire
*between* chips rather than the memory *inside* one: the GPU tolerates slow individual
memory fetches by having enormous bandwidth and many threads in flight. NVLink gives the
**inter-GPU** link that same enormous bandwidth, so the exchange between GPUs can be
hidden the way local memory latency already was — instead of standing exposed as a
stall that idles every lane.

### Worked instance: 8 GPUs combining gradients each step

Take a concrete, non-degenerate case: **8 GPUs in one server training one model**.
Each GPU holds its own copy of the model's weights and processes a different batch of
training examples. After each step every GPU has computed a gradient — the same shape as
the weights, say a block of **2 gigabytes** of numbers — but eight *different* gradients,
because each saw different data. For the training to be correct, all eight gradients must
be **summed** and the sum delivered back to every GPU, so all copies update identically.
This forces an all-to-all exchange: every GPU's 2 GB must reach every other GPU. This is
non-degenerate — all eight participate, the full 2 GB moves (no term collapses), and it
repeats *every single step*, thousands of times per run.

**Over the host bus.** The link tops out around, say, **60 GB/s**. Moving one GPU's 2 GB
across it takes about `2 ÷ 60 ≈ 0.033 s = 33 ms`, and the combine requires each GPU to
both send its gradient out and receive the others' — so the exchange takes on the order of
**tens of milliseconds per step**. If the actual gradient *computation* on the GPU took,
say, ~20 ms, then the machine spends *more than half* of every step with its lanes idle,
waiting on the wire. The eight-GPU machine delivers far less than eight GPUs' worth of
throughput; the exchange bill, paid over the narrow pipe, dominates.

**Over NVLink.** The link runs at **~900 GB/s** — about **15× faster** here. The same
2 GB now crosses in `2 ÷ 900 ≈ 0.0022 s ≈ 2.2 ms`, and the whole gradient combine
finishes in **a few milliseconds**. Against the same ~20 ms of compute, the exchange is
now a small fraction of the step rather than the majority. The lanes stay busy; the
machine actually approaches the eight-GPU throughput it was built for. Identical training
code, identical math — only the wire changed, and the wire decided whether the many-GPU
bet paid off.

### From one server to one rack

The same idea scales past a single box. Inside one server NVLink wires its handful of
GPUs together, often through small switch chips so that *any* GPU can reach *any* other at
full NVLink speed (not just neighbors). NVIDIA pushes this two ways. **NVLink-C2C**
("chip-to-chip") runs an NVLink-grade link *between a CPU and a GPU* packaged on one
module, again at ~900 GB/s versus the host bus's tens of GB/s, with the two chips sharing
a coherent view of memory — the CPU can address the GPU's memory and vice versa, so they
act as one logical node. **Rack-scale NVLink** (e.g. the NVL72 design) extends the fabric
beyond a single server's GPUs to *dozens* across a whole rack, connected through banks of
NVLink switches, so that 72 GPUs share one high-bandwidth fabric and behave almost like a
single, enormous GPU.

The reason this matters is the same one that started this node, now amplified: the bigger
the model, the more GPUs it must be split across, and the more total exchange traffic the
fabric must carry without becoming the bottleneck. NVLink's order-of-magnitude bandwidth
advantage is what keeps the many-GPU machine from collapsing back to the speed of the
ordinary host bus. (Connecting GPUs across *separate machines* uses a different,
network-based path — a separate topic; NVLink is the within-the-box, and now
within-the-rack, fabric.)

### The takeaway

A single GPU's memory and lanes are finite, so large models are split across many GPUs —
extending the throughput bet of [[cpu-vs-gpu]] from one chip to many. But split work must
be continuously recombined, and if that recombination runs over the slow general-purpose
host bus, the exchange dominates and the lanes idle. NVLink is a dedicated, ~10×-wider,
CPU-bypassing wire between GPUs (and, via C2C, between CPU and GPU) that removes the
exchange as the limiter — turning many separate GPUs into something that acts, for the
work that matters, like one big one.

## Prerequisites

- [[cpu-vs-gpu]]

## Sources

- linux-internals-complete.html, *Multi-GPU — how GPUs talk to each other* — the three increasingly direct paths (CPU-staged copy, peer-to-peer over the host bus, and NVLink) and their bandwidths (~32 / ~64 / ~900 GB/s); *What NVLink looks like in practice* — a single GPU load that routes over NVLink to a peer's memory, and the unified address space that makes a remote read look local; *Beyond NVLink — NVLink C2C and NVL72* — chip-to-chip CPU↔GPU coherence and the rack-scale 72-GPU fabric.
