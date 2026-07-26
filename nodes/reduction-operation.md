---
id: reduction-operation
title: Reduction operation
summary: A reduction operation is a binary arithmetic operation that combines two values into one and is associative — e.g.
type: concept
tags: [parallel-computing]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Reduction operation

## Summary

A **reduction operation** is a **binary [[arithmetic]] operation that combines two
values into one and is associative** — e.g. sum, product, max, min. Because it is
associative, applying it across a whole list folds many values down to a **single**
result, and the order in which the combining is done does not change that result.
This is the `op` argument that `reduce`-style collectives take.

## Grounded explanation

Start from a single [[arithmetic]] operation `⊕` that takes two numbers and returns
one — say `+`. Two properties make it usable as a *reduction*:

1. **It folds a list to one value.** Apply `⊕` repeatedly: `a ⊕ b ⊕ c ⊕ d` collapses
   four numbers into one. So "combine everything into a single answer" is just this
   one operation used `n-1` times.
2. **Associativity means the grouping is free.** `(a ⊕ b) ⊕ (c ⊕ d)` gives the same
   result as `((a ⊕ b) ⊕ c) ⊕ d`. The combining can therefore be split up and done
   in **any grouping** — crucially, **in parallel** (a tree of partial combines)
   rather than strictly one-at-a-time. This is exactly why reductions are cheap on
   many processes: the work can be shared and the partial results merged.

Common reductions — `SUM`, `PROD`, `MAX`, `MIN` — are all just an associative
[[arithmetic]] `⊕`. (Most are also commutative, so even the left-to-right order of
operands is free.) This node is what lets a collective **compute** a result instead
of merely moving data: it supplies the `⊕` that turns "all the values" into "one
value."

This node closes against [[arithmetic]], an axiom, so nothing is left unexplained.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
