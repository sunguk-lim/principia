---
id: determinant
title: Determinant
summary: The determinant is a signed scale factor for oriented volume under a square linear transformation and is zero exactly when the transformation collapses dimension.
type: concept
tags: [math/linear-algebra]
prereqs: [linear-transformation, matrix-multiplication, arithmetic, linear-independence]
sources: [https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Determinant

## Summary

For a square matrix $A$, the **determinant** $\det(A)$ is the signed factor by which its [[linear-transformation]] scales oriented volume.

## Grounded explanation

For a $2\times2$ matrix,

$$A=\begin{bmatrix}a&b\\c&d\end{bmatrix},\qquad \det(A)=ad-bc.$$

If $A=\begin{bmatrix}2&0\\0&3\end{bmatrix}$, a unit square maps to a rectangle of area $6$, so $\det(A)=6$. Swapping the two coordinate directions reverses orientation and changes the sign. A negative determinant therefore does not mean negative physical area; its magnitude is the volume scale and its sign records orientation.

If $\det(A)=0$, the transformed basis vectors are linearly dependent and a full-dimensional region collapses into lower dimension. Thus a square matrix is invertible exactly when its determinant is nonzero.

Composition multiplies scale factors:

$$\det(AB)=\det(A)\det(B).$$

This mirrors composition by [[matrix-multiplication]]. Determinants are not defined as a single scalar for arbitrary rectangular matrices, and computing them is not the preferred numerical test for solving a large linear system. Factorizations and condition estimates are usually more informative computationally.

Validate formulas on identity, diagonal, triangular, row-swapped, and singular matrices. Check geometric magnitude separately from orientation, and compare symbolic small cases with a trusted factorization-based implementation.

## Prerequisites

- [[linear-transformation]]
- [[matrix-multiplication]]
- [[arithmetic]]
- [[linear-independence]]

## Sources

- [MIT OpenCourseWare 18.06 Linear Algebra readings](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/): assigns determinant properties, formulas, applications, and linear transformations in Strang's course sequence.
