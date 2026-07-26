---
id: warp-shuffle
title: Warp Shuffle
summary: A warp shuffle is a single hardware instruction (__shfl_sync and its variants) that lets the 32 threads of a warp read each other's register values directly — one lane hands…
type: concept
tags: [gpu]
prereqs: [warp]
sources:
  - "linux-internals-complete.html — Synchronization — making threads wait for each other: Warp-level primitives (__shfl_sync / __shfl_xor_sync read another lane's register directly, no shared memory or sync, used heavily in fast reductions); __syncthreads() (the block-wide barrier the shuffle path avoids); Atomic operations; Memory access patterns — Bank conflicts (the shared-memory hazard the shuffle path sidesteps)"
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Warp Shuffle

## Summary

A **warp shuffle** is a single hardware instruction (`__shfl_sync` and its variants) that lets
the 32 threads of a [[warp]] read each other's **register** values *directly* — one lane hands
another lane the contents of one of its registers without that value ever touching memory. A
register is the tiny, fastest on-chip storage slot where a thread holds a value it is actively
computing on; ordinarily each lane's registers are private to that lane. The shuffle is the one
exception: because a [[warp]]'s 32 lanes execute in lockstep and physically sit together, the
hardware can route lane A's register straight into lane B's in one step, with **no shared
scratchpad memory and no barrier**. The killer use is a **warp-level reduction** — summing or
max-ing the 32 lanes' values down to one answer in just 5 steps, each step every lane combining
its value with one shuffled from a lane a fixed distance away. The reason it matters: for
exchanging data *inside* a single warp, shuffle is faster and simpler than the alternative
(staging through shared memory), because it skips the barrier, avoids the shared-memory access
hazards, and uses fewer instructions — exploiting that the [[warp]] is already a synchronized,
co-located unit.

## Grounded explanation

### What a shuffle is, and the substrate that makes it possible

The prerequisite [[warp]] node established the fact this whole concept rests on: a [[warp]] is 32
threads that the hardware runs in **lockstep** — every cycle all 32 lanes (the 32 thread-positions,
numbered 0 to 31) execute the *same* instruction at the *same* point in the program. They are not
32 independent agents that happen to run nearby; they are one synchronized bundle marching as a
unit. A warp shuffle is the instruction that cashes in on exactly that property.

First, two terms defined before they are used. A **register** is the small, fastest storage slot
on the chip where a thread keeps a value it is currently working with — when a thread computes
`x = a + b`, `a`, `b`, and `x` live in registers. Each lane has its *own* private set of registers;
normally one lane cannot see another lane's. Separately, **shared-memory** is a block of on-chip
scratchpad that *many* threads can read and write to pass data between each other — but reaching it
costs a memory access, and using it safely to communicate requires a **barrier**: an instruction
(`__syncthreads()`) at which no thread may proceed until *every* thread in the group has arrived, so
that a value one thread wrote is guaranteed visible before another thread reads it.

Against that backdrop, here is what a shuffle does. The instruction `__shfl_sync` takes a value
sitting in the calling lane's register and a *source lane number*, and returns to the calling lane
the value that the source lane holds in *its* register — **directly, register-to-register, in a
single instruction.** Nothing is written to shared memory; no barrier is executed. The data never
leaves the register file. This is the one sanctioned way for the otherwise-private lanes of a
[[warp]] to read each other's registers.

Why is the hardware *able* to do this when registers are private? Precisely because of lockstep and
physical co-location. Since all 32 lanes of the [[warp]] are executing the *same* shuffle
instruction on the *same* cycle, every lane is simultaneously offering up the register the
instruction names; and since the 32 lanes' register files sit physically together in one
[[warp]]-wide hardware unit, there are wires that can route any lane's named register to any other
lane's input in that one cycle. The shuffle is not a memory operation that happens to be fast — it
is a *permutation across the warp's registers*, made possible only because the [[warp]] is a single
lockstepped, co-located object rather than 32 scattered threads. A group of threads that were *not*
in lockstep could not do this: there would be no single cycle on which all of them are presenting
the same register to be routed.

