---
id: atomic-operation
title: Atomic Operation
summary: An atomic operation performs a read-modify-write on one memory location indivisibly — the hardware guarantees that once a thread starts reading that location, no other thread can…
type: concept
tags: [gpu]
prereqs: [cuda-thread-hierarchy]
sources:
  - "linux-internals-complete.html — Atomic operations (CUDA): atomicAdd/atomicCAS on global and shared memory, the histogram example, \"atomics serialize\" and the contention/per-block-then-global pattern; \"atomically\" defined as all-at-once with no observable in-between state; the lost-update race from x += 1 (load/add/store with a switch landing in the gap)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Atomic Operation

## Summary

An **atomic operation** performs a **read-modify-write** on one memory location **indivisibly** —
the hardware guarantees that once a thread starts reading that location, no other thread can touch
it until the same thread has written its new value back. (A read-modify-write means: read the
current value, compute a new value from it, write the new value; *atomic* means "all-at-once, like
a light switch — there is no observable in-between state.") The problem it solves: when many
threads of the [[cuda-thread-hierarchy]] update the *same* location with an ordinary `x += v`,
that one statement is secretly three steps — read `x`, add `v`, store back — and the steps of
different threads **interleave**, so updates are silently **lost**. The classic loss: two threads
both read the value `5`, both add `1`, and both write `6`; two increments happened but the location
only advanced by one — one update vanished. An atomic add, written `atomicAdd(&x, v)`, fuses the
read, the modify, and the write into a single uninterruptible step, so no thread can ever slip into
the gap, and the final value is exactly right. The cost is that atomics aimed at the *same address*
**serialize** — only one contending thread proceeds at a time — so a million threads all hammering
one counter is correct but slow. The standard cure is to **privatize**: let each block accumulate
its own partial result first, then combine the few partials at the end.

## Grounded explanation

### What "atomic" means, and why a plain update is not

The prerequisite [[cuda-thread-hierarchy]] node established that a GPU launch spawns an army of
threads — grid ⊃ block ⊃ thread — and that, by design, no ordering is guaranteed between threads in
different blocks: the hardware is free to run them in any order, in any overlap. That freedom is
exactly what makes a shared update dangerous. When two threads independently try to change the same
memory cell, the language gives no promise about whose steps happen first, or whether they happen
without interruption.

Take the most innocent-looking line a thread can write: `x += v`, meaning "add `v` to `x`." The
single `+=` hides **three** separate machine steps:

1. **read** — load the current value of `x` from memory into a private register;
2. **modify** — add `v` to that register;
3. **write** — store the register's new value back into `x`.

This trio is a **read-modify-write**: the new value *depends on* the value just read. The trouble is
that another thread can act in the *gap* between any two of these steps. Thread A reads `x` and gets
`5`. Before A writes anything back, thread B *also* reads `x` and gets the same stale `5`. Now both
threads add `1` in their own registers (both compute `6`), and both store `6`. Two increments were
issued, but `x` went from `5` to `6`, not to `7`. One increment was **lost**. This is a **race**: a
bug whose outcome depends on the unpredictable relative timing of threads, and it is precisely the
kind of timing the thread hierarchy refuses to pin down.

The fix is to make the whole read-modify-write **atomic** — Greek *a-tomos*, "uncuttable." An atomic
operation is one the hardware promises to carry out as a single indivisible event: from the instant a
thread begins the atomic read of `x` to the instant it completes the write, no other thread is
allowed to read or write that same location. There is no observable half-finished state — like a
light switch, the location is either at its old value or its new one, never caught mid-flip. So the
gap that thread B exploited simply does not exist: B cannot read `x` until A's entire increment has
landed. With the read-modify-write fused, B reads `6`, computes `7`, and stores `7`. Nothing is lost.

In CUDA you request this by calling a named atomic instead of writing the bare operator. The
workhorse is `atomicAdd(&x, v)`: "add `v` to the location at address `&x`, atomically." (`&x` is the
*address* of `x` — atomics take a pointer to the cell they must update, not the value, because they
must lock that cell for the duration.) The hardware also provides `atomicMax`/`atomicMin` (keep the
larger/smaller of the stored value and a new one — useful for finding a maximum across all threads),
and the most general one, `atomicCAS` (**compare-and-swap**): "read the location; *if* it still holds
the value I expected, write my new value; either way tell me what was there." Compare-and-swap is the
**universal primitive** — given only atomic CAS you can build any other atomic update by reading the
current value, computing the desired new value, and CAS-ing it in, retrying if someone changed the
location in between. That retry loop is how lock-free updates of *arbitrary* shapes are built on top
of one hardware guarantee.

### Why it works: the indivisible step removes the gap the race lived in

The whole danger of `x += v` was the *gap* between read and write — a window in which the value a
thread is about to write has gone stale, because someone else updated `x` in the meantime. Every
lost update is one thread writing a value computed from data that is no longer current.

Atomicity is the direct denial of that window. By promising the read-modify-write is one
uninterruptible event, the hardware makes it *impossible* for any thread to observe or alter the
location between another thread's read and its write. The value a thread reads inside an atomic is
therefore guaranteed to still be current at the moment it writes, because nothing could have changed
it in between. The invariant this maintains is exact: **every contributed update is reflected in the
final value, and none is overwritten by a thread working from stale data.** That is why `atomicAdd`
is correct where `+=` is not — not because addition changed, but because the indivisibility closed
the gap the race needed.

The cost is the flip side of the same promise. "No other thread may touch this location during my
atomic" means that when many threads aim atomics at the **same** address, they cannot all proceed at
once — the hardware must let them through **one at a time**. They **serialize**: a queue forms on
that address, and its length is the number of contending threads. Atomics to *different* addresses do
not contend and run in parallel as usual; it is only same-address traffic that lines up. So an atomic
is correct regardless of contention, but its *speed* degrades as more threads pile onto one cell. The
guarantee and the bottleneck are two faces of the single rule "indivisible per location."

### The cure for contention: privatize, then combine

Because the slowdown comes from many threads queueing on *one* address, the remedy is to stop them
sharing that address until the last moment. This is **privatization**. The thread hierarchy already
gives the natural unit: the block, whose threads sit together on one streaming multiprocessor and can
share a small fast on-chip scratch memory. Instead of every thread in the grid doing an atomic on the
single global location, you give *each block* its own private partial accumulator — kept in the
block's fast shared scratch memory — and the threads of that block do their atomics on **their own**
block's partial. Contention is now confined to within a block (far fewer threads, on far faster
memory) instead of across the whole grid. Then, exactly **once per block**, a single thread does one
atomic that adds the block's finished partial into the one true global location. The number of
atomics hitting the global cell drops from "one per thread" to "one per block" — a thousandfold
reduction when blocks hold hundreds of threads. The result is identical; the serialization on the hot
global address is slashed.

