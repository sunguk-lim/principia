---
id: memory-coalescing
title: Memory Coalescing
summary: Memory coalescing is about the pattern in which the 32 threads of a warp read or write global memory — the large, slow off-chip space from gpu-memory-spaces.
type: concept
tags: [gpu]
prereqs: [warp, gpu-memory-spaces]
sources:
  - "linux-internals-complete.html — 'Coalescing — global memory access pattern'"
  - "linux-internals-complete.html — 'Memory access patterns — coalescing and bank conflicts'"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Memory Coalescing

## Summary

**Memory coalescing** is about the *pattern* in which the 32 threads of a [[warp]] read or
write **global memory** — the large, slow off-chip space from [[gpu-memory-spaces]]. The
hardware never services those 32 accesses one at a time; it fetches global memory only in
fixed-width chunks called **transactions** (a transaction is one all-or-nothing trip to that
slow space that moves a whole aligned block of bytes — say 128 bytes — no matter how few of
them anyone asked for). The defining question is: do the warp's 32 accesses *fall inside the
same block*? If consecutive [[warp]] lanes touch consecutive addresses (lane *k* touches
element *k*), all 32 land in one 128-byte block and the hardware **coalesces** them into a
single wide transaction — every fetched byte is used, near-peak bandwidth, no waste. If the
lanes touch scattered or strided addresses, each one lands in a *different* block, so the one
warp triggers up to **32 separate transactions**, and almost all of each fetched block is
thrown away. The why: global/off-chip bandwidth is the GPU's scarcest resource (the
[[gpu-memory-spaces]] node showed off-chip is roughly an order of magnitude slower than
on-chip), and coalescing is the single biggest lever on it — and it is decided entirely by
*how you map [[warp]] lanes to addresses*.

## Grounded explanation

### What the concept *is*: the access pattern of a warp against the slow space

Two prerequisites set the stage, and the concept lives exactly at their meeting point.

From [[warp]]: the hardware's true unit of execution is not a thread but a **warp** — a fixed
bundle of 32 threads running in lockstep, each cycle issuing *one* instruction that all 32
**lanes** (the 32 thread-positions, numbered 0 to 31) carry out together, each on its own
data. When that one instruction is a memory load or store, all 32 lanes issue their accesses
*at the same moment*, as one batch.

From [[gpu-memory-spaces]]: data lives in named spaces, and the one that matters here is
**global memory** — the grid-wide space physically backed by off-chip HBM, the large-but-slow
bottom rung. That node's central lesson was that off-chip access is *the* dominant cost, far
slower than on-chip storage, so the bytes you move to and from global memory are what you pay
for.

Memory coalescing is what happens when those two facts collide: **a whole warp's worth of
global-memory accesses arriving at once, against a space the hardware can only touch in
fixed-width blocks.** The hardware does not, and cannot cheaply, fetch one arbitrary 4-byte
float from HBM in isolation; the smallest thing it moves is a whole aligned chunk — here we
will use a **128-byte transaction**, a single trip that delivers an aligned 128-byte block of
global memory (which is exactly 32 four-byte floats). So when a warp issues 32 loads, the
hardware's real question is not "fetch these 32 values" but "which 128-byte blocks do these
32 addresses fall into, and how many transactions does that take?" *Coalescing* is the good
case — the 32 accesses collapse ("coalesce") into the fewest transactions because they share
blocks. The concept *is* this mapping from a warp's access pattern to a transaction count.

Define the term plainly: a warp's accesses are **coalesced** when its 32 lanes hit addresses
that fall within one (or very few) aligned 128-byte blocks, so the hardware serves them in
one (or very few) transactions. They are **uncoalesced** when the lanes are spread across many
blocks, forcing many transactions.

### Why it matters: bandwidth is the scarce resource, and the pattern sets the waste

Here is the why, and it follows straight from [[gpu-memory-spaces]]. A transaction always
moves a *full* block (128 bytes) regardless of how much of it the warp actually wanted. The
useful work in a load is the bytes the lanes asked for; the *cost* is the blocks the hardware
had to drag across the slow off-chip link. So the figure of merit is

> useful bytes ÷ bytes actually moved.

When a warp's 32 lanes each want a 4-byte float and all 32 floats sit inside one 128-byte
block, one transaction moves 128 bytes and the warp wanted all 128 — efficiency is 100%, and
the warp consumed exactly *one* unit of the GPU's scarcest resource. When those same 32 floats
are scattered one-per-block, the hardware must run 32 transactions to gather them: it moves
32 × 128 = 4096 bytes to deliver the same 128 useful bytes — efficiency is 128 ÷ 4096 = 1/32,
and the warp burned *32* units of bandwidth for the identical result. Same arithmetic, same
output, same 32 floats consumed — but **32× the off-chip traffic** purely because of how the
addresses were laid out relative to lanes.

