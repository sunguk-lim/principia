---
id: python-break-statement
title: Python Break Statement
summary: Python's break statement exits the nearest enclosing for or while loop, still running intervening finally blocks and suppressing that loop's else clause.
type: concept
tags: [languages/python]
prereqs: [python-loop]
sources: [https://docs.python.org/3/reference/simple_stmts.html#the-break-statement]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Break Statement

## Summary

Python’s **`break` statement** terminates the nearest syntactically enclosing [[python-loop]]. Execution continues after that loop, not after every enclosing loop or function.

## Grounded explanation

```python
for value in values:
    if value < 0:
        first_negative = value
        break
else:
    first_negative = None
```

The `else` suite runs only when the loop finishes without `break`. It therefore expresses “no early terminating case was found,” including an empty iterable. A `return` would leave the entire function instead, while `continue` would skip only the rest of the current iteration.

In nested loops, `break` exits only the innermost loop containing it. To leave multiple levels, restructure the search into a function and `return`, set an explicit flag, or use another control abstraction whose intent is clear.

If `break` transfers control out of a `try` statement with a `finally` clause, Python executes the `finally` clause before leaving the loop. Iterator cleanup beyond ordinary reference handling depends on the iterator or context manager; `break` is not a universal resource-release operation.

Use `break` when a loop’s stopping condition is discovered inside its body, such as finding the first match or satisfying a convergence criterion. Test empty input, a match on the first and last iterations, no match, nested control flow, and cleanup paths. Prefer a direct bounded loop condition when it states the termination rule more clearly.

## Prerequisites

- [[python-loop]]

## Sources

- [Python Language Reference, “The `break` statement”](https://docs.python.org/3/reference/simple_stmts.html#the-break-statement): nearest-loop termination, loop-`else` suppression, and `finally` execution during control transfer.
