---
id: diffusion-transformer
title: Diffusion Transformer
summary: A diffusion transformer replaces a convolutional denoising backbone with transformer blocks that operate on image or latent patches under timestep and other conditioning.
type: concept
tags: [ml/deep-learning]
prereqs: [denoising-diffusion-probabilistic-model, transformer-attention, adaptive-layer-normalization, autoencoder]
sources: [https://arxiv.org/abs/2212.09748]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Diffusion Transformer

## Summary

A **diffusion transformer** (DiT) uses transformer blocks as the prediction backbone of a [[denoising-diffusion-probabilistic-model]]. A common design processes patches from a compressed image representation and conditions every block on noise level and class or text information.

## Grounded explanation

Let a latent feature map have height $H$, width $W$, and patch side $P$. Non-overlapping patches produce

$$N=\frac{H}{P}\frac{W}{P}$$

tokens. The sequence is processed with [[transformer-attention]], then projected back to a spatial prediction used by the diffusion objective. An [[autoencoder]] often maps between pixels and this lower-resolution latent space.

Patch size affects compute without necessarily changing model parameter count. Halving $P$ in each spatial dimension makes four times as many tokens. Dense self-attention's score matrix grows approximately with $N^2$, although projections and feed-forward layers add other terms. Depth and width increase parameters and operations differently, so neither parameter count nor patch size alone is a complete scaling axis.

The original DiT study compared model depth, width, and patch size through forward-pass Gflops and observed lower FID for higher-compute variants in its class-conditional ImageNet setting. That is an empirical result, not a universal law that quality always follows Gflops. Data, optimization, training duration, latent compression, conditioning, sampler, and metric uncertainty can become bottlenecks.

Global timestep or class information is commonly injected by [[adaptive-layer-normalization]]. Rich text can instead use attention-based conditioning. Evaluate designs at matched training compute and matched inference budgets; report loss and image metrics against operations, wall-clock time, memory, sample count, and confidence intervals.

## Prerequisites

- [[denoising-diffusion-probabilistic-model]]
- [[transformer-attention]]
- [[adaptive-layer-normalization]]
- [[autoencoder]]

## Sources

- [Peebles and Xie, “Scalable Diffusion Models with Transformers”](https://arxiv.org/abs/2212.09748): introduces latent-patch DiTs and studies scaling through depth, width, patch size, and forward-pass Gflops.
