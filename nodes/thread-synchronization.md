---
id: thread-synchronization
title: Thread Synchronization
summary: Recall from cuda-thread-hierarchy that a block is a bundle of threads placed together on one chip unit, and that the hardware does not run those threads all at once — it slices…
type: concept
tags: [gpu]
prereqs: [cuda-thread-hierarchy, warp, streaming-multiprocessor, barrier]
sources:
  - "linux-internals-complete.html — §15 Synchronization — making threads wait for each other (__syncthreads() barrier across all warps in a block; divergent-barrier trap); Shared memory — the per-block scratchpad (the load → __syncthreads() → use tile pattern); the level table (blocks can't synchronize with each other)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Thread Synchronization

## Summary

Recall from [[cuda-thread-hierarchy]] that a **block** is a bundle of threads placed
together on one chip unit, and that the hardware does not run those threads all at once —
it slices the block into groups of 32 ([[warp]]s) and runs the groups at its own pace,
interleaving them so that one group can race far ahead of another. That freedom is good for
speed but dangerous for cooperation: if some threads are meant to hand data to others, a
thread that runs ahead might try to read a value that the slower thread has not written yet.
**Thread synchronization** is the tool that fixes this, and in CUDA its core form is a single
call, `__syncthreads()`, which is a [[barrier]] — a line in the code that no thread of the
block may cross until *every* thread of the block has reached it. Threads that arrive early
wait; once the last one arrives, all are released together. Its main job is to make
cooperative work through the block's shared scratch memory correct: you put a barrier *after*
the threads write their data and *before* anyone reads it, so no thread ever reads a slot
another thread has not filled. Two hard limits define its scope. First, it synchronizes
**only within one block** — there is no built-in barrier across the whole grid, because the
hierarchy makes different blocks independent and they may not even run at the same time.
Second, **every thread in the block must reach the *same* barrier**; hiding a `__syncthreads()`
inside a branch that only some threads take makes the block wait forever for threads that will
never arrive.

## Grounded explanation

### The problem the barrier solves: warps run at different speeds

The prerequisite [[cuda-thread-hierarchy]] established the layering you need here:
**grid ⊃ block ⊃ warp ⊃ thread**. A **thread** is one independent execution of your GPU
function; a **block** is a fixed-size group of threads guaranteed to share one physical unit
(the [[streaming-multiprocessor]]) so that they can cooperate; the **grid** is all the
blocks of one launch; and — the load-bearing fact for this node — when a block lands on its
unit, the hardware chops its threads into **warps** of 32 and runs the warps *independently*,
each advancing at its own rate. A 256-thread block is 8 warps, and at any instant those 8
warps can be at 8 different points in the same code: warp 0 might be issuing a memory load
while warp 3 is still computing an earlier line. The prerequisite called the block the
"co-located, cooperative" level precisely because the threads *can* hand data to each other —
but it did not say how they keep that hand-off safe. **This node is that mechanism.**

The danger is a **race**: two threads touch the same memory location and the result depends on
which one happens to get there first. The specific race that matters here is a
**read-before-write**: thread A is supposed to write a value that thread B will later read, but
because A and B live in different warps and the warps run at different speeds, B can reach its
read *before* A has done its write. B then reads stale or garbage data, and the kernel produces
a wrong answer with no error message. The threads were never actually in lockstep across warp
boundaries, so "A writes, then B reads" — which looks guaranteed when you read the code top to
bottom — is not guaranteed at all in time. Something must *force* the ordering. That something
is the barrier.

### What `__syncthreads()` is and the invariant it maintains

`__syncthreads()` is a **barrier for all the threads of one block**. Operationally: when a
thread reaches the call, it stops and waits; it is allowed to continue past the call only once
*every other thread in the same block* has also reached that call. So the barrier enforces one
clean invariant:

> At the moment any thread executes the first instruction *after* the barrier, **every**
> instruction *before* the barrier has already been executed by **every** thread in the block.

That single guarantee is exactly what kills the read-before-write race. If thread A's write
sits *before* the barrier and thread B's read sits *after* it, then by the invariant B cannot
start its read until A's write is done — no matter how far ahead B's warp had run, the barrier
holds it until the slowest warp catches up. The barrier does not make the warps run in
lockstep all the time (that would throw away the scheduling freedom that hides memory latency);
it re-aligns them *at one chosen point*, just long enough to make a hand-off safe, and then lets
them diverge again.

It is worth being precise about *who* waits for *whom*. The barrier's reach is exactly one
block — the same scope as the block's shared scratch memory and for the same reason. The
prerequisite's level table is the justification: within a block, the threads (and their warps)
share one physical unit, so the hardware can make them wait for each other cheaply; the unit
simply does not release any warp of the block from the barrier until it has counted all of them
in.

### Scope limit: there is no grid-wide barrier inside a kernel

The most consequential thing to understand is what `__syncthreads()` does *not* do: it does not,
and cannot, synchronize across blocks. There is no call that makes the whole grid wait at a
line. This is not an oversight — it falls directly out of the prerequisite's design. Blocks are
**mutually independent**: the hardware is free to run them on different units, or on the same
unit at different times, or in any order it likes, and that freedom is the source of the GPU's
ability to scale across chip sizes. A block that finished an hour's worth of warps ago could be
long gone; a block that has not started yet has no threads in existence to wait. You cannot make
two things meet at a barrier when one of them may not exist while the other runs. So a barrier
can only ever gather threads that are guaranteed to be alive together on one unit — and the
hierarchy guarantees that for the threads of one block, and for nothing larger.

