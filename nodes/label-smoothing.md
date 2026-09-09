---
id: label-smoothing
title: Label Smoothing
summary: Label smoothing trains a classifier against a mixture of the observed one-hot target and a reference label distribution instead of assigning all target mass to one class.
type: concept
tags: [ml/training]
prereqs: [regularization, softmax, loss-function, model-calibration, probability-distribution]
sources: [https://arxiv.org/abs/1512.00567, https://arxiv.org/abs/1906.02629]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Label Smoothing

## Summary

**Label smoothing** replaces a one-hot classification target with a convex mixture of that target and a reference distribution over labels.

## Grounded explanation

For $K$ classes, observed class $y$, smoothing strength $\varepsilon\in[0,1]$, and reference distribution $u$, define

$$q(k\mid y)=(1-\varepsilon)\mathbf 1[k=y]+\varepsilon u(k).$$

Uniform smoothing sets $u(k)=1/K$. Training then evaluates the classification [[loss-function]] against $q$ rather than the one-hot target. The [[softmax]] model is discouraged from assigning all mass to the observed label, making label smoothing a form of target-side [[regularization]].

The exact convention matters. Some libraries distribute $\varepsilon$ across all classes; others distribute it only among incorrect classes. These definitions produce different target probabilities for the same numeric value, so record the formula rather than only the hyperparameter.

Smoothing can improve optimization or generalization, but it changes the meaning of learned scores. It does not universally worsen [[model-calibration]]; empirical work has found improved calibration in some settings while also finding reduced information useful for teacher–student distillation. Effects depend on label noise, class count, imbalance, metric, and downstream use.

Uniform smoothing encodes a uniform reference [[probability-distribution]], which may be inappropriate under structured or cost-sensitive labels. Alternatives include class-dependent priors, data augmentation, weight decay, focal objectives, and post-hoc calibration; they solve different problems.

Tune $\varepsilon$ on held-out data and report accuracy, negative log score, Brier score, reliability diagrams, and class slices. For distillation or uncertainty-sensitive use, measure those tasks directly instead of inferring them from lower confidence alone.

## Prerequisites

- [[regularization]]
- [[softmax]]
- [[loss-function]]
- [[model-calibration]]
- [[probability-distribution]]

## Sources

- [Szegedy et al., “Rethinking the Inception Architecture for Computer Vision”](https://arxiv.org/abs/1512.00567): introduces label smoothing as a regularizing target distribution in the Inception training setup.
- [Müller, Kornblith, and Hinton, “When Does Label Smoothing Help?”](https://arxiv.org/abs/1906.02629): studies generalization, calibration, learned representations, and reduced effectiveness for knowledge distillation.
