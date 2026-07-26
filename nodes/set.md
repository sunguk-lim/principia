---
id: set
title: Set (membership)
summary: A collection of distinct elements with membership — "is x in S?" answered yes/no — taken as primitive; unordered, no duplicates.
type: axiom
tags: [math/set-theory]
prereqs: []
sources: []
status: explained
created: 2026-06-29
updated: 2026-06-29
---

# Set (membership)

## Axiom

A **set** is a collection of **distinct** elements, taken as primitive. Two
operations are assumed and explained no further:

- **membership** — for any element `x` and set `S`, the question "is `x` in `S`?"
  has a definite yes/no answer (written `x ∈ S` or `x ∉ S`);
- **distinctness** — an element is either in a set once or not at all; a set
  never holds the "same" element twice (so `{a, b}` and `{a, b, b}` denote the
  same set).

A set is **unordered**: `{a, b}` and `{b, a}` are the same set — membership is
the only thing it records, not position or count. To decide membership you must
be able to tell whether two elements are *the same one*; that notion of element
**equality** is assumed along with membership. The elements may themselves be
anything, including ordered pairs `(k, v)` — a key–value mapping is exactly a
set of such pairs whose first components are all distinct.

## Why stop here

Going deeper means the axioms of set theory (ZFC — extensionality, pairing,
union, the membership relation `∈` itself) — foundations no data-structure or
backend concept in this brain needs to invoke. For our purposes "a collection of
distinct things you can test for membership" is the agreed floor: sets and
membership are assumed, just as `arithmetic` assumes numbers and their four
operations. (`set` is the *mathematical* floor; the runtime `hash-set` data
structure that realizes it fast is a separate, much higher node.)
