---
id: representation-alignment
title: Representation Alignment
summary: Representation alignment trains an internal student feature to match a projected representation from another model as an auxiliary learning signal.
type: concept
tags: [ml/training]
prereqs: [embedding, neural-network, regularization, diffusion-transformer]
sources: [https://arxiv.org/abs/2410.06940]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Representation Alignment

## Summary

**Representation alignment** adds an auxiliary objective that makes an internal feature of a student network resemble a representation produced by a pretrained teacher. REPA applies this idea to a [[diffusion-transformer]] using clean-image features from an external visual encoder.

## Grounded explanation

Let $h_l(x_t,t)$ be the student's hidden state at layer $l$ for noisy input $x_t$, $g(x_0)$ a frozen teacher's clean-image feature, and $P$ a learned projection. A schematic objective is

$$L=L_{\text{generation}}+\lambda D(P(h_l),g(x_0)),$$

where $D$ compares normalized vectors or corresponding spatial tokens. This is a form of [[regularization]]: the generation target remains, while the auxiliary loss biases internal learning toward a teacher's representation.

The interface matters. Student and teacher tokens may differ in spatial resolution, dimensionality, normalization, and semantic abstraction. Alignment therefore requires an explicit correspondence and a projector with enough capacity. Choosing a layer solely because it is “early” or “late” is not a mechanism; test layers where resolution and information content are compatible.

The REPA paper aligns projections of noisy-input hidden states with clean-image representations and reports substantially faster convergence in its SiT experiments. Its quoted 17.5× result is a specific threshold comparison, not a guaranteed wall-clock speedup for every architecture, dataset, teacher, or final quality target.

Alignment can import useful invariances but also teacher bias, suppress features needed for generation, or let a large auxiliary gradient overwhelm denoising. Track generation and alignment losses, gradient norms and conflict, layerwise similarity, throughput overhead, convergence versus wall-clock compute, and final quality and diversity. Ablate teacher, target layer, projector, loss weight, schedule, and random seed under a matched budget.

## Prerequisites

- [[embedding]]
- [[neural-network]]
- [[regularization]]
- [[diffusion-transformer]]

## Sources

- [Yu et al., “REPresentation Alignment for Generation”](https://arxiv.org/abs/2410.06940): introduces REPA by aligning projected denoiser hidden states with external clean-image representations and evaluates convergence and generation quality.
