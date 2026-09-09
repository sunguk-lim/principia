---
id: python-membership-test
title: Python Membership Test
summary: Python's `in` and `not in` operators delegate containment to an operand protocol, then fall back to iteration or indexed access when explicit containment is absent.
type: concept
tags: [languages/python]
prereqs: [interpreter, python-loop]
sources: [https://docs.python.org/3/reference/expressions.html#membership-test-operations]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Membership Test

## Summary

A **Python membership test** asks whether a value belongs to an object with `x in y`; `x not in y` negates that result.

## Grounded explanation

For user-defined collection objects, Python first calls `y.__contains__(x)`. If absent, it iterates and compares each produced value by identity or equality. If iteration is unavailable but indexed access exists, it requests non-negative indices until `IndexError`. Exceptions from these protocols propagate rather than becoming `False`.

Built-in sequences test elements, mappings test keys rather than values, and strings or bytes test substrings. The empty string is a substring of every string. These distinctions make explicit tests clearer than manually writing a [[python-loop]].

Performance follows the operand's protocol and representation. A linear sequence usually scans; hashed collections can often provide average constant-time lookup but still depend on correct hash and equality behavior and can degrade under collisions. A generator search consumes values and may not terminate for an infinite stream when the target is absent.

Custom `__contains__` should agree with the object's public meaning, return a truth-valued result, avoid surprising mutation, and document cost or I/O. Test present and absent values, empty collections, duplicates, unhashable probes where relevant, custom equality exceptions, substring boundaries, generator consumption, and `not in` as the exact logical inverse.

## Prerequisites

- [[interpreter]]
- [[python-loop]]

## Sources

- [Python Language Reference, “Membership test operations”](https://docs.python.org/3/reference/expressions.html#membership-test-operations): specifies built-in behavior and the `__contains__`, iteration, and indexed-access fallback order.
