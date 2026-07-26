---
id: streaming-multiprocessor
title: Streaming Multiprocessor
summary: A streaming multiprocessor (an SM) is the GPU's core compute building block, and a GPU is essentially an array of many of them — about 132 on an NVIDIA H100.
type: concept
tags: [gpu]
prereqs: [cpu-vs-gpu, memory-hierarchy]
sources:
  - "linux-internals-complete.html — Phase 7: Two parallel hierarchies; The full chip and one SM; Inside one SM; Massive concurrency, time-multiplexed through small schedulers; H100 spec table (132 SMs, 128 CUDA cores/SM, 228 KB shared memory)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Streaming Multiprocessor

## Summary

A **streaming multiprocessor** (an **SM**) is the GPU's core compute building block, and
a GPU is essentially an array of many of them — about 132 on an NVIDIA H100. Each SM
bundles four things: many simple arithmetic **lanes** (in the prerequisite [[cpu-vs-gpu]]
sense — a lane is one position that can do one multiply or add per cycle, and NVIDIA
markets these as "CUDA cores"); one or more small hardware **schedulers** that decide,
every cycle, which work to feed those lanes; a very large **register file** (fast on-chip
storage holding each running thread's working values); and a block of fast on-chip
**scratchpad memory** sitting on a high rung of the memory hierarchy. The SM is where the
GPU's *throughput bet* from [[cpu-vs-gpu]] becomes a concrete machine. It keeps far **more
threads loaded and ready than it has lanes to run**, and its scheduler time-multiplexes
them: the instant one group of threads stalls waiting on slow memory, the scheduler issues
a different ready group instead, so the lanes stay busy and the long memory wait is
*hidden* behind other threads' useful work. That is the "tolerate latency" strategy of
[[cpu-vs-gpu]] turned into hardware. The whole-chip picture follows: the GPU chops a job
into many independent pieces and spreads them across all its SMs, each SM running its
assigned pieces on its own, so total throughput ≈ (lanes per SM) × (number of SMs kept
busy).

## Grounded explanation

### Where this sits: the SM is the GPU's "core-level" unit

The prerequisite [[cpu-vs-gpu]] node already established the GPU's bet and named this very
object. Recall its conclusion about the word **core**: a CPU "core" is a heavyweight
independent engine that can run a whole program by itself, while a GPU's advertised "cores"
are just **lanes** — single arithmetic positions, each ~30–50× weaker than a CPU core, that
cannot run a program alone. The true counterpart of a CPU core on a GPU, [[cpu-vs-gpu]]
said, is the **streaming multiprocessor**: the block that has its own scheduler and its own
register storage and drives many lanes. This node opens up that block and shows how it
works. So the SM is the GPU's *core-level* unit — the thing that sits at the same level of
the design as a CPU core, even though it is built on the opposite principle.

Before going further, two terms used throughout, defined now so nothing is used before it
is introduced:

- A **thread** is one independent stream of work — one element's worth of computation,
  with its own working values. (On a CPU you would call this a thread too; on a GPU there
  are vastly more of them, each tiny.)
- **Resident** means *loaded onto the SM and ready to run* — the SM is holding this thread's
  state right now, whether or not it happens to be executing this cycle. The distinction
  between "resident" and "currently executing" is the heart of everything below.

### What an SM is made of, and why each part is there

An SM bundles four kinds of hardware. Each one exists to serve the throughput bet, so it is
worth naming what each part *is* and *why it earns its silicon*:

- **Many lanes (the "CUDA cores").** These are the arithmetic positions from [[cpu-vs-gpu]]
  — simple, plentiful, each doing one multiply or add per cycle. On an H100 an SM has 128 of
  them. They are the *only* part that does actual computation; everything else exists to
  keep them fed. This is the throughput half of the bet: spend transistors on width, not on
  making one stream fast.

- **One or more schedulers.** A scheduler is a *tiny* piece of fixed hardware — a few
  thousand transistors, not a program — whose entire job is, each cycle, to look over the
  threads resident on the SM, find a group whose next instruction is *ready* (all its inputs
  available), and issue that instruction to the lanes. It does not compute anything itself;
  it just decides *which* ready work to run next. An H100 SM has four such schedulers, so up
  to four groups can issue in the same cycle. This is the piece that makes "tolerate
  latency" actually happen, as the next section shows.

- **A large register file.** Registers are the fastest, closest storage a processor has —
  the working values an instruction reads and writes sit in registers. The SM's register
  file is the pool of all those registers, and on a GPU it is enormous: it must hold the live
  working values of **every resident thread at once**, not just the few currently executing.
  This size is not an accident; it is the price of the central trick, explained below.

- **A block of fast on-chip scratchpad memory plus a small cache.** This is storage on a
  high rung of the [[memory-hierarchy]] — far faster than the chip's distant main memory
  (HBM), which sits several rungs down the ladder. On an H100 it is 228 KB per SM. Threads working on the same piece of the problem can stage data
  here and cooperate through it, instead of each making a slow trip to main memory. (How
  threads coordinate through this scratchpad is its own topic; here it is enough that the SM
  *has* fast local memory for the lanes to reach.)

### The why: how the SM hides memory latency (the central trick)

This is the one non-obvious step, so it gets the full justification. Recall the core tension
from [[cpu-vs-gpu]]: fetching a number from the far rungs of the memory hierarchy costs on
the order of *hundreds of cycles* of waiting — **latency** — while doing arithmetic on a
number costs ~one cycle. A CPU spends transistors to *avoid* that wait (big caches,
out-of-order execution). The SM does the opposite: it *tolerates* the wait. Here is the
machine that does it.

The SM deliberately keeps **many more threads resident than it has lanes**. Suppose the SM
has lanes for, say, a few hundred threads at a time, but it holds the live state of a few
*thousand* threads, all resident. Now the scheduler plays a simple game every single cycle:

1. It scans the resident threads for a group whose next instruction is **ready**.
2. It issues that group's instruction to the lanes.
3. If the instruction was a load from slow memory, that group becomes **stalled** — it
   cannot proceed until the data arrives, hundreds of cycles later. The scheduler marks it
   so and *moves on*.
4. Next cycle, it simply picks a **different** ready group. The stalled group's wait is now
   overlapping with other groups' useful arithmetic.

The magic-looking part is step 4 — *switching groups costs zero cycles*. On a CPU, switching
to a different thread is expensive: you must save one thread's registers and restore
another's, hundreds to thousands of cycles of bookkeeping. The SM pays *nothing* to switch.
And here is the justifying reason, the identity that makes it work: **every resident thread
already owns its own permanent slice of the register file.** Nothing is saved or restored
because nothing moves — each thread's working values are sitting in their own slots the whole
time. The scheduler just points at a different thread index next cycle, and that thread's
registers are already there. *This is exactly why the register file has to be so large:* it
must hold every resident thread's state simultaneously, precisely so that switching between
any of them is free.

That free switch is what converts the GPU's bet into reality. With enough resident threads,
there is *always* some ready group, so a memory request that takes hundreds of cycles never
stalls the lanes — by the time it returns, hundreds of other instructions from other threads
have run on those same lanes. The latency did not get shorter; it got **buried** under other
work. The SM never avoids the wait; it tolerates it, paying for the tolerance with sheer
resident-thread count and a register file big enough to make switching free. That is the
"tolerate latency" half of [[cpu-vs-gpu]], now a concrete circuit.

(The fixed-size groups the scheduler issues, the rule that those grouped threads all run the
same instruction in lockstep, and the name for "how many threads are resident" are each
their own separate topics; here the load-bearing facts are only that the SM oversubscribes
itself with resident threads and switches between them for free.)

### The whole-chip view: many SMs, work spread across them

One SM is the building block; a GPU is an **array of many SMs** — about 132 on an H100 —
all sharing the chip's distant main memory. So the GPU needs a way to spread a job across
all of them.

It works like this. A job for the GPU — a single computation applied across a huge pile of
data, called a **kernel** — is partitioned by the programmer into many independent pieces,
each piece a bundle of threads. (These pieces are commonly called *blocks*; treating their
internal structure is a separate topic.) A small global distributor on the chip then hands
these pieces out to the SMs, packing several onto each SM up to its resource limits, and
refilling an SM with a fresh piece whenever one finishes. Crucially the pieces are
**independent**: a piece runs entirely on the one SM it was assigned to, never migrating,
and pieces on different SMs neither share state nor synchronize. That independence is what
lets the design *scale*: a GPU with twice as many SMs simply runs twice as many pieces at
once, with no coordination cost. The SMs are the parallel hardware; the pieces are the
parallel work; the distributor is the matchmaker between them.

So the GPU's total throughput is, to first order, **(work each SM does per cycle) ×
(number of SMs kept busy)** — the lanes inside each SM multiplied across all the SMs on the
chip, with each SM's scheduler locally keeping its own lanes saturated by the
latency-hiding trick above.

### Worked instance: a kernel over one million elements on a 132-SM GPU

Take the same non-degenerate task as [[cpu-vs-gpu]] — element-wise addition `c = a + b`
over `n = 1,000,000` elements — and watch it land on the SMs. It is non-degenerate: it
touches every element, no term collapses, it is **memory-bound** in the [[memory-hierarchy]]
sense (arithmetic intensity far below the machine's balance point — one `+` per element but
several bytes dragged from HBM per element), and it is perfectly regular (every element does
the identical, independent operation). Memory-bound and regular is exactly the case the SM
is built to win.

**Partition into pieces.** The programmer assigns roughly one thread per element — about
1,000,000 threads — and groups them into pieces of, say, 256 threads each. That is
`1,000,000 ÷ 256 ≈ 3,907` pieces. So the job is ~3,907 independent pieces, far more than the
132 SMs can hold at once.

**Distribute across SMs.** The chip's distributor hands pieces to the 132 SMs. Each SM holds
several pieces resident at a time — say it can fit 8 pieces, which is `8 × 256 = 2,048`
resident threads per SM. Across the chip that is roughly `132 × 2,048 ≈ 270,000` threads
resident *simultaneously*, with the remaining ~3,907 − (132 × 8) ≈ 2,851 pieces waiting their
turn. As any SM finishes a piece, the distributor refills it with a waiting piece, until all
3,907 are done.

**Inside one SM, watch the lanes stay busy.** That SM has 128 lanes but 2,048 threads
resident. Every cycle its schedulers pick ready groups and issue their adds to the lanes. The
moment a group issues its `load a[i]` / `load b[i]` from slow memory, it stalls for hundreds
of cycles — but the SM has thousands of other resident threads, so the scheduler immediately
issues a *different* group's ready instruction, switching for free because each thread's
registers are already in place. With 2,048 threads resident, the chance that *all* of them
are stalled at the same instant is vanishingly small, so the 128 lanes essentially never go
idle. The hundreds-of-cycles memory latency of one group is completely buried under the adds
of the others.

**Total throughput.** At any instant the GPU is running ~132 SMs' worth of work — 132 SMs ×
128 lanes ≈ 16,896 lanes all issuing adds — each SM locally hiding its own memory waits. The
million additions stream through at a rate set by *lanes × SMs kept busy*, not by how long
any single memory fetch takes. That product, sustained while latency is hidden, is precisely
the throughput advantage [[cpu-vs-gpu]] promised — and the SM is the piece of hardware that
delivers it.

## Prerequisites

- [[cpu-vs-gpu]]
- [[memory-hierarchy]]

## Sources

- linux-internals-complete.html — *Two parallel hierarchies*, *The full chip and one SM*,
  *Inside one SM*, and *Massive concurrency, time-multiplexed through small schedulers*:
  the SM as the GPU's compute building block; its lanes ("CUDA cores"), schedulers,
  register file, and on-chip shared memory; the zero-cost warp/thread switch enabled by a
  register file large enough to hold every resident thread's state; the global distributor
  that hands independent work pieces to SMs; and the H100 figures used here (132 SMs, 128
  CUDA cores per SM, 228 KB on-chip memory, ~270,000 threads in flight).
