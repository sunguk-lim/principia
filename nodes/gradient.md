---
id: gradient
title: Gradient
summary: The gradient collects the partial derivatives of a multi-input function into a vector that points in the direction of steepest increase.
type: concept
tags: [math/calculus]
prereqs: [derivative, partial-derivative]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-24
---

# Gradient

## Summary

The **gradient** collects the partial derivatives of a multi-input function into a
vector that points in the direction of steepest increase.

## Grounded explanation

For a function $f(\theta_1,\dots,\theta_n)$ of many parameters,

$$\nabla f = \left(\frac{\partial f}{\partial \theta_1},\dots,\frac{\partial f}{\partial \theta_n}\right)$$

where each entry is a [[partial-derivative]] of $f$ — a [[derivative]] taken with
respect to one input while holding the rest fixed. The vector points uphill, so $-\nabla f$ points toward the steepest
*decrease* — the direction gradient-descent steps in to reduce a loss.

## Prerequisites

- [[partial-derivative]]
- [[derivative]]

## Sources

_none_
