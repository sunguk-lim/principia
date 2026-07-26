---
id: numeric-precision-formats
title: Numeric Precision Formats
summary: A numeric precision format is the fixed recipe for laying out one number inside a small, fixed number of bits.
type: concept
tags: [ml/llm/inference]
prereqs: [quantization]
sources:
  - "llm_parallelism_strategies.jsx — KV-Quantization panel (precision menu: FP16/FP8 E4M3·E5M2/INT8/INT4/FP4·NVFP4, bit widths, memory savings, hardware support)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Numeric Precision Formats

## Summary

A numeric precision format is the fixed recipe for laying out one number inside a
small, fixed number of bits. It is the *target* a number is mapped into: where
[[quantization]] is the procedure for rounding values onto a coarse grid and
remembering a scale, a precision format is the concrete container that holds the
result. The formats split into two families. **Floating-point** formats spend
their bits on three fields — one **sign** bit, some **exponent** bits that set how
large or small a number can get (its *range*), and some **mantissa** bits that set
how finely values are resolved (its *precision*) — so a value is `±mantissa ×
2^exponent`. **Integer** formats (INT8, INT4) spend every bit on a plain whole
number and carry no exponent at all; they get their range from an external scale,
exactly the [[quantization]] scheme. The single trade running through every choice
is: **fewer bits → less memory and more numbers moved or multiplied per unit of
hardware work, but a coarser, narrower representation** — more rounding error, or
a smaller span of representable magnitudes, or both. The famous lesson is BF16 vs
FP16: same 16 bits, but BF16 reallocates bits from mantissa to exponent to keep a
huge range, avoiding the overflow that plagues FP16 in training.

## Grounded explanation

**The two families, and why a format exists.** Every weight or activation in a
network is ultimately a pattern of bits. A *precision format* is the agreed
interpretation of that pattern — how many bits there are and what each one means.
Two families dominate. A **floating-point** format reads its bits as three fields
and reconstructs the number as `sign × mantissa × 2^exponent`. An **integer**
format reads all its bits as one signed whole number and has no built-in notion of
magnitude beyond the integers themselves; to mean anything in the real-valued
world of a network it must be paired with a separate **scale** — which is precisely
the device [[quantization]] introduces (a code `q` stands for the real value
`q × s`). So the integer formats below are just the *storage end* of
[[quantization]]; the floating-point formats are a different mechanism that builds
range into the number itself.

**Floating-point anatomy: sign, exponent, mantissa.** Spend the bits of a
floating-point number in three groups:

- The **sign** is 1 bit: `0` for positive, `1` for negative.
- The **exponent** is a block of bits holding an integer power of two. It is the
  *coarse dial* for magnitude — each step doubles or halves the value's scale. The
  more exponent bits, the wider the span of magnitudes the format can reach,
  because the exponent can run from a large negative number (tiny values) to a
  large positive one (huge values). This span is the format's **dynamic range**.
- The **mantissa** (also called the significand or fraction) is the remaining
  bits, holding the leading digits of the number *within* the scale chosen by the
  exponent. It is the *fine dial*: more mantissa bits subdivide the gap between two
  consecutive powers of two more finely, so values are resolved more precisely.
  This is the format's **precision**.

The reconstruction is `value = (−1)^sign × (1.mantissa) × 2^exponent`. The split is
the whole story: **exponent bits buy range, mantissa bits buy precision, and a
fixed bit budget forces a trade between the two.** A format with a small exponent
field cannot represent very large or very tiny numbers — they *overflow* (exceed
the largest representable value, becoming infinity) or *underflow* (fall below the
smallest, becoming zero). A format with a small mantissa rounds aggressively even
for numbers comfortably in range.

**The floating-point menu.**

- **FP32** — 1 sign + 8 exponent + 23 mantissa = 32 bits. The classic
  "full-precision" float. Eight exponent bits give an enormous range (magnitudes
  from roughly `10^−38` to `10^38`), and 23 mantissa bits give about seven decimal
  digits of precision. This is the reference everything else is compared against.

- **FP16** ("half precision") — 1 + **5** exponent + **10** mantissa = 16 bits.
  Half the bits of FP32. With only 5 exponent bits its range is small: the largest
  representable value is about **65504**. Ten mantissa bits give decent local
  precision, but the narrow range makes it **prone to overflow** — a value that
  drifts past 65504 (easy during training, where sums of gradients or activations
  can spike) becomes infinity and poisons the computation.

- **BF16** ("brain float") — 1 + **8** exponent + **7** mantissa = 16 bits. Also 16
  bits, *but the split is different*: it keeps FP32's full 8 exponent bits and pays
  for them out of the mantissa, leaving only 7. The consequence is the key lesson
  of this node — BF16 has the **same dynamic range as FP32** (the same ~`10^38`
  ceiling, so it does not overflow where FP16 would) at the cost of *coarser
  precision* (7 mantissa bits ≈ two to three decimal digits). Networks tolerate
  imprecise individual numbers far better than they tolerate a single overflowed
  one, which is why **BF16 is the training favorite**: same memory as FP16, but
  trades the precision it doesn't need for the range it does.

- **FP8** — 8 bits, and it comes in **two flavors** that make the range-vs-precision
  trade explicit by reallocating the same 8 bits:
  - **E4M3** — 4 exponent + 3 mantissa (plus the sign). More mantissa, so **more
    precision** but less range. The "compute" flavor, used where values are kept in
    a controlled range and fidelity matters.
  - **E5M2** — 5 exponent + 2 mantissa (plus the sign). More exponent, so **more
    range** but less precision. The "wide-range" flavor, used where occasional large
    magnitudes (like gradients) must not overflow.

  Their very names announce the split: `E4M3` is *4 exponent, 3 mantissa*; `E5M2`
  is *5 exponent, 2 mantissa*. Same 8 bits, opposite ends of the same trade.

