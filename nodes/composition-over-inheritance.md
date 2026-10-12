---
id: composition-over-inheritance
title: Composition over Inheritance
summary: Object composition varies behavior by connecting collaborators at runtime instead of multiplying subclasses for every combination.
type: concept
tags: [languages/semantics]
prereqs: [object-oriented-inheritance]
sources: [https://python-patterns.guide/gang-of-four/composition-over-inheritance/]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Composition over Inheritance

## Summary

**Composition over inheritance** means building behavior by combining objects with narrow responsibilities. It is a design preference, not a ban on subclasses: choose composition when independently varying features would otherwise produce a subclass for each combination.

## Grounded explanation

Suppose a logger can send to a file or network, format as plain text or JSON, and optionally filter sensitive fields. A hierarchy that encodes every combination soon needs many classes. Instead, a logger holds a destination, formatter, and filter collaborator. It calls their methods in sequence; changing one collaborator need not change the others. With [[object-oriented-inheritance]], subclasses can still implement a stable collaborator contract, but the whole logger no longer inherits each feature combination.

Composition shifts complexity rather than eliminating it. The wiring must define who owns collaborators, their lifetime, error behavior, and whether they may be replaced. An extra interface for a single fixed implementation can be worse than one small class. Prefer inheritance when the derived object genuinely substitutes for the base contract and shared behavior is stable; prefer composition when behavior varies independently or must be configured per instance.

A useful test is to add a new formatter and destination. If each can be combined without modifying existing classes or duplicating the logger workflow, composition has isolated the axes. Also test resource cleanup and failure propagation, because a graph of collaborators can hide those contracts.

## Prerequisites

- [[object-oriented-inheritance]]

## Sources

- [Python Patterns Guide, Composition Over Inheritance](https://python-patterns.guide/gang-of-four/composition-over-inheritance/): uses logger examples to show subclass proliferation and object-composition alternatives.