That is why coalescing is the dominant lever. The [[gpu-memory-spaces]] node established that
trips to the slow space are what you pay for; coalescing decides *how many trips* one warp
forces. And the non-obvious, almost magic-looking part is that the program's *math* and its
*results* are unchanged between the fast and slow versions — what changed is invisible to the
output and lives entirely in the lane-to-address map. A reader who does not see the
transaction-block granularity finds a 32× slowdown with no change in computed values
inexplicable; the granularity *is* the explanation. (The same idea recurs one level up in the
fast on-chip space: shared memory is split into 32 *banks*, and a warp whose lanes hit
distinct banks is served in one cycle while one that piles onto a single bank serializes —
the on-chip analog of coalescing, called *bank conflicts*. It is a separate topic; the point
here is only that "match the warp's pattern to the hardware's chunking" is the recurring rule,
and for the slow global space that rule is coalescing.)

### Worked instance: one warp, two address maps

Take one [[warp]] — 32 threads, lanes 0 through 31 — reading from a contiguous array `a` of
4-byte floats that lives in global memory (HBM). Let `lane` be the lane's number, 0..31. The
hardware serves global reads in aligned **128-byte transactions**, and 128 bytes ÷ 4 bytes =
exactly **32 consecutive floats per transaction**. We run the *same* warp under two
lane-to-address maps and count transactions. Neither case is degenerate: both issue all 32
loads; what differs is only the stride.

**Case 1 — coalesced: each lane reads `a[lane]`.** Lane 0 reads `a[0]`, lane 1 reads `a[1]`,
…, lane 31 reads `a[31]`. These are 32 consecutive floats — elements 0 through 31 — which is
exactly one aligned 128-byte block (32 floats × 4 bytes = 128 bytes). All 32 lanes fall inside
that single block, so the hardware issues **one** 128-byte transaction. It moves 128 bytes;
the warp wanted all 128. Useful ÷ moved = 128 ÷ 128 = **100%**, **1 transaction**. This is the
design point: the warp pulls a full block, every byte of which feeds a lane. (This is the very
pattern the [[gpu-memory-spaces]] worked example used when 256 threads cooperated to load a
tile "one element per thread" — that split is coalesced precisely because consecutive lanes
took consecutive elements.)

**Case 2 — strided, uncoalesced: each lane reads `a[lane * 32]`.** Now lane 0 reads `a[0]`,
lane 1 reads `a[32]`, lane 2 reads `a[64]`, …, lane 31 reads `a[992]`. Walk the blocks: a
128-byte block holds 32 consecutive floats, so block 0 is `a[0..31]`, block 1 is `a[32..63]`,
block 2 is `a[64..95]`, and so on. Lane 0's `a[0]` sits in block 0; lane 1's `a[32]` sits in
block 1; lane 2's `a[64]` sits in block 2; … lane 31's `a[992]` sits in block 31. **Every lane
lands in a different block.** The hardware cannot coalesce — it must run **32** separate
128-byte transactions, one per lane. Each transaction drags in 128 bytes but the warp uses
only the single 4-byte float it asked for; the other 124 bytes of each block are fetched and
discarded. Total bytes moved = 32 × 128 = 4096; useful bytes = 32 × 4 = 128. Useful ÷ moved =
128 ÷ 4096 = **1/32 ≈ 3%**, **32 transactions**.

**Compare the two:**

| | lane → element | distinct 128-byte blocks touched | transactions | useful ÷ moved |
|---|---|---|---|---|
| Case 1 (coalesced) | `a[lane]` | 1 | 1 | 128/128 = 100% |
| Case 2 (strided) | `a[lane*32]` | 32 | 32 | 128/4096 ≈ 3% |

Same warp, same 32 floats' worth of useful data, same downstream computation — but Case 2
moves **32× more bytes** across the slow off-chip link and so runs at roughly **1/32 the
effective bandwidth**. The entire difference is the stride in the address map.

**The rule, and the fix.** Make consecutive [[warp]] lanes touch consecutive addresses —
"thread *i* accesses element *i*." That single discipline turns Case 2 into Case 1. When the
data's natural layout forbids it (for instance, you must read down the *columns* of a matrix,
which are strided in memory), the standard remedy uses [[gpu-memory-spaces]]: have the warp
load the data with a *coalesced* pattern into the block's fast on-chip **shared memory** first,
then read it back from there in whatever order the math wants. The expensive global trips stay
coalesced; the awkward, strided rearrangement happens in the fast space where, per
[[gpu-memory-spaces]], the cost is an order of magnitude smaller. That is why "is this access
coalesced?" is among the first questions asked of any GPU kernel.

## Prerequisites

- [[warp]]
- [[gpu-memory-spaces]]

## Sources

- *linux-internals-complete.html* — "Coalescing — global memory access pattern": the hardware
  combines a warp's global-memory requests into a single transaction *if* they fall in a
  contiguous, aligned 128-byte chunk; coalesced `a[threadIdx.x]` → 1 transaction of 128 bytes,
  strided `a[threadIdx.x*32]` → 32 separate transactions, up to a 32× loss; the design rule
  "thread *i* should access element *i*," and using shared memory as a staging area to fix a
  bad layout.
- *linux-internals-complete.html* — "Memory access patterns — coalescing and bank conflicts":
  access pattern is the #1 determinant of kernel speed; the per-warp load/store coalescing
  into one 128-byte transaction (the `c[i]=a[i]+b[i]` walkthrough), and the shared-memory bank
  analog kept here as plain-prose mention only.
