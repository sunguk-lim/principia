---
id: mean-squared-error
title: Mean Squared Error
summary: Mean squared error averages squared prediction residuals, penalizing large errors disproportionately and retaining squared target units.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function]
sources: [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html]
status: explained
created: 2026-11-02
updated: 2026-11-02
---

# Mean Squared Error

## Meaning

Mean squared error is a regression [[loss-function]] that squares each prediction's difference from its target and averages the results. Squaring prevents positive and negative errors from canceling and makes large errors more influential than small ones.

## Mechanism

Let N be a positive number of examples, y_i the numeric target for example i, and p_i its prediction in the same units. The residual is p_i-y_i. Mean squared error is the sum of (p_i-y_i)² over all examples, divided by N. It is nonnegative and equals zero exactly when every included prediction matches its target. Its units are the square of the target unit. The square root returns the original unit, but it is not the mean absolute error.

Weights and multiple outputs require an explicit aggregation rule. If weights are used, normalize by their sum rather than silently treating them as unweighted counts. Averaging different output dimensions without regard to scale can let the largest-unit dimension dominate. A metric evaluated on held-out predictions is distinct from a model's complete training objective, which may include additional penalties.

## Worked example

Three targets are 2, 4 and 8; predictions are 3, 2 and 11. Residuals are 1, -2 and 3, whose squares are 1, 4 and 9. Their mean is 14/3, approximately 4.667 squared target units. The signed residual mean is 2/3, a different quantity that partly cancels errors. If the final prediction changes from 11 to 14, its residual doubles from 3 to 6 and its contribution quadruples from 9 to 36; total mean squared error becomes 41/3, approximately 13.667.

## Boundaries and validation

The large-error emphasis may match an application's costs or make the metric vulnerable to corrupt extreme labels. Check residual slices and compare alternatives appropriate to the actual error penalty. MSE is not intrinsically restricted to linear regression and does not establish that one model family dominates another. Compare identical targets, units, sample weights and output aggregation on data not used for fitting. A small average can still hide an important subgroup failure.

## Prerequisites

- [[loss-function]]

## Sources

- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html>