The practical consequence: when a computation genuinely needs *all* blocks to finish one phase
before *any* block starts the next (a true grid-wide ordering), you cannot get it from
`__syncthreads()`. You get it by ending the kernel and starting another. The boundary between
two kernel launches is the only grid-wide barrier the model gives you: a launch's blocks are all
guaranteed complete before the next launch's blocks begin. (The mechanics of launching kernels
are a separate topic; what matters here is the principle — *in-kernel barrier = one block;
across blocks = a new launch*.)

### Correctness rule: every thread must hit the *same* barrier

The barrier counts threads, and it will not release anyone until its count is complete. This
gives a strict rule for where you may place it: **every thread in the block must reach the very
same `__syncthreads()` call.** Break that rule and the block hangs forever, because the barrier
is waiting for arrivals that will never come.

The classic way to break it is to put the barrier inside *divergent control flow* — a branch
that some threads of the block take and others skip. Suppose the code says "if my index is even,
do some work and then call `__syncthreads()`." The odd-indexed threads never enter the branch, so
they never reach that barrier. The even-indexed threads arrive and wait — for the odd threads,
who have sailed past to later code or finished entirely. The count never completes; the waiting
threads are stuck; the block deadlocks. (Recall from the prerequisite that a branch is resolved
at the warp level — a whole warp goes one way as a unit — so the failure is usually whole warps
going missing from the count, but the rule is simplest to state per thread: all of them, same
barrier.) The discipline is therefore to place barriers only at points the *entire* block is
guaranteed to reach — out in the common code path, never tucked inside a conditional that only
some threads enter.

### Worked instance: a cooperatively loaded shared-memory tile

Here is the canonical use, run with concrete numbers. A block of **256 threads** needs to work
over a 256-element chunk of data — call it a **tile**. The tile lives in the block's fast on-unit
scratch memory (the chip's *shared memory*, the per-block scratchpad the prerequisite mentioned),
declared as a 256-slot array `tile` that all 256 threads of the block see. The plan is: load the
tile from slow main memory once, cooperatively, then let every thread reuse it — far cheaper than
each thread re-reading main memory.

The kernel body, in three phases, is:

1. **Cooperative load.** Each thread loads exactly one element. The thread whose in-block
   coordinate (`threadIdx.x`, from the prerequisite) is 0 writes `tile[0]`, the thread with
   coordinate 1 writes `tile[1]`, …, the thread with coordinate 255 writes `tile[255]`. After this
   phase *every slot of the tile has an owner who has filled it* — but only if all 256 writes have
   actually happened.
2. **The barrier.** `__syncthreads()`.
3. **Reuse.** Now each thread reads from the tile freely — including slots it did not write. For
   instance a thread might compute something from `tile[200]`, a slot that a *different* thread
   (coordinate 200) was responsible for filling.

Trace why the barrier in phase 2 is load-bearing. Consider the thread with `threadIdx.x = 5`. It
is in warp 0 of the block (warps are 32 threads wide, so coordinates 0–31 are warp 0). The thread
that must fill `tile[200]` has coordinate 200, which lands in warp 6 (since 200 ÷ 32 = 6 remainder
8 — it is lane 8 of warp 6). Warp 0 and warp 6 are scheduled independently. Without the barrier,
warp 0 can finish its single write (`tile[5]`) and rush straight into phase 3, reading `tile[200]`
*while warp 6 has not yet executed its write of `tile[200]`*. Thread 5 reads whatever happened to
be sitting in that slot — uninitialized garbage — and computes a wrong result. This is the
read-before-write race, concrete: a fast warp reading a slot a slow warp owns.

Insert `__syncthreads()` and the invariant takes over. Thread 5's warp finishes `tile[5]` and hits
the barrier; it is held there. It cannot reach the read of `tile[200]` until *every* warp of the
block — including warp 6 — has reached the barrier, which means warp 6 has executed its write of
`tile[200]` (that write is before the barrier). Only then are all warps released, and only then
does thread 5 read `tile[200]` — now guaranteed to hold the value warp 6 wrote. Every thread can
now read every slot safely, because every slot was written before the barrier and every read
happens after it.

Two symmetric placements both matter, which is why "after the writes, before the reads" is the
whole rule. If the barrier came *before* the loads, it would order nothing useful — threads could
still read before writing. If a *second* round of writes followed the reads (say the block updates
the tile and reads it again), that round would need its *own* barrier, for the same reason. The
barrier is not a one-time setup; it is placed at each point where a write-then-read hand-off
crosses warp boundaries. Strip the barrier out of the tile pattern and the kernel still compiles
and runs — it just sometimes produces garbage, intermittently, depending on how the warps happened
to interleave on that run. That silent, non-deterministic wrongness is exactly the failure mode
synchronization exists to prevent.

## Prerequisites

- [[cuda-thread-hierarchy]]
- [[warp]]
- [[streaming-multiprocessor]]
- [[barrier]]

## Sources

- linux-internals-complete.html — *§15 Synchronization — making threads wait for each other*
  (`__syncthreads()` is "a barrier across all warps in a block: no thread proceeds past the call
  until every thread in the block has reached it," used "after writing shared memory, before
  reading what someone else wrote"; the divergent-barrier *trap*: a `__syncthreads()` only some
  threads reach causes the kernel to "hang or silently corrupt data"); *Shared memory — the
  per-block scratchpad* (the load-one-element → `__syncthreads()` → use-the-whole-tile pattern,
  and "wait until all threads finished loading"); the per-level rules table (blocks "can't
  synchronize with each other," motivating the no-grid-barrier scope limit and the use of separate
  kernel launches for cross-block ordering).
