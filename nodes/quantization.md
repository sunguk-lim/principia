---
id: quantization
title: Quantization
summary: Quantization stores a number with fewer bits by rounding it to one of a small, evenly spaced set of integer levels and remembering a single scaling number.
type: concept
tags: [ml/llm/inference]
prereqs: [arithmetic]
sources:
  - "Jacob et al., 'Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference' (2018), arXiv:1712.05877"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Quantization

## Summary

Quantization stores a number with **fewer bits** by rounding it to one of a small,
evenly spaced set of integer levels and remembering a single scaling number. A
weight like `3.1`, normally kept as a wide floating-point value, becomes a small
integer code (say `7`) plus a shared **scale** `s ≈ 0.443`; to read it back you
multiply: `7 × 0.443 ≈ 3.1`. Because there are only a handful of levels, most
values land *between* two of them and must be rounded — so quantization trades a
small, bounded **rounding error** for a large saving in memory and in the time
spent moving numbers around. The whole scheme is just division, rounding, and
multiplication — [[arithmetic]].

## Grounded explanation

**The problem.** A neural network is a long list of numbers (weights, and the
activations they produce). Each is normally stored in many bits — 16 for the
common half-precision float, "FP16" — so a model with billions of numbers needs
billions of 16-bit slots. Memory is finite and, more often, the bottleneck is
*moving* those numbers from memory into the arithmetic unit. Halving the bits
roughly halves both costs. So we ask: can we represent each number in, say, 8
bits ("INT8") or even 4 bits ("INT4") — a plain signed integer — and still
recover a good approximation of the original?

**The central object: a scale.** A `b`-bit signed integer can hold only a fixed
set of whole-number *codes*. With `b` bits the largest magnitude code is
`q_max = 2^(b−1) − 1` (the `−1` because one bit picks the sign, and another code
is spent on zero / the negative side). For `b = 4`: `q_max = 2^3 − 1 = 7`, so the
codes run `−7 … +7`. These codes are evenly spaced integers; real weights are not
integers and span a different range. Quantization bridges the two with **one
shared real number, the scale `s`**: a code `q` *stands for* the real value
`q × s`. Picking `s` is the entire game — it sets how much real-world value one
integer step is worth.

**Why the scale is `max(|x|) / q_max`.** We want the *largest-magnitude* value in
the group to be representable without overflowing the code range. If the biggest
magnitude is `M = max(|x|)` and the biggest code is `q_max`, then setting
`s = M / q_max` makes that extreme value map exactly to the extreme code
(`M / s = q_max`), and everything smaller falls *inside* the `[−q_max, q_max]`
range. Choose `s` any smaller and the largest values overflow (clip); any larger
and you waste codes you never use, coarsening every value needlessly. So
`s = max(|x|) / q_max` is the tightest scale that loses nothing to clipping. This
is the **symmetric** scheme: the real range `[−M, +M]` is centered on zero, and
code `0` always means real `0`.

**Quantize and dequantize.** With `s` fixed, two operations move between worlds.
To **quantize** a real value `x` to a code: divide by the scale and round to the
nearest integer,

  `q = round(x / s)`.

To **dequantize** (read it back as a real value):

  `x̂ = q × s`.

The rounding is the only lossy step — and it is exactly where quantization *is*
quantization, so we look at it closely. Since `q` is the nearest integer to
`x / s`, the leftover `x/s − q` is at most `½` in magnitude; multiplying back by
`s`, the recovered value `x̂` differs from `x` by at most `s/2`. That is the
**quantization error**, and it is *bounded*: `|x̂ − x| ≤ s/2`. This bound is the
justification for the whole trade-off — error cannot exceed half of one integer
step, and the step `s` shrinks as you add bits (bigger `q_max` ⇒ smaller `s`).
Going FP16 → INT8 → INT4 makes `q_max` smaller, so `s` larger, so the error bound
grows — fewer bits, coarser grid, more rounding. That is the cost you pay for the
memory you save.

