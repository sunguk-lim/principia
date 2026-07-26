---
id: gather
title: Gather
summary: Gather is the collective-operation in which every process sends its chunk to the root-process, which collects them into one buffer.
type: concept
tags: [parallel-computing]
prereqs: [collective-operation, root-process]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Gather

## Summary

**Gather** is the [[collective-operation]] in which every process sends its chunk to
the [[root-process]], which **collects** them into one buffer. It is the exact
**inverse of scatter**: where scatter deals distinct chunks *out* from the root,
gather pulls distinct chunks *in* to the root. The shape is **all → one**, and as
with scatter it only moves data — nothing is combined.

![Gather: P0..P3 each hold a chunk; after the call root P0 holds the full A·B·C·D buffer](gather.svg)

## Grounded explanation

Gather is asymmetric in the [[root-process]] direction, but reversed from scatter:
here the root is the **sink**, not the source.

1. **Start state.** Every rank holds its own chunk — `P0=A, P1=B, P2=C, P3=D` in the
   figure. The root holds only its own piece so far.
2. **The operation.** Every rank calls gather naming the same root. Each one *sends*
   its chunk to the root; the root *receives* all of them and lays them out **in rank
   order** — chunk from rank `i` goes to slot `i` of the result buffer. That ordering
   is why the collected `A B C D` is meaningful and not a jumble.
3. **End state.** Only the root holds the assembled buffer (`P0 = A B C D`); the other
   ranks are unchanged. The pieces were *collected*, not copied and not summed.

As a [[collective-operation]] it is point-to-point sends converging on the root, one
per source. Keep the family straight: **scatter** = root deals chunks *out* (one → all);
**gather** = root collects chunks *in* (all → one). If instead of *collecting* the
chunks the root *combined* them into a single value, that would be **reduce**.

## Prerequisites

- [[collective-operation]]
- [[root-process]]

## Sources

_none_
