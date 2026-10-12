---
id: hard-negative-mining
title: Hard-Negative Mining
summary: Hard-negative mining selects currently confusing negative examples for training, balancing learning signal against noise and selection bias.
type: concept
tags: [ml/training]
prereqs: [class-weighted-loss, focal-loss]
sources: [https://arxiv.org/abs/1503.03832, https://arxiv.org/abs/1708.02002]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Hard-Negative Mining

## Summary

**Hard-negative mining** gives training attention to negative examples the current model finds confusing. A negative is not “hard” by class label alone: it is hard relative to the current model, objective, and sampling distribution.

## Grounded explanation

In an imbalanced detection or retrieval task, many easy negatives already receive near-zero loss, while a smaller set of false positives carries useful discrimination signal. A training loop can score candidate negatives, retain a bounded high-loss subset, and update on those along with positives. This differs from [[class-weighted-loss]], which scales *all* examples of a class using fixed weights. [[focal-loss]] continuously downweights easy examples through the loss itself; explicit mining changes which examples enter the batch.

The method can fail when hard examples are mislabeled, out of distribution, or dominated by a narrow failure mode. Selecting only the worst current errors can overfit noise and distort the effective training prior. In metric learning, “too hard” examples early in training may be unstable; a staged or semi-hard policy can be better. The selection computation itself can be costly, and mining from validation or test data leaks information.

Compare random sampling, class weighting, focal loss, and bounded hard-negative mining under matched data and compute. Measure precision-recall, false-positive burden at an operational threshold, calibration, and performance on temporal or source-separated holdouts. Audit mined examples for label quality and diversity, and keep evaluation distributions representative of deployment rather than the mining distribution.

## Prerequisites

- [[class-weighted-loss]]
- [[focal-loss]]

## Sources

- [FaceNet](https://arxiv.org/abs/1503.03832): discusses online semi-hard negative selection for metric learning.
- [Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002): motivates reducing easy-negative dominance and contrasts sampling-based approaches.
