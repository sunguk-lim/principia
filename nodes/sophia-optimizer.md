---
id: sophia-optimizer
title: Sophia Optimizer
summary: Sophia scales smoothed gradients by a periodically estimated diagonal curvature statistic and clips coordinate updates to bound their magnitude.
type: concept
tags: [ml/deep-learning]
prereqs: [momentum, hessian]
sources: [https://arxiv.org/abs/2305.14342, https://github.com/Liuhong99/Sophia]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Sophia Optimizer

## Meaning

Sophia introduces an explicit curvature estimate into a clipped momentum update. Unlike squared-gradient normalization alone, it aims to estimate a diagonal curvature-related quantity. Periodic refresh spreads the estimator's expense across multiple ordinary steps, but makes freshness and estimator choice part of the algorithm.

## Mechanism

Let m_i be coordinate i of an exponential gradient average as in [[momentum]], h_i a nonnegative stabilized diagonal curvature estimate, rho a positive scaling parameter, epsilon a positive denominator floor and eta the learning rate. One reference-code convention forms

$$u_i=\operatorname{clip}\left(\frac{m_i}{\rho h_i+\epsilon},-1,1\right),\qquad
\theta_i\leftarrow\theta_i-\eta u_i.$$

Clip limits a value to the stated interval, so the data-step magnitude is at most eta. Decoupled shrinkage can be applied separately. [[hessian]] defines true local second derivatives, but Sophia variants use different stochastic estimators; Sophia-G's sampled-label construction and normalization must not be called an exact Hessian diagonal. The published paper and reference code use equivalent reparameterizations of the clipping scale, so compare complete formulas, not eta labels alone.

## One example

Take m=[0.6,-0.2], h=[2,0.1], rho=0.5, epsilon=0.01 and eta=0.1. Denominators are [1.01,0.06], giving ratios approximately [0.5941,-3.3333]. Clipping yields [0.5941,-1], so the parameter changes are [-0.05941,+0.1]. The second coordinate is capped; the first still responds to the estimated scale. A tiny denominator cannot make the data update exceed the chosen cap.

## Check your understanding

Does clipping guarantee that a stale or biased curvature estimate is harmless? No. It bounds this step term, not accumulated error, decay or convergence. Verify estimator sampling, loss normalization, batch/token scaling, refresh frequency and clipped-coordinate fraction. Charge extra estimator passes to wall-clock and compute budgets; test held-out quality and instability instead of assuming paper-level speedups transfer.

## Prerequisites

- [[momentum]]
- [[hessian]]

## Sources

- <https://arxiv.org/abs/2305.14342>
- <https://github.com/Liuhong99/Sophia>
