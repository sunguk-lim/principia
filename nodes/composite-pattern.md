---
id: composite-pattern
title: Composite Pattern
summary: A composite gives individual objects and containers a common operation so clients can traverse a hierarchy uniformly.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance]
sources: [https://python-patterns.guide/gang-of-four/composite/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Composite Pattern

## Summary

A composite gives individual objects and containers a common operation so clients can traverse a hierarchy uniformly.

## Grounded explanation

A **composite** represents a part-whole tree through a common operation on leaves and containers. A file and a directory can both answer a size query; the directory delegates to its children and combines their answers. [[composition-over-inheritance]] lets a container hold components rather than inherit all their implementation.

The common interface does not mean every operation is meaningful on both leaves and groups. Mutation, ownership, cycles, and error propagation need explicit contracts. Python duck typing can be enough; a formal base class is useful when the shared behavior needs runtime enforcement or documentation.

Test nested trees, empty containers, repeated references, cycles if permitted, and failures in a child. If a client still branches on leaf versus container for the core operation, the abstraction may not be doing useful work.

## Prerequisites

- [[composition-over-inheritance]]

## Sources

- [Python Patterns Guide, Composite Pattern](https://python-patterns.guide/gang-of-four/composite/): author-maintained discussion of the mechanism and Python-specific trade-offs.
