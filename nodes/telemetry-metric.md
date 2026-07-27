---
id: telemetry-metric
title: Telemetry Metric
summary: A telemetry metric is a named series or aggregation of runtime measurements over time, using instruments such as counters, gauges, and histograms to summarize system behavior efficiently rather than retain every individual occurrence.
type: concept
tags: [observability/signals]
prereqs: [measurement]
sources: [https://opentelemetry.io/docs/concepts/signals/metrics/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Telemetry Metric

## Summary

A **telemetry metric** turns repeated runtime [[measurement]] values into a named
time series or aggregation. It answers quantitative questions such as “how many
requests completed?”, “how much memory is used now?”, and “how are request
durations distributed?”

## Grounded explanation

Three common instrument shapes preserve different facts. A counter accumulates
nondecreasing totals, such as 412 completed requests. A gauge reports a current
value, such as 7 active requests. A histogram groups many observations into
buckets, preserving a distribution summary without retaining every request.

Take four request-duration [[measurement]] values: 80, 120, 230, and 900 ms.
With buckets `≤100`, `≤250`, and `>250`, the histogram counts are 1, 2, and 1.
It can also retain count 4 and sum 1330 ms. The mean is therefore 332.5 ms, but
the buckets reveal something the mean hides: one request was much slower than
the other three.

Metrics trade detail for bounded cost. Recording each request as a distinct
history grows with traffic; updating a counter or fixed set of histogram buckets
keeps storage and query work compact. Attributes such as `method=POST` can split
one metric into series, but each unique attribute combination consumes state, so
unbounded identifiers such as user IDs create dangerous cardinality.

## Prerequisites

- [[measurement]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/metrics/
