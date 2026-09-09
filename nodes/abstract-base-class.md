---
id: abstract-base-class
title: Abstract Base Class
summary: A Python abstract base class declares an interface and can prevent instantiation until required abstract members are implemented, while also supporting virtual subclass checks.
type: concept
tags: [languages/python]
prereqs: [object-oriented-inheritance, python-descriptor, static-type-checking]
sources: [https://docs.python.org/3/library/abc.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Abstract Base Class

## Summary

An **abstract base class** (ABC) defines a nominal runtime interface. Python's `abc` module prevents instantiation of a class using `ABCMeta` until all required abstract methods and properties have concrete overrides.

## Grounded explanation

A class derives from `ABC` and marks requirements with `@abstractmethod`. Abstract methods may still contain an implementation that subclasses call through `super()`. When abstract properties, class methods, or static methods combine decorators, `abstractmethod` must be the innermost decorator so the descriptor exposes its abstract status correctly through the [[python-descriptor]] protocol.

Direct subclasses participate in ordinary [[object-oriented-inheritance]] and method resolution. `ABCMeta.register()` can instead mark an unrelated class as a virtual subclass: `isinstance` and `issubclass` recognize it, but the ABC is absent from the class's method resolution order and contributes no implementations through `super()`. A `__subclasshook__` can define structural recognition for a specific interface.

ABCs provide runtime nominal checks and instantiation constraints; they are not the same as [[static-type-checking]]. Static protocols can describe structural behavior without runtime registration, and composition may be simpler when implementations need shared collaborators rather than subtype identity.

Use an ABC when downstream code needs a stable interface, runtime subtype checks are meaningful, and shared default behavior belongs to the contract. Avoid marker hierarchies with no useful invariant. Test that incomplete concrete subclasses cannot instantiate, complete ones satisfy behavior rather than merely method names, virtual subclasses do not accidentally rely on inherited implementations, and cooperative multiple-inheritance chains remain valid.

## Prerequisites

- [[object-oriented-inheritance]]
- [[python-descriptor]]
- [[static-type-checking]]

## Sources

- [Python documentation, `abc` — Abstract Base Classes](https://docs.python.org/3/library/abc.html): specifies `ABC`, `ABCMeta`, abstract members, virtual subclasses, subclass hooks, descriptor ordering, and instantiation rules.
