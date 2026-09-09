---
id: static-type-checking
title: Static Type Checking
summary: Static type checking analyzes a program against declared or inferred type constraints before execution, rejecting operations that cannot be shown type-compatible without changing runtime values.
type: concept
tags: [languages/semantics]
prereqs: [dynamic-typing]
sources: [https://docs.python.org/3/library/typing.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Static Type Checking

## Summary

**Static type checking** analyzes expressions before they run and reports code whose values cannot satisfy the operations or interfaces declared for them. It complements [[dynamic-typing]]: the checker reasons from annotations and inference, while the runtime still executes the original values and may enforce different or additional rules.

## Grounded explanation

A type is a set of values together with the operations permitted on them. A static checker assigns a type to each expression, either from an annotation or by inference, and propagates constraints through assignments and calls. If a function requires an integer, every statically visible path that calls it must provide an expression compatible with that requirement.

Consider:

```python
def add_one(value: int) -> int:
    return value + 1

count: int = 4
label: str = "four"
add_one(count)  # compatible
add_one(label)  # static error
```

The checker accepts the first call because `count` has type `int`. It rejects the second because `str` does not satisfy the parameter constraint. That report can be produced without executing either call. By contrast, under [[dynamic-typing]], Python itself attaches types to the runtime values and only rejects the invalid addition if execution reaches it.

Static success is not a proof that the whole program is correct. An unchecked boundary can provide a value that violates its annotation, a cast can suppress evidence, and many invariants—such as a number being positive—are more specific than the declared type. Python's documentation explicitly states that the runtime does not enforce function and variable annotations. Static checking therefore moves a class of interface mistakes earlier; runtime validation and tests remain responsible for external data and behavioral requirements.

## Prerequisites

- [[dynamic-typing]]

## Sources

- [Python `typing` documentation](https://docs.python.org/3/library/typing.html): annotations support static tools and are not enforced by the Python runtime.
