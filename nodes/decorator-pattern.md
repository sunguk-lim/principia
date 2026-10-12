---
id: decorator-pattern
title: Decorator Pattern
summary: A decorator wraps an object to add behavior while preserving the interface expected by its clients.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance, abstract-base-class]
sources: [https://python-patterns.guide/gang-of-four/decorator-pattern/]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Decorator Pattern

## Summary

An **object decorator** wraps another object with the same client-facing interface and adds behavior before, after, or around delegated calls. It can be stacked at runtime without making a subclass for each feature combination.

## Grounded explanation

Suppose a stream exposes `write(data)`. A counting wrapper also exposes `write(data)`, increments a counter, and forwards to the wrapped stream. A compression wrapper could be layered around either. This is [[composition-over-inheritance]]: behavior is assembled per instance. An [[abstract-base-class]] or protocol can define the common contract, but method signatures and semantics must still match.

The GoF object decorator is related to, but not identical with, Python's `@decorator` syntax for wrapping functions. Both wrap a callable interface, yet object decorators can preserve a multi-method object contract. Transparent wrapping is difficult if clients rely on identity, concrete type checks, undocumented attributes, special methods, or exact exception behavior. Forwarding every attribute automatically can leak capabilities that the wrapper meant to constrain.

Test the wrapper alone and in both stacking orders. Check that it forwards all required operations, preserves relevant return values and exceptions, and closes resources exactly once. If the client only needs one optional flag, a parameter may be clearer than several wrapper classes.

## Prerequisites

- [[composition-over-inheritance]]
- [[abstract-base-class]]

## Sources

- [Python Patterns Guide, Decorator Pattern](https://python-patterns.guide/gang-of-four/decorator-pattern/): explains wrappers and the limits of transparent delegation in Python.
