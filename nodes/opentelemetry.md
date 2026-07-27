---
id: opentelemetry
title: OpenTelemetry
summary: OpenTelemetry is a vendor-neutral observability specification and toolkit that standardizes how applications are instrumented to generate correlated traces, metrics, and logs and how those signals are collected and exported without choosing the storage or visualization backend.
type: concept
tags: [observability/opentelemetry]
prereqs: [observability, telemetry-signal, observability-instrumentation, distributed-tracing, telemetry-metric, log-record, telemetry-context, context-propagation, opentelemetry-collector]
sources: [https://opentelemetry.io/docs/what-is-opentelemetry/, https://opentelemetry.io/docs/specs/otel/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# OpenTelemetry

## Summary

**OpenTelemetry** (OTel) is a vendor-neutral specification and toolkit for
producing, correlating, collecting, and exporting observability data. It
standardizes the path from [[observability-instrumentation]] to backend delivery,
but intentionally does not provide the backend that stores or visualizes data.

## Grounded explanation

The problem OTel solves is fragmentation. Without a common contract, an
application may use one vendor's tracing API, another metrics library, a separate
logging format, and backend-specific exporters. Changing backend then means
rewriting observation code. OpenTelemetry defines common APIs, language SDK
behavior, data models, semantic field names, and the OTLP transport so generation
and destination can vary independently.

The flow begins with [[observability-instrumentation]]. Manual API calls or
automatic library hooks turn application activity into [[telemetry-signal]] data.
The main views are [[distributed-tracing]] paths built from spans,
[[telemetry-metric]] aggregations, and [[log-record]] occurrences. A shared
[[telemetry-context]] identifies the current operation, while
[[context-propagation]] carries selected identifiers across service boundaries so
signals from different processes can be correlated.

Trace one checkout through Frontend and Payment. Frontend instrumentation starts
trace `T`, span `A`, records a request counter, and calls Payment. Propagation
injects `T/A` into the outgoing request. Payment extracts it, creates child span
`B`, and emits an error log if the card is declined. All records use standard
field meanings, so they can be joined: the counter reports volume, the trace
shows the 180 ms Payment path, and the log explains the decline at 140 ms.

SDK exporters can send directly to a backend, but production systems commonly
send OTLP to an [[opentelemetry-collector]]. Its receivers accept the signals,
processors batch or sanitize them, and exporters route them to one or several
backends. Replacing the backend changes Collector/exporter configuration rather
than the application's instrumentation. This is the vendor-neutrality invariant:
the producer owns standard telemetry and the destination remains replaceable.

OpenTelemetry therefore enables [[observability]] but is not itself an
observability backend. It creates and moves evidence; another system stores,
queries, alerts on, and visualizes that evidence.

## Prerequisites

- [[observability]]
- [[telemetry-signal]]
- [[observability-instrumentation]]
- [[distributed-tracing]]
- [[telemetry-metric]]
- [[log-record]]
- [[telemetry-context]]
- [[context-propagation]]
- [[opentelemetry-collector]]

## Sources

- https://opentelemetry.io/docs/what-is-opentelemetry/
- https://opentelemetry.io/docs/specs/otel/
