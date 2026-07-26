---
id: divergence
title: Divergence (∇·F)
summary: Divergence turns a vector-field into a scalar measuring the net outflow at each point.
type: concept
tags: [math/calculus]
prereqs: [del-operator, vector-dot-product, vector-field, differential, jacobian]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-24
---

# Divergence (∇·F)

## Summary

**Divergence** turns a [[vector-field]] into a scalar measuring the net outflow at
each point. Input: vector field → output: scalar.

## Grounded explanation

It is the [[vector-dot-product]] of the [[del-operator]] with the field:

$$\nabla \cdot F = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z}$$

— the sum of the *diagonal* partials; each $\partial F_i/\partial x_i$ is one entry from the [[differential]] of the corresponding field component (the trace of the [[jacobian]] of F). Positive
divergence means the field is spreading out (a source); negative means it is
converging (a sink).

## Prerequisites

- [[del-operator]]
- [[vector-dot-product]]
- [[vector-field]]
- [[differential]]
- [[jacobian]]

## Sources

- etc/differential-operators-summary.html
