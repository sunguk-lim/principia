---
id: receptive-field
title: Receptive Field
summary: A unit's theoretical receptive field is the input region that can affect it, while its effective receptive field measures where changes actually exert substantial influence.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, transformer-attention]
sources: [https://arxiv.org/abs/1701.04128]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Receptive Field

## Summary

The **receptive field** of a unit is the region of an input that can influence it. The theoretical field follows connectivity; the effective field weights input positions by their actual influence and can occupy only part of the theoretical region.

## Grounded explanation

For stride-one layers with odd kernel widths $k_1,\ldots,k_L$, a simple one-dimensional theoretical width is

$$r_L=1+\sum_{\ell=1}^{L}(k_\ell-1).$$

With three width-3 layers, $r_3=7$: seven input positions have a path to one output. Stride, dilation, downsampling, and skip paths change this recurrence.

Connectivity does not mean equal influence. Luo et al. measured gradients from an output unit back to input positions and found influence concentrated near the center in studied deep convolutional networks, often approximately Gaussian. Nonlinearities, subsampling, dropout, and skip connections alter this effective pattern.

A larger theoretical field therefore does not guarantee strong long-range use, but neither does it prove distant information becomes unusable. [[transformer-attention]] offers short interaction paths between tokens, while convolutional hierarchies provide locality and favorable scaling. Attention can itself be windowed, sparse, or weakly trained, so “global attention” is not the same as demonstrated global coherence.

Measure both architecture and behavior: compute theoretical coverage, backpropagate influence maps, and run controlled tasks where a prediction requires distant evidence. Compare quality, memory, and throughput at matched parameter and compute budgets before attributing gains to interaction distance.

## Prerequisites

- [[neural-network]]
- [[transformer-attention]]

## Sources

- [Luo et al., “Understanding the Effective Receptive Field in Deep Convolutional Neural Networks”](https://arxiv.org/abs/1701.04128): distinguishes effective from theoretical receptive fields and studies architecture-dependent influence patterns.
