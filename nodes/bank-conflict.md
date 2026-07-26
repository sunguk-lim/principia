---
id: bank-conflict
title: Bank Conflict
summary: A bank conflict is the one way that shared-memory — the fast, on-chip, block-scoped space that is supposed to be roughly as quick as a register — can silently turn slow.
type: concept
tags: [gpu]
prereqs: [shared-memory, warp]
sources:
  - "linux-internals-complete.html — 'Memory access patterns — coalescing and bank conflicts'"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Bank Conflict

## Summary

A **bank conflict** is the one way that [[shared-memory]] — the fast, on-chip,
block-scoped space that is supposed to be roughly as quick as a register — can silently
turn slow. The hardware does not build shared memory as a single monolithic block of
storage; it physically splits it into **32 equal-width slices called banks**, and each
bank can serve only **one access per cycle**. The 32 banks work in parallel, so the *best*
case is that the 32 lockstep threads of a [[warp]] each touch a *different* bank — then all 32 accesses
finish together in a single cycle. A bank conflict is the *worst* case: when several
threads of the warp ask for **different addresses that happen to live in the same bank**,
that one bank cannot serve them at once, so the hardware **serializes** them — it runs them
one after another. If *N* threads collide on a bank, their access takes *N* times as long;
the textbook disaster is a **32-way conflict**, where all 32 threads hit one bank and the
access is 32× slower. Because shared memory's whole reason for existing is to be fast, a
bank conflict throws away exactly the advantage you reached for — which is why the *layout*
of a shared array (and a one-element padding trick) is a real performance lever, not a
detail.

## Grounded explanation

### What a bank is, and the mapping that decides everything

From [[shared-memory]] we already have the picture in outline: shared memory is divided into
**32 banks**, each bank serves one request per cycle, and a warp of 32 threads gets its
fastest possible behaviour when those threads land on 32 distinct banks. This node makes that
the spine and explains *exactly* when threads collide, why the collision costs what it costs,
and how to lay data out to avoid it.

The first thing to pin down is **which bank a given location lives in**, because the entire
phenomenon is a consequence of that one mapping. Shared memory is addressed in 4-byte words
(the size of one `float` or one 32-bit integer), and the words are *striped* across the banks
in round-robin order:

- word 0 → bank 0, word 1 → bank 1, …, word 31 → bank 31,
- word 32 → bank 0 again, word 33 → bank 1, and so on.

In one sentence: **word *i* lives in bank *(i mod 32)*** — you take the word's index, divide
by 32, and the remainder is its bank. This is the only rule you need. Two locations conflict
when, and only when, they have the *same remainder mod 32* — that is, when their indices differ
by a multiple of 32. "Differ by a multiple of 32" is the precise meaning of the loose phrase
*stride 32*: stepping through memory 32 words at a time keeps landing you in the same bank.

### The three cases a warp can fall into

When the 32 threads of a warp access shared memory in one instruction, exactly one of three
things happens, and naming all three is what keeps the worked instance below from being
degenerate (it is the conflict case — case 3 — that actually triggers the mechanism):

1. **All distinct banks — the ideal, full speed.** Each of the 32 threads targets a different
   bank. All 32 banks fire in parallel, the whole warp's access completes in **one cycle**.
   This is what you get for free when thread *i* reads word *i* of a contiguous array: the 32
   consecutive words 0…31 map to the 32 distinct banks 0…31.

2. **All the same address — a broadcast, also full speed.** If *every* thread of the warp reads
   the *identical* location (e.g. all 32 threads read word 7), the hardware does **not** treat
   that as 32 colliding requests. It reads the word once and hands the same value to all 32
   threads — a **broadcast** — in one cycle. This is the subtle exception that makes the rule
   precise: a conflict requires *different* addresses in the same bank. Same address is free;
   same bank, different address is not.

3. **Same bank, different addresses — a bank conflict, the slow case.** If two or more threads
   ask for *different* words that happen to share a bank, that bank has only one port and must
   answer them in sequence. The warp's access is split into as many cycles as the most-loaded
   bank has distinct requests. If *N* threads pile different addresses onto one bank, that is an
   **N-way conflict** and the access costs **N cycles** instead of one — an *N×* slowdown. The
   reads still all happen and the answers are still correct; you simply pay *N* times the time.

So the cost of a shared access is set by the single most-contended bank in the warp: one cycle
if no bank is asked for more than one distinct address, *N* cycles if some bank is asked for *N*.

### The worked instance: row vs. column of a 32×32 tile, and the padding fix

