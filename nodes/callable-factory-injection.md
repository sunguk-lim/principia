---
id: callable-factory-injection
title: Callable Factory Injection
summary: Callable factory injection passes an object-creation operation into a consumer so construction can vary without requiring a subclass or hard-coded concrete type.
type: concept
tags: [languages/python]
prereqs: [first-class-function]
sources: [https://python-patterns.guide/gang-of-four/abstract-factory/, https://docs.python.org/3/library/json.html#json.loads]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Callable Factory Injection

## Meaning

A callable factory is a function, class or other callable that returns an object when invoked. Injection means the consumer receives that callable rather than selecting a concrete constructor internally. It separates when an object is needed from how it is made, without forcing an inheritance hierarchy.

## Mechanism

A [[first-class-function]] can be passed, stored and invoked later. The consumer declares the factory's input and result contract, stores it and calls it where creation is needed. In Python, a class can often satisfy that contract directly because calling it constructs an instance. A configured factory can carry additional state. None of these choices makes every arbitrary callable a compatible factory.

The standard JSON loader provides a primary example: its `parse_float` argument is called with a number's string representation. Passing `Decimal` selects decimal construction without replacing the parser. An injected callable is not the same as a factory method overridden by subclasses. It is also not necessarily an abstract factory grouping a compatible family of products. Those patterns solve related but distinct construction problems.

## One example

An invented decoder sees two amount tokens, `12.30` and `0.70`. With `parse_float=Decimal`, it constructs Decimal values whose decimal sum is 13.00. Passing `int` instead violates the effective input contract because `int('12.30')` raises an error. Both are callables, but only one accepts these inputs with the desired numeric semantics. A wrapper stripping a currency symbol is useful only if the producer's token contract permits such input; ordinary JSON number tokens do not include currency symbols.

## Check your understanding

Must a consumer know the concrete returned class? Ideally it relies on the agreed operations and meaning, but tests must still verify them. Test accepted arguments, result behavior, factory exceptions and repeated creation. Decide whether each call must return a fresh object or may share one. Prefer a simple constructor parameter when that is enough; an extra abstract-factory class adds no guarantee merely by having a pattern name.

## Prerequisites

- [[first-class-function]]

## Sources

- <https://python-patterns.guide/gang-of-four/abstract-factory/>
- <https://docs.python.org/3/library/json.html#json.loads>
