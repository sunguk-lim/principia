# Bagging Variance Reduction

## Meaning

Bagging trains multiple versions of a predictor on resampled datasets, then aggregates them. It is especially useful when a learner changes substantially under small training-data changes. The goal is to stabilize prediction, not to turn repeated copies of the same error into independent evidence.

## Mechanism

Treat n observed training examples as an empirical [[probability-distribution]]. For each model, draw n example indices with replacement and fit on that resample. Some examples repeat and others are absent. Aggregate regression outputs by averaging; classification often uses a vote or averaged class probabilities, which are not identical rules. Use only training data in resampling and keep the evaluation set untouched.

For a fixed input, let M model predictions have equal [[variance]] sigma^2 and equal pairwise correlation rho over repeated training-data randomness. Expanding the variance of their average into diagonal and off-diagonal terms gives sigma^2/M + (M-1)*rho*sigma^2/M. This illustrative equal-correlation model exposes a dependence limit: increasing M removes the independent part but leaves correlated variation. It is not an assumption that every real ensemble has identical variance and correlation.

## One example

With sigma^2=9, M=3 and rho=0.5, the average variance is 9/3+(2/3)*0.5*9=6, not 3. Under these assumptions, infinitely many models approach variance 4.5 rather than zero. If rho=1, averaging retains variance 9: identical predictions gain nothing from more copies. These values describe variability at one input, not a measured classification accuracy improvement.

## Check your understanding

Does reducing variance remove bias or fix bad labels? No. Shared bias, leakage and distribution shift can remain. Compare with one tuned learner using held-out task metrics, calibration, memory and serving latency. Out-of-resample evaluation needs the same entity/time leakage discipline as other validation. Random forests add feature randomization to tree ensembles; that is a further diversity mechanism, not the definition of every bagging method.
