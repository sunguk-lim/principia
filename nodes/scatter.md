---
id: scatter
title: Scatter
summary: Scatter is the collective-operation in which the root-process holds an array split into one chunk per process and sends a different chunk to each.
type: concept
tags: [parallel-computing]
prereqs: [collective-operation, root-process]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Scatter

## Summary

**Scatter** is the [[collective-operation]] in which the [[root-process]] holds an
array split into one chunk per process and sends a **different** chunk to each. Like
broadcast it is **one → all** from the root, but where broadcast copies the *same*
value to everyone, scatter **distributes distinct pieces** — process `i` gets chunk
`i`, and no two processes get the same data. Still pure movement; nothing is
computed.

![Scatter: P0 holds chunks A,B,C,D; after the call P0→A, P1→B, P2→C, P3→D](scatter.svg)

## Grounded explanation

Scatter has the same asymmetric shape as broadcast — the [[root-process]] is the
sole source — but a different *who-gets-what*:

1. **Start state.** Only the root holds the data, and that data is logically an array
   of `n` chunks, one per rank. In the figure P0 holds `A B C D` (four distinct
   chunks, four colours).
2. **The operation.** Every rank calls scatter naming the same root. The root keeps
   (or receives) chunk `0`, sends chunk `1` to rank `1`, chunk `2` to rank `2`, and
   so on — the *i*-th chunk goes to the *i*-th rank. The match between chunk index
   and rank is what makes the split well-defined.
3. **End state.** Each process holds **its own, different** piece — `P0=A, P1=B,
   P2=C, P3=D`. The distinct colours (versus broadcast's single colour) are the point:
   the data was *partitioned*, not *replicated*.

As a [[collective-operation]] it is built from point-to-point sends fanning out from
the root, one per destination. The contrast to remember: **broadcast copies one value
to all; scatter deals out a different chunk to each.** (Its mirror image —
every process sending its chunk back to the root — is *gather*.)

## Prerequisites

- [[collective-operation]]
- [[root-process]]

## Sources

_none_
