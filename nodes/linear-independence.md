---
id: linear-independence
title: Linear independence
summary: A set of vectors is linearly independent when none of them can be written as a combination of the others — each adds a genuinely new direction.
type: concept
tags: [math/linear-algebra]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Linear independence

## Summary

A set of vectors is **linearly independent** when none of them can be written as
a combination of the others — each adds a genuinely new direction.

## Grounded explanation

Vectors $v_1,\dots,v_k$ are linearly independent if the only way to combine them
(scalar-multiply and add — i.e. [[arithmetic]]) to reach zero is the trivial one:

$$\sum_{i=1}^{k} c_i v_i = 0 \;\Rightarrow\; c_1 = c_2 = \dots = c_k = 0$$

If some nontrivial combination gives zero, one vector is redundant. The number of
linearly independent rows (or columns) is exactly what matrix-rank counts.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
