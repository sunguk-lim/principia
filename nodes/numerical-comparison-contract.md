---
id: numerical-comparison-contract
title: Numerical Comparison Contract
summary: A numerical comparison contract defines reference semantics, scale-aware error limits and downstream acceptance separately from bitwise reproducibility.
type: concept
tags: [software/testing]
prereqs: [floating-point-reduction-order, measurement]
sources: [https://docs.pytorch.org/docs/2.15/testing.html, https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html]
status: explained
created: 2026-11-18
updated: 2026-11-18
---

# Numerical Comparison Contract

## Meaning

A numerical comparison contract says what a computation must approximate, under which inputs and arithmetic settings, and how much deviation is acceptable. It does not infer correctness from a small-looking number. [[floating-point-reduction-order]] explains why equal real-arithmetic formulas may yield different machine values; [[measurement]] turns the intended accuracy into observable checks.

## Mechanism

First fix the mathematical operation, input representation, mask semantics, randomness, storage and accumulation formats, and software/backend version. Then choose an independently implemented reference on tractable cases. A wider-precision reference often reduces rounding but is not exact real arithmetic and cannot repair a shared wrong mask or formula. Compare each implementation with the reference, not merely with its peer: two wrong implementations may agree.

For finite scalar components, one common rule is `abs(actual-reference) <= atol + rtol*abs(reference)`. Here `atol` bounds tolerated error near zero and `rtol` permits error that scales with the reference magnitude. The formula is reference-oriented, so swapping the arguments can change the decision. Select both limits before examining a failing case, using the application's error budget and observed arithmetic; framework dtype defaults are a starting policy, not a proof.

Machine epsilon conventionally describes the gap from one to the next larger representable number. It is not a universal absolute output-error bound. Input scale, cancellation, reduction length and intermediate precision matter. Nor does a half-precision input prove that every accumulation used that format. Finite checks and explicit NaN/Inf policy are separate from the finite closeness formula.

## Worked example

With `atol=1e-6` and `rtol=1e-4`, reference value 100 permits deviation up to 0.010001. Actual 100.005 passes. Reference zero permits only 0.000001, so actual 0.000002 fails despite its much smaller absolute difference. These are invented limits illustrating the contract, not recommended defaults for every kernel.

## Diagnostic and application boundaries

Report maximum and quantile absolute errors, relative errors with an explicit near-zero convention, and locations of failures. Sweep shape, scale, masks, partial tiles and forward/gradient paths. Boundary patterns are useful diagnostic clues, but rounding can be structured and a bug can be small; neither pattern nor magnitude alone proves the cause. Isolate one variable and use analytically checkable cases.

Finally test the downstream task under its own acceptance budget. A tiny score perturbation can change a near-tied discrete choice, yet a changed choice alone does not establish worse task quality. Conversely, acceptable average task quality can hide a rare invalid output. Bitwise repeatability at fixed configuration, numerical accuracy relative to a reference, and application quality are three independent requirements. Tightening a tolerance may expose issues but can also reject an acceptable faster algorithm; loosening it after every failure destroys the test's meaning.

## Sources

- <https://docs.pytorch.org/docs/2.15/testing.html>
- <https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html>
