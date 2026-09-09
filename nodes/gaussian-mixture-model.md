---
id: gaussian-mixture-model
title: Gaussian Mixture Model
summary: A Gaussian mixture model represents a density as a weighted sum of Gaussian components, yielding soft component assignments and covariance-dependent cluster shapes.
type: concept
tags: [ml/training]
prereqs: [probability-distribution, likelihood, expectation, expectation-maximization]
sources: [https://scikit-learn.org/stable/modules/mixture.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Gaussian Mixture Model

## Summary

A **Gaussian mixture model** (GMM) is a latent-variable [[probability-distribution]] formed from a finite weighted sum of Gaussian component densities.

## Grounded explanation

For $K$ components,

$$p(x)=\sum_{k=1}^K \pi_k\,\mathcal N(x\mid\mu_k,\Sigma_k),$$

where $\pi_k\ge0$ and $\sum_k\pi_k=1$. The posterior responsibility

$$r_{nk}=\frac{\pi_k\mathcal N(x_n\mid\mu_k,\Sigma_k)}{\sum_j\pi_j\mathcal N(x_n\mid\mu_j,\Sigma_j)}$$

is a soft assignment of point $n$ to component $k$.

[[expectation-maximization]] uses an [[expectation]] step for responsibilities and alternates between computing them and updating weights, means, and covariances to increase the data [[likelihood]]. Convergence is to a stationary point, often a local optimum, so initialization and multiple restarts matter.

Covariance restrictions determine geometry and parameter cost. Spherical covariance gives round equal-variance contours per component; diagonal covariance allows axis-aligned ellipses; tied covariance shares one matrix; full covariance permits rotated ellipses but requires more data and computation.

K-means is related but not simply identical to every GMM. It makes hard nearest-centroid assignments and corresponds to a limiting equal spherical-variance view under particular assumptions. A GMM can model density and uncertainty, but it does not guarantee that components equal meaningful real-world clusters.

Maximum likelihood can become singular when a component collapses onto too few points. Regularize covariances, inspect component weights, and compare several initializations. Choose component count with held-out likelihood or an information criterion while acknowledging its assumptions; validate stability and usefulness on the downstream task.

## Prerequisites

- [[probability-distribution]]
- [[likelihood]]
- [[expectation]]
- [[expectation-maximization]]

## Sources

- [scikit-learn User Guide, “Gaussian Mixture Models”](https://scikit-learn.org/stable/modules/mixture.html): defines finite Gaussian mixtures, EM fitting, covariance options, soft assignments, singularities, and component-selection limits.
