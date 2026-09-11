---
id: quantile-regression
title: Quantile Regression
summary: Quantile regression estimates a chosen conditional quantile of an outcome, exposing distributional variation that a conditional-mean prediction hides.
type: concept
tags: [ml/regression]
prereqs: [loss-function]
sources: [https://doi.org/10.2307/1913643, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.QuantileRegressor.html]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Quantile Regression

## Summary

**Quantile regression** fits a prediction for a specified conditional quantile of an outcome rather than only its conditional mean. It is useful when the uncertainty or spread of the outcome changes with the inputs and a single average prediction would conceal that variation.

## Grounded explanation

An ordinary squared-error regression target makes over-predictions and under-predictions equally costly, so its optimum estimates a conditional mean. Quantile regression instead uses an asymmetric [[loss-function]] for a selected level $\tau$ between 0 and 1. For residual $r = y - \hat y$, the pinball loss is

$$
\rho_\tau(r) =
\begin{cases}
\tau r & r \ge 0, \\
(\tau - 1)r & r < 0.
\end{cases}
$$

At $\tau=0.5$, positive and negative residuals receive equal absolute-error weight, so the fitted value is a conditional median. At $\tau=0.9$, under-prediction ($r>0$) costs nine times as much per unit as over-prediction, moving the fitted prediction upward until roughly 90% of the conditional outcomes lie at or below it. The asymmetry, rather than a post-processing percentile calculation, is what makes the target a quantile.

**Worked instance.** A delivery-time model can fit $\tau=0.5$ to report a typical delivery time and $\tau=0.9$ to report a conservative planning time for the same route and conditions. If the median estimate is 30 minutes while the 90th-percentile estimate is 48 minutes, the difference represents conditional outcome spread; it does not mean that any one delivery will take exactly 48 minutes or that the model is calibrated without evaluation.

Fit each requested $\tau$ separately (or use a model that supports multiple quantiles), then evaluate whether empirical coverage on held-out data matches the requested level. Quantile curves can cross—for example, a predicted 90th percentile below a predicted median—when fitted independently. Constraining or correcting crossings may be appropriate, but it is a modeling choice with accuracy trade-offs. Quantile estimates also do not by themselves supply a full probability distribution, causal effect, or decision threshold; those require additional assumptions and validation.

## Prerequisites

- [[loss-function]]

## Sources

- Koenker and Bassett, ["Regression Quantiles"](https://doi.org/10.2307/1913643), *Econometrica* 46(1), 1978: introduces regression quantiles and their asymmetric absolute-loss formulation.
- [scikit-learn `QuantileRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.QuantileRegressor.html): documents a production implementation whose `quantile` parameter selects the conditional quantile to estimate.
