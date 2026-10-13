---
id: sentinel-object-pattern
title: Sentinel Object Pattern
summary: A unique sentinel distinguishes an omitted value from valid data such as None.
type: concept
tags: [languages/python]
prereqs: [hash-map]
sources: [https://python-patterns.guide/python/sentinel-object/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Sentinel Object Pattern

## Summary

A unique sentinel distinguishes an omitted value from valid data such as None.

## Grounded explanation

A **sentinel object** is a distinguished value whose identity means “not supplied” or “not found.” In Python, `None` works when it cannot be a legitimate value; otherwise `MISSING = object()` gives a unique identity. Check `value is MISSING`, not equality, because user-defined equality can be surprising.

For a [[hash-map]] lookup whose stored value may be `None`, `result = mapping.get(key, MISSING)` distinguishes an absent key from a present key mapped to `None`. A sentinel is not a substitute for an exception when absence is exceptional, and a bare `object()` may need a named wrapper or custom serialization policy when values cross process boundaries.

Test absent, present-None, falsey, and ordinary values. Document whether the sentinel is private to one module or part of a public API; avoid accidentally serializing it as user data.

## Prerequisites

- [[hash-map]]

## Sources

- [Python Patterns Guide, Sentinel Object Pattern](https://python-patterns.guide/python/sentinel-object/): author-maintained discussion of the mechanism and Python-specific trade-offs.
