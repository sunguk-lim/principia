---
id: tree-split-impurity
title: Tree Split Impurity
summary: Tree split impurity scores how much a candidate partition reduces target heterogeneity within child nodes, using a criterion matched to classification or regression.
type: concept
tags: [ml/evaluation]
prereqs: [probability-distribution, loss-function]
sources: [https://scikit-learn.org/stable/modules/tree.html]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Tree Split Impurity

## Summary

A decision tree chooses a feature threshold by comparing how mixed the target labels or values are before and after a split. **Tree split impurity** is that local comparison, not the model's final generalization score.

## Grounded explanation

For classification, Gini impurity sums the chance of drawing different labels from the node's empirical [[probability-distribution]]; entropy is another uncertainty criterion. A split is attractive when the sample-weighted impurity of its children is lower than that of the parent. For regression, squared-error criteria measure within-child target dispersion instead. The impurity choice is related to, but not identical with, the eventual task [[loss-function]] and evaluation metric.

A perfectly pure leaf can be an overfit leaf supported by one observation. Check minimum leaf size, class imbalance, missing-value behavior, and validation performance. Compare candidate criteria using the same train/validation split and tree complexity controls. Report held-out discrimination or error and calibration where relevant rather than claiming that lower training impurity proves a better classifier.

## Prerequisites

- [[probability-distribution]]
- [[loss-function]]

## Sources

- [scikit-learn decision trees](https://scikit-learn.org/stable/modules/tree.html): split criteria and overfitting controls.
