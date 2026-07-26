---
id: all-reduce
title: All-reduce
summary: "All-reduce is reduce followed by broadcast: every process contributes a value, the values are combined into one result, and then every process — not just the root — receives that…"
type: concept
tags: [parallel-computing]
prereqs: [reduce, broadcast, reduction-operation]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-24
---

# All-reduce

## Summary

**All-reduce** is **[[reduce]] followed by [[broadcast]]**: every process contributes
a value, the values are combined into one result, and then **every** process — not
just the root — receives that result. Same combine as reduce, but the answer ends up
everywhere. It is the workhorse collective of distributed ML training, where it
averages each step's gradients across all the GPUs.

![All-reduce: P0..P3 hold 3,5,2,7; they are summed to 17 and every process ends with 17](all-reduce.svg)

## Grounded explanation

All-reduce is built from two collectives already in the brain:

1. **The reduce part.** Exactly as in [[reduce]], every rank's value is folded by the
   [[reduction-operation]] into a single result — `3 + 5 + 2 + 7 = 17` in the figure
   (here the operation is sum, but any associative op — max, min, product — works just
   as well). The
   `17` is *computed*, so it carries the amber "result" colour, not any process's data
   colour.
2. **The broadcast part.** That result is then sent to **all** ranks, exactly as in
   [[broadcast]] — so the end state is `P0 = P1 = P2 = P3 = 17`, rather than the result
   sitting only at the root.

So the difference from [[reduce]] is purely the destination: **reduce** leaves the
answer at one process; **all-reduce** leaves it at every process. (In practice it is
implemented more cleverly than literally reduce-then-broadcast — e.g. a ring
algorithm — but *as a meaning* it is exactly those two composed.)

Why it dominates ML: in data-parallel training each GPU computes a gradient from its
own batch, and all-reduce **sums (or averages) those gradients and hands the same
combined gradient back to every GPU**, so all replicas apply an identical update and
stay in sync.

## Prerequisites

- [[reduce]]
- [[broadcast]]
- [[reduction-operation]]

## Sources

_none_
