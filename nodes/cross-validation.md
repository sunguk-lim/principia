---
id: cross-validation
title: Cross-Validation
summary: Cross-validation estimates model performance by fitting repeatedly on training folds and evaluating on held-out folds, with split design matched to the data-generating process.
type: concept
tags: [ml/evaluation]
prereqs: [measurement, hypothesis-testing]
sources: [https://scikit-learn.org/stable/modules/cross_validation.html]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Cross-Validation

## Summary

**Cross-validation** repeats a train/validation split so a model is judged on examples not used for that fit. In $K$-fold cross-validation, each fold serves as validation once, and the resulting scores show variation across partitions. This is a performance-estimation and model-selection procedure, not a guarantee of deployment behavior.

## Grounded explanation

Divide the available training data into $K$ folds. For each iteration, fit preprocessing and the model on $K-1$ folds and evaluate on the held-out fold. Aggregate the measured scores and their variation. Every learned transformation, including imputation, feature selection, and scaling, must be fitted inside the training portion of each iteration; fitting once on all data leaks validation information. An untouched final test set is still useful after model selection.

The split must reflect the actual prediction task. Random folds can leak a patient's repeated records across train and validation; group folds keep the same entity together. For future forecasting, time-ordered validation avoids training on later observations. Class imbalance may call for stratified folds. Nested cross-validation separates hyperparameter selection from performance estimation when the selection procedure itself is being evaluated.

Use [[measurement]] to report the same task metric and computational budget for every candidate model. Fold-to-fold variation is informative, but folds are not independent experimental replications; do not attach an unjustified narrow confidence interval or [[hypothesis-testing]] claim. Compare models under matched splits and preprocessing, then check performance on a representative later holdout and important subgroups. A high cross-validation mean can still hide distribution shift or an inappropriate metric.

## Prerequisites

- [[measurement]]
- [[hypothesis-testing]]

## Sources

- [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html): fold methods, pitfalls, and variants.