There are a few variants, distinguished only by *how the source lane is chosen*:

- **`__shfl_sync`** — read from an *arbitrary* lane you name outright ("give me lane 7's value").
- **`__shfl_down_sync` / `__shfl_up_sync`** — read from a lane a fixed offset *N* away (down = from
  lane *k+N*, up = from lane *k−N*). These are the workhorses of reductions, below, because they
  let every lane reach a partner a controlled distance away.
- **`__shfl_xor_sync`** — read from the lane whose number is your own lane number XOR'd with a mask.
  XOR (exclusive-or) flips selected bits of the lane index, which pairs lanes up in a **butterfly**
  pattern: with mask 16, lane 0 pairs with lane 16, lane 1 with lane 17, and so on; halve the mask
  and the pairing tightens. Its nice property is that the pairing is *symmetric* — both partners
  read each other — so a reduction built on it leaves the final answer in **every** lane at once,
  not just lane 0.

### The why: a warp-level reduction, and why shuffle beats the shared-memory route

A **reduction** means collapsing many values into one by a combining operation — summing 32
per-lane numbers into a single total, or taking their maximum. This is the canonical job for warp
shuffle, and seeing it is the whole point of the concept.

The naive way to add up 32 values would be to hand them one by one to a single accumulator — 32
sequential adds. The shuffle reduction instead uses a **tree**: at each step it *halves the number
of distinct partial sums* by having every lane add in a value shuffled from a partner a fixed
distance away. Because each step halves the work, the whole reduction finishes in log₂(32) = **5
steps** instead of 32. The non-obvious, "magic-looking" step is *why this leaves a correct total
in one lane*, so here is the justifying invariant, made precise.

Let each lane *k* hold a value `v[k]`. The reduction runs five rounds with halving offsets 16, 8,
4, 2, 1. In each round every lane does the same thing:

> `v[k] = v[k] + __shfl_down_sync(v[k], offset)`

— that is, lane *k* adds to its own value the value currently held by lane *k + offset*.

The invariant that makes it correct: **after the round with offset *d*, lane *k* holds the sum of
the original values in lanes *k* through *k + (2·d − 1)*** — a contiguous block of `2d` original
values, anchored at lane *k*. Walk it through. Before any round, lane *k* holds just `v[k]` (a block
of 1). Round with offset 16: lane *k* adds lane *k+16*'s value; lane 0 now holds `v[0]+v[16]`, and
in general the block size doubles from 1 to 2 — but written as the invariant, after the *last*
round (offset 1) lane 0 holds the sum of lanes 0 through 31, i.e. **all 32 values**. Each halving
of the offset exactly doubles the span of original values that lane 0's running sum covers: it
covers 16-wide reach after offset 16, then the offsets 8, 4, 2, 1 fill in and stitch the halves
together, until lane 0's block spans the entire warp. Lane 0 holds the answer. (If we had used
`__shfl_xor_sync` with the same halving masks instead, the symmetry of the butterfly would leave the
*identical* total sitting in **all 32 lanes**, not just lane 0 — that is the one functional
difference of the XOR variant.)

Now the WHY this is the preferred tool. The classic alternative for combining values across threads
is to route them through **shared memory**: each lane writes its value to a shared scratchpad slot,
everyone hits a `__syncthreads()` barrier so the writes are visible, then lanes read partners' slots
and combine. That path carries three costs the shuffle avoids:

1. **A barrier.** The shared-memory route must execute `__syncthreads()` so no lane reads a slot
   before its writer has filled it. The shuffle needs *no* barrier: the [[warp]]'s lanes are
   *already* in lockstep, so a value is intrinsically ready to be read on the same cycle it is
   offered. The synchronization the barrier buys is free here, baked into what a [[warp]] is.

2. **Memory traffic and a layout hazard.** The shared-memory route does real reads and writes to
   the scratchpad, and shared-memory is split into 32 **banks** (independent slots that each serve
   one access per cycle); if several lanes' chosen addresses fall in the *same* bank, those accesses
   **serialize** instead of happening at once — a slowdown called a *bank conflict*, which kernel
   authors must contort their data layout to avoid. The shuffle touches no shared memory at all, so
   there are no banks involved and no conflict to design around — the data stays in registers.

