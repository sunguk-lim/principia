---
id: loss-function
title: Loss function
summary: A loss function turns "how wrong is the model?" into a single number to minimize.
type: concept
tags: [ml/deep-learning]
prereqs: [arithmetic, maximum-likelihood-estimation, likelihood]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-24
---

# Loss function

## Summary

A **loss function** turns "how wrong is the model?" into a single number to
minimize.

## Grounded explanation

It maps the model's parameters $\theta$ to a non-negative error computed from
predictions versus targets (sums, differences, products — [[arithmetic]]):

$$\mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^{N} \ell\big(f_\theta(x_i),\, y_i\big)$$

where $\ell$ scores one prediction against its target. Training is the search for
$\theta$ that makes $\mathcal{L}$ small; its gradient tells gradient-descent
which way to move.

**Where the loss comes from.** A principled choice of $\ell$ falls out of
[[maximum-likelihood-estimation]]: the **cross-entropy** loss is the **negative
log-[[likelihood]]** of the targets under the model, so minimizing it is *exactly*
maximizing the likelihood of the data —
$\mathcal{L}(\theta) = -\frac{1}{N}\sum_{i} \log p_\theta(y_i \mid x_i)$. (Mean
squared error is the same story under Gaussian noise.) So "fit by maximum
likelihood" and "minimize this loss" are one objective, viewed from two sides.

## Prerequisites

- [[arithmetic]]
- [[likelihood]]
- [[maximum-likelihood-estimation]]

## Sources

_none_
