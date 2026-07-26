---
id: all-gather
title: All-gather
summary: "All-gather is gather followed by broadcast: every process contributes its chunk, the chunks are collected into the full buffer, and then every process — not just the root —…"
type: concept
tags: [parallel-computing]
prereqs: [gather, broadcast]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# All-gather

## Summary

**All-gather** is **[[gather]] followed by [[broadcast]]**: every process contributes
its chunk, the chunks are collected into the full buffer, and then **every** process
— not just the root — receives that complete buffer. It is to [[gather]] what
all-reduce is to reduce: same collection, but the result ends up everywhere.
Crucially it only *moves* data — nothing is combined — so each chunk keeps its own
identity.

![All-gather: P0..P3 hold A,B,C,D; after the call every process holds the full A·B·C·D buffer](all-gather.svg)

## Grounded explanation

All-gather composes two collectives already in the brain:

1. **The gather part.** As in [[gather]], each rank's chunk is collected, in rank
   order, into one buffer — `A B C D` in the figure.
2. **The broadcast part.** That full buffer is then sent to **every** rank, as in
   [[broadcast]] — so the end state is `P0 = P1 = P2 = P3 = [A B C D]`, not the buffer
   sitting only at a root.

The pieces stay **distinct** — four colours, side by side — because all-gather
*collects*; it never applies a reduction-operation. That is the one difference
from all-reduce:

- **all-reduce** folds the contributed values into a single computed result (one
  amber `17`) and gives that to everyone;
- **all-gather** keeps every contributed value and gives the whole concatenated
  collection to everyone.

Both end with all ranks holding the same thing; the question is whether that thing is
*combined* (all-reduce) or *collected* (all-gather). (As with all-reduce, real
implementations use a ring rather than literal gather-then-broadcast, but the meaning
is exactly those two composed.)

## Prerequisites

- [[gather]]
- [[broadcast]]

## Sources

_none_
