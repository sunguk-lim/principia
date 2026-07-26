---
id: cpu-vs-gpu
title: CPU vs GPU
summary: "A CPU and a GPU are both processors that do arithmetic, and both face the same problem: the data they need lives far down a slow memory-hierarchy, where moving a number costs…"
type: concept
tags: [gpu]
prereqs: [memory-hierarchy]
sources:
  - "linux-internals-complete.html — Phase 9: CPU vs GPU (latency vs throughput; what a core means; what a lane is; memory: avoid vs tolerate latency; SIMD vs SIMT)"
  - "NVIDIA H100 architecture whitepaper (SM count, CUDA-core count, HBM bandwidth)"
  - "Harris & Patterson, Computer Organization and Design (out-of-order execution, caches, branch prediction)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# CPU vs GPU

## Summary

A CPU and a GPU are both processors that do arithmetic, and both face the *same*
problem: the data they need lives far down a slow [[memory-hierarchy]], where moving a
number costs vastly more than computing on it. They answer that problem with **opposite
bets**. The CPU is **latency-optimized**: a few powerful cores, each with large caches,
hardware that guesses which way branches go, and the ability to run instructions out of
order — all spent on finishing **one** stream of work as fast as possible. It tries to
**avoid** the slow rungs of the hierarchy by keeping data close. The GPU is
**throughput-optimized**: thousands of simple arithmetic lanes that run in lockstep,
spending the same transistors on raw bandwidth and on keeping a huge number of threads
resident at once. It **tolerates** the slow rungs instead of avoiding them — whenever
some threads stall waiting on memory, the scheduler instantly runs others, so the wait
hides behind useful work. The word "core" even means different things on the two chips.
The rule that falls out: use a CPU for **latency-bound, sequential, branchy** work; use
a GPU for **throughput-bound, regular, data-parallel** work.

## Grounded explanation

### The shared problem both chips are answering

Recall the central fact of the [[memory-hierarchy]]: a processor's data sits on a ladder
of stores, each step down bigger but slower, and doing arithmetic on a number is much
cheaper than fetching that number from a distant rung. Two terms make this precise:

- **Latency** — the time you wait for *one* requested number to arrive. Fetching from the
  far rungs (main memory) takes on the order of a hundred nanoseconds, which is hundreds
  of "wasted" arithmetic slots, exactly the gap the [[memory-hierarchy]] worked instance
  exposed.
- **Throughput** — the *total* amount of useful work completed per second, summed across
  everything running.

These are different goals, and you cannot maximize both with the same transistors. Make
one instruction stream finish as soon as possible and you spend silicon on machinery that
serves that single stream (latency). Make the most work happen per second and you spend
silicon on width and on keeping many streams in flight (throughput). The CPU and the GPU
sit at the two ends of that choice. Everything that follows is downstream of this one
split.

### The CPU's bet: avoid latency, finish one thread fast

The CPU pours its transistor budget into making a *single* instruction stream race
ahead. Three pieces of machinery do this, and each is worth defining because each costs
silicon that could have gone to raw arithmetic:

- **Large private caches.** Each core keeps its own fast copies of recently used data on
  the high rungs of the [[memory-hierarchy]]. When the data is already cached, the core
  reads it in a few cycles instead of waiting the full main-memory latency. This is the
  CPU literally *avoiding* the slow rungs.
- **Branch prediction.** When the code hits an `if`, the hardware *guesses* which way it
  will go and starts running that path before the condition is even computed — so the core
  rarely sits idle at a fork. (A **branch** is just a fork in the instructions, like an
  `if`/`else`.)
- **Out-of-order execution.** If the next instruction is stuck waiting on a number from
  memory, the core looks further down the stream, finds an instruction whose inputs *are*
  ready, and runs that one meanwhile — reordering work to keep the arithmetic units busy
  despite a stall.

All three serve one thread. The result is a **core** that is an independent, heavyweight
engine: it can run an entire program by itself, at a high clock rate (roughly 3–5 billion
cycles per second). A server CPU has only a *handful* to a couple hundred such cores
(order 100), because each one is expensive in transistors. The bet: spend a lot per core,
keep data close, and the one thread you care about almost never waits.

### The GPU's bet: tolerate latency, keep thousands of lanes busy

The GPU makes the opposite bet. Instead of a few expensive cores, it fills the chip with
thousands of **lanes** — a lane is one simple arithmetic position, hardware that can do
one multiply or add per cycle and not much else. It deliberately *omits* the CPU's
latency machinery: little cache per lane, no branch prediction, no out-of-order
execution, and a more modest clock (around 1.8 billion cycles per second). Those omitted
transistors are reinvested in two things: **many** lanes, and **high memory bandwidth**
(many bytes per second off the lower rungs, even though each individual fetch is still
slow).

