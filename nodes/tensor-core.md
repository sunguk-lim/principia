---
id: tensor-core
title: Tensor Core
summary: A Tensor Core is a specialized piece of hardware sitting inside each streaming-multiprocessor whose one job is to compute a small fixed-size matrix-multiplication — and to do it…
type: concept
tags: [gpu]
prereqs: [streaming-multiprocessor, matrix-multiplication, fma]
sources:
  - "linux-internals-complete.html — FMA — the basic GPU operation (FMA = a×b+c in one instruction; a Tensor Core is a pile of FMA units doing a small matrix multiply in one shot); What hardware supports — Tensor Core dtype menu by generation (FP16/BF16/TF32/FP8/FP4/INT8 inputs by GPU generation); Pattern C — low-precision Tensor Cores (low-precision inputs, wider accumulation: FP8×FP8→FP32, INT8×INT8→INT32); HMMA.16816 SASS instruction (16×8×16 tile, FP16→FP32)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Tensor Core

## Summary

A **Tensor Core** is a specialized piece of hardware sitting inside each
[[streaming-multiprocessor]] whose one job is to compute a small fixed-size
[[matrix-multiplication]] — and to do it as a *single* hardware operation. Where the SM's
ordinary arithmetic lanes (the "CUDA cores" from [[streaming-multiprocessor]]) each do one
scalar multiply-add per cycle, a Tensor Core swallows two whole small matrices at once,
multiplies them, and adds the result onto a running accumulator — a *matrix*
multiply-accumulate, `D = A·B + C` on small tiles such as 16×16 — finishing in a handful of
cycles what the lanes would need thousands of individual multiply-adds to do. The reason this
unit exists is blunt economics: modern deep learning is overwhelmingly
[[matrix-multiplication]] (the linear layers and attention scores that dominate every
network), so dedicating silicon to a fast tiled-matmul engine buys an order-of-magnitude
throughput jump on exactly the operation that matters most. A Tensor Core also accepts
**low-precision** inputs (formats with fewer bits, like FP16, BF16, FP8, or INT8) while
*accumulating* the running sum in a wider, higher-precision format — trading a little
numerical range for a lot more throughput. An H100 carries four Tensor Cores per SM, and
they are the reason a GPU's advertised matrix-math FLOPS dwarf its plain arithmetic rate.

## Grounded explanation

### Starting point: one lane does one fused multiply-add per cycle

