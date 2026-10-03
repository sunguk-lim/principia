---
id: maximum-margin-hinge-loss
title: Maximum-Margin Hinge Loss
summary: Hinge loss penalizes examples whose signed classification margin is below a target threshold, including correct but low-margin predictions.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, regularization]
sources: [https://scikit-learn.org/stable/modules/svm.html]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Maximum-Margin Hinge Loss

## Summary

**Hinge loss** is `max(0, 1 - y f(x))` for binary labels `y` in `{-1, +1}` and a decision score `f(x)`. A correct classification can still incur loss if its signed margin is below one.

## Grounded explanation

The threshold creates a buffer around the decision boundary: examples beyond it contribute zero hinge loss; examples inside it exert pressure to move the boundary. A soft-margin support-vector machine combines that [[loss-function]] with [[regularization]] on model complexity. The regularization coefficient trades margin violations against model complexity, and feature scaling affects that trade.

The score is not automatically a calibrated probability. Hinge loss also does not uniquely belong to SVMs, nor does every SVM use the same objective. Validate with held-out classification error, precision/recall, subgroup errors, and calibration if probabilities are needed. Compare against logistic loss under matched features and tuning budgets, particularly when classes overlap or labels are noisy.

## Prerequisites

- [[loss-function]]
- [[regularization]]

## Sources

- [scikit-learn support vector machines](https://scikit-learn.org/stable/modules/svm.html): margin objectives, kernels, and tuning considerations.
