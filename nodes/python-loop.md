---
id: python-loop
title: Python Loop
summary: Python repeats a suite with while by retesting a condition or with for by consuming successive values from an iterable.
type: concept
tags: [languages/python]
prereqs: [interpreter]
sources: [https://docs.python.org/3/reference/compound_stmts.html#the-while-statement, https://docs.python.org/3/reference/compound_stmts.html#the-for-statement]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Loop

## Summary

A **Python loop** repeatedly executes a suite. `while` retests an expression before each iteration; `for` requests successive values from an iterable until it is exhausted.

## Grounded explanation

```python
while condition:
    step()
```

The [[interpreter]] evaluates `condition` before the first iteration and again after every completed iteration. The body can therefore run zero times. Correctness requires that the body or external state eventually falsify the condition unless nontermination is intentional.

```python
for item in iterable:
    consume(item)
```

Python evaluates `iterable` once, obtains an iterator, repeatedly requests its next item, assigns that item to the target, and executes the suite. Reassigning the target inside the body does not control which item the iterator supplies next.

Both forms may have an `else` suite. It runs after normal condition failure or iterator exhaustion, including zero iterations, but not when `break` exits the loop. `continue` skips the rest of the current body and proceeds with the next condition test or item.

Iteration count alone does not determine performance. Body cost, iterator work, allocation, I/O, and termination checks can dominate. Prefer direct iteration to index bookkeeping when the items themselves are needed, and use a bounded condition or explicit stopping rule when termination must be auditable.

Test empty input, one iteration, normal exhaustion, early termination, exceptions, and mutation of traversed data. For potentially unbounded loops, add observable progress and an external time, iteration, or cancellation limit where the surrounding system requires one.

## Prerequisites

- [[interpreter]]

## Sources

- [Python Language Reference, “The `while` statement”](https://docs.python.org/3/reference/compound_stmts.html#the-while-statement): repeated condition testing, `else`, `break`, and `continue` semantics.
- [Python Language Reference, “The `for` statement”](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement): iterable evaluation, iterator exhaustion, target assignment, and loop control.
