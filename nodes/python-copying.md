---
id: python-copying
title: Python Shallow and Deep Copying
summary: A shallow copy creates a new outer compound object but retains references to its contained objects, whereas a deep copy recursively copies the reachable object graph while preserving shared references and avoiding infinite recursion through a memo.
type: concept
tags: [languages/python]
prereqs: [dynamic-typing]
sources: [https://docs.python.org/3/library/copy.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Shallow and Deep Copying

## Summary

In Python, assignment binds another name to an existing object. `copy.copy()` instead creates a new outer compound object, while `copy.deepcopy()` recursively copies contained objects when an independent mutable object graph is required.

## Grounded explanation

Consider `original = [[1], [2]]`. A shallow copy creates a distinct outer list, so appending a third inner list to the copy does not alter `original`. But both outer lists still reference the same first inner list: mutating `shallow[0]` also changes `original[0]`. This is often correct and cheaper when nested values are immutable or intentionally shared.

A deep copy recursively constructs copies of contained objects, so mutating a nested mutable object in the result normally does not affect the original. It does not blindly duplicate every reference. Python's `copy` module keeps a memo of objects already copied, which both preserves sharing within the copied graph and prevents infinite recursion for cycles. Custom classes can define `__copy__` and `__deepcopy__` to specify their copying behavior, using [[dynamic-typing]] to provide that protocol.

Neither operation is a universal way to duplicate program state. Functions, modules, and several runtime resources are returned unchanged by the module, and copying a file handle, socket, lock, or external resource does not create an independent remote resource. Choose the shallow operation when sharing nested objects is part of the contract; choose a deep copy only when the required isolation and its time and memory cost are understood. Test nested mutation and cyclic graphs explicitly.

## Prerequisites

- [[dynamic-typing]]

## Sources

- [Python `copy` module documentation](https://docs.python.org/3/library/copy.html): assignment bindings, shallow versus deep copy behavior, recursion and shared-data problems, memoization, and customization hooks.
