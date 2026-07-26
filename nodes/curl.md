---
id: curl
title: Curl (∇×F)
summary: Curl turns a vector-field into a vector measuring the local rotation (spin) at each point.
type: concept
tags: [math/calculus]
prereqs: [del-operator, vector-field, cross-product, jacobian]
sources: [etc/differential-operators-summary.html]
status: explained
created: 2026-06-18
updated: 2026-06-24
---

# Curl (∇×F)

## Summary

**Curl** turns a [[vector-field]] into a vector measuring the local rotation (spin) at
each point. Input: vector → output: vector.

## Grounded explanation

It is the [[cross-product]] of the [[del-operator]] with the field; each component is
a mirror-pair difference of partials:

$$\nabla \times F = \left(\frac{\partial F_z}{\partial y}-\frac{\partial F_y}{\partial z},\ \frac{\partial F_x}{\partial z}-\frac{\partial F_z}{\partial x},\ \frac{\partial F_y}{\partial x}-\frac{\partial F_x}{\partial y}\right)$$

Curl is the only one of the operators with minus signs — it captures the
*antisymmetric* part of the [[jacobian]] (the rigid-rotation component of a flow).

## Prerequisites

- [[del-operator]]
- [[vector-field]]
- [[cross-product]]
- [[jacobian]]

## Sources

- etc/differential-operators-summary.html
