---
id: linear-transformation
title: Linear Transformation
summary: A linear transformation preserves vector addition and scalar multiplication, and a matrix represents such a map after bases are chosen.
type: concept
tags: [math/linear-algebra]
prereqs: [matrix-multiplication, arithmetic]
sources: [https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Linear Transformation

## Summary

A map $T$ is a **linear transformation** when it preserves addition and scalar multiplication:

$$T(u+v)=T(u)+T(v),\qquad T(cu)=cT(u).$$

## Grounded explanation

After choosing coordinate bases, a finite-dimensional linear map is represented by a matrix $A$ and acts as $T(x)=Ax$. The columns of $A$ are the output coordinates of the input basis vectors. This is why knowing a linear map on a basis determines it everywhere.

For

$$A=\begin{bmatrix}2&0\\0&1\end{bmatrix},$$

the map doubles the first coordinate and leaves the second unchanged. A unit square becomes a rectangle of area two. For a rotation matrix, lengths and area magnitude are preserved even though coordinates change.

Composing maps corresponds to [[matrix-multiplication]]. If $T_A(x)=Ax$ and $T_B(x)=Bx$, then applying $B$ first and $A$ second gives $T_A(T_B(x))=(AB)x$. The order therefore matters.

Animation can build intuition by showing basis vectors, a grid, and intermediate states, but an arbitrary interpolation between two matrices need not preserve properties such as invertibility or rotation. Validate a claimed linear map with the two defining identities, check dimensions, and test basis vectors and combinations.

## Prerequisites

- [[matrix-multiplication]]
- [[arithmetic]]

## Sources

- [MIT OpenCourseWare 18.06 Linear Algebra readings](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/): assigns matrix operations, determinants, and linear transformations in Strang's course sequence.
