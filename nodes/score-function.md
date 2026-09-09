---
id: score-function
title: Score Function
summary: The score function of a differentiable density is the gradient of its log density with respect to the sample, pointing locally toward increasing density without specifying a transport velocity by itself.
type: concept
tags: [math/probability]
prereqs: [probability-distribution, gradient, vector-field, expectation]
sources: [https://arxiv.org/abs/2011.13456]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Score Function

## Summary

For a differentiable density $p(x)$, the **score function** with respect to the sample is

$$s(x)=\nabla_x\log p(x).$$

It describes the local geometry of a [[probability-distribution]]; it is not synonymous with every vector field used to move samples.

## Grounded explanation

Using the chain rule,

$$\nabla_x\log p(x)=\frac{\nabla_x p(x)}{p(x)}$$

where $p(x)>0$. The score points in a direction where local log density increases. Its [[expectation]] under suitable boundary conditions is zero, so it is not a global direction toward one universal mode.

For a one-dimensional Gaussian $\mathcal N(\mu,\sigma^2)$,

$$s(x)=-\frac{x-\mu}{\sigma^2}.$$

The value points toward the mean and grows in magnitude with standardized distance. In a time-indexed noising process, $s_t(x)=\nabla_x\log p_t(x)$ changes with the perturbed density $p_t$.

A general [[vector-field]] may encode particle velocity, force, or another dynamics. The score is constrained to be a spatial log-density gradient. A transport velocity can be related to a score through a particular generative construction, but coefficients, drift, and time convention are part of that relation.

Following a static score deterministically performs local mode seeking, not distribution-preserving sampling. Likewise, adding arbitrary noise does not define a valid sampler. Check an implementation against an analytic density, verify signs and scale at several times, and distinguish score error from numerical integration error.

## Prerequisites

- [[probability-distribution]]
- [[gradient]]
- [[vector-field]]
- [[expectation]]

## Sources

- [Song et al. (2021)](https://arxiv.org/abs/2011.13456): defines the time-dependent score as the gradient field of perturbed data distributions and uses it in reverse-time dynamics.
