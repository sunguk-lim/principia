---
id: partial-derivative
title: Partial derivative
summary: A partial derivative measures how a multi-input function changes as one input moves, holding the others fixed.
type: concept
tags: [math/calculus]
prereqs: [derivative]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Partial derivative

## Summary

A **partial derivative** measures how a multi-input function changes as **one**
input moves, holding the others fixed.

## Grounded explanation

It is just a [[derivative]] taken with respect to one variable while the rest are
treated as constants:

$$\frac{\partial f}{\partial x_i} = \lim_{h\to 0}\frac{f(\dots,x_i+h,\dots)-f(\dots,x_i,\dots)}{h}$$

Stacking all of them is how the del-operator, the gradient, the
jacobian and the hessian are built.

## Prerequisites

- [[derivative]]

## Sources

- etc/differential-operators-summary.html
