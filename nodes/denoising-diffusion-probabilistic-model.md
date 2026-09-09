---
id: denoising-diffusion-probabilistic-model
title: Denoising Diffusion Probabilistic Model
summary: A denoising diffusion probabilistic model learns to reverse a fixed gradual noising process, turning a simple noise distribution into data through repeated denoising transitions.
type: concept
tags: [ml/deep-learning]
prereqs: [stochastic-process, conditional-probability, divergence, kl-divergence, reparameterization-trick, neural-network]
sources: [https://arxiv.org/abs/2006.11239]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Denoising Diffusion Probabilistic Model

## Summary

A **denoising diffusion probabilistic model** (DDPM) defines a fixed forward [[stochastic-process]] that gradually adds Gaussian noise, then trains a [[neural-network]] to approximate the reverse transitions needed to generate data from noise.

## Grounded explanation

For data $x_0$, a variance-preserving forward transition is

$$q(x_t\mid x_{t-1})=\mathcal N\!\left(\sqrt{\alpha_t}x_{t-1},(1-\alpha_t)I\right),$$

with $\alpha_t=1-\beta_t$. Define $\bar\alpha_t=\prod_{s=1}^t\alpha_s$. Because the transitions are linear Gaussians, their marginal [[conditional-probability]] has the closed form

$$q(x_t\mid x_0)=\mathcal N\!\left(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I\right).$$

Using the [[reparameterization-trick]], training can sample any timestep directly:

$$x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\,\epsilon,\qquad \epsilon\sim\mathcal N(0,I).$$

There is no need to materialize every earlier state when only $x_t$ is required. Correlated Gaussian noise can also admit a direct marginal when its covariance propagation remains tractable; isotropy is a convenient standard case, not the only possible one.

The exact forward posterior $q(x_{t-1}\mid x_t,x_0)$ is Gaussian. A common reverse model uses a Gaussian $p_\theta(x_{t-1}\mid x_t)$ whose mean is parameterized through predicted noise, clean data, or velocity. Terms in the variational objective then involve analytic Gaussian [[kl-divergence]]s and often reduce to a weighted regression loss. The familiar unweighted noise-prediction loss is a design choice, not a universal algebraic identity.

Generation remains iterative: start from the terminal noise distribution and apply reverse transitions. Learned variance, prediction target, timestep weighting, and sampler affect speed and quality. Verify closed-form sampling against an iterated forward chain, test endpoint moments, and evaluate both variational objectives and sample quality across timesteps.

## Prerequisites

- [[stochastic-process]]
- [[conditional-probability]]
- [[divergence]]
- [[kl-divergence]]
- [[reparameterization-trick]]
- [[neural-network]]

## Sources

- [Ho, Jain, and Abbeel, “Denoising Diffusion Probabilistic Models”](https://arxiv.org/abs/2006.11239): develops DDPM training through a weighted variational bound and its connection to denoising score matching.
