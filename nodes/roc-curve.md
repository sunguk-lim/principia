---
id: roc-curve
title: ROC Curve
summary: A receiver operating characteristic curve shows the trade-off between true-positive rate and false-positive rate as a binary classifier's decision threshold changes.
type: concept
tags: [ml/evaluation]
prereqs: [confusion-matrix]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# ROC Curve

## Summary

A **receiver operating characteristic (ROC) curve** plots a binary classifier's true-positive rate against its false-positive rate as the score threshold changes. It evaluates score ranking across thresholds; it does not choose the threshold or tell you whether predicted probabilities are calibrated.

## Grounded explanation

For every candidate threshold, classify examples at or above the threshold as positive and form a [[confusion-matrix]]. The true-positive rate is $TP/(TP+FN)$ and the false-positive rate is $FP/(FP+TN)$. Moving the threshold downward normally labels more examples positive, increasing both rates. Plotting the resulting pairs traces the ROC curve from $(0,0)$ to $(1,1)$.

**Worked instance.** With two actual positives and two actual negatives, suppose a model scores them $0.8, 0.4, 0.35, 0.1$, respectively ordered as positive, positive, negative, negative. At threshold $0.8$, the classifier identifies one positive and no negatives: $(FPR,TPR)=(0,0.5)$. At $0.4$, it identifies both positives and no negatives: $(0,1)$. At $0.35$, it also includes one negative: $(0.5,1)$. The threshold must be selected from the operational cost of false positives and false negatives, not from the curve alone.

The area under the curve (ROC-AUC) summarizes how well scores rank positives above negatives across possible thresholds. It can compare score functions when a threshold is not fixed, but it can hide poor precision in a rare-positive problem and does not establish calibration or expected deployment utility. Report the curve together with a threshold-specific confusion matrix and, when positives are rare, precision-recall behavior and the real error costs.

## Prerequisites

- [[confusion-matrix]]

## Sources

- [scikit-learn `roc_curve`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html): specifies binary labels, prediction scores, thresholds, false-positive rate, and true-positive rate.
- [scikit-learn `roc_auc_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html): specifies ROC-AUC from prediction scores and its supported classification settings.
