---
id: gpu-memory-spaces
title: GPU Memory Spaces
summary: When you write a GPU program, every piece of data you touch lives in one of a few distinct memory spaces — named regions like registers, shared memory, and global memory.
type: concept
tags: [gpu]
prereqs: [memory-hierarchy, cuda-thread-hierarchy]
sources:
  - "linux-internals-complete.html — 'Memory spaces — where pointers live'"
  - "linux-internals-complete.html — 'Resource scope — what's shared at what level'"
  - "linux-internals-complete.html — 'Shared memory — the per-block scratchpad'"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# GPU Memory Spaces

## Summary

When you write a GPU program, every piece of data you touch lives in one of a few
distinct **memory spaces** — named regions like *registers*, *shared memory*, and
*global memory*. These spaces are not new hardware; they are the **programmer-visible
faces** of the [[memory-hierarchy]]'s physical levels (the tiny-but-instant register
slots, the fast on-chip SRAM, the large-but-slow off-chip HBM). The defining fact is
that each space's **scope** — who is allowed to see the data in it — lines up exactly
with a level of the [[cuda-thread-hierarchy]]: registers are private to one **thread**,
shared memory is private to one **block**, and global memory is visible to the whole
**grid** (and to the host that launched it). Because the [[memory-hierarchy]] makes
on-chip storage vastly faster than off-chip HBM, *where a pointer lives decides how fast
reading it is*. This makes memory spaces **the** central performance lever in GPU
programming: a good program keeps frequently-used data in the fast, small, private
spaces and minimizes trips to the large, slow, shared one.

## Grounded explanation

### What the concept *is*: physical levels wearing programmer-facing names, each tied to a scope

The [[memory-hierarchy]] gives us the physical picture: a ladder of stores where each
rung *down* holds more bytes but moves them slower — a few hundred kilobytes of register
slots beside the math units (effectively instant), tens of megabytes of on-chip SRAM
(very fast), and tens of gigabytes of off-chip HBM, the GPU's main memory (large but
slow). That is the *hardware's* view.

A GPU program never names a "rung" directly. Instead it works with **memory spaces**: a
memory space is a labelled region that the program can put data in, and the label tells
the compiler *which physical level the data lives on* and *which threads are allowed to
reach it*. So a memory space pairs a **physical home** (a rung of the
[[memory-hierarchy]]) with a **scope** (a level of the [[cuda-thread-hierarchy]]). Recall
from [[cuda-thread-hierarchy]] the three nested levels of parallelism: a single **thread**
is the smallest worker; threads are grouped into a **block**; blocks together form the
**grid** that runs one launch of the program. The key structural fact of this node is that
the spaces' scopes are exactly these levels:

| Memory space | Physical home (rung of [[memory-hierarchy]]) | Scope (level of [[cuda-thread-hierarchy]]) | Who can read/write it |
|---|---|---|---|
| **Registers** | register slots beside the math units (fastest, tiny) | **thread** | one thread — its own private slice |
| **Shared memory** | on-chip SRAM (fast) | **block** | every thread in the same block |
| **Global memory** | off-chip HBM (large, slow) | **grid** + host | every thread in the grid, and the host |

Two more spaces exist, mentioned once for completeness and not used again: **constant**
memory is a small read-only region living in HBM but heavily cached, so it reads almost as
fast as a register when the cache holds it; **local** memory has a misleading name — it is
*per-thread* like registers, but it is actually backed by slow HBM, used only when a thread
needs more private storage than its register slice can hold. The three rows in the table are
the ones that matter.

This is the whole concept: **registers ↔ thread, shared ↔ block, global ↔ grid.** A
pointer's space is part of its identity. Two pointers can hold the same numeric address-like
value yet refer to different spaces, and the compiler emits a *different* load/store
instruction for each, because reaching a register, on-chip SRAM, or off-chip HBM are
physically different operations.

### Why it matters: the on-chip / off-chip speed gap makes "where it lives" the dominant cost

Why should a programmer care which space a value sits in? Because the [[memory-hierarchy]]
already told us the answer: the rungs differ enormously in speed. Reading a value from a
register or from on-chip SRAM costs on the order of a single cycle to a few tens of cycles.
Reading the *same* value from off-chip HBM (global memory) costs on the order of several
hundred cycles — the [[memory-hierarchy]]'s slow bottom rung. The gap between on-chip and
off-chip access is large, roughly an order of magnitude or more.

So the space a value lives in *is* its access cost. The scopes make this a real design
choice rather than an accident:

- **Registers (per thread)** are the fastest and smallest. A thread keeps its hot working
  values here. Nothing else can see them, which is exactly why they can be the fastest — no
  coordination with other threads is needed.
