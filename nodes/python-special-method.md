---
id: python-special-method
title: Python Special Method
summary: A Python special method is a conventionally named method that Python's language syntax and built-in operations invoke to customize an object's behavior, such as calling, indexing, iteration, arithmetic, or representation.
type: concept
tags: [languages/python]
prereqs: [dynamic-typing]
sources: [https://docs.python.org/3/reference/datamodel.html#special-method-names]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Special Method

## Summary

Python special methods—often called *dunder methods*—let a class participate in language operations by defining names such as `__len__`, `__iter__`, `__getitem__`, or `__add__`.

## Grounded explanation

Python syntax is connected to protocol methods. For example, `len(x)` can invoke `type(x).__len__(x)`, `for item in x` uses the iteration protocol, and `x[key]` uses the subscription protocol. A class therefore need not inherit from one common interface to support an operation: it can provide the methods the operation requires. This is an application of [[dynamic-typing]].

The lookup rules matter. Python generally looks up special methods on the type rather than by ordinary instance attribute lookup, so setting `instance.__len__` does not reliably alter what `len(instance)` does. Define the method on the class instead. That choice lets implementations optimize and makes the operation's behavior consistent across instances.

Implement only the protocols the type can honor. `__repr__` should aid debugging; `__str__` should provide a readable representation; `__eq__` and `__hash__` must respect their consistency contract when instances are used as keys. A class that merely adds many special methods without a coherent value or container model becomes harder to reason about. Test the actual syntax or built-in operation, not just a direct call to the method.

## Prerequisites

- [[dynamic-typing]]

## Sources

- [Python data model: special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names): invocation through language operations, naming conventions, lookup behavior, and protocol-specific contracts.
