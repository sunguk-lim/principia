---
id: gradient-boosting-objective
title: Gradient Boosting Objective
summary: Gradient boosting adds weak learners in stages to reduce a chosen differentiable objective by fitting each stage to a local descent direction.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, gradient-descent]
sources: [https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Gradient Boosting Objective

## Summary

**Gradient boosting** grows an additive predictor one stage at a time. Each new weak learner approximates the direction in which changing current predictions would reduce the chosen objective.

## Grounded explanation

Given a differentiable [[loss-function]], compute the negative gradient of loss with respect to each training prediction. Fit a weak learner, often a shallow tree, to those pseudo-residuals and add a scaled version to the ensemble. This is functional [[gradient-descent]]: the update changes the prediction function, not just a fixed vector of coefficients. Squared error yields ordinary residuals, while classification objectives produce different gradients; there is no one loss shared by all boosting tasks.

Learning rate, tree size, round count, and regularization interact. Use a held-out set or cross-validation to choose them, watch for overfitting, and compare against a simple tree or linear baseline. For structured data, claims that boosting always beats neural networks require matched preprocessing, tuning, compute, and test splits—not anecdotal competition results.

## Prerequisites

- [[loss-function]]
- [[gradient-descent]]

## Sources

- [scikit-learn gradient boosting](https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting): stagewise optimization and supported losses.
