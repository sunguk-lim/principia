---
id: linear-least-squares
title: Linear Least Squares
summary: Linear least squares chooses coefficients that minimize the squared Euclidean residual of a linear system, with rank and conditioning determining uniqueness and numerical reliability.
type: concept
tags: [math/linear-algebra]
prereqs: [matrix-multiplication, vector-dot-product, matrix-rank, linear-independence]
sources: [https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html, https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html, https://www.netlib.org/lapack/explore-html/d9/d67/group__gelsd_ga0bee7e1b9e7e43f59ecf2419b2759c42.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Linear Least Squares

## Summary

**Linear least squares** finds coefficients $x$ that minimize

$$\lVert b-Ax\rVert_2^2,$$

whether $Ax=b$ is overdetermined, underdetermined, inconsistent, or exactly solvable.

## Grounded explanation

For $A\in\mathbb R^{m\times n}$ and $b\in\mathbb R^m$, the residual is $r=b-Ax$, where $Ax$ is [[matrix-multiplication]]. Expanding the squared Euclidean norm gives $r^Tr$, a [[vector-dot-product]]. If the columns of $A$ have full [[matrix-rank]], the minimizing coefficient vector is unique. When multiple minimizers exist, NumPy's `lstsq` returns the one with the smallest coefficient norm.

If $A$ is square, full rank, and the equation is well determined, solve $Ax=b$ directly. NumPy's `solve` uses a LAPACK solver and rejects singular or nonsquare coefficient arrays. Explicitly computing $A^{-1}b$ is usually unnecessary and can add cost and numerical error.

For least squares, forming the normal equations $A^TAx=A^Tb$ squares the condition number and can magnify floating-point error. LAPACK's `DGELSD` instead computes a minimum-norm solution using a divide-and-conquer singular-value procedure. A singular-value cutoff determines effective rank, so changing it can change both the reported rank and solution; this is a modeling and numerical decision rather than harmless syntax.

The residual array alone is not proof of a good model. It may be empty for rank-deficient or underdetermined cases, and a small training residual can coexist with unstable coefficients or poor prediction. Inspect dimensions, effective rank, singular values, scaled residuals, and sensitivity to perturbations. Verify $Ax\approx b$ for exact systems, compare against analytically solvable examples, and evaluate predictive uses on held-out data.

## Prerequisites

- [[matrix-multiplication]]
- [[vector-dot-product]]
- [[matrix-rank]]
- [[linear-independence]]

## Sources

- [NumPy, `numpy.linalg.lstsq`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html): defines the minimum-residual and minimum-norm solutions, rank cutoff, residual output, rank, and singular values.
- [NumPy, `numpy.linalg.solve`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html): distinguishes full-rank square solves from least-squares problems and documents the LAPACK-based solver contract.
- [LAPACK, `DGELSD`](https://www.netlib.org/lapack/explore-html/d9/d67/group__gelsd_ga0bee7e1b9e7e43f59ecf2419b2759c42.html): specifies minimum-norm least squares through a divide-and-conquer singular-value algorithm.
