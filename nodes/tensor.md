---
id: tensor
title: Tensor
summary: A tensor is a rectangular multidimensional collection whose shape locates each element and whose element type determines how every stored value is encoded.
type: concept
tags: [math/linear-algebra]
prereqs: [dynamic-array, numeric-precision-formats]
sources: [https://onnx.ai/onnx/repo-docs/IR.html]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Tensor

## Summary

A **tensor** is a rectangular multidimensional collection of values. Its **shape**
gives the length of every axis, and one shared element type says how all values are
encoded. A scalar has zero axes, a vector one, a matrix two, and a tensor may have
any number.

## Grounded explanation

A [[dynamic-array]] gives two ingredients needed to understand a tensor: ordered
storage and integer indexing. A tensor extends that idea to several axes while
requiring a rectangular shape. Shape `[2, 3]`, for example, means two rows of three
elements. Index `[1, 2]` selects the second row and third column. The total element
count is the product of the axis lengths, so `[2, 3]` holds `2 × 3 = 6` values.

The other ingredient is a single element type from [[numeric-precision-formats]].
A tensor declared as `float32[2,3]` contains six values, each encoded in the same
32-bit floating-point format. Shape and element type are distinct: `float32[2,3]`
and `int8[2,3]` have the same locations but encode their values differently, while
`float32[3,2]` has the same number of values arranged along different axes.

**Worked instance.** Take values `[1, 2, 3, 4, 5, 6]` with shape `[2, 3]` and
element type `float32`. Splitting the flat values by the last axis gives rows
`[1, 2, 3]` and `[4, 5, 6]`. Therefore index `[0, 1]` is `2`, and index `[1, 2]` is
`6`. A consumer needs all three pieces—values, shape, and element type—to interpret
the bytes unambiguously.

## Prerequisites

- [[dynamic-array]]
- [[numeric-precision-formats]]

## Sources

- https://onnx.ai/onnx/repo-docs/IR.html
