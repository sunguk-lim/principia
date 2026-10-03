---
id: lazy-nearest-neighbor-learning
title: Lazy Nearest-Neighbor Learning
summary: Lazy nearest-neighbor learning stores labeled examples and makes a prediction by retrieving nearby examples at query time instead of fitting a global parametric decision function.
type: concept
tags: [ml/evaluation]
prereqs: [nearest-neighbor-search, measurement]
sources: [https://scikit-learn.org/stable/modules/neighbors.html]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Lazy Nearest-Neighbor Learning

## Summary

A nearest-neighbor predictor defers much of its work until a query arrives. It keeps training examples and predicts a label or value from the `k` most similar examples under a chosen distance rule.

## Grounded explanation

[[nearest-neighbor-search]] identifies candidates; classification can vote among their labels, while regression can average their values. There may be no gradient-trained global parameters, but the method still has an objective and choices that affect error: representation, distance, `k`, weighting, and data preprocessing. Calling it “no loss function” should not imply it needs no validation or tuning.

Local prediction can adapt to irregular boundaries but makes storage, query latency, scaling, and high-dimensional distance behavior important. Leakage is easy if duplicates or related records cross a train/test boundary. Use [[measurement]] to compare held-out accuracy or error, query latency, memory, and robustness to feature scaling against a simple fitted baseline. If approximate search is used, measure retrieval recall separately from predictive quality.

## Prerequisites

- [[nearest-neighbor-search]]
- [[measurement]]

## Sources

- [scikit-learn nearest neighbors](https://scikit-learn.org/stable/modules/neighbors.html): supervised classification/regression and distance choices.
