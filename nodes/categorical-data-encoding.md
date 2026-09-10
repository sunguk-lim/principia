---
id: categorical-data-encoding
title: Categorical Data Encoding
summary: Categorical data encoding maps discrete labels into numeric feature representations while preserving the training-serving mapping and controlling dimensionality, ordering assumptions, and label leakage.
type: concept
tags: [ml/feature-engineering]
prereqs: [tensor, temporal-data-leakage]
sources: [https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-categorical-features]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Categorical Data Encoding

## Summary

**Categorical data encoding** turns a discrete value such as `bronze`, `silver`, or `gold` into a numeric [[tensor]] that a model can consume. The representation is part of the model contract: it must be fitted on training data and applied identically at inference.

## Grounded explanation

For a feature with $k$ known categories, one-hot encoding assigns a separate coordinate to each category. `silver` might become $[0,1,0]$. This does not imply that silver lies numerically between bronze and gold, but it can create many sparse coordinates when cardinality is large. An ordinal encoding instead maps categories to integers. It is appropriate only when the order itself is meaningful and the downstream model can use that meaning; assigning arbitrary IDs to unordered cities or product names introduces a false numeric relation.

An encoder is fitted on the training partition, which fixes its vocabulary, category order, and handling of unseen values. Fitting it before a split lets held-out categories influence the representation and is a form of [[temporal-data-leakage]] when the split simulates a decision in time. At serving time, unknown categories need an explicit policy such as an all-zero one-hot vector, a reserved unknown category, or a deterministic hashing scheme. Silently changing the policy changes the input schema seen by the trained model.

Target encoding replaces a category with a statistic estimated from labels, such as a category's mean training outcome. It can compact a high-cardinality feature, but it is especially leakage-prone: using an example's own label to encode that example makes validation overly optimistic. Estimate the statistic on each training fold and apply it only to that fold's held-out rows; smoothing toward the global statistic reduces variance for rare categories.

Choose the encoding with the model and data distribution in mind. One-hot encoding is a robust default for modest-cardinality unordered fields. Ordinal encoding suits genuinely ordered fields. Target or hashing encodings trade interpretability for compactness or open-vocabulary handling. Validate the whole fitted preprocessing pipeline on held-out data, including missing and previously unseen categories, rather than evaluating a model against a representation built with future information.

## Prerequisites

- [[tensor]]
- [[temporal-data-leakage]]

## Sources

- [scikit-learn, “Preprocessing categorical features”](https://scikit-learn.org/stable/modules/preprocessing.html#preprocessing-categorical-features): documents ordinal, one-hot, and target encoders, including unknown-category handling and cross-fitting for target encoding.