The trick that makes this work is **latency hiding through oversubscription**. The GPU
keeps far more threads *resident* — loaded and ready — than it has lanes to run at any
instant. A hardware **scheduler** picks, every cycle, some ready group of threads to run.
The moment a running group issues a memory request and must wait, the scheduler does not
sit idle the way a lone CPU thread would; it instantly switches to another resident group
whose data is ready. With enough resident threads, there is *always* something ready, so
the long memory latency disappears behind other threads' useful work. The GPU never
avoids the wait — it *tolerates* it, paying for the tolerance with sheer thread count and
bandwidth.

This is the same bet applied to memory, mirror-imaged: the CPU builds **big caches to
avoid** trips down the [[memory-hierarchy]]; the GPU builds **huge bandwidth plus many
threads to tolerate** them.

### "Core" means two different things

Because of these opposite bets, the word **core** does not denote the same kind of object
on each chip, and naive count comparisons mislead. A CPU "core" is one of those
independent out-of-order engines — it has its own caches and can run a program alone. The
GPU's true counterpart at that level is a **streaming multiprocessor** (an SM): a block
that has its own scheduler and its own register storage and drives many lanes. A GPU's
advertised "cores" (the individual lanes) are *not* the equal of a CPU core — each lane is
roughly 30–50× weaker than a full CPU core and cannot run a program on its own; it is just
one position in a group forced through the same instruction in lockstep. So a chip with,
say, ~130 SMs and ~17,000 lanes lines up against a CPU with ~100–300 cores: at the
*scheduler* level (SM vs core) the two are the same order of magnitude, and the GPU's edge
is at the *lane* level, where it has many times more arithmetic positions. (The mechanics
of SMs, warps, and lockstep "SIMT" execution are their own topic; here the point is only
that "core" is an apples-to-oranges word across the two chips.)

### Worked instance: add two million-element arrays

Take a concrete, non-degenerate task: element-wise vector addition `c = a + b`, where
`a`, `b`, `c` each hold `n = 1,000,000` numbers. This is non-degenerate — it touches every
element, no term collapses, and (as the [[memory-hierarchy]] node showed) it is deeply
**memory-bound**: each element does one cheap `+` but must drag several bytes off the slow
rungs. The work is also perfectly **regular**: every element does the identical operation,
independently, with no branches. That regularity is exactly what the two bets handle
differently.

**On the CPU.** Split the million elements across the cores — say ~8 of them. Each core
loops over its own ~125,000 elements (`1,000,000 ÷ 8 = 125,000`), streaming them through its
caches and adding them. With only 8 streams in flight, a core that stalls on memory mostly
just waits — its latency machinery helps a little, but there is not much else to do. Still,
8 fast cores chew through a million simple additions quickly, in the low microseconds.

**On the GPU.** Assign roughly **one lane per element** — about a million threads, each
adding a single pair `a[i] + b[i]`. Only a few thousand lanes run at any instant, but a
million threads are resident, so the scheduler always has ready ones. The instant a batch
of threads stalls fetching `a[i]` and `b[i]` from the lower rungs, the scheduler runs the
next batch, and the next — the memory latency is buried under other threads' adds. Because
the GPU has far more lanes *and* much higher bandwidth to feed them, it streams through the
million elements at a higher total rate: more **elements per second** than the CPU.

**Now break the symmetry.** Change the task to a single sequential, branchy job — parse one
text file: read a byte, branch on what it is, update parser state, decide what to read
next, repeat. There is only *one* stream of work, every step depends on the previous one,
and it is full of `if`s. A million GPU lanes are useless here: there is nothing to spread
across them, and the branches would force lanes that took the other path to sit masked and
idle. The CPU's whole bet pays off instead — branch prediction guesses the next byte's
path, out-of-order execution presses ahead, and caches keep the file's bytes close. The
CPU finishes this far faster than the GPU.

### The rule this yields

The two examples are the same trade-off seen from both sides, so the decision rule is
clean:

- Use a **CPU** for **latency-bound, sequential, branchy** work — one critical thread,
  steps that depend on each other, lots of `if`s (parsing, control logic, anything where
  finishing *this* stream sooner is what matters).
- Use a **GPU** for **throughput-bound, regular, data-parallel** work — the same simple
  operation over a huge pile of independent elements (the vector add, and more generally
  the dense numeric kernels behind graphics and neural networks), where total elements per
  second is what matters and the slow [[memory-hierarchy]] can be hidden behind a flood of
  threads.

Neither chip is "faster" in the abstract. Each is the right answer to a different shape of
the same underlying problem — a slow [[memory-hierarchy]] — and the shape of *your* work
decides which bet wins.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- linux-internals-complete.html, *Phase 9: CPU vs GPU* — the latency-vs-throughput split, "what a core means" (CPU core vs SM vs lane), "what a lane actually is," "memory — avoid latency vs tolerate it," and the SIMD/SIMT execution model.
- NVIDIA H100 architecture whitepaper — SM count, per-SM lane count, and HBM bandwidth used for the order-of-magnitude comparisons.
- Harris & Patterson, *Computer Organization and Design* — out-of-order execution, cache hierarchies, and branch prediction as the CPU's latency-avoiding machinery.
