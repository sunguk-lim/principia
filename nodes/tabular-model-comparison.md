---
id: tabular-model-comparison
title: Tabular Model Comparison
summary: A tabular model comparison evaluates tree ensembles and neural or linear baselines on matched data splits, tuning budgets, metrics, and deployment constraints instead of treating one family as universally superior.
type: concept
tags: [ml/evaluation]
prereqs: [gradient-boosting-objective, cross-validation, measurement]
sources: [https://arxiv.org/abs/2207.08815]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Tabular Model Comparison

## Summary

“Boosting beats neural networks on structured data” is not a portable result. **Tabular model comparison** is the controlled procedure for deciding which model family works for a particular dataset and deployment budget. The objective, data split, feature types, tuning budget, and metric must be matched before an observed gap means anything.

## Grounded explanation

Begin with a simple linear or tree baseline, a boosted-tree model, and a relevant neural baseline. [[gradient-boosting-objective]] explains one family but not the comparison itself. Use the same training, validation, and test populations, with [[cross-validation]] or a temporal split appropriate to the data-generating process. Keep test data out of preprocessing and hyperparameter selection. Allocate a documented search budget per family and report both the best quality and the resources required to reach it.

Tabular data often mixes numerical and categorical fields, missingness, skewed targets, and small sample sizes. Preprocessing choices can advantage one model: a tree may handle threshold-like patterns naturally, while a neural model may benefit from scale, embeddings, or multimodal covariates. Dataset properties, not a model label, govern the result. Grinsztajn and colleagues benchmarked many medium-sized datasets and found strong tree-based baselines in their setting; that finding motivates a baseline, not a universal winner.

For a credit-risk example, choose a time-respecting holdout and compare discrimination, calibration, subgroup error, latency, training cost, and maintenance burden. [[measurement]] should report uncertainty across folds or seeds and the complete tuning budget. Try uninformative features, rare categories, missing values, and distribution shift. A small quality gain can be outweighed by update cost or inference latency; conversely, a neural model may be preferable when representations transfer across related tasks. Do not turn a contest leaderboard or an unbalanced tuning run into a general superiority claim.

## Prerequisites

- [[gradient-boosting-objective]]
- [[cross-validation]]
- [[measurement]]

## Sources

- [Grinsztajn et al., Why do tree-based models still outperform deep learning on tabular data?](https://arxiv.org/abs/2207.08815): bounded benchmark and methodology.
