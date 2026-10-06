# Principal Component Analysis

## Meaning

Principal component analysis (PCA) makes a lower-dimensional linear representation of data. It finds directions along which centered observations vary most, then projects onto a chosen number of those directions. It is a compression or exploration method, not a guarantee of better prediction.

## Mechanism

Arrange observations as rows of a matrix, subtract each feature's training-set mean, and find orthogonal directions ordered by retained variance. If $W_k$ contains the first $k$ directions, the projected coordinates are $Z=XW_k$, a [[matrix-multiplication]]. Choosing a smaller $k$ discards more information but makes the representation cheaper to store or inspect. Fit the transformation on training data; applying a transform fitted on all data can leak validation information.

Feature units matter. A column measured in thousands may dominate one measured in tenths, so standardize when domain meaning calls for it. Individual component signs are arbitrary, and nearly equal leading variances can make component directions unstable while the subspace remains similar. A two-dimensional scatterplot can hide important task information even when explained variance looks high.

## One example

Suppose points form a narrow diagonal cloud in two dimensions. One principal direction along the cloud retains most geometric spread. But if labels differ only across the narrow width, dropping the second direction damages classification despite excellent variance retention.

## Check your understanding

**Question:** Does retaining 95% of variance prove that PCA kept 95% of the information useful for a label?

**Answer:** No. Variance is unsupervised spread; the label signal may live in a low-variance direction. Test the downstream task against a no-PCA baseline.
