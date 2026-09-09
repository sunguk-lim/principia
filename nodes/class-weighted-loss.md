---
id: class-weighted-loss
title: Class-Weighted Loss
summary: Class weighting changes the relative penalty of training examples and can change the probability represented by a model score.
type: concept
tags: [ml/deep-learning]
prereqs: [loss-function, derivative, model-calibration, precision-recall]
sources: [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression, https://arxiv.org/abs/1708.02002]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Class-Weighted Loss

## Summary

A class weight multiplies the penalty attached to examples of that class. This can make rare positive errors matter more, but it changes the training objective; it is not a guarantee of calibrated probabilities or useful production alerts.

## Grounded explanation

Start from the logarithmic [[loss-function]] for binary outcomes. For a fixed input, define:

| Symbol | Type and meaning |
|---|---|
| $y$ | Binary observed label, 0 or 1 |
| $p$ | Scalar true positive probability at this input |
| $q$ | Scalar predicted score, strictly between 0 and 1 |
| $a,b$ | Positive scalar weights for positive and negative labels |

The weighted loss is

$$\ell(q,y)=-ay\log q-b(1-y)\log(1-q).$$

### Independent derivation: what score is learned?

Across repeated outcomes at that input, the population objective is

$$L(q)=-ap\log q-b(1-p)\log(1-q).$$

Its [[derivative]] is $-ap/q+b(1-p)/(1-q)$. Setting it to zero and collecting terms gives

$$q^*=\frac{ap}{ap+b(1-p)}.$$

With positive weights and an interior probability, the second derivative is positive, so this stationary point minimizes the objective. This is the unconstrained population optimum, not a promise about a finite trained model.

Take $p=0.01$, $a=99$, and $b=1$. Then $ap=0.99$ and $b(1-p)=0.99$, giving $q^*=0.5$. A score of 0.5 can therefore correspond to only 1% positives. Calling it a 50% probability would violate [[model-calibration]]. Under precisely these weighting assumptions, the inverse relationship is

$$p=\frac{bq}{a(1-q)+bq}.$$

This inverse does not correct arbitrary data shifts or model errors. Resampling and weighting together can compound changes to the effective class balance; account for both.

### Weighting is a choice, not an automatic mistake

Use weights to express a justified training objective and compare with unweighted learning. Select the deployed threshold separately using [[precision-recall]] and operational costs. Evaluate on data with representative class proportions, rather than assuming a balanced test sample predicts alert volume.

Focal loss adds a confidence-dependent factor to reduce easy examples' influence. The original paper demonstrates it for dense object detection; it does not establish that class weighting always fails or that focal loss is universally superior for rare fraud. Hard examples may also include mislabeled cases. Compare alternatives at fixed data and training budgets and check calibration as well as task performance.

## Sources

- [scikit-learn linear models](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression): weighted logistic objectives.
- [Lin et al., Focal Loss for Dense Object Detection](https://arxiv.org/abs/1708.02002): confidence-dependent loss modulation and its original evaluation setting.
