---
id: matrix-rank
title: Matrix rank
summary: The rank of a matrix is the number of "genuinely independent" directions it spans — informally, how much non-redundant information the matrix carries.
type: concept
tags: [math/linear-algebra]
prereqs: [matrix-multiplication, linear-independence]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Matrix rank

## Summary

The rank of a matrix is the number of "genuinely independent" directions it
spans — informally, how much non-redundant information the matrix carries. A
matrix that is `m×n` can have rank at most `min(m, n)`.

## Grounded explanation

When we form products via [[matrix-multiplication]], some rows or columns may be
exact combinations of others and add no new direction. Rank counts the rows (or
columns) that are *not* such combinations. A precise definition needs
[[linear-independence]], which is on the frontier; until it is archived we use
the informal "number of non-redundant directions" reading, which is enough to
make sense of *low* rank below.

## Prerequisites

- [[matrix-multiplication]]
- [[linear-independence]]

## Sources

_none_
