---
id: context-propagation
title: Context Propagation
summary: Context propagation preserves causal identity across process boundaries by injecting selected telemetry-context fields into an outgoing carrier such as HTTP headers and extracting them into the receiver's local context.
type: concept
tags: [observability/tracing]
prereqs: [telemetry-context, http]
sources: [https://opentelemetry.io/docs/concepts/context-propagation/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Context Propagation

## Summary

**Context propagation** moves correlation identity across a process or service
boundary. A sender serializes selected fields from its [[telemetry-context]] into
a transport carrier; a receiver extracts those fields and derives its own local
context before doing work.

## Grounded explanation

The carrier is whatever the transport can convey alongside the message. For
[[http]], it is normally request headers. OpenTelemetry's default W3C Trace
Context representation uses a `traceparent` header containing a version, trace
ID, parent span ID, and flags. Injection writes the current identifiers into that
header; extraction reads and validates them at the receiving boundary.

Suppose the Frontend service has trace ID `7fa1` and current span ID `a10c` when
it calls Inventory. It sends a simplified header
`traceparent: 00-7fa1-a10c-01`. Inventory extracts the trace ID and remote parent,
then starts a local span with a new ID `b205`. The resulting relationship is
trace `7fa1`, parent `a10c`, child `b205`. Without propagation, Inventory would
invent a new trace ID and the two halves of one user request would look unrelated.

Propagation is usually performed by instrumentation at outgoing and incoming
boundaries, not by business logic. It must also treat incoming context as
untrusted: malformed identifiers are ignored, and sensitive baggage should not
be forwarded to external services. The mechanism preserves correlation, not
authorization; a trace header grants no access rights.

## Prerequisites

- [[telemetry-context]]
- [[http]]

## Sources

- https://opentelemetry.io/docs/concepts/context-propagation/
