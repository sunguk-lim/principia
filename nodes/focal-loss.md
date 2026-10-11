---
id: focal-loss
title: Focal Loss
summary: Focal loss multiplies cross-entropy by a confidence-dependent factor so already-easy examples contribute less to the training gradient.
type: concept
tags: [ml/deep-learning]
prereqs: [class-weighted-loss]
sources: [https://arxiv.org/abs/1708.02002]
status: explained
created: 2026-10-12
updated: 2026-10-12
---

# Focal Loss

## Summary

**Focal loss** reduces the training contribution of confidently correct examples. It was introduced for dense object detection, where many easy background anchors can dominate ordinary cross-entropy. It is a possible response to a hard/easy-example imbalance, not a universal remedy for rare positive classes.

## Grounded explanation

For the probability $p_t$ assigned to the true class, binary cross-entropy is $-\log p_t$. Focal loss adds a factor $(1-p_t)^\gamma$ and optionally a class weight $\alpha_t$:

$$L_{\mathrm{focal}}=-\alpha_t(1-p_t)^\gamma\log p_t.$$

When $p_t$ is close to one, the factor approaches zero, so easy examples are downweighted. When $p_t$ is small, the factor remains larger, preserving more gradient for hard examples. At $\gamma=0$, this reduces to ordinary (optionally [[class-weighted-loss|class-weighted]]) cross-entropy. The focusing parameter $\gamma$ changes a confidence-dependent weight; $\alpha_t$ separately addresses class weighting.

This mechanism does not identify why an example is hard. Ambiguous or incorrectly labeled examples may get extra attention, and altered training weights can change probability calibration. A fraud dataset with many easy negatives is not automatically equivalent to the paper's dense detection setting.

## Validation

Compare unweighted, class-weighted, focal, and hard-negative sampling baselines with the same data and compute. Sweep $\gamma$ and $\alpha$ on training/validation data only. Evaluate precision and recall at operating capacity, calibration, delayed labels, and hard-example error types on a temporal holdout. Reject claims of superiority based only on training loss or a single AUC.

## Prerequisites

- [[class-weighted-loss]]

## Sources

- [Lin et al., *Focal Loss for Dense Object Detection*](https://arxiv.org/abs/1708.02002)
