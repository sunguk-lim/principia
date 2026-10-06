---
id: principal-component-analysis
title: Principal Component Analysis
summary: Principal component analysis finds orthogonal linear directions that retain as much of a centered dataset's variance as possible under a chosen dimension budget.
type: concept
tags: [ml/representation-learning]
prereqs: [matrix-multiplication]
sources: [https://scikit-learn.org/stable/modules/decomposition.html#pca]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Principal Component Analysis

## Summary

Principal component analysis (PCA) compresses a dataset by rotating its coordinate system, then retaining a few axes with the greatest observed spread. It is a linear transformation, useful for compression, noise exploration, or a baseline visualization. High variance is not automatically the same as task relevance.

## Grounded explanation

Let $X$ be an $n\times d$ matrix whose columns have been centered by subtracting their means. PCA chooses a unit direction $w$ maximizing the variance of $Xw$; later directions are constrained to be orthogonal to earlier ones. Equivalently, an SVD of centered $X$ yields directions ordered by singular value. The first $k$ directions form a matrix $W_k$, and the lower-dimensional coordinates are $Z=XW_k$, a [[matrix-multiplication]]. Reconstruction $ZW_k^\top$ retains only information in that subspace.

Consider points elongated mostly along a diagonal in two dimensions. Projecting onto that diagonal keeps more observed spread than projecting onto a perpendicular axis. This does not mean the diagonal predicts a label: a low-variance direction can carry the discriminating signal. Fit centering and PCA on training data only, then apply that fitted transformation to validation data; otherwise preprocessing leaks information across a split.

Scaling matters: a variable measured in thousands can dominate one measured in tenths even if it is not intrinsically more important. Decide whether standardization is appropriate for the domain before fitting. With repeated or nearly equal singular values, individual component directions may rotate or change sign while the retained subspace remains essentially the same. Thus, the newsletter's claim that PCA always yields one unique projection is too strong. Solver, numerical tolerance, missing-data handling, and streaming updates also affect reproducibility.

Choose $k$ with a reconstruction or explained-variance budget, then evaluate the downstream task separately. Compare the retained subspace, reconstruction error, training-only fit, and task metric against a no-PCA baseline. For visualization, axis directions can be interpreted through feature loadings, but a two-dimensional view still discards information. Nonlinear neighborhood visualizers answer a different question; visual cluster separation alone is not validation.

## Prerequisites

- [[matrix-multiplication]]

## Sources

- [scikit-learn, PCA user guide](https://scikit-learn.org/stable/modules/decomposition.html#pca): centering, singular-value decomposition, components, and solver considerations.
