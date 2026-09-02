---
id: variational-inference
title: Variational Inference
summary: Variational inference turns posterior approximation into optimization by choosing the tractable distribution closest to the Bayesian posterior under KL divergence.
type: concept
tags: [math/probability]
prereqs: [bayes-rule, kl-divergence]
sources: [arxiv:1601.00670]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Variational Inference

## Summary

**Variational inference** approximates an intractable posterior by selecting, from a tractable family, the distribution that minimizes [[kl-divergence]] to the posterior implied by [[bayes-rule]].

## Grounded explanation

For observations $x$, latent variables $z$, and approximation $q(z)$, the evidence lower bound is

$$\mathcal L(q)=E_q[\log p(x,z)]-E_q[\log q(z)].$$

The identity

$$\log p(x)=\mathcal L(q)+D_{KL}(q(z)\|p(z\mid x))$$

shows why maximizing $\mathcal L$ works: the left side is fixed and [[kl-divergence]] is nonnegative, so raising the bound lowers divergence to the posterior from [[bayes-rule]].

### Worked example

Suppose two candidate approximations have ELBO values $-12.0$ and $-10.5$ for the same observation. Because the evidence is fixed, the second has KL divergence smaller by 1.5 nats and is the better approximation, even if the exact evidence is unknown.

The tractable family controls the trade-off. A simple independent family is cheap but cannot represent strong posterior dependence; a richer family can fit better but costs more to optimize. The output is an approximation plus a lower bound, not an exact posterior guarantee.

## Prerequisites

- [[bayes-rule]]
- [[kl-divergence]]

## Sources

- Blei, Kucukelbir, and McAuliffe, “Variational Inference: A Review for Statisticians,” arXiv:1601.00670.