3. **Fewer instructions.** Write-barrier-read is several instructions; a shuffle-and-combine is one
   shuffle plus one add per step. For communication that stays *inside one warp*, the shuffle path
   is strictly shorter.

So warp shuffle is not merely an alternative to shared memory — it is the *right* tool for the
specific case of intra-warp communication, because it spends nothing on the coordination (barrier)
and staging (shared-memory banks) that the general route needs, by exploiting that the [[warp]] is
already a synchronized, physically-unified object. (When threads in *different* warps must
communicate, lockstep no longer holds across them, so the shared-memory-plus-barrier route is still
required; shuffle's reach stops at the 32-lane warp boundary.)

### Worked instance: summing 32 per-lane values in 5 shuffles

Take one [[warp]] where lane *k* holds the number `v[k]`. To keep the arithmetic checkable, let
`v[k] = k + 1`, so the lanes hold `1, 2, 3, …, 32`, and the true total is `1 + 2 + ⋯ + 32 = 528`.
Run the five `__shfl_down_sync` rounds with offsets 16, 8, 4, 2, 1 and track lane 0 (the lane that
ends with the answer); each number below is derived from the previous round, no jumps.

- **Start.** Lane 0 holds `v[0] = 1`. (Block of 1: just lane 0.)
- **Round offset 16.** Lane 0 adds lane 16's value, `v[16] = 17`. Lane 0 now holds `1 + 17 = 18`.
  More usefully, by the invariant lane 0 now holds the sum of original lanes 0–1's *halves*; what
  matters is that after all rounds the block grows to cover everything. Lane 0 = `18`.
- **Round offset 8.** Lane 0 adds what lane 8 *currently* holds. Lane 8 went through the offset-16
  round too, so it holds `v[8] + v[24] = 9 + 25 = 34`. Lane 0 now holds `18 + 34 = 52`.
- **Round offset 4.** Lane 0 adds lane 4's current value. Lane 4 holds the sum of original lanes
  4, 12, 20, 28 = `5 + 13 + 21 + 29 = 68`. Lane 0 now holds `52 + 68 = 120`.
- **Round offset 2.** Lane 0 adds lane 2's current value, which by now is the sum of original lanes
  2, 6, 10, 14, 18, 22, 26, 30 = `3 + 7 + 11 + 15 + 19 + 23 + 27 + 31 = 136`. Lane 0 holds
  `120 + 136 = 256`.
- **Round offset 1.** Lane 0 adds lane 1's current value, the sum of all 16 odd-indexed original
  lanes = `2 + 4 + 6 + ⋯ + 32 = 272`. Lane 0 holds `256 + 272 = 528`.

After five shuffles lane 0 holds **528** — the sum of all 32 values — computed entirely in
registers, with no shared-memory write, no bank to worry about, and no `__syncthreads()`. Each round
exactly doubled the span of the partial sum (lane 0's running total covered 2, then 4, 8, 16, and
finally all 32 original values), which is why 5 = log₂(32) rounds suffice. Had the rounds used
`__shfl_xor_sync` with masks 16, 8, 4, 2, 1 instead, the same `528` would sit in *all* 32 lanes at
the end rather than only lane 0 — the butterfly's symmetry being the one behavioral difference from
the down-shift version.

## Prerequisites

- [[warp]]
## Sources

- linux-internals-complete.html — *Synchronization — making threads wait for each other*,
  subsection *Warp-level primitives*: for exchanging data between threads within a warp you need no
  shared memory or sync — `__shfl_sync` / `__shfl_xor_sync` read another lane's register directly,
  used heavily in fast reductions. Supporting context from the same and adjacent sections:
  *`__syncthreads()`* (the block-wide barrier the shuffle path avoids), *Atomic operations*, and
  *Memory access patterns — Bank conflicts* (shared memory's 32 banks serialize on same-bank access
  — the hazard the register-only shuffle sidesteps).
