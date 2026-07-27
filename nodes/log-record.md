---
id: log-record
title: Log Record
summary: A log record is a timestamped recording of an event whose structured form stores stable typed fields and arbitrary key-value attributes, allowing machines to filter, correlate, and analyze occurrences reliably.
type: concept
tags: [observability/signals]
prereqs: [event, key-value]
sources: [https://opentelemetry.io/docs/concepts/signals/logs/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Log Record

## Summary

A **log record** captures an [[event]] at a time. Its structured form combines
well-known fields—timestamp, severity, body, and correlation IDs—with arbitrary
[[key-value]] attributes that describe the source and occurrence.

## Grounded explanation

The difference between text and structure is a contract. The line
`ERROR checkout failed user=42` is readable, but every consumer must guess how
to parse it. A structured record can state
`{timestamp: 10:00:00.180, severity: ERROR, event: checkout.failed,
user_id: 42}`. Stable field names and types let downstream tools filter severity,
group event names, and retain numeric values without parsing prose.

Consider a payment failure inside one request. The [[event]] is “payment was
declined.” The log record adds when it happened, where it came from, severity,
and fields such as `order_id=817`. If trace and span IDs are present, the same
record can be displayed beside the operation that emitted it. The log remains a
point-in-time occurrence; correlation fields do not turn it into a duration.

Unstructured logs remain useful for humans and existing applications, so
OpenTelemetry can collect and normalize them rather than requiring every program
to adopt a new logging API. Structure becomes especially valuable at scale:
machines can reliably redact sensitive attributes, route selected records, and
join logs with other telemetry.

## Prerequisites

- [[event]]
- [[key-value]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/logs/