### Worked instance: a thousand threads incrementing one counter

Launch `1000` threads of the hierarchy, each told to add `1` to a single global integer
`counter`, which starts at `0`. The correct final value is plainly `1000` — a thousand increments of
one. Run it three ways and follow the numbers.

**The plain `counter += 1` (broken).** Each thread does read → add → store, and these interleave
freely because the hierarchy guarantees no ordering. Concretely, suppose at some moment `counter`
holds `742`. Thread P reads `742`. Before P stores, thread Q also reads `742`. P computes `743` and
stores it; Q computes `743` from its own stale read and stores `743` too. Two threads ran, but
`counter` advanced from `742` to `743` — a single step. One increment was lost, and this collision
recurs throughout the run. The final value is some number **less than 1000** (how much less depends
on the timing — say `968` on one run, `981` on another, never repeatable). That non-determinism is
the signature of the race.

**The atomic `atomicAdd(&counter, 1)` (correct, serialized).** Now each thread's read-add-write is
one indivisible event on `&counter`. When P is mid-increment, Q is blocked from reading `counter` at
all; Q must wait until P's `743` has fully landed, then Q reads `743`, computes `744`, stores `744`.
No two threads ever read the same value, so no increment is lost. Every one of the 1000 atomics
advances the counter by exactly `1`, and the final value is **exactly `1000`**, every run, with no
variability. The price: those 1000 atomics all target the one address `&counter`, so they
**serialize** into a queue of length 1000 — the threads pass through that single cell strictly one
after another, which is the slow part, even though the answer is now right.

**Privatized (correct *and* fast).** Say the 1000 threads are arranged as 4 blocks of 250. Give each
block a private partial counter (`0` to start) in its fast shared scratch memory. Within a block, the
250 threads `atomicAdd` into *their own* block's partial — contention is now at most 250-wide and on
fast memory, so each block independently reaches a partial of `250`. Then one designated thread per
block does a single `atomicAdd(&counter, partial)` into the global counter. The global address now
sees only **4** atomics (one per block), not 1000: `0 + 250 = 250`, `250 + 250 = 500`,
`500 + 250 = 750`, `750 + 250 = 1000`. Same exact answer, `1000`, but the queue on the hot global
cell shrank from 1000 deep to 4 deep. This is the histogram pattern in miniature — when many threads
tally counts into bins, each block tallies a private copy of the bins first, then merges block
copies into the global bins at the end, so the only globally contended atomics are the few merges.

## Prerequisites

- [[cuda-thread-hierarchy]]

## Sources

- linux-internals-complete.html — *Atomic operations* (CUDA): `atomicAdd` / `atomicCAS` provided on
  both global and shared memory; the `atomicAdd(&histogram[bin], 1)` example for safely tallying when
  you don't know which thread writes last; "atomics serialize," heavy use creates contention from
  "many threads queueing on the same address," and the standard "per-block atomics on shared memory,
  then one atomic per block to global at the end" pattern (privatization). The definition of
  *atomically* as "all-at-once, like a light switch — no observable in-between state," and the
  lost-update race in which `x += 1` compiles to load / add / store and "two threads both reading the
  old value produce a lost update," are taken from the same document's treatment of single
  uninterruptible operations versus multi-step ones.
