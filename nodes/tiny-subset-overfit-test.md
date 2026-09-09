---
id: tiny-subset-overfit-test
title: Tiny-Subset Overfit Test
summary: A tiny-subset overfit test checks whether a training pipeline can memorize a deliberately small sample before expensive full-data training obscures basic optimization or data-path defects.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, gradient-descent, regularization]
sources: [https://cs231n.github.io/neural-networks-3/#sanitycheck]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Tiny-Subset Overfit Test

## Summary

A **tiny-subset overfit test** trains a model repeatedly on a handful of examples and checks whether it can drive their data [[loss-function]] very low. It is a plumbing and optimization diagnostic, not evidence that the model will generalize.

## Grounded explanation

Full training entangles data loading, augmentation, distributed communication, numerical precision, [[gradient-descent]], and evaluation. Restricting the run to perhaps one batch makes failures cheaper and easier to localize. Use deterministic inputs, turn off stochastic augmentation and dropout, and set [[regularization]] to zero when it would prevent memorization.

Suppose a classifier repeatedly sees 20 correctly labeled images. Training loss remains near its chance value and predictions never change. Before adding hardware, inspect whether labels align with examples, parameters receive nonzero gradients, the optimizer updates those parameters, masks preserve the target signal, and the decoded predictions match the intended classes. If the loss falls near zero, these basic paths are plausible.

Passing is weak evidence by design. A sufficiently flexible model can memorize random features or wrong labels, so the test cannot prove data quality, validation correctness, robustness, or deployment parity. Failure is also not automatically a bug: label noise, an under-capacity model, hard constraints, or an irreducible probabilistic objective may impose a nonzero floor.

Record the exact sample, seed, disabled components, expected loss scale, and stopping criterion. Then restore components incrementally—augmentation, mixed precision, batching, partitioned execution, and distributed execution—while comparing loss and parameter updates. This turns a single sanity check into a controlled fault-localization sequence.

## Prerequisites

- [[loss-function]]
- [[gradient-descent]]
- [[regularization]]

## Sources

- [Stanford CS231n, “Sanity checks”](https://cs231n.github.io/neural-networks-3/#sanitycheck): check initial loss, disable regularization, overfit a tiny subset before full training, and recognize that passing can coexist with implementation defects.
