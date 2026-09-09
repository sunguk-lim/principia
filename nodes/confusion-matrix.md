---
id: confusion-matrix
title: Confusion Matrix
summary: A confusion matrix counts examples by true class and predicted class, exposing which classes a classifier confuses rather than collapsing performance to one scalar.
type: concept
tags: [ml/evaluation]
prereqs: [set, measurement]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Confusion Matrix

## Summary

A **confusion matrix** cross-tabulates true labels and predicted labels. With a fixed class order, entry $C_{ij}$ counts examples whose true class is $i$ and predicted class is $j$.

## Grounded explanation

For a [[set]] of classes $\{0,\ldots,K-1\}$,

$$C_{ij}=\sum_n \mathbf 1[y_n=i\ \text{and}\ \hat y_n=j].$$

Rows therefore condition on truth and columns on prediction under this convention. Some tools transpose that convention, so always label axes explicitly.

For binary classes ordered negative then positive,

$$C=\begin{bmatrix}TN&FP\\FN&TP\end{bmatrix}.$$

“True” means the prediction is correct; “positive” or “negative” names the predicted class. Thus a false negative is actually positive but predicted negative, while a false positive is actually negative but predicted positive.

Raw counts preserve prevalence and sample size. Row normalization estimates the distribution of predictions given each true class; column normalization estimates the distribution of true classes given each prediction. Normalizing the whole table gives population proportions. These are different [[measurement]]s and should not be interchanged.

A matrix depends on the evaluated dataset, class mapping, decision threshold, and weighting. It does not express probability calibration, ranking quality before thresholding, or the relative cost of errors. Report counts and relevant normalized views by deployment slice, then derive threshold-dependent rates with their denominators visible.

## Prerequisites

- [[set]]
- [[measurement]]

## Sources

- [scikit-learn, `confusion_matrix`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html): defines $C_{ij}$ by true and predicted class and identifies the binary TN, FP, FN, and TP cells.