- **Global memory (per grid)** is the only space large enough to hold the program's full
  input and output arrays, and the only one the host can fill before launch and read back
  after. But it sits on the slow HBM rung, so every access to it is expensive.
- **Shared memory (per block)** is the bridge. It sits on the fast on-chip SRAM rung yet,
  unlike registers, is visible to *all* threads in a block — so a block of threads can
  **cooperate** through it: one thread writes a value, another reads it, without anyone
  making the slow trip out to HBM.

This yields the single most important rule of GPU performance, and it follows directly from
the [[memory-hierarchy]]'s lesson that *moving bytes from the slow rung is what you pay for*:
**a good program keeps frequently-reused data in the fast, private spaces (registers and
shared memory) and minimizes the number of trips to slow global memory.** The
[[memory-hierarchy]] node showed that an algorithm wins by loading a chunk into fast storage
*once* and reusing it many times; memory spaces are the programmer's controls for doing
exactly that, and **shared memory** is the lever's handle — the on-chip scratchpad a block
loads once and reuses. (Shared memory's own mechanics are a separate topic; here it is just
"the fast space a whole block can see.")

There is also a temporal edge to scope worth one sentence: when one launch of the grid
finishes and another begins, registers and shared memory **evaporate** — only global memory
(HBM) survives across launches. That is the other reason the input/output arrays must live in
global memory: they are the only data that outlasts a single grid.

### Worked instance: a block of 256 threads reusing a 256-element tile

Take a concrete, non-degenerate case. A block of **256 threads** must each compute something
that depends on the *same* 256-element array — call it a **tile** — and the tile is reused
**many** times during the block's work, say 256 times (once per thread's inner loop pass).
The tile starts out, like all input data, in **global memory** (HBM). The question is *which
space we read the tile from*, and the [[memory-hierarchy]]'s speed gap decides the cost.

**Plan A — read the tile from global memory every time.** Each of the 256 threads reads all
256 tile elements, 256 times over. Count the slow HBM reads:

```
global reads = 256 threads × 256 elements × 256 reuses
             = 256 × 256 × 256
             = 16,777,216 reads from HBM.
```

Every one of those ~16.8 million reads pays the slow off-chip latency of the
[[memory-hierarchy]]'s bottom rung (several hundred cycles each). The block spends almost all
its time waiting on HBM — precisely the *memory-bound* trap the [[memory-hierarchy]] warns of.

**Plan B — load the tile into shared memory once, then reuse it on-chip.** The block uses its
**shared-memory** space (the fast on-chip rung, scope = the whole block). First the 256
threads cooperate to copy the tile in from global memory — the natural split is one element
per thread, so the *entire* tile arrives in **one pass** of 256 global reads:

```
global reads = 256 elements × 1 (each loaded once, by one thread) = 256 reads from HBM.
```

After that load, the tile sits in shared memory, where **every** thread in the block can see
it (that is what block-scope buys us). All the reuse now happens on-chip:

```
shared reads = 256 threads × 256 elements × 256 reuses = 16,777,216 reads from shared memory.
```

The reuse count is *identical* to Plan A — we did not do less work. What changed is *which
rung* served it. Compare the slow-rung traffic, the only term the [[memory-hierarchy]] says we
pay dearly for:

```
HBM reads, Plan A : 16,777,216
HBM reads, Plan B :        256
reduction         : 16,777,216 ÷ 256 = 65,536× fewer trips to slow global memory.
```

The ~16.8 million expensive HBM reads collapse into 256 expensive reads plus ~16.8 million
*cheap* on-chip shared reads. Because the on-chip rung is roughly an order of magnitude faster
per access, the block's running time drops by a comparable factor. We did not buy faster
hardware and we did not reduce the arithmetic — we only changed **where the reused data
lives**, moving it from the grid-scoped slow space into the block-scoped fast space. That is
the entire payoff of understanding memory spaces, and it is why "where does this pointer live?"
is the first question a GPU programmer asks.

## Prerequisites

- [[memory-hierarchy]]
- [[cuda-thread-hierarchy]]

## Sources

- *linux-internals-complete.html* — "Memory spaces — where pointers live": the table of spaces (registers, shared, L1/L2, global/HBM, constant, local), their physical home, scope, and latency, plus the note that "local" is HBM under a misleading name.
- *linux-internals-complete.html* — "Resource scope — what's shared at what level": registers per thread, shared memory per block, global (HBM) per GPU/grid, and the fact that only HBM survives across grid launches.
- *linux-internals-complete.html* — "Shared memory — the per-block scratchpad": shared memory is ~30× faster than HBM, lets a block's threads cooperate, and the tile-reuse example where loading once and reusing cuts HBM traffic sharply.
