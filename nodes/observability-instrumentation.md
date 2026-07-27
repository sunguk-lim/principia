---
id: observability-instrumentation
title: Observability Instrumentation
summary: Observability instrumentation is the code or runtime integration that observes application operations and emits telemetry signals, either through explicit API calls or automatic hooks around libraries and execution environments.
type: concept
tags: [observability/instrumentation]
prereqs: [telemetry-signal, observability]
sources: [https://opentelemetry.io/docs/concepts/instrumentation/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Observability Instrumentation

## Summary

**Observability instrumentation** is the code or runtime integration that watches
application activity and emits a [[telemetry-signal]]. It is the bridge between
work occurring inside a program and evidence available outside it, giving the
system [[observability]].

## Grounded explanation

Code-based instrumentation makes the bridge explicit. A checkout handler can
start an operation record, attach `cart.items=3`, record a duration, and end the
record when the handler returns. The developer chooses domain-specific points
and attributes, which yields rich evidence but requires source changes.

Zero-code instrumentation inserts equivalent hooks through an agent, runtime,
or library integration. It can wrap common boundaries such as incoming requests,
database calls, and message consumers without changing business code. This is
fast to adopt and broad in coverage, but it sees standardized library operations
more easily than application-specific meaning such as “coupon rejected.” The two
approaches can be used together.

The decisive requirement is that instrumentation preserve operation lifecycle
and context correctly. If it starts a record but never ends it, records the wrong
parent, or emits an unbounded attribute such as a unique user ID on every metric,
the resulting [[telemetry-signal]] is misleading or expensive. Instrumentation is
therefore not just “turn logging on”; it is a deliberate observation boundary.

## Prerequisites

- [[telemetry-signal]]
- [[observability]]

## Sources

- https://opentelemetry.io/docs/concepts/instrumentation/
