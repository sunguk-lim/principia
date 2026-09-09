---
id: matrix-multiplication
title: Matrix Multiplication
summary: Matrix multiplication composes compatible linear arrays by taking each output entry as a row–column dot product; order matters even though grouping does not.
type: concept
tags: [math/linear-algebra]
prereqs: [arithmetic, vector-dot-product]
sources: [https://mathworld.wolfram.com/MatrixMultiplication.html]
status: explained
created: 2026-06-18
updated: 2026-09-10
---

# Matrix Multiplication

## Summary

If $A$ has shape $m\times k$ and $B$ has shape $k\times n$, their product $C=AB$ has shape $m\times n$ with

$$C_{ij}=\sum_{r=1}^{k}A_{ir}B_{rj}.$$

Each entry is the [[vector-dot-product]] of row $i$ of $A$ and column $j$ of $B$.

## Grounded explanation

For

$$A=\begin{bmatrix}1&2\\3&4\end{bmatrix},\qquad B=\begin{bmatrix}5&6\\7&8\end{bmatrix},$$

the upper-left entry is $1\cdot5+2\cdot7=19$, and

$$AB=\begin{bmatrix}19&22\\43&50\end{bmatrix}.$$

The inner dimensions must match because every row–column dot product needs the same number of terms. The outer dimensions determine the output shape.

Matrix multiplication represents composition when matrices encode linear maps: in $ABx$, $B$ acts on $x$ first and $A$ acts second. This explains three important properties:

- **Associative:** $(AB)C=A(BC)$ when dimensions are compatible, so grouping can change computation cost without changing the result.
- **Distributive:** $A(B+C)=AB+AC$ and $(A+B)C=AC+BC$.
- **Usually noncommutative:** $AB$ and $BA$ may differ or one may not even be defined.

Matrix multiplication is not elementwise multiplication. Libraries often expose both operations with different syntax, so tests should verify shapes and one hand-calculated entry. For long chains, compare parenthesizations because multiplying smaller intermediate shapes can require far fewer scalar operations.

## Prerequisites

- [[arithmetic]]
- [[vector-dot-product]]

## Sources

- [Wolfram MathWorld, “Matrix Multiplication”](https://mathworld.wolfram.com/MatrixMultiplication.html): defines compatible dimensions and row–column products and records associativity, distributivity, and noncommutativity.
