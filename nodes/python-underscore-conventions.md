---
id: python-underscore-conventions
title: Python Underscore Conventions
summary: Underscores in Python participate in identifiers and numeric literals, while specific leading and trailing forms have distinct language-defined or conventional meanings.
type: concept
tags: [languages/python]
prereqs: [namespace, interpreter]
sources: [https://docs.python.org/3/reference/lexical_analysis.html#reserved-classes-of-identifiers, https://docs.python.org/3/tutorial/classes.html#private-variables]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Python Underscore Conventions

## Summary

Python uses underscore in ordinary identifiers and numeric literals, but `_name`, `name_`, `__name`, and `__name__` do not all mean the same thing.

## Grounded explanation

- `_name` conventionally marks a non-public name. At module level, it is omitted from `from module import *` unless explicitly exported. It remains directly accessible; this is not access control.
- `name_` avoids collision with a keyword or another preferred name. It has no special runtime semantics.
- `__name` inside a class definition is transformed by name mangling to include the class name. This reduces accidental collisions in subclasses; it does not make an attribute private or inaccessible.
- `__name__` is reserved for system-defined special names such as `__iter__`; applications should not invent undocumented special-name protocols.
- `_` is an ordinary assignable identifier. Code often uses it for an intentionally ignored value, but assignment still occurs in the current [[namespace]]. Some interactive [[interpreter]] environments additionally bind `_` to a previous result; a normal script does not receive that interactive convenience by language rule.
- Numeric literals may contain underscores between digits for readability, such as `1_000_000`; the value is unchanged.

These categories mix grammar, runtime transformation, import behavior, interpreter convention, and style. Verify each claim in its relevant context rather than treating underscore as one operator. Tests should include module wildcard import, subclass name collisions, normal script execution, interactive execution, and numeric-literal parsing.

## Prerequisites

- [[namespace]]
- [[interpreter]]

## Sources

- [Python Language Reference, “Reserved classes of identifiers”](https://docs.python.org/3/reference/lexical_analysis.html#reserved-classes-of-identifiers): specifies wildcard-import handling, system names, class-private name mangling, and underscore in names and numeric literals.
- [Python Tutorial, “Private Variables”](https://docs.python.org/3/tutorial/classes.html#private-variables): explains non-public convention and the collision-avoidance purpose and limits of name mangling.
