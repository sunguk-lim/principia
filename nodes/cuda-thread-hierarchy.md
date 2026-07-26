---
id: cuda-thread-hierarchy
title: CUDA Thread Hierarchy
summary: When you run a program on an NVIDIA GPU, you do not start one execution — you start a whole army of them at once, and CUDA (NVIDIA's name for both the GPU and the programming…
type: concept
tags: [gpu]
prereqs: [warp, streaming-multiprocessor]
sources:
  - "linux-internals-complete.html — Thread indexing — how each thread knows what to compute; The \"loop disappears\" — central insight for kernel writing; Level 1 — the grid: 3907 blocks; Level 3 — warps inside the block; Occupancy — how many blocks fit on an SM"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# CUDA Thread Hierarchy

## Summary

When you run a program on an NVIDIA GPU, you do not start one execution — you start a
whole army of them at once, and **CUDA** (NVIDIA's name for both the GPU and the programming
model you write it in) organizes that army into a strict three-level hierarchy. At the bottom
is a **thread**: one independent execution that runs the body of your GPU function once, start
to finish, on its own data. Threads are grouped into a **block**: a fixed-size bundle of
threads that are guaranteed to be placed together on one physical processing unit (the chip
calls each unit a [[streaming-multiprocessor]], or SM), so the threads in a
block can cooperate. All the blocks of a single launch together form the **grid** — the
complete set of work that one launch must do. The crucial connection to what you already know:
inside a block, the hardware does not run the threads one at a time or all at once; it chops
them into groups of 32 and runs each group as a [[warp]] — the lockstep unit from the
prerequisite. So the hierarchy is **grid ⊃ block ⊃ warp ⊃ thread**, where the warp level is
the physical one. The single most important thing the hierarchy buys you is that **the loop
disappears**: instead of writing a CPU `for` loop that walks an array index by index, you
launch one thread per array element, and each thread computes *which* element it owns from its
own coordinates in the hierarchy. The grid *is* the loop.

## Grounded explanation

### The three levels, defined from the bottom up

The prerequisite [[warp]] node taught the physical reality: a streaming multiprocessor runs
threads 32 at a time, in lockstep, as a warp, and that warp is the hardware's real scheduling
unit. But it deliberately left a gap. It noted that "programmers declare how many threads they
want in a bundle the SM calls a *block*; the SM then slices each block into warps of 32," and
flagged blocks as a separate topic. **This node is that topic** — it gives the levels *above*
the warp, the ones you actually write in your code, and shows how they reduce to warps at
launch time.

Three terms, each defined before it is used:

- A **thread** is one execution of your GPU function — the function you write to run on the
  GPU is called a *kernel* (plain term: the per-element body of work; kernel-launch mechanics
  are not this node's subject). Every thread runs the *same* kernel code, but each one is an
  independent stream of work with its own register values. This is exactly the "thread" of the
  [[warp]] node — one independent stream of work with its own values — now seen as the thing
  *you* asked the GPU to spawn, in bulk.

- A **block** is a group of threads that you size, and that the hardware guarantees to place
  *together* on **one** [[streaming-multiprocessor]] (SM) for the block's whole lifetime. Because they share one SM, the
  threads in a block can do things threads in different blocks cannot: they can hand data to
  each other through a small fast on-SM scratch memory (the chip calls it *shared memory* — a
  separate topic) and they can wait for one another at a common point (a *barrier*). Co-location
  is what makes cooperation possible. You choose the block size; 256 threads per block is a
  common default.

- A **grid** is the entire collection of blocks produced by one launch. Nothing in the grid is
  special hardware; "grid" is simply the name for *all the work this one launch has to do*. You
  pick how many blocks the grid contains.

So when you launch, you give two numbers: how many blocks (the grid) and how many threads each
block holds (the block size). The hierarchy is containment: the grid contains blocks, each
block contains threads, and — the hinge to the prerequisite — when a block lands on an SM, the
SM automatically slices its threads into [[warp]]s of 32. A 256-thread block *is* 8 warps
(256 / 32 = 8); threads 0–31 form warp 0, threads 32–63 form warp 1, and so on. The block and
grid are the levels you reason about in software; the warp is the level the silicon actually
executes. You never write a warp — you write threads and blocks, and the warp emerges.

### The why of the levels: independence buys scalability, co-location buys cooperation

Why two levels above the thread instead of one flat pool of threads? Each level answers a
different need, and the split between them is the whole design.

**Blocks are mutually independent, and that independence is deliberate.** Block 5 and block 6
know nothing about each other; they may run on different SMs, or on the same SM at different
times, or simultaneously — the program is forbidden from assuming any order or any
communication between blocks. This looks like a restriction, but it is the source of the GPU's
scalability. Because blocks do not depend on each other, the hardware's distributor is free to
shovel them onto whatever SMs have room, in any order. A small GPU with few SMs runs a few
blocks at a time and works through the grid in waves; a large GPU with many SMs runs many
blocks at once and finishes sooner — **the same program, unchanged, gets faster on a bigger
chip purely because more independent blocks can be in flight.** If blocks could depend on one
another, the hardware could not reorder or redistribute them freely, and that automatic scaling
would be lost. Independence is the price, scalability is what it buys.

**Threads within a block are co-located precisely so they *can* depend on each other.** The
opposite trade. By guaranteeing that a block's threads share one SM, CUDA gives them a place to
meet — the fast on-SM scratch memory and the barrier — so a block can act as a little
cooperating team (loading a chunk of data once and sharing it, or combining partial results).
You cannot do that across the whole grid, because the grid is spread across the chip with no
shared meeting place; you *can* do it inside a block, because a block is, by construction, all
in one spot.

That is the reason for exactly two levels: the grid level is the **independent, scalable** one,
and the block level is the **co-located, cooperative** one. The warp underneath is the
**lockstep, efficient** one from the prerequisite. Three levels, three distinct properties.

### Thread indexing: how a thread learns which element it owns

A thread runs the same code as every other thread, so something must tell each thread which
piece of data is *its* piece. That something is the thread's **coordinates** in the hierarchy,
which the hardware hands to every thread as built-in read-only values:

- `threadIdx` — the thread's position *within its own block* (for a 256-thread block, a number
  from 0 to 255).
- `blockIdx` — the block's position *within the grid* (for a 3907-block grid, 0 to 3906).
- `blockDim` — the size of a block, i.e. how many threads per block (here, 256).

From these, every thread computes a single **global index** — its unique position across the
entire grid — with the classic one-dimensional formula:

> `i = blockIdx.x * blockDim.x + threadIdx.x`

(The `.x` is because these coordinates can be up to three-dimensional, for naturally 2-D or 3-D
problems like images; for a flat array we use only the `x` component.) Read the formula as: "skip
over all the threads in the blocks before mine (`blockIdx.x` whole blocks, each `blockDim.x`
threads wide), then add my offset inside my own block." The result `i` is unique across the whole
grid — no two threads compute the same `i` — and it is the element of the array that this thread,
and only this thread, is responsible for.

### The loop disappears: the grid *is* the loop

This is the central insight, and it is what makes GPU code look so different from CPU code. On a
CPU you add two arrays with an explicit loop — one worker walking the index from `0` to `n-1`:

> `for (int i = 0; i < n; i++)  out[i] = a[i] + b[i];`

One worker, `n` iterations, done in sequence. On the GPU you do not write the loop at all. You
write only **what one thread does** for one value of `i`, and you launch `n` threads:

> `int i = blockIdx.x * blockDim.x + threadIdx.x;`
> `if (i < n)  out[i] = a[i] + b[i];`

There is no `for`. What was the loop variable `i = 0, 1, 2, …` is now the computed global index,
a *different* constant in each of the `n` threads, all of them live at the same moment. The
iteration that the CPU performed in time, the GPU performs in space — across the grid. That is
why the slogan is *the grid is the loop*: laying out `n` threads in the hierarchy replaces
walking an index `n` times. You stop describing a sequence of steps and start describing one
thread's job, then spawn an army to cover every index in parallel.

The `if (i < n)` guard is there for one reason: the number of threads you launch is usually a
little larger than `n`, because the grid is built from whole blocks and `n` rarely divides evenly
by the block size. The extra threads at the tail have a global index `i ≥ n` and must do nothing,
or they would read and write past the end of the array. The guard switches them off.

### Worked instance: adding two million-element arrays, no loop

Add two arrays `a` and `b` of `N = 1,000,000` floats each into `c`, with a block size of
`blockDim.x = 256`. Walk the hierarchy with real numbers; every number comes from the previous
one.

**Size the grid.** Each block covers 256 consecutive elements, so the number of blocks must be
enough to cover all 1,000,000 elements: `ceil(1000000 / 256) = 3907` blocks. (Plain division
gives `3906.25`; you cannot launch a fraction of a block, so you round *up* to 3907 — this is
exactly why the guard is needed.) The grid therefore holds 3907 blocks, and the total thread
count is `3907 × 256 = 1,000,192` — that is **192 more threads than elements**. Those 192 surplus
threads are the non-degenerate detail: they are the reason `if (i < n)` exists, and a worked
instance that ignored them (say, an array length that divided evenly) would hide that whole
branch.

**Trace one specific thread.** Take the thread with `blockIdx.x = 10` and `threadIdx.x = 5`. Its
global index is

> `i = 10 * 256 + 5 = 2560 + 5 = 2565`.

So this one thread checks `2565 < 1000000` (true, so it proceeds) and executes
`c[2565] = a[2565] + b[2565]` — one add, on element 2565, and nothing else. It neither knows nor
cares about any other element. Its neighbor `threadIdx.x = 6` in the same block owns `i = 2566`;
the first thread of the *next* block (`blockIdx.x = 11`, `threadIdx.x = 0`) owns
`i = 11*256 + 0 = 2816`, picking up right where block 10's last thread (`i = 10*256 + 255 = 2815`)
left off — the blocks tile the array into contiguous, non-overlapping slices of 256.

**Trace a tail thread to fire the guard.** Take the very last thread, in the last block:
`blockIdx.x = 3906`, `threadIdx.x = 255`. Its index is `i = 3906*256 + 255 = 999936 + 255 =
1,000,191`. The check `1000191 < 1000000` is **false**, so this thread does nothing — correctly,
since element 1,000,191 does not exist. The same is true of the last 192 threads (indices
1,000,000 through 1,000,191). The guard is the only thing standing between them and an
out-of-bounds write.

**Tie it back to the warp.** Block 10's 256 threads are not run independently; the SM slices them
into `256 / 32 = 8` [[warp]]s. Our thread `i = 2565` (`threadIdx.x = 5`) sits in warp 0 of
block 10 (lanes are threads 0–31), at lane 5. All 32 threads of that warp — owning consecutive
indices 2560 through 2591 — issue the *same* load/add/store instructions in lockstep, each on its
own element, exactly as the prerequisite described. Because every thread wants the identical
instruction (a plain add, no data-dependent branch), the warp runs at full width with no
divergence — the aligned, full-efficiency case from the [[warp]] node. So the hierarchy bottoms
out cleanly: 3907 blocks × 8 warps × 32 lanes cover all 1,000,192 thread-slots, the guard kills
the 192 phantom ones, and **not a single `for` loop was written** — the grid was the loop.

(How many of those 3907 blocks actually run at the same instant depends on how many fit on each
SM at once — the chip's term for that is *occupancy*, set by how much of each SM's limited
resources a block consumes, and it is a separate topic. The point here is only that because the
blocks are independent, the hardware is free to run as many simultaneously as it can fit, in
whatever waves it likes, and the program does not change.)

## Prerequisites

- [[warp]]
- [[streaming-multiprocessor]]

## Sources

- linux-internals-complete.html — *Thread indexing — how each thread knows what to compute*
  (the built-in `threadIdx` / `blockIdx` / `blockDim` / `gridDim` coordinates and the
  `i = blockIdx.x * blockDim.x + threadIdx.x` global-index formula); *The "loop disappears" —
  central insight for kernel writing* (CPU `for` loop vs. one-thread-per-element launch; "the
  grid is the loop"; the `if (i < n)` bounds guard); *Level 1 — the grid: 3907 blocks* (grid =
  all the work of one launch; blocks are independent and tile the array into contiguous 256-element
  slices; distributed across SMs); *Level 3 — warps inside the block* (a 256-thread block is split
  into 8 warps of 32); *Occupancy — how many blocks fit on an SM* (block independence lets the
  hardware pack many blocks per SM up to a resource limit, enabling scaling across chip sizes).