Take a concrete, non-degenerate case — a **32×32 tile of `float`s** staged in shared memory by
a block, exactly the kind of staging tile [[shared-memory]] used for tiled matrix multiply.
Stored row-major, the tile occupies words 0…1023, and the element at row *r*, column *c* sits at
word index **`r * 32 + c`**. Apply the mapping (bank = index mod 32):

**Reading a row (conflict-free).** Suppose the 32 threads of a warp read one full row — thread
*c* reads element (row 5, column *c*) for *c* = 0…31. The word indices are
`5*32 + 0, 5*32 + 1, …, 5*32 + 31` = 160, 161, …, 191. Their banks are `160 mod 32 = 0`,
`161 mod 32 = 1`, …, `191 mod 32 = 31` — the 32 distinct banks 0…31. This is **case 1**: one
cycle, full speed. Consecutive words → consecutive banks, always.

**Reading a column (a 32-way conflict).** Now have the 32 threads read one full *column* instead
— thread *r* reads element (row *r*, column 0) for *r* = 0…31. The word indices are
`0*32 + 0, 1*32 + 0, …, 31*32 + 0` = 0, 32, 64, …, 992 — that is **stride 32**. Their banks are
`0 mod 32 = 0`, `32 mod 32 = 0`, `64 mod 32 = 0`, …, all the way to `992 mod 32 = 0`. **Every
one of the 32 threads lands in bank 0**, asking for 32 *different* words. That is **case 3** at
its worst: a 32-way conflict, served in 32 cycles, **32× slower** than the row read — even
though the row read and the column read move the exact same number of bytes. The slowdown is
created entirely by the access *pattern* meeting the bank *layout*; nothing about the data
changed.

**The fix: pad the row to 33 (`tile[32][33]`).** The cure is to declare the tile one element
wider than it needs to be — 33 columns instead of 32 — and just never use the extra column.
Now the element at row *r*, column *c* sits at word **`r * 33 + c`**. Redo the column read
(column 0, rows 0…31): the indices are `0*33, 1*33, …, 31*33` = 0, 33, 66, …, 1023, a **stride
of 33**. Their banks are `0 mod 32 = 0`, `33 mod 32 = 1`, `66 mod 32 = 2`, …, `1023 mod 32 = 31`
— the 32 distinct banks 0…31 again. **Conflict gone; back to one cycle.** The reason it works is
exactly the mapping: a stride of 33 is *coprime* to 32 (33 = 32 + 1, so each successive row
advances the bank by one and wraps cleanly through all 32), whereas the stride of 32 was a
multiple of 32 and so kept the bank pinned. Padding by one element shifts every row's bank
alignment by one, which is the minimum nudge that breaks the lockstep collision. The price is a
single wasted column of storage — a trivial cost to recover a 32× read.

### Why this matters, and the global-memory cousin

The point of all of this is the *why*. [[shared-memory]] earns its keep by being on the fast
on-chip rung, roughly an order of magnitude quicker per access than off-chip global memory — that
is the entire reason a kernel bothers to stage data into it. A bank conflict quietly hands a
chunk of that win back: a 32-way conflict makes the "fast" space take 32 cycles for what should
have taken one, so a kernel can do all the work of tiling into shared memory and still run slow
because its threads read the tile down columns. This is why bank-conflict-free layout — and the
one-element padding trick in particular — is a standard tuning lever, not a curiosity: it is how
you make sure the fast space is actually fast.

It is worth separating bank conflicts from their close relative so the two are not confused.
**Coalescing** is the analogous "spread your accesses out" rule, but for *global* memory rather
than shared. When the 32 threads of a warp read *contiguous, aligned* addresses in global memory
(thread *i* reads element *i*), the hardware fuses all 32 reads into a single wide memory
transaction — coalesced, fast. When they read with a large stride or scattered addresses, the
warp's reads break into many separate transactions, up to 32× slower. So both rules reward
consecutive, regular access by a warp and punish strided or scattered access — but a bank
conflict is about parallel *banks within shared memory*, while coalescing is about fusing
*transactions to global memory*. Same instinct, two different spaces.

## Prerequisites

- [[shared-memory]]
- [[warp]]

## Sources

- *linux-internals-complete.html* — "Memory access patterns — coalescing and bank conflicts": shared memory is divided into 32 banks, each serving one access per cycle, with 32 distinct banks giving a 1-cycle warp access and a same-bank collision giving 32 cycles serialized; the striping rule (`shared[0]`→bank 0, …, `shared[31]`→bank 31, `shared[32]` wraps to bank 0) so consecutive access is conflict-free while stride-32 access hits one bank; the classic fix of padding a 2D tile's last dimension by one (`tile[16][17]`) to shift each row's bank assignment; and coalescing as the analogous contiguous-access rule for global memory (one warp's 32 contiguous loads → one transaction; strided/scattered → up to 32 transactions).
