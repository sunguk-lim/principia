---
id: broadcast
title: Broadcast
summary: Broadcast is the collective-operation in which one process — the root-process — holds a piece of data and, after the call, every process in the group holds an identical copy of it.
type: concept
tags: [parallel-computing]
prereqs: [collective-operation, root-process]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Broadcast

## Summary

**Broadcast** is the [[collective-operation]] in which **one** process — the
[[root-process]] — holds a piece of data and, after the call, **every** process in
the group holds an identical copy of it. It is the simplest collective: pure
**one → all** movement, with no computation. Data flows out from a single source;
nothing is combined or changed.

![Broadcast: P0 (root) holds A; after the call every process holds a copy of A](broadcast.svg)

## Grounded explanation

A [[collective-operation]] is defined by its *shape* — who contributes data and who
receives it. Broadcast's shape is the most one-sided: **the [[root-process]] is the
sole contributor, and all ranks (including the root) are receivers.**

1. **Start state.** Only the root holds the value; the buffers on the other ranks
   are empty (or undefined). In the figure, P0 is the root and holds `A`.
2. **The operation.** Every rank in the group calls broadcast naming the same root.
   The root *sends*; the others *receive*. As a collective it is not finished until
   all ranks have participated.
3. **End state.** Each rank now holds its **own copy** of the value — consistent with
   the rule that processes never share memory, they only receive copies. The single
   colour in the figure marks one datum traced from its source to every destination.

Underneath, this is just the many point-to-point sends of a [[collective-operation]]
arranged as a fan-out from the root (in practice a tree, so the cost grows like
`log n` rather than `n`). The abstraction lets you write one call instead of wiring
each rank's receive by hand.

`root-process` is currently on the frontier; once archived, this node closes against
it and [[collective-operation]] down to the parallel-process floor.

## Prerequisites

- [[collective-operation]]
- [[root-process]]

## Sources

_none_
