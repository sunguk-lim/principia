---
id: abstract-factory-pattern
title: Abstract Factory Pattern
summary: An abstract factory groups creation operations for related products behind one replaceable family contract.
type: concept
tags: [languages/python]
prereqs: [factory-method-pattern]
sources: [https://python-patterns.guide/gang-of-four/abstract-factory/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Abstract Factory Pattern

## Summary

An abstract factory groups creation operations for related products behind one replaceable family contract.

## Grounded explanation

An **abstract factory** supplies a *family* of related products without clients naming their concrete classes. A rendering factory might create both a button and a dialog for one UI theme; swapping the factory changes both consistently. This differs from [[factory-method-pattern]], which delegates one creation choice to an overrideable method within a workflow.

In Python, a small object containing callables, or simply passing factories directly, often expresses the same contract with less class machinery. Use the named pattern when several products must vary together and the invariant that they are compatible matters. A collection of unrelated constructors is not automatically an abstract factory.

Test that every factory variant creates a compatible family, that the client never branches on concrete product types, and that failure to construct one product is handled coherently.

## Prerequisites

- [[factory-method-pattern]]

## Sources

- [Python Patterns Guide, Abstract Factory Pattern](https://python-patterns.guide/gang-of-four/abstract-factory/): author-maintained discussion of the mechanism and Python-specific trade-offs.
