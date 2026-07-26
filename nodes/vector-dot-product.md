---
id: vector-dot-product
title: Vector dot product
summary: The dot product combines two equal-length vectors into a single scalar by multiplying matching entries and summing them.
type: concept
tags: [math/linear-algebra]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Vector dot product

## Summary

The **dot product** combines two equal-length vectors into a single scalar by
multiplying matching entries and summing them.

## Grounded explanation

For vectors $a, b \in \mathbb{R}^n$,

$$a \cdot b \;=\; \sum_{i=1}^{n} a_i\, b_i \;\in\; \mathbb{R}$$

— a sum of products, i.e. pure [[arithmetic]]. Geometrically it measures how much
the two vectors point the same way (it equals $\lVert a\rVert\,\lVert b\rVert\cos\theta$).
It is the atomic operation behind every entry of a matrix-multiplication:
each output entry is one row · column dot product.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
