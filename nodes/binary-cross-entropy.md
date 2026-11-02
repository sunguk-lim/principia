---
id: binary-cross-entropy
title: Binary Cross-Entropy
summary: Binary cross-entropy scores a binary probability prediction by the negative log probability assigned to the observed label.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, logarithm]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html]
status: explained
created: 2026-11-03
updated: 2026-11-03
---

# Binary Cross-Entropy

## Meaning

Binary cross-entropy is a [[loss-function]] for predictions of a binary outcome. It uses the full predicted probability rather than only the thresholded label. A confident wrong prediction receives a large penalty, whereas two correct labels can still have different losses.

## Mechanism

Let y be an observed label in {0,1}, and let p strictly between zero and one be the predicted probability of label 1. The probability assigned to the observed label is p when y=1 and 1-p when y=0. Using the natural [[logarithm]], the loss is

$$\ell(y,p)=-[y\ln p+(1-y)\ln(1-p)].$$

This is the negative log-likelihood of the binary model. Over n equally weighted examples, average their n losses. If examples have nonnegative weights, state whether the reported loss is a weighted sum or divided by total weight. These conventions change the scale and its relationship to any added penalty.

For a fixed event probability r, expected loss is -r ln p-(1-r)ln(1-p). Differentiating with respect to p gives (p-r)/(p(1-p)), whose sign is negative below r and positive above r. Thus the expected loss is minimized at p=r in the interior. This explains why truthful probabilities are preferred in the ideal population, not a guarantee that a finite fitted model is calibrated.

## Worked example

Two examples have labels [1,0] and positive-class probabilities [0.8,0.3]. The observed-label probabilities are 0.8 and 0.7. Losses are -ln(0.8), about 0.223, and -ln(0.7), about 0.357. Their mean is about 0.290. At threshold 0.5 both labels are correct. Predicting [0.6,0.4] also gets both labels right, but mean loss rises to -ln(0.6), about 0.511. Thresholded accuracy hides the changed probability quality.

## Boundaries and validation

At an impossible observed label with predicted probability zero, ideal log loss is infinite. Probability APIs clip at small positive limits; logits-based training implementations use stable formulations to avoid premature rounding to zero or one. Check class-column ordering, positive-label mapping, weights and aggregation when comparing libraries. Multilabel binary losses and mutually exclusive multiclass cross-entropy have different normalization contracts.

Class weighting can change which probability minimizes the weighted objective. A threshold and a decision cost must therefore be chosen separately from the training loss. Evaluate held-out log loss, calibration, error slices and operational decisions; neither a low training loss nor perfect accuracy on one cohort proves reliable probabilities elsewhere.

## Prerequisites

- [[loss-function]]
- [[logarithm]]

## Sources

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html>
