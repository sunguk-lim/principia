---
id: prototype-pattern
title: Prototype Pattern
summary: A prototype creates a new object by copying a configured exemplar instead of selecting and invoking a concrete constructor.
type: concept
tags: [languages/python]
prereqs: [object-oriented-inheritance]
sources: [https://python-patterns.guide/gang-of-four/prototype/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Prototype Pattern

## Summary

A prototype creates a new object by copying a configured exemplar instead of selecting and invoking a concrete constructor.

## Grounded explanation

A **prototype** is an exemplar object used to create another object by copying. A registry can hold configured exemplars and clone the selected one on demand, avoiding a hard-coded constructor choice. The key decision is copy semantics: shallow copies share nested objects, while deep copies attempt to duplicate reachable state and can fail on resources such as locks or sockets.

Python's first-class classes and factory callables often make copying unnecessary. Prefer a factory when each new object should be initialized from parameters, and a copy only when preserving a complex configured state is the actual requirement. [[object-oriented-inheritance]] may still define a clone contract for heterogeneous prototypes, but it is not required for simple Python objects.

Test identity separation, nested mutable state, resource ownership, and whether later mutations to the exemplar leak into clones.

## Prerequisites

- [[object-oriented-inheritance]]

## Sources

- [Python Patterns Guide, Prototype Pattern](https://python-patterns.guide/gang-of-four/prototype/): author-maintained discussion of the mechanism and Python-specific trade-offs.
