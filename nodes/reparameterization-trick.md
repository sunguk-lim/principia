---
id: reparameterization-trick
title: Reparameterization Trick
summary: The reparameterization trick expresses a parameterized random sample as a differentiable transformation of parameter-free noise, allowing gradients to pass through sampling.
type: concept
tags: [ml/deep-learning]
prereqs: [change-of-variables, normal-distribution]
sources: [arxiv:1312.6114]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Reparameterization Trick

## Summary

The **reparameterization trick** rewrites a sample from a parameterized distribution as a differentiable function of its parameters and an auxiliary noise sample whose distribution does not depend on those parameters.

## Grounded explanation

For a [[normal-distribution]] with mean $\mu$ and standard deviation $\sigma$,

$$z\sim N(\mu,\sigma^2)$$

can be written as

$$\epsilon\sim N(0,1),\qquad z=\mu+\sigma\epsilon.$$

This is a [[change-of-variables]]: randomness lives in $\epsilon$, while $z$ is differentiable with respect to $\mu$ and $\sigma$ for the sampled value.

### Worked example

Let $\mu=2$, $\sigma=0.5$, and sampled noise $\epsilon=-0.4$. Then $z=2+0.5(-0.4)=1.8$. For objective $g(z)=z^2$, the sampled value is 3.24 and derivatives pass through: $\partial g/\partial\mu=2z=3.6$ and $\partial g/\partial\sigma=2z\epsilon=-1.44$.

Sampling $z$ as an opaque random operation would hide this path from ordinary differentiation. Reparameterization exposes it, producing low-variance pathwise gradient estimates when a suitable transformation exists.

## Prerequisites

- [[change-of-variables]]
- [[normal-distribution]]

## Sources

- Kingma and Welling, “Auto-Encoding Variational Bayes,” arXiv:1312.6114 — SGVB reparameterization estimator.
