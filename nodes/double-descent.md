---
id: double-descent
title: Double descent
summary: Double descent is a test-error curve that can fall, rise near interpolation, and fall again as model capacity or training time increases.
type: concept
tags: [ml/deep-learning]
prereqs: [regularization, loss-function]
sources: [https://arxiv.org/abs/1812.11118]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Double descent

## Summary

**Double descent** describes settings in which held-out error does not follow one U-shaped curve as capacity grows: it can decrease, peak near the point at which training data are exactly interpolated, then decrease again in a more overparameterized regime.

## Grounded explanation

Classical bias--variance intuition often expects increasing capacity to lower approximation bias while eventually increasing sensitivity to the finite training sample. Modern interpolating models can instead show a second descent. Let a capacity control be $c$ (for example, number of features or parameters). At small $c$, a model may underfit. Near an interpolation threshold it can fit training labels while making unstable choices among many nearly fitting solutions, producing a test-error peak. At larger $c$, the training algorithm and parameterization can select a different interpolating solution whose held-out error is lower.

This is an observed regime, not a promise that extra parameters improve generalization. The curve depends on data distribution, label noise, architecture, optimizer, training duration, and the metric. The training [[loss-function]] can remain near zero on both sides of the peak, so it cannot by itself diagnose generalization.

To evaluate a suspected double-descent effect, vary only the capacity control while keeping the split, optimizer schedule, and preprocessing fixed; repeat seeds; report training and test error, uncertainty, and the interpolation threshold. Compare against explicit [[regularization]] and against changes in data size or label noise. Do not infer the phenomenon from one noisy sweep or use it to justify unchecked model scaling.

## Prerequisites

- [[regularization]]
- [[loss-function]]

## Sources

- [Belkin et al., “Reconciling modern machine-learning practice and the classical bias--variance trade-off”](https://arxiv.org/abs/1812.11118): documents double-descent risk curves across model classes and the interpolation threshold.
