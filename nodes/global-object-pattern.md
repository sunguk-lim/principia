---
id: global-object-pattern
title: Global Object Pattern
summary: A module-global object supplies shared application state through Python import caching, with lifecycle and test-isolation costs.
type: concept
tags: [languages/python]
prereqs: [hash-map]
sources: [https://python-patterns.guide/python/module-globals/, https://docs.python.org/3/reference/import.html]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Global Object Pattern

## Summary

A **global object** is a single object stored in a module's namespace and imported where needed. Python's module caching makes the same module object available to ordinary imports, so clients can share the referenced object without explicitly passing it through every call.

## Grounded explanation

A module can create `metrics = Registry()` at import time. Code that imports that module can refer to the same registry through its module-level name mapping, conceptually a [[hash-map]]. That convenience hides a dependency: functions that use `metrics` now depend on process-global setup, import order, and shared mutable state. A module-global object is not automatically a safe singleton across worker processes, subinterpreters, or distributed deployments.

Global constants are simpler because they do not mutate. A mutable global registry, client, or cache needs explicit initialization, ownership, and shutdown rules. Import-time network I/O can make import failure or circular imports surprising. Tests may contaminate one another unless they reset or replace the object. Passing a dependency explicitly is usually clearer when behavior changes per request, tenant, or test.

Use a global only when process scope is genuinely the intended lifetime. Test repeated imports, test isolation, concurrent access, shutdown, and multiprocess behavior. If two workers must see the same state, a module global is insufficient; use an external shared store.

## Prerequisites

- [[hash-map]]

## Sources

- [Python Patterns Guide, Module Globals](https://python-patterns.guide/python/module-globals/): distinguishes constants, import-time setup, and mutable global objects.
- [Python import system reference](https://docs.python.org/3/reference/import.html): documents import caching and module objects.
