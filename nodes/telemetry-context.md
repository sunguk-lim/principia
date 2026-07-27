---
id: telemetry-context
title: Telemetry Context
summary: Telemetry context is an immutable execution-scoped key-value mapping that carries correlation identifiers and baggage alongside the current operation so instrumentation can associate newly emitted signals with the right request.
type: concept
tags: [observability/tracing]
prereqs: [key-value]
sources: [https://opentelemetry.io/docs/specs/otel/context/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Telemetry Context

## Summary

**Telemetry context** is the small, execution-scoped bundle of correlation data
associated with the operation currently running. Conceptually it is an immutable
[[key-value]] mapping: keys identify fields such as a trace ID, span ID, or baggage
item, and values hold the corresponding identifiers or metadata.

## Grounded explanation

The context solves an ownership problem. Many requests can execute concurrently
inside one process, so instrumentation cannot store “the current trace ID” in one
ordinary global variable. Each execution unit instead sees its own current
context. Starting a child operation derives a new mapping from the parent rather
than mutating the parent mapping, which lets nested work restore the previous
context when it finishes.

For example, a checkout handler begins with
`{trace_id: "7fa1", span_id: "a10c"}`. When it starts a database operation, it
derives `{trace_id: "7fa1", span_id: "b205"}`. The trace ID remains stable because
both operations belong to one request; the span ID changes because the database
call is a different operation. When that call ends, the handler restores the
first mapping.

The mapping may also carry baggage—application-defined pairs such as
`tenant=shop-42`—but arbitrary baggage requires care because it can cross trust
boundaries. Context is the in-process representation; moving its selected fields
to another process is the separate job of context propagation.

## Prerequisites

- [[key-value]]

## Sources

- https://opentelemetry.io/docs/specs/otel/context/
