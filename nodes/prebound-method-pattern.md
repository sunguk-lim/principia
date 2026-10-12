---
id: prebound-method-pattern
title: Prebound Method Pattern
summary: A prebound method stores a callable already paired with one receiver so later callers need supply only the remaining arguments.
type: concept
tags: [languages/python]
prereqs: [python-descriptor, first-class-function]
sources: [https://python-patterns.guide/python/prebound-methods/, https://docs.python.org/3/reference/datamodel.html#instance-methods]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Prebound Method Pattern

## Summary

A **prebound method** is a callable that has already captured the object on which it will operate. Later callers invoke it without supplying that receiver again.

## Grounded explanation

In Python, retrieving `worker.handle` from an instance creates a bound method. The [[python-descriptor]] mechanism pairs the function with `worker`; the call `callback(event)` later invokes `worker.handle(event)`. Because functions and methods are [[first-class-function]] values, the bound method can be stored in a registry, callback table, or queue. This often replaces a tiny forwarding closure or a class whose only role is to remember one object.

The pattern is useful when an API accepts a callback but the behavior naturally belongs to an existing instance. Retaining the bound method also retains a reference to its receiver, so careless long-lived registrations can keep objects alive longer than intended. Callback signatures, error propagation, and thread-safety still matter. `functools.partial` is a related way to pre-bind arguments, but it is not required for ordinary instance-method binding.

Test that the callback invokes the intended receiver and that changing or unregistering a receiver works. For event loops or registries, verify cleanup and lifetime; a callback that survives its owning object may be a memory leak rather than a convenience.

## Prerequisites

- [[python-descriptor]]
- [[first-class-function]]

## Sources

- [Python Patterns Guide, Prebound Methods](https://python-patterns.guide/python/prebound-methods/): describes callback use of methods already bound to instances.
- [Python data model, instance methods](https://docs.python.org/3/reference/datamodel.html#instance-methods): specifies how bound method objects carry a receiver and function.
