---
id: hessian
title: Hessian (H)
summary: The Hessian is the matrix of second partial derivatives of a scalar function — the Jacobian of its gradient.
type: concept
tags: [math/calculus]
prereqs: [jacobian, gradient, partial-derivative]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-25
---

# Hessian (H)

## Summary

The **Hessian** is the matrix of second partial derivatives of a scalar function —
the Jacobian of its gradient. Input: scalar → output: matrix.

## Grounded explanation

It is the [[jacobian]] of the [[gradient]] $\nabla f$:

$$H_{ij} = \frac{\partial^2 f}{\partial x_i\, \partial x_j}$$

Each entry is a second [[partial-derivative]] — differentiate $f$ once with respect to $x_j$, then again with respect to $x_i$.

It describes the local curvature of $f$ — the second-order information that the first differential (the linear approximation) cannot see. It is used in second-order optimization, e.g. Newton's method. It is **symmetric** — mixed partials commute — so its mirror cells are equal, which is also why the curl of a gradient vanishes.

## Prerequisites

- [[jacobian]]
- [[gradient]]
- [[partial-derivative]]
## Sources

- etc/differential-operators-summary.html
