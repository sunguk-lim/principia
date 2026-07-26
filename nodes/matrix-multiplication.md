---
id: matrix-multiplication
title: Matrix multiplication
summary: Combining an m×k matrix A with a k×n matrix B into an m×n matrix C, where each entry C[i][j] is the sum of the products of row i of A with column j of B.
type: concept
tags: [math/linear-algebra]
prereqs: [arithmetic, vector-dot-product]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Matrix multiplication

## Summary

Combining an `m×k` matrix A with a `k×n` matrix B into an `m×n` matrix C, where
each entry `C[i][j]` is the sum of the products of row `i` of A with column `j`
of B.

## Grounded explanation

Each output entry is `C[i][j] = A[i][1]·B[1][j] + … + A[i][k]·B[k][j]` — a chain
of multiplications and additions, i.e. pure [[arithmetic]]. That same per-entry
pattern (row × column, summed) is exactly the [[vector-dot-product]] of a row and
a column; that node is on the frontier, so here we rely only on [[arithmetic]]
and treat the dot-product framing as a deferred refinement.

## Prerequisites

- [[arithmetic]]
- [[vector-dot-product]]

## Sources

_none_
