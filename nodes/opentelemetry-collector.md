---
id: opentelemetry-collector
title: OpenTelemetry Collector
summary: The OpenTelemetry Collector is a vendor-neutral telemetry pipeline service whose receivers ingest signals, ordered processors batch, filter, enrich, or transform them, and exporters send the results to one or more observability backends.
type: concept
tags: [observability/collection]
prereqs: [telemetry-signal]
sources: [https://opentelemetry.io/docs/collector/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# OpenTelemetry Collector

## Summary

The **OpenTelemetry Collector** is a vendor-neutral service that receives,
processes, and exports [[telemetry-signal]] data. It separates applications from
backend-specific protocols and operational concerns such as batching, retries,
filtering, and redaction.

## Grounded explanation

A Collector pipeline has three ordered roles. A **receiver** accepts incoming
data, for example OTLP over HTTP. Zero or more **processors** transform the data
in order—batch records, drop unwanted attributes, add environment metadata, or
sample. An **exporter** sends the result to a destination. One Collector can run
separate pipelines for traces, metrics, and logs while sharing components.

Suppose three services each emit 100 [[telemetry-signal]] items per second.
Without a Collector, every service needs backend credentials, retry logic, and a
vendor exporter. With a Collector, all three send to one local OTLP endpoint. A
batch processor groups 300 one-second arrivals into fewer network requests, an
attribute processor removes `customer.email`, and two exporters copy the clean
data to a production backend and an archive. The applications know neither
destination.

The Collector can run beside each application as an agent, as a shared gateway,
or in both layers. An agent offloads data quickly and can attach local resource
information; a gateway centralizes routing and policy. It is not the storage or
visualization backend: if every exporter is unavailable beyond its buffering and
retry capacity, data can still be lost. Its defining job is the controllable
receive → process → export boundary.

## Prerequisites

- [[telemetry-signal]]

## Sources

- https://opentelemetry.io/docs/collector/
