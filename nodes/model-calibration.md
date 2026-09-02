---
id: model-calibration
title: Model Calibration
summary: Model calibration is agreement between a predictive probability and the empirical outcome frequency among cases receiving that probability.
type: concept
tags: [ml/deep-learning]
prereqs: [conditional-probability]
sources: [https://scikit-learn.org/stable/modules/calibration.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Model Calibration

## Summary

A probabilistic model is **calibrated** when cases assigned probability $p$ experience the event about a fraction $p$ of the time. Calibration tests whether a score can be interpreted as a probability, separately from whether the model ranks positive cases above negative ones.

## Grounded explanation

Let $S$ be a model score between $0$ and $1$, and let $Y=1$ mean the predicted event occurs. Perfect calibration means

$$P(Y=1\mid S=p)=p$$

for every score value $p$ that the model emits. This is a [[conditional-probability]] statement: among cases whose score is $p$, the positive-event frequency must equal $p$.

Because an exact score may occur rarely, a reliability diagram groups nearby scores into bins. For each bin it plots the average predicted probability against the observed positive fraction. Points on the diagonal are calibrated; a point below the diagonal is overconfident, and a point above it is underconfident.

### Worked example

Suppose ten independent loan applications each receive a default probability near $0.8$, with average score $0.80$. If eight actually default, the observed fraction is $8/10=0.80$, so that bin is calibrated. If only five default, its point is $(0.80,0.50)$: the predictions are overconfident by $0.30$ in that bin.

Calibration does not imply accuracy or discrimination. A model that predicts the base rate $0.20$ for every case can be calibrated when 20% default, yet it cannot rank risky cases. Conversely, a model may rank cases perfectly but emit scores such as $0.99$ where only 80% are positive.

A calibrator learns a mapping from raw model scores to estimated event frequencies using data not used to fit the original model. Keeping that data separate matters: fitting on training predictions sees unusually optimistic scores and can produce an optimistic mapping. Validation should report the reliability curve and the number of examples in each bin, since an apparently large gap from a nearly empty bin is uncertain.

## Prerequisites

- [[conditional-probability]]

## Sources

- scikit-learn User Guide, “Probability calibration” — calibration identity, reliability diagrams, and held-out calibration.
