---
id: distributed-tracing
title: Distributed Tracing
summary: Distributed tracing reconstructs one request's end-to-end causal path as a tree or graph of timed trace spans, using context propagation to preserve the trace and parent identifiers when execution crosses service and process boundaries.
type: concept
tags: [observability/tracing]
prereqs: [trace-span, context-propagation]
sources: [https://opentelemetry.io/docs/concepts/signals/traces/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Distributed Tracing

## Summary

**Distributed tracing** reconstructs the path of one request through many
processes as related [[trace-span]] records. [[context-propagation]] preserves the
identifiers needed to attach each remote operation to the same causal history.

## Grounded explanation

The key invariant is simple: every operation in one request keeps the same trace
ID, while every operation receives a distinct span ID and records its parent.
The result is not merely a chronological list. It is a causal tree that answers
which operation called which other operation, even when their clocks overlap.

Trace one checkout. Frontend creates root span `A` from 0–230 ms. It calls
Inventory, whose span `B` runs from 20–80 ms, then Payment, whose span `C` runs
from 90–220 ms. [[context-propagation]] carries `A`'s identity to each service,
so both remote [[trace-span]] records share trace ID `T` and name `A` as their
parent. The assembled trace is `A → {B, C}`. If Payment creates database span
`D` from 110–180 ms, the tree becomes `A → C → D` on that branch.

This structure localizes delay. The total request took 230 ms; Inventory used
60 ms, Payment used 130 ms, and Payment's database child used 70 ms. A flat log
could show all four durations but would not by itself prove their parent-child
relationships. The propagated IDs make that proof explicit and let a backend
render an end-to-end waterfall across machines.

## Prerequisites

- [[trace-span]]
- [[context-propagation]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/traces/