The prerequisite [[streaming-multiprocessor]] established what an SM's ordinary **lanes**
are: simple arithmetic positions (NVIDIA's "CUDA cores"), each able to do one multiply or one
add per cycle. The single most common thing those lanes do is a **fused multiply-add** ([[fma]]):
one hardware step that computes `a × b + c` — a
multiply and an add rolled into one instruction, with a single rounding at the end. The FMA
is the atom of numerical computing; dot products, convolutions, and matrix multiplies are all
just enormous piles of FMAs.

Now connect this to the prerequisite [[matrix-multiplication]]. That node defined the product
`C = A·B` of an `m×k` matrix `A` and a `k×n` matrix `B`: each output entry is
`C[i][j] = A[i][1]·B[1][j] + … + A[i][k]·B[k][j]` — a row of `A` marched against a column of
`B`, multiplying paired entries and summing them. Read that sum as a chain of FMAs: start an
accumulator at `0`, then for each of the `k` index positions do one FMA that multiplies a pair
and adds it onto the accumulator. So **one output entry of a matrix product is `k` FMAs**, and
an `m×n` output has `m·n` such entries — `m·n·k` FMAs in total to multiply the two matrices.
For the square case `N×N` times `N×N`, that is `N³` FMAs. On the SM's ordinary lanes those
`N³` scalar FMAs must be issued one batch at a time, cycle after cycle. *That* is the cost a
Tensor Core is built to crush.

### What a Tensor Core is: a whole tile-matmul in one operation

A **Tensor Core** is a block of fixed hardware, placed inside the SM right alongside the
ordinary lanes, that performs a small [[matrix-multiplication]]-and-accumulate as **one
hardware operation**. Concretely it computes

`D = A·B + C`

where `A`, `B`, `C`, and `D` are small fixed-size **tiles** — small rectangular blocks of a
matrix, e.g. 16×16 — rather than single scalars. The `+ C` term is the *accumulate* part: a
matrix product is rarely wanted alone; you usually want to add this tile's product onto a
partial sum already built up from earlier tiles. So the Tensor Core's native verb is
"multiply these two tiles and add the result onto the running tile," a *matrix*
multiply-accumulate — the tile-sized generalization of the scalar FMA above.

The defining contrast is *granularity*. An ordinary lane consumes one scalar `a`, one scalar
`b`, one scalar `c` and emits one scalar per FMA. A Tensor Core consumes whole sub-tiles of
`A` and `B` per operation and emits a whole sub-tile of partial products, internally firing
hundreds of multiply-adds in parallel and summing them — all wired in silicon, all in a few
cycles. It is, in effect, a giant pile of FMA units permanently arranged in the exact
cross-product pattern that [[matrix-multiplication]] needs, instead of a single
general-purpose lane that has to be *told*, scalar by scalar, to trace that pattern out.

This is why a Tensor Core is genuinely the *concept* and not just "a fast lane": its central
object is a **tile**, and its contribution is collapsing the `row × column, summed` structure
of a matrix product into one issued instruction. The ordinary lane is general (it will do any
FMA you point it at); the Tensor Core is specialized (it only knows how to multiply-accumulate
tiles), and that specialization is exactly what buys the speed.

### The why: matmul dominates, so dedicate silicon to matmul

Two questions need answering: *why is this worth a chunk of the chip*, and *why does it go
faster* rather than just looking different.

**Why worth the silicon.** A modern neural network spends the overwhelming majority of its
arithmetic inside [[matrix-multiplication]] — every linear layer multiplies an input matrix by
a weight matrix, and an attention block multiplies query and key matrices to score every token
against every other. If one operation eats most of your cycles, the highest-leverage thing
hardware can do is make *that* operation fast. The ordinary lanes are general-purpose and must
stay so (kernels do all kinds of work); but you can also bolt on a unit that does *nothing but*
the dominant operation, extremely fast. That is the bet the Tensor Core makes, and it pays
because the workload is so lopsided toward matmul.

**Why it goes faster — the non-obvious step.** It is not magic; it is amortization. The `N³`
scalar FMAs of an `N×N` matmul are not independent busywork — they share enormous structure:
the same row of `A` is reused across a whole row of outputs, the same column of `B` across a
whole column. An ordinary lane re-fetches and re-issues against that shared structure one
scalar at a time, paying instruction-issue and data-movement overhead on every single FMA. A
Tensor Core instead loads a tile of `A` and a tile of `B` *once* and lets dedicated wiring
reuse those loaded values across the hundreds of multiply-adds the tile product requires,
performed together in a few cycles. The throughput win comes from doing many multiply-adds per
issued instruction and reusing each loaded operand many times inside the hardware — turning a
long stream of overhead-laden scalar steps into a few dense, fully-utilized matrix steps. The
arithmetic answer is identical to what the lanes would compute; only the *rate* changes.

**Why low precision helps, and the invariant that keeps it safe.** Tensor Cores accept inputs
in low-precision number formats — formats that use fewer bits per value, such as FP16, BF16,
FP8, or the integer format INT8 (this is the "quantization" idea in plain prose: storing and
multiplying numbers in a coarser format to move and crunch more of them per cycle). Narrower
inputs mean more values fit through the same wires and more multiply-adds fit in the same
silicon, so peak throughput climbs as precision drops. The danger is that a matrix product
sums many terms, and summing many small low-precision numbers loses accuracy fast. The Tensor
Core's safeguard — the invariant that makes the trade survive — is to **accumulate in a wider
format than it multiplies in**: it may multiply two FP8 tiles, but it keeps the running sum
`C`/`D` in FP32 (a 32-bit format); it may multiply two INT8 tiles but accumulate in INT32.
The lossy step is confined to the *inputs*; the long chain of additions stays in high
precision, so the accumulated error does not blow up. That is the deal in one line: coarse,
fast operands; precise, safe running total.

### Worked instance: a 16×16×16 tile multiply-accumulate

Take a concrete, non-degenerate tile: multiply a 16×16 tile `A` by a 16×16 tile `B` and add
the product onto a 16×16 accumulator `C`, giving `D = A·B + C`. It is non-degenerate on
purpose — every dimension is 16 (no dimension is 1, which would collapse the matmul into a
vector or scalar case and hide the cross-product structure), and the `+ C` term is present and
nonzero (so the *accumulate* half of the unit is actually exercised, not just the multiply).

**Count the work the old way.** By the rule derived above, an `m×n` output with inner
dimension `k` costs `m·n·k` FMAs. Here `m = n = k = 16`, so the product is
`16 × 16 × 16 = 4096` scalar FMAs — and the `+ C` adds another `16 × 16 = 256` scalar adds to
fold in the accumulator, for ~`4096` multiply-adds dominating the bill. On the SM's ordinary
lanes, those 4096 FMAs are issued in batches across many cycles: even with, say, 32 lanes
firing one FMA each per cycle, `4096 ÷ 32 = 128` cycles of pure issue, before counting the
overhead of marching through the rows and columns.

**Now the Tensor Core.** The very same `16×16×16` multiply-accumulate is what one Tensor Core
operation is *built* to do: it ingests the two tiles, fires those ~4096 multiply-adds in
parallel across its dedicated wiring, folds in `C`, and produces the full 16×16 result tile
`D` — in a *handful* of cycles rather than ~128. The output numbers are bit-for-bit what the
lanes would have produced (given the same accumulation precision); only the time changed. That
ratio — roughly two orders of magnitude fewer cycles for this one tile — is, summed over the
millions of such tiles in a real layer, the order-of-magnitude jump in matmul throughput.

**Scale it back up to the whole machine.** A real layer's matmul is far larger than 16×16, so
the software chops it into a grid of 16×16(×16) tiles and streams them through the Tensor
Cores, accumulating partial products tile by tile into each output block — exactly the
`D = A·B + C` accumulate step, reused. Each of the GPU's many [[streaming-multiprocessor]]s
runs four Tensor Cores, and the SM's scheduler keeps them fed using the same latency-hiding
trick from [[streaming-multiprocessor]] (while one tile waits on memory, another tile's
multiply-accumulate issues). So the chip-level throughput is, to first order, *(tile matmuls
per cycle per Tensor Core) × (Tensor Cores per SM) × (SMs kept busy)* — and because each tile
matmul is hundreds of FMAs, that product towers over what the plain lanes alone could reach.
That gap is precisely why training and inference speed lean so heavily on Tensor Cores: they
make the operation that dominates deep learning the operation the hardware is fastest at.

## Prerequisites

- [[streaming-multiprocessor]]
- [[matrix-multiplication]]
- [[fma]]

## Sources

- linux-internals-complete.html — *FMA — the basic GPU operation* (a fused multiply-add is
  `a × b + c` in one instruction; "a Tensor Core is a giant pile of FMA units arranged to do
  small matrix multiplies in one shot — hundreds of FMAs per Tensor Core instruction"); the
  `HMMA.16816.F32` SASS instruction (one Tensor Core op = a 16×8×16 tile matmul, FP16 inputs
  accumulating to FP32); *What hardware supports — Tensor Core dtype menu by generation* (the
  low-precision input formats FP16 / BF16 / TF32 / FP8 / FP4 / INT8 by GPU generation); and
  *Pattern C — low-precision Tensor Cores* (low-precision inputs with wider accumulation:
  `INT8×INT8→INT32`, `FP8×FP8→FP32`, `FP4×FP4→FP32`). Per-SM count (four Tensor Cores per SM,
  one per sub-core) from the chip/SM organization tables.
