---
id: flyweight-pattern
title: Flyweight Pattern
summary: A flyweight shares immutable intrinsic state among many logical objects while keeping context-specific state outside the shared object.
type: concept
tags: [languages/python]
prereqs: [hash-map]
sources: [https://python-patterns.guide/gang-of-four/flyweight/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Flyweight Pattern

## Summary

A flyweight shares immutable intrinsic state among many logical objects while keeping context-specific state outside the shared object.

## Grounded explanation

A **flyweight** reuses one object for many equal intrinsic values. A cache keyed by value, conceptually a [[hash-map]], can return a shared immutable object while callers keep per-use position or ownership outside it. Python's `sys.intern()` illustrates identity reuse for equal strings, but interning is an optimization rather than a semantic requirement for ordinary string equality.

The memory saving must exceed cache bookkeeping and lookup cost. Sharing mutable context would let one caller corrupt another, so separate intrinsic from extrinsic state. Weak references or bounded caches may be needed when the set of distinct values grows without limit.

Profile allocation count, peak memory, and lookup overhead under representative cardinality; test that changing one logical use does not mutate another.

## Prerequisites

- [[hash-map]]

## Sources

- [Python Patterns Guide, Flyweight Pattern](https://python-patterns.guide/gang-of-four/flyweight/): author-maintained discussion of the mechanism and Python-specific trade-offs.
