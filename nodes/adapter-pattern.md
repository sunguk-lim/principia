---
id: adapter-pattern
title: Adapter Pattern
summary: An adapter translates one existing interface into the contract expected by a client without changing either side.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance, abstract-base-class]
sources: [https://python-patterns.guide/gang-of-four/composition-over-inheritance/]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Adapter Pattern

## Summary

An **adapter** makes an existing object usable by a client that expects a different interface. It translates calls and results at one boundary; it does not change the underlying object's behavior.

## Grounded explanation

Suppose an exporter expects `write(text)` but a legacy service exposes `send(payload, encoding)`. An adapter stores the service and implements `write(text)` by encoding and forwarding the payload. This uses [[composition-over-inheritance]]: the exporter depends on the small expected contract, while the adapter owns translation. An [[abstract-base-class]] can document or check that contract in Python, though a structural protocol or ordinary duck typing may suffice.

An adapter is justified when the source API cannot or should not be changed and the translation is stable. If every caller has to understand the source service's exceptions or special state anyway, the boundary is leaky. If the mismatch is only one call site, a small function may be clearer than a named class. Do not confuse an adapter with a decorator: the adapter changes the interface; the decorator preserves it while adding behavior.

Test both normal values and semantic mismatches: encoding, timeouts, error mapping, and ownership of closing the source object. A passing type check alone does not prove that translated operations have the meaning the client expects.

## Prerequisites

- [[composition-over-inheritance]]
- [[abstract-base-class]]

## Sources

- [Python Patterns Guide, Adapter section](https://python-patterns.guide/gang-of-four/composition-over-inheritance/#solution-1-the-adapter-pattern): shows interface adaptation as an object-composition alternative.
