---
id: laplacian
title: Laplacian (∇²f)
summary: The Laplacian is the divergence of the gradient — the sum of the second partials.
type: concept
tags: [math/calculus]
prereqs: [divergence, gradient]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Laplacian (∇²f)

## Summary

The **Laplacian** is the divergence of the gradient — the sum of the second
partials. Input: scalar → output: scalar.

## Grounded explanation

Take the [[gradient]] of $f$, then its [[divergence]]:

$$\nabla^2 f = \nabla \cdot (\nabla f) = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}$$

Equivalently $\nabla \cdot \nabla$ — "del dotted with del." It measures how much a
point's value differs from the average of its neighbors, which is why it governs
diffusion, heat flow, and smoothing.

## Prerequisites

- [[divergence]]
- [[gradient]]

## Figure

![The Laplacian is ∇·∇ — the dot product of del with itself: the sum of second partials, equivalently the divergence of the gradient](laplacian.svg)

## Sources

- etc/differential-operators-summary.html
