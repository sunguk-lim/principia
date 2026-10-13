---
id: singleton-pattern
title: Singleton Pattern
summary: A singleton constrains a class or service to one instance within a defined scope, which is different from global discoverability.
type: concept
tags: [languages/python]
prereqs: [global-object-pattern]
sources: [https://python-patterns.guide/gang-of-four/singleton/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Singleton Pattern

## Summary

A singleton constrains a class or service to one instance within a defined scope, which is different from global discoverability.

## Grounded explanation

A **singleton** constrains instance creation so clients in a chosen scope receive the same object. That scope must be stated: one Python process, one application container, or one distributed deployment are different guarantees. A [[global-object-pattern]] makes one module-held object easy to reach but does not prevent another instance of its class from being constructed.

A custom `__new__` can enforce process-local identity, but initialization, thread safety, reloading, tests, and subprocesses complicate the contract. Dependency injection or a module global is often simpler when only shared access is needed. A process-local singleton cannot coordinate multiple workers; use an external service or store when uniqueness must be global.

Test repeated construction, concurrent first use, state reset between tests, and multiprocess behavior before claiming uniqueness.

## Prerequisites

- [[global-object-pattern]]

## Sources

- [Python Patterns Guide, Singleton Pattern](https://python-patterns.guide/gang-of-four/singleton/): author-maintained discussion of the mechanism and Python-specific trade-offs.
