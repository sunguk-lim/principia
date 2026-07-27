---
id: trace-span
title: Trace Span
summary: A trace span is a timed record of one bounded operation, carrying its trace and span identifiers, parent relationship, attributes, status, and point-in-time events so it can become one node in a request's causal execution tree.
type: concept
tags: [observability/tracing]
prereqs: [event]
sources: [https://opentelemetry.io/docs/concepts/signals/traces/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Trace Span

## Summary

A **trace span** is the record of one bounded operation: it has a start, an end,
a name, and correlation identifiers. It may also contain attributes, status, and
point-in-time [[event]] records that occurred during the operation.

## Grounded explanation

A span answers “what work occupied this interval?” Consider an HTTP handler that
starts at `10:00:00.000` and ends at `10:00:00.230`. Its span duration is 230 ms.
The span may be named `POST /checkout`, carry `http.status_code=200`, and finish
with status `OK`. If a retry begins at `10:00:00.180`, that instantaneous
occurrence is an [[event]] inside the longer span rather than another duration.

Each span has its own span ID and normally shares a trace ID with related spans.
A parent span ID gives the common tree relationship. A checkout span with ID
`a10c` can have an inventory child `b205` and payment child `c309`; their time
intervals show when each operation ran, while the IDs show how they are related.
A root span has no parent.

Attributes describe the operation, events mark meaningful instants, and status
records its outcome. These fields make the span structured rather than a pair of
timestamps. A single span explains one operation; assembling spans from multiple
services into an end-to-end causal view is distributed tracing.

## Prerequisites

- [[event]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/traces/
