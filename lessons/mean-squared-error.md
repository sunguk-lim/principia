# Mean Squared Error

## Meaning

Mean squared error averages the square of each numeric prediction error. It is useful when large deviations should count disproportionately and when positive and negative deviations must not cancel. It is a loss or evaluation metric, not a particular regression algorithm.

## Mechanism

For each example, subtract its target from its prediction to obtain a residual. Square that residual, sum the squared values and divide by the number of examples. The result cannot be negative. It is zero only if all included residuals are zero. Because the errors are squared, the output has squared target units; if the targets are meters, MSE is measured in square meters.

State the averaging rule. Weighted examples require a declared normalization, and multiple output dimensions can be returned separately or combined using explicit weights. Outputs on different scales should not be casually averaged. A model can also train with MSE plus a separate complexity penalty, so the entire training objective need not equal the reported held-out metric.

## One example

Targets are 2, 4 and 8. Predictions are 3, 2 and 11. The residuals are 1, -2 and 3. Their squares are 1, 4 and 9, which sum to 14. Dividing by three gives MSE approximately 4.667. The negative error did not cancel the positive errors.

If the last prediction becomes 14, its residual becomes 6 instead of 3. Its squared contribution rises from 9 to 36, four times larger. The new MSE is (1+4+36)/3, approximately 13.667. This illustrates why a few extreme errors can dominate the result.

## Check your understanding

Does low average MSE prove every subgroup is served well? **No.** Inspect residual slices, units and label quality. Choose the error penalty that matches the task, and compare models on the same held-out targets and aggregation rule.
