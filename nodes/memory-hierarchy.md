---
id: memory-hierarchy
title: Memory Hierarchy
summary: A processor keeps data in a ladder of stores (bigger = slower), so a computation's speed is set by its operations-per-byte ratio versus the balance point of the (machine, number-format) pair it runs on.
type: concept
tags: [os/memory]
prereqs: [arithmetic, numeric-precision-formats]
sources:
  - "Harris & Patterson, Computer Organization and Design (memory hierarchy)"
  - "NVIDIA A100 / H100 architecture whitepapers (HBM, L2, SRAM bandwidths)"
  - "Williams, Waterman & Patterson, 'Roofline: An Insightful Visual Performance Model' (CACM 2009)"
status: explained
created: 2026-06-23
updated: 2026-07-03
---

# Memory Hierarchy

## Summary

A modern processor does not store its data in one place. It keeps a few numbers in
tiny, blazing-fast **registers** right next to the arithmetic units, a few megabytes
in fast on-chip **SRAM**, tens of megabytes in a shared **L2 cache**, tens of
gigabytes in roomy-but-slower **HBM** (the GPU's main memory), and even more in the
host's **DRAM** further away. Each step *down* the ladder holds far more data but
*moves* it far slower. The defining consequence: doing arithmetic on a number is much
cheaper than fetching that number from a distant level. So for many programs the limit
is not how many `+ − × ÷` operations you can do per second, but how many *bytes* you
can drag up the ladder per second. Whether a computation is **memory-bound** (waiting
on bytes) or **compute-bound** (waiting on arithmetic) is decided by a single ratio —
operations performed per byte moved — compared against the balance point of the
machine *and the number format it runs*, taken together as one pair.

## Grounded explanation

### What the concept *is*: a ladder of stores, each bigger but slower

A processor needs somewhere to keep the numbers it is working on. There is no single
ideal store: a memory that is both enormous and instantly readable does not exist
physically (large means far away on the chip, and far away means slow). The engineering
answer is a **hierarchy** — several stores stacked into levels, where every level *down*
is **larger in capacity** but **lower in bandwidth** (bandwidth = how many bytes per
second you can read or write from it).

Two numbers describe each level, and both are plain counts:

- **Capacity** — how many bytes it can hold.
- **Bandwidth** — how many bytes per second flow in or out.

Here is a representative ladder for a modern GPU (order-of-magnitude values; the exact
figures vary by chip, but the *gradient* is the point):

| Level | What it is | Capacity (bytes) | Bandwidth (bytes/sec) |
|---|---|---|---|
| Registers | scratch slots beside the math units | ~256 KB (per SM) | effectively instant |
| SRAM / shared memory | fast on-chip scratchpad | ~20 MB total on-chip | ~20 TB/s |
| L2 cache | shared on-chip cache | ~40 MB | ~7 TB/s |
| HBM | the GPU's main memory | ~80 GB | ~3 TB/s |
| Host DRAM | the CPU's memory, across a link | ~1 TB | ~0.03 TB/s (~30 GB/s) |

Read the table as ratios — which is all [[arithmetic]] (`÷`) needs. Going from HBM up to
SRAM, capacity *shrinks* by `80 GB ÷ 20 MB = 80{,}000 MB ÷ 20 MB = 4000×`, while
bandwidth *grows* by `20 TB/s ÷ 3 TB/s ≈ 6.7×`. Going from HBM *down* to host DRAM,
bandwidth collapses by `3 TB/s ÷ 0.03 TB/s = 100×`. Every rung is a trade: more room,
slower access. That opposed gradient — capacity up, speed down — *is* the memory
hierarchy.

### Why it matters: arithmetic is cheap, moving data is expensive

Now place the math units beside this ladder. A modern GPU can perform on the order of
`10^14` floating-point operations per second (100 TFLOP/s) — call this its **compute
rate**. One machine actually has *several* compute rates — one per number format it can
run (the caveat below unpacks this); throughout this node we fix a single illustrative
pair: **a 4-byte format at 100 TFLOP/s**. Its HBM delivers about `3 × 10^12` bytes per
second — its **memory bandwidth**. Divide one by the other (`÷`, from [[arithmetic]]):

```
compute rate ÷ memory bandwidth
  = 100 × 10^12 FLOP/s  ÷  3 × 10^12 bytes/s
  ≈ 33 FLOP per byte.
```

This single number is the pair's **balance point**: the machine can do about **33
arithmetic operations in the time its memory takes to deliver one byte from HBM**. Scale
that up to one whole number: a number stored as 4 bytes occupies the memory bus 4× as
long as one byte does (a statement about *sustained delivery rate*, not about the fixed
latency of a single load), and in that same stretch of time the math units could have
executed `33 × 4 ≈ 130` operations. So each
4-byte number costs about **130 operations' worth of time just to *arrive*** — an
opportunity cost measured in forgone arithmetic. The arithmetic is nearly free; the
*travel* is what you pay for.

### A caveat: a FLOP is dtype-blind, but a FLOP/s rating is not

A **FLOP** counts an *event* — one `+` or one `×` — regardless of how the numbers
involved are laid out in bits: their **dtype** (short for *data type*), i.e. which of
the [[numeric-precision-formats]] the machine is running. FP64 spends 8 bytes per
number, FP32 spends 4, FP16 spends 2 — yet multiplying two 8-byte doubles and
multiplying two 2-byte halves are each exactly **1 FLOP**.

What is *not* dtype-blind is the machine's **compute rate** — a chip's peak FLOP/s is
always quoted *per format*, so the balance point is a property of a **(machine,
format) pair**, never of the machine alone. Two separate mechanisms set those
per-format rates. First, on the *same* general-purpose math units, half-width numbers
finish about **2×** faster — that is the first two rows below doubling from FP64 to
FP32. Second, a chip may carry *extra, specialized* silicon that runs only one shape
of work at narrow formats: the A100's dedicated matrix-multiply hardware is why its
FP16 row jumps far beyond the factor-of-two pattern — and that row applies **only to
matrix-shaped work**; element-wise work (like the vector add below) cannot use it.
Real numbers for one machine (NVIDIA A100 **80 GB**, whose HBM ≈ `2 × 10^12` bytes/s):

| Format | Bytes per number | Peak rate | Balance point (rate ÷ bandwidth) |
|---|---|---|---|
| FP64, general-purpose units | 8 | ~9.7 TFLOP/s | ~5 FLOP/byte |
| FP32, general-purpose units | 4 | ~19.5 TFLOP/s | ~10 FLOP/byte |
| FP16, matrix work on the dedicated matrix hardware | 2 | ~312 TFLOP/s | ~156 FLOP/byte |

This is exactly why the section above pinned one pair before dividing — an illustrative
machine running a **4-byte format at 100 TFLOP/s**. The `≈ 33 FLOP/byte` balance point
belongs to *that pair*, and the whole node keeps using it so the numbers stay comparable.

Note which way the trade moves — and that the two mechanisms move it differently.
Switching to a narrower format also changes *your computation's* intensity: its FLOP
count stays put while its bytes moved halve, so its operations-per-byte **doubles**.
Against the same-silicon mechanism that is a wash: FP64 → FP32 doubles the bar
(~5 → ~10) *and* doubles the intensity — memory-boundedness is unchanged. The famous
shift comes from the *second* mechanism: for matrix work, FP32 → FP16 raises the bar
~16× (~10 → ~156) while the intensity only doubles — a net ~8× gap. Cheaper-to-move
numbers make that bar **higher**, not lower: at low precision, matrix work must supply
far *more* operations per byte to keep the math units fed, so it becomes **more
memory-bound, not less**.

So to predict whether a computation is limited by math or by movement, count two things
about it — both plain counts:

- **FLOPs** — how many `+ − × ÷` operations the computation performs.
- **Bytes moved** — how many bytes it must read from / write to the slow level (HBM).

Their ratio is the computation's **arithmetic intensity**:

```
arithmetic intensity = FLOPs ÷ bytes moved   (operations per byte).
```

Compare it to the balance point of our fixed (machine, format) pair (≈ 33 FLOP/byte):

- If intensity **< 33** → the math units finish early and sit idle waiting for bytes.
  The computation is **memory-bound**; its speed is set by bandwidth, not by the
  compute rate.
- If intensity **> 33** → bytes arrive faster than they can be chewed through; the math
  units are the bottleneck. The computation is **compute-bound**.

The key insight: a computation's fate is not its FLOP count alone, nor its byte count
alone, but **their ratio against the (machine, format) pair's ratio**.

### Worked instance: a vector add is hopelessly memory-bound

Take a concrete, non-degenerate operation: **element-wise vector addition**,
`c = a + b`, on three vectors of `n = 1,000,000` numbers each, stored as 4-byte floats
in HBM. (This is non-degenerate: it really touches every element, no factor collapses
to 1 or 0, and it genuinely streams from HBM — there is no reuse to hide.)

Count the FLOPs. One `+` per element (from [[arithmetic]]), across `n` elements:

```
FLOPs = 1 × 1,000,000 = 1,000,000 operations.
```

Count the bytes moved. We must **read** `a` and `b` and **write** `c` — three vectors,
each `n` numbers, each number 4 bytes:

```
bytes moved = 3 × 1,000,000 × 4 = 12,000,000 bytes.
```

Now the arithmetic intensity (`÷`):

```
intensity = 1,000,000 FLOPs ÷ 12,000,000 bytes = 0.0833 FLOP per byte.
```

Compare to the balance point: `0.0833` versus `33`. The operation does about **400×
fewer** operations per byte than our (machine, format) pair is built to sustain
(`33 ÷ 0.0833 ≈ 400`). It is deeply **memory-bound**.

We can even read off the runtime. The bytes dominate, so time ≈ bytes ÷ bandwidth:

```
time ≈ 12,000,000 bytes ÷ (3 × 10^12 bytes/s) = 4 × 10^-6 s = 4 microseconds.
```

In those 4 microseconds the math units *could have* done
`100 × 10^12 FLOP/s × 4 × 10^-6 s = 400,000,000` operations — yet our vector add asked
for only `1,000,000`. So **399 out of every 400** arithmetic slots go to waste; the
hardware spends 99.75% of the time simply waiting for HBM to hand over the next number.
Buying a chip with twice the compute rate would not speed this up at all; only faster
*memory* would.

### The lever this exposes

That gap is exactly what the hierarchy invites you to exploit. The slow level (HBM) set
the runtime; the fast level (SRAM, ~7× the bandwidth, and reusable once loaded) sat
nearly unused. If an algorithm can load a chunk of data into SRAM **once** and then do
*many* operations on it before evicting it, it drives the *bytes-moved-from-HBM* term
down while the FLOP term stays fixed — pushing arithmetic intensity up and over the
balance point, turning a memory-bound computation into a compute-bound one. That is why
the memory hierarchy is the substrate beneath every "IO-aware" technique: the ladder of
bandwidths is the scoreboard those techniques are playing against.

## Prerequisites

- [[arithmetic]]
- [[numeric-precision-formats]]

## Sources

- Harris & Patterson, *Computer Organization and Design* — the classic treatment of the memory hierarchy (registers → cache → main memory) and the capacity/bandwidth trade-off.
- NVIDIA A100 / H100 architecture whitepapers — concrete register, SRAM/shared-memory, L2, and HBM capacities and bandwidths.
- Williams, Waterman & Patterson, "Roofline: An Insightful Visual Performance Model," *CACM* 2009 — arithmetic intensity and the memory-bound vs. compute-bound balance point.
