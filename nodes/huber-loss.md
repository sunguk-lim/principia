---
id: huber-loss
title: Huber Loss
summary: Huber loss is quadratic for small residuals and linear for large ones, retaining smooth optimization near zero while limiting the influence of extreme errors.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, derivative, convexity]
sources: [https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.huber.html, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Huber Loss

## Summary

**Huber loss** combines squared and absolute error. For residual $r=y-\hat y$ and threshold $\delta>0$,

$$L_\delta(r)=\begin{cases}
\frac12r^2,&|r|\le\delta,\\
\delta\left(|r|-\frac12\delta\right),&|r|>\delta.
\end{cases}$$

Small errors receive the smooth quadratic treatment of squared loss; large errors grow only linearly.

## Grounded explanation

As a [[loss-function]], Huber loss changes how strongly each residual affects fitting. Its [[derivative]] with respect to $r$ is

$$L_\delta'(r)=\begin{cases}r,&|r|\le\delta,\\ \delta\,\mathrm{sign}(r),&|r|>\delta.\end{cases}$$

Squared error has derivative $r$ everywhere, so an error of magnitude 100 contributes ten times the gradient of an error of magnitude 10. Huber clips that gradient magnitude at $\delta$, limiting one extreme observation’s leverage without discarding it.

For $\delta=2$, residuals $1$ and $5$ have losses $0.5$ and $2(5-1)=8$. Squared loss would give $0.5$ and $12.5$. Both Huber pieces meet at $|r|=2$ with the same value and slope. The derivative never decreases as $r$ increases, so the objective has [[convexity]] and is continuously differentiable at the join.

The threshold encodes a scale assumption. If target units change, a fixed $\delta$ changes meaning; standardize residuals or jointly estimate scale when appropriate. Smaller thresholds behave more like absolute error and increase robustness, while larger thresholds approach squared error and preserve more sensitivity under light-tailed noise.

Huber loss does not make arbitrary data trustworthy. High-leverage input outliers, systematic label errors, multimodal targets, and distribution shift require separate diagnosis. Select $\delta$ using training-only procedures, compare held-out residual distributions and task metrics, and report performance on both ordinary and extreme-error slices.

## Prerequisites

- [[loss-function]]
- [[derivative]]
- [[convexity]]

## Sources

- [SciPy `huber`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.huber.html): piecewise definition, convexity, and reduced influence relative to squared error.
- [scikit-learn `HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html): scaled residual threshold and robust linear-regression formulation.
