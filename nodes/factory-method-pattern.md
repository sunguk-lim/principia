---
id: factory-method-pattern
title: Factory Method Pattern
summary: A factory method delegates the choice of which concrete object to construct to an overrideable method while callers depend on a stable interface.
type: concept
tags: [languages/python]
prereqs: [object-oriented-inheritance, abstract-base-class]
sources: [https://python-patterns.guide/gang-of-four/factory-method/, https://docs.python.org/3/library/abc.html]
status: explained
created: 2026-10-12
updated: 2026-10-12
---

# Factory Method Pattern

## Summary

The **factory method pattern** leaves object creation to an overrideable method. A base workflow calls that method and uses the returned object through a common contract; a subclass chooses the concrete implementation. This separates construction choice from the workflow that consumes the object.

## Grounded explanation

Suppose a report-export workflow needs a writer. The base workflow calls `make_writer()` and then calls `write()` on the result. A CSV subclass returns a CSV writer; a JSON subclass returns a JSON writer. Python's [[object-oriented-inheritance]] supplies the override mechanism. An [[abstract-base-class]] can express the required creation method or writer interface, but Python also allows duck-typed implementations.

The essential distinction is **where the choice lives**. A standalone function `make_writer(format)` that switches on a string is a simple factory, not the subclass-overridden factory method. The pattern is useful when the workflow stays stable while product selection varies by subclass. It costs an extra inheritance structure and may be unnecessary when a constructor argument, mapping of callables, or dependency injection is clearer.

## Validation

Add a new concrete writer without editing the base workflow and test that the workflow calls only the common contract. Test unsupported products and construction failures. If each new writer still requires changing a central switch, the proposed design has not actually delegated product choice.

## Prerequisites

- [[object-oriented-inheritance]]
- [[abstract-base-class]]

## Sources

- [Python Patterns Guide, Factory Method](https://python-patterns.guide/gang-of-four/factory-method/)
- [Python `abc` documentation](https://docs.python.org/3/library/abc.html)
