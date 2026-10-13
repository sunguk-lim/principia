---
id: builder-pattern
title: Builder Pattern
summary: A builder accumulates construction steps so a client can create a complex product without assembling every internal part.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance]
sources: [https://python-patterns.guide/gang-of-four/builder/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Builder Pattern

## Summary

A builder accumulates construction steps so a client can create a complex product without assembling every internal part.

## Grounded explanation

A **builder** accepts a sequence of construction commands and creates a complex result behind a simpler interface. For example, a report builder can accept title, sections, and figures while assembling the internal document tree. This uses [[composition-over-inheritance]] when the builder delegates parts of construction to collaborators.

The original Gang-of-Four form can run the same construction sequence against different builders to produce different representations. In Python, builders are also used for fluent convenience; that is useful but not the same requirement. If an ordinary constructor with optional parameters is clear, a separate mutable builder adds state and ordering hazards without benefit.

Test required-step validation, repeated build calls, partial failure, and whether construction order changes the result. A builder should make invalid intermediate states explicit or keep them private until the final product is validated.

## Prerequisites

- [[composition-over-inheritance]]

## Sources

- [Python Patterns Guide, Builder Pattern](https://python-patterns.guide/gang-of-four/builder/): author-maintained discussion of the mechanism and Python-specific trade-offs.
