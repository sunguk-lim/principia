---
id: bridge-pattern
title: Bridge Pattern
summary: A bridge separates two independently varying design axes by connecting an abstraction to a replaceable implementation object.
type: concept
tags: [languages/python]
prereqs: [composition-over-inheritance]
sources: [https://python-patterns.guide/gang-of-four/composition-over-inheritance/]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Bridge Pattern

## Summary

A **bridge** separates an abstraction from an implementation axis so each can vary without a subclass for every pair. The abstraction delegates to an implementation object through a small stable contract.

## Grounded explanation

Consider notifications with urgency levels and delivery transports. If both axes use subclasses, the product of urgent/normal and email/SMS/push grows with each new option. A notification object can instead hold a transport collaborator. Urgency policy decides content and timing; transport decides delivery. This is [[composition-over-inheritance]] applied to two dimensions whose choices should not be locked together.

The bridge is more specific than generic composition: it is useful when *both* abstraction variants and implementation variants matter independently. An adapter instead accepts a pre-existing mismatched interface; a bridge is designed as the separation between the axes. In Python, passing a callable or a small object may be enough; avoid formal class hierarchies unless they clarify a real extension boundary.

Test each abstraction variant against each transport contract, including failure and retry semantics. A new transport should not require editing urgency policy, and a new urgency policy should not require implementing every transport again. If the cross-product is tiny and fixed, direct code may be simpler.

## Prerequisites

- [[composition-over-inheritance]]

## Sources

- [Python Patterns Guide, Bridge section](https://python-patterns.guide/gang-of-four/composition-over-inheritance/#solution-2-the-bridge-pattern): motivates the pattern with independently varying dimensions.
