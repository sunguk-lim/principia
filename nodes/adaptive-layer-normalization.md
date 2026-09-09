---
id: adaptive-layer-normalization
title: Adaptive Layer Normalization
summary: Adaptive layer normalization conditions a network block by deriving feature-wise scale and shift parameters, and sometimes residual gates, from an external conditioning vector.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, transformer-attention, denoising-diffusion-probabilistic-model, embedding]
sources: [https://arxiv.org/abs/2212.09748]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Adaptive Layer Normalization

## Summary

**Adaptive layer normalization** conditions a block by computing normalization parameters from an external vector such as a diffusion timestep and class label.

## Grounded explanation

For hidden vector $h$, ordinary layer normalization standardizes features within a token. Adaptive normalization then applies condition-dependent vectors:

$$\operatorname{AdaLN}(h,c)=\gamma(c)\odot\operatorname{LN}(h)+\beta(c).$$

Here $c$ is encoded by a [[neural-network]], and $\gamma(c)$ and $\beta(c)$ scale and shift feature channels. A residual variant can also predict a gate $\alpha(c)$ for the block output.

In a diffusion transformer, the timestep and class [[embedding]] are global conditions for the [[denoising-diffusion-probabilistic-model]]. Applying their modulation inside each [[transformer-attention]] block avoids adding condition tokens to the sequence. This can be cheaper than attention-based injection, but “free” is inaccurate: parameter projections and elementwise work remain.

AdaLN-Zero initializes selected modulation or residual-output parameters so the residual branch initially contributes near zero. This creates an identity-like starting path, but it is an initialization choice rather than a universal convergence guarantee.

Global modulation and token-level conditioning solve different problems. A timestep may fit global modulation; a detailed text prompt may benefit from cross- or joint-token interaction. Compare concatenation, cross-attention, and modulation at matched compute, then measure convergence, gradient flow, condition sensitivity, latency, and sample quality.

## Prerequisites

- [[neural-network]]
- [[transformer-attention]]
- [[denoising-diffusion-probabilistic-model]]
- [[embedding]]

## Sources

- [Peebles and Xie, “Scalable Diffusion Models with Transformers”](https://arxiv.org/abs/2212.09748): evaluates conditioning mechanisms for diffusion transformers, including adaptive layer normalization and zero-initialized modulation.
