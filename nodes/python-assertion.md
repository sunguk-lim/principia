---
id: python-assertion
title: Python Assertion
summary: Python’s `assert` statement conditionally raises `AssertionError` for internal invariants, and the interpreter can omit it under optimization.
type: concept
tags: [languages/python]
prereqs: [interpreter]
sources: [https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Python Assertion

## Summary

A **Python assertion** uses `assert condition` to state an internal condition that should hold while a program is being developed or tested.

## Grounded explanation

The [[interpreter]] evaluates the condition. When it is false, `assert condition, message` behaves like raising `AssertionError(message)`; without a message, it raises `AssertionError`. This makes an assertion useful for checking an invariant after a local computation, such as a parser consuming all of an input it claims to handle.

An assertion is not input validation or ordinary error handling. Python’s optimization mode can remove assertion statements, so externally supplied data, security checks, and required runtime behavior must use explicit conditionals and a deliberate exception instead. A caller must not rely on an asserted check to run.

A good assertion names a property controlled by the code at that point and fails close to the defect: an index is within a computed bound, a state transition preserves a representation invariant, or two independently computed values agree. Keep the condition side-effect free, because its evaluation may be omitted. Test the surrounding behavior with assertions enabled and disabled when correctness depends on the distinction.

## Prerequisites

- [[interpreter]]

## Sources

- [Python Language Reference, “The assert statement”](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement): specifies `assert` expansion and its omission when optimization is requested.
