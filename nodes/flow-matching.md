---
id: flow-matching
title: Flow Matching
summary: Flow matching trains a continuous normalizing flow by regressing a vector field that generates a chosen probability path between a simple base distribution and data.
type: concept
tags: [ml/deep-learning]
prereqs: [vector-field, differential-equation, differential, probability-distribution, conditional-probability, neural-network, score-function]
sources: [https://arxiv.org/abs/2210.02747]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Flow Matching

## Summary

**Flow matching** trains a time-dependent [[vector-field]] by regression so that its ordinary [[differential-equation]] transports a simple base distribution along a selected probability path toward the data distribution.

## Grounded explanation

Let $p_t$ be a path of densities and let $u_t(x)$ be a velocity satisfying the continuity equation

$$\partial_t p_t(x)+\nabla\cdot\bigl(p_t(x)u_t(x)\bigr)=0.$$

A parameterized field $v_\theta(t,x)$ is trained to match a target field associated with [[conditional-probability]] paths. Conditional flow matching makes this regression practical without simulating the learned differential equation during every training example.

After training, sampling draws $X_0$ from the base [[probability-distribution]] and solves

$$\frac{dX_t}{dt}=v_\theta(t,X_t)$$

to the data endpoint. A [[neural-network]] commonly represents the field.

Time orientation is notation, not a fundamental distinction from diffusion. Either endpoint may be labeled zero if the path and signs are changed consistently. Flow matching may use Gaussian paths that overlap with diffusion paths or other choices such as displacement interpolations. Diffusion models can also have deterministic probability-flow formulations, so “flow means ODE and diffusion means stochastic” is too broad.

A velocity is not generally a [[score-function]]: it describes particle transport, while a score is a log-density gradient. A particular probability-flow construction may relate them through schedule-dependent drift and diffusion coefficients.

Validate endpoint distributions and sign conventions on toy data, measure field regression error by time, visualize trajectories, and compare solvers at matched function evaluations. Report sample quality, mode coverage, solver failures, and wall-clock cost because a straighter path does not guarantee a cheaper complete system.

## Prerequisites

- [[vector-field]]
- [[differential-equation]]
- [[differential]]
- [[probability-distribution]]
- [[conditional-probability]]
- [[neural-network]]
- [[score-function]]

## Sources

- [Lipman et al., “Flow Matching for Generative Modeling”](https://arxiv.org/abs/2210.02747): introduces simulation-free vector-field regression over conditional probability paths for continuous normalizing flows.