- **FP4 / NVFP4** — 4-bit floating-point. With so few bits there is almost no room
  for both fields, so these formats lean on a shared scale per small block of
  values (borrowing the [[quantization]] idea even inside a "float" format).
  NVFP4 is a specific 4-bit float native to recent hardware that reports under 1%
  quality loss on real models.

**The integer menu (this is [[quantization]]'s storage end).** An integer format
holds a plain signed whole number and *no exponent*. On its own it cannot express
`3.1`; it expresses the integer code `7` and relies on the [[quantization]] scale
`s` to mean `7 × s ≈ 3.1`. The grid is **uniform** — every code is one fixed step
`s` apart — which is the defining contrast with floating-point, whose
exponent makes the grid *non*-uniform (fine near zero, coarse out at large
magnitudes).

- **INT8** — 8-bit signed integer, codes roughly `−127 … +127`. Paired with a scale,
  it is the standard 8-bit [[quantization]] target.
- **INT4** — 4-bit signed integer, codes `−7 … +7` (the worked case in
  [[quantization]]). Four-bit memory at the price of a very coarse grid.

**The single trade, made precise.** Read off the cost and benefit of dropping
bits. *Memory and movement:* a 16-bit value occupies 2 bytes, an 8-bit value 1
byte, a 4-bit value half a byte — so going FP16 → FP8 packs **2× more numbers per
byte moved**, and FP16 → INT4 packs **4×**. Because moving numbers from memory into
the arithmetic unit is usually the bottleneck (the same point [[quantization]]
makes), fewer bits means proportionally higher throughput, and the same tensor-core
operation chews through more values at once. *Fidelity:* fewer bits means fewer
exponent bits (narrower range, more overflow/underflow risk) and/or fewer mantissa
bits (coarser steps, more rounding error). The whole menu is one knob — bits — read
two ways.

**Worked instance 1 — FP16 vs BF16 on a large value.** Take the value **70000**
and feed it to each 16-bit format.

- *FP16* has 5 exponent bits. The largest magnitude its exponent can reach
  corresponds to a maximum representable value of **65504**. Since `70000 > 65504`,
  there is no FP16 bit pattern for it: it **overflows to infinity**. The 10 mantissa
  bits are irrelevant — the number is simply out of range. This is the failure mode
  that breaks FP16 training: one large intermediate value turns into `inf` and
  corrupts everything downstream.
- *BF16* has 8 exponent bits — the same as FP32 — so its ceiling is about `10^38`,
  vastly above 70000. The value **fits with room to spare**. The price is paid in
  the mantissa: with only 7 mantissa bits, the representable values near 70000 are
  spaced about `2^16 / 2^7 = 512` apart, so 70000 is stored as the nearest such
  grid point (e.g. `≈ 69632` or `70144`, a rounding error of a few hundred). BF16
  keeps the number *finite and roughly right* where FP16 loses it *entirely* — the
  exact reason training prefers range over precision.

So with identical 16-bit budgets, the bit *allocation* alone decides whether 70000
is representable: FP16 says infinity, BF16 says "about 70000." That is the lesson in
one number.

**Worked instance 2 — INT8 holding `[−1.3, 3.1]` (reusing [[quantization]]'s
scale).** Suppose a group's largest magnitude is `M = 3.1`. INT8's biggest code is
`q_max = 127`, so by the [[quantization]] rule the scale is `s = M / q_max =
3.1 / 127 ≈ 0.0244`. Now store the two values as integer codes:

- `−1.3 / 0.0244 = −53.3 → round → −53`, which reads back as `−53 × 0.0244 ≈
  −1.293` (error ≈ 0.007).
- `3.1 / 0.0244 = 127.0 → round → 127`, which reads back as `127 × 0.0244 = 3.100`
  (the maximum lands exactly on `q_max`, as the scale is designed to make it).

There is no exponent anywhere — both numbers live on the *same* uniform grid of
step `0.0244`, and their magnitudes are carried entirely by the shared scale `s`,
not by the bit pattern. That is the structural difference from a float: a float
would give 3.1 and 1.3 *different* local step sizes via their exponents, while INT8
gives every value in the group one step. The 8-bit grid here is fine (step
`0.0244`); the 4-bit grid from [[quantization]]'s example (step `0.4429`, codes
`−7…+7`) is 18× coarser — the same value, far more rounding — which is exactly the
bits-vs-fidelity trade this node is about, now seen from the integer side.

**On KV-cache quantization and methods (in passing).** A common place these formats
are chosen is the key/value cache an attention model keeps as it generates: storing
it in FP8 instead of FP16 halves that memory and roughly doubles the context that
fits, and INT4 quarters it, at a small reported quality cost. The *methods* for
choosing scales well — per-channel and per-group scaling, keeping outlier channels
in higher precision, activation-aware schemes — are all techniques on top of
[[quantization]]; they decide *how* to map values into these formats, while this
node is about the formats themselves: the fixed bit layouts the values land in.

## Prerequisites

- [[quantization]]

## Sources

- `llm_parallelism_strategies.jsx`, KV-Quantization panel — supplies the precision
  menu used here (FP16 baseline; FP8 in E4M3/E5M2 flavors; INT8 per-channel; INT4;
  FP4 / NVFP4 "Blackwell native, <1% loss"), their bit widths, relative memory
  savings (FP16 1×, FP8/INT8 2×, INT4/FP4 4×), and hardware support notes. The
  floating-point field splits (FP32 1+8+23, FP16 1+5+10, BF16 1+8+7, FP8 E4M3 /
  E5M2) and the FP16 maximum of 65504 are standard IEEE-754 / bfloat16 / OCP-FP8
  format facts used to ground the anatomy.
