---
id: iterator-pattern
title: Iterator Pattern
summary: An iterator exposes sequential access to elements without requiring callers to know a container’s internal representation.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance]
sources: [https://python-patterns.guide/gang-of-four/iterator/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Iterator Pattern

## Summary

An iterator exposes sequential access to elements without requiring callers to know a container’s internal representation.

## Grounded explanation

An **iterator** yields elements one at a time through a stable traversal interface. In Python, `iter(container)` obtains an iterator and `next(iterator)` advances it until `StopIteration`; a `for` loop drives that protocol automatically. The container can change its internal storage without changing the consumer's loop.

A container is *iterable* if it can produce an iterator; an iterator is usually single-pass and also iterable by returning itself. Confusing those two contracts causes accidental exhaustion. Generators implement the protocol concisely, while custom iterator objects are useful when traversal state or reset rules need explicit control. [[composition-over-inheritance]] can keep traversal logic separate from container storage.

Test empty input, repeated iteration, concurrent iterators, mutation during iteration, and early termination. Document whether iteration observes a snapshot or live changes.

## Prerequisites

- [[composition-over-inheritance]]

## Sources

- [Python Patterns Guide, Iterator Pattern](https://python-patterns.guide/gang-of-four/iterator/): author-maintained discussion of the mechanism and Python-specific trade-offs.
