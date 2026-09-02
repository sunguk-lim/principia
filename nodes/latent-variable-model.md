---
id: latent-variable-model
title: Latent-Variable Model
summary: A latent-variable model explains observed data through an unobserved random variable and obtains observation probabilities by summing or integrating over that hidden variable.
type: concept
tags: [math/probability]
prereqs: [probability-distribution, likelihood]
sources: [https://arxiv.org/abs/1312.6114]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Latent-Variable Model

## Summary

A **latent-variable model** introduces an unobserved random variable $Z$ that helps generate observed data $X$, defining their joint [[probability-distribution]] and obtaining the observed-data probability by marginalizing $Z$.

## Grounded explanation

A common factorization is

$$p_\theta(x,z)=p(z)p_\theta(x\mid z),$$

where $p(z)$ is a prior and $p_\theta(x\mid z)$ is the [[likelihood]] of an observation given the latent value. The observed-data density is

$$p_\theta(x)=\int p(z)p_\theta(x\mid z)\,dz.$$

### Worked example

Let hidden $Z$ choose one of two coins with equal probability. Coin A produces heads with probability 0.8 and coin B with probability 0.2. The observed probability of heads is $0.5(0.8)+0.5(0.2)=0.5$. After seeing heads, the hidden coin remains unobserved, but A is more plausible because it assigns higher likelihood to heads.

The latent variable can represent a cluster, cause, or compressed factor. Learning adjusts parameters so the marginal model explains observed data; inference asks which latent values plausibly produced a particular observation.

## Prerequisites

- [[probability-distribution]]
- [[likelihood]]

## Sources

- Kingma and Welling, “Auto-Encoding Variational Bayes,” arXiv:1312.6114 — latent generative model and marginal likelihood.
