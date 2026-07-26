---
id: collective-operation
title: Collective operation
summary: A collective operation is a single communication step that the whole group of processes participates in together — every process in the group calls it, and the operation is only…
type: concept
tags: [parallel-computing]
prereqs: [communicator, message-passing]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Collective operation

## Summary

A **collective operation** is a single communication step that the **whole group
of processes participates in together** — every process in the group calls it, and
the operation is only complete once all of them have. Instead of one process
talking to one other, data is moved and/or combined across the entire group at
once (e.g. "send this array from one process to all the others", or "sum one
number from every process"). It is the group-wide counterpart to point-to-point
[[message-passing]].

## Grounded explanation

Plain [[message-passing]] is *point-to-point*: one process names another and they
exchange a message. A collective operation lifts that from a pair to a whole
[[communicator]] — the named group of processes and their ranks. Three things
define it:

1. **All ranks call it.** Every process in the group invokes the same operation.
   A process that skips it stalls the others — the step cannot finish until the
   group is whole. (Each process is identified by a **rank**, an integer
   `0, 1, …, n-1`.)
2. **It has a shape.** The operation specifies *who contributes data* and *who
   receives the result* — one process, or all of them. This who-to-whom pattern is
   what distinguishes the different collectives (broadcast, scatter, gather,
   reduce, …), which are added next as children of this node.
3. **It may compute, not just move.** Some collectives only relocate data; others
   fold all the contributed values into one (a sum, max, …) on the way.

Under the hood there is no magic: a collective is *built out of* many ordinary
point-to-point [[message-passing]] exchanges arranged in a pattern (a chain, a
tree, a ring). The collective is the **named abstraction** over that pattern, so
the programmer writes one call instead of wiring the individual sends and
receives by hand.

`message-passing` is currently on the frontier; once it is archived, this node's
explanation closes against it down to the parallel-process floor.

## Prerequisites

- [[communicator]]
- [[message-passing]]

## Sources

_none_
