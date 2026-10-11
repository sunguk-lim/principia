---
id: bayesian-optimization
title: Bayesian Optimization
summary: Bayesian optimization selects expensive black-box evaluations by combining a probabilistic surrogate with an acquisition rule that balances promising values and uncertainty.
type: concept
tags: [math/optimization]
prereqs: [conditional-probability]
sources: [https://arxiv.org/abs/1206.2944]
status: explained
created: 2026-10-12
updated: 2026-10-12
---

# Bayesian Optimization

## Summary

**Bayesian optimization** is a sequential strategy for an expensive black-box objective. It fits a probabilistic surrogate to observed inputs and outcomes, then chooses the next input with an acquisition rule. It is useful when each experiment is costly and only a modest number can be run; it is not inherently faster than every grid or random search.

## Grounded explanation

Suppose a training pipeline returns validation score $f(x)$ for hyperparameters $x$, but evaluating $f$ takes hours and derivatives are unavailable. The surrogate estimates a distribution over unmeasured scores given prior observations: $p(f(x)\mid D)$, an application of [[conditional-probability]]. A Gaussian process is one surrogate choice, not the definition of the method. An acquisition rule turns predicted value and uncertainty into a utility for the next experiment: expected improvement, for example, favors points that might exceed the current best. The algorithm proposes $x$, evaluates the real pipeline, updates $D$, and repeats.

The method balances exploration of uncertain regions and exploitation of promising ones within the declared search domain. It cannot discover a setting outside that domain, and noisy, conditional, high-dimensional, or drifting objectives can make the surrogate misleading. Discrete and categorical parameters are possible with suitable models; claiming Bayesian optimization only handles continuous values would be false.

## Validation

Use identical search spaces, compute budgets, seed controls, and evaluation splits when comparing with random or grid search. Report best-held-out objective versus cumulative wall time and number of trials, across multiple independent runs. Keep test data outside the tuning loop to avoid overfitting model selection to a holdout.

## Prerequisites

- [[conditional-probability]]

## Sources

- [Snoek, Larochelle, and Adams, *Practical Bayesian Optimization of Machine Learning Algorithms*](https://arxiv.org/abs/1206.2944)