**Worked instance (INT4, `b = 4`).** Take the four-number group
`x = [0.2, −1.3, 3.1, 0.05]` and quantize to 4-bit codes (`q_max = 7`).

1. **Scale.** The largest magnitude is `M = max(|0.2|, |−1.3|, |3.1|, |0.05|) =
   3.1`. So `s = M / q_max = 3.1 / 7 ≈ 0.4429`. One integer step is now worth
   about `0.4429` — note it is *not* `1`, so codes and real values genuinely
   differ.

2. **Codes** (`q = round(x / s)`):
   - `0.2 / 0.4429 = 0.452 → round → 0`
   - `−1.3 / 0.4429 = −2.936 → round → −3`
   - `3.1 / 0.4429 = 7.000 → round → 7`  *(the max lands exactly on `q_max`, as designed)*
   - `0.05 / 0.4429 = 0.113 → round → 0`

   So the group is stored as the integer codes `[0, −3, 7, 0]` plus the single
   shared scale `0.4429`.

3. **Dequantize** (`x̂ = q × s`):
   - `0 × 0.4429 = 0.000`
   - `−3 × 0.4429 = −1.329`
   - `7 × 0.4429 = 3.100`
   - `0 × 0.4429 = 0.000`

   Recovered group: `[0.000, −1.329, 3.100, 0.000]`.

4. **Error** (`x̂ − x`):
   - `0.000 − 0.2  = −0.200`
   - `−1.329 − (−1.3) = −0.029`
   - `3.100 − 3.1  =  0.000`
   - `0.000 − 0.05 = −0.050`

   Every error obeys the bound `|x̂ − x| ≤ s/2 = 0.4429 / 2 ≈ 0.221`. The largest
   error here, `0.200` on the value `0.2`, sits just under it. Notice the failure
   mode: small values (`0.2`, `0.05`) both collapse to code `0` and lose their
   identity, while the large value `3.1` is captured exactly. INT4 is a coarse
   grid; quantizing the same group to INT8 (`q_max = 127`, `s ≈ 0.0244`) would
   give these small values their own distinct codes and shrink every error by
   roughly 18×. This is the visible meaning of "more bits, less error."

**Asymmetric quantization (the zero-point).** The symmetric scheme above wastes
half its codes when the real values are lopsided — e.g. all positive (like the
outputs of a function that clamps negatives to `0`), where the whole `−7 … −1`
half goes unused. The fix adds a second stored number, the **zero-point** `z`, an
integer code that represents real `0`. Then `q = round(x / s) + z` and
`x̂ = (q − z) × s`. The scale is now built from the full range
`s = (max(x) − min(x)) / (2^b − 1)`, and `z` shifts the grid so it straddles the
actual data instead of being forced to center on zero. Symmetric quantization is
just the special case `z = 0`. The cost is one extra subtraction per value (still
[[arithmetic]]) and storing `z`.

**Granularity (briefly).** The scale `s` is shared across a *group* of values; how
big that group is, is a choice. **Per-tensor** quantization uses one `s` for an
entire weight matrix — cheapest to store, but one large outlier inflates `M` and
coarsens every other value (had our example contained a stray `30.0`, the scale
would jump to `≈ 4.3` and `0.2`, `−1.3` would *all* round to `0`). **Per-channel**
or **per-group** quantization gives each row, column, or small block of the
tensor its own `s`, so a local outlier only coarsens its own neighborhood. Finer
granularity means more scales to store but smaller errors — the same bits-vs-error
trade-off, applied to the scales themselves.

## Prerequisites

- [[arithmetic]]

## Sources

- Jacob et al., "Quantization and Training of Neural Networks for Efficient
  Integer-Arithmetic-Only Inference" (2018), arXiv:1712.05877 — establishes the
  scale-and-zero-point integer mapping used here.
