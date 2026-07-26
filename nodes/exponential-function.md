---
id: exponential-function
title: Exponential function
summary: The exponential function $e^{x}$ grows in proportion to its own value; it is always positive and turns addition into multiplication.
type: concept
tags: [math/calculus]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Exponential function

## Summary

The **exponential function** $e^{x}$ grows in proportion to its own value; it is
always positive and turns addition into multiplication.

## Grounded explanation

Built on [[arithmetic]] (repeated multiplication, extended to all reals):

$$e^{x} = \sum_{k=0}^{\infty} \frac{x^{k}}{k!}, \qquad e^{x} > 0 \ \text{ for all } x,
\qquad e^{x+y} = e^{x}\,e^{y}$$

Two properties matter downstream: it is **always positive** (so it can turn any
real score into a positive weight) and **monotonic** (larger input → larger
output). That is exactly what softmax needs to convert scores into
probabilities.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
