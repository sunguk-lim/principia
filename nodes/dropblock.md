---
id: dropblock
title: DropBlock
summary: DropBlock is a structured regularizer that masks contiguous spatial regions in convolutional feature maps during training.
type: concept
tags: [ml/deep-learning]
prereqs: [regularization, neural-network]
sources: [https://arxiv.org/abs/1810.12890]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# DropBlock

## Summary

**DropBlock** is a training-time [[regularization]] method for convolutional networks that zeros a contiguous block of activations rather than independently masking individual activations.

## Grounded explanation

In a convolutional feature map, nearby activations can be strongly correlated. Independent dropout can remove one activation while leaving adjacent activations that carry similar local evidence. DropBlock samples block centers and masks surrounding $b\times b$ regions. The mask is then applied to a feature map and the retained activations are rescaled so their expected scale is comparable during training.

The block size and drop probability control the perturbation. Larger blocks remove wider local evidence but can destroy too much signal, especially on small feature maps. At inference, DropBlock is disabled, as with ordinary dropout. It is therefore a training perturbation, not an architectural replacement for convolution.

Evaluate DropBlock with a matched training budget and compare it with ordinary dropout, weight decay, augmentation, and no structured masking. Sweep block size and keep probability separately for feature-map resolution; report held-out accuracy, calibration, robustness slices, and training stability. A result on one architecture or dataset does not establish that contiguous masking is universally superior.

## Prerequisites

- [[regularization]]
- [[neural-network]]

## Sources

- [Ghiasi, Lin, and Le, “DropBlock: A regularization method for convolutional networks”](https://arxiv.org/abs/1810.12890): introduces contiguous activation masking and reports its convolutional-network experiments.
