---
id: measurement
title: Measurement
summary: A measurement assigns a numeric value and unit to an observed property at a time—such as 230 milliseconds of latency—so repeated observations can be compared and combined with arithmetic.
type: concept
tags: [observability/fundamentals]
prereqs: [arithmetic]
sources: [https://opentelemetry.io/docs/concepts/signals/metrics/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Measurement

## Summary

A **measurement** turns an observed property into a number with a meaning: a
value, a unit, and the time or interval to which it applies. “230” alone is only
a number; “request duration = 230 milliseconds at 12:00:01” is a measurement.

## Grounded explanation

The value makes observations comparable. Once three requests have durations of
120 ms, 150 ms, and 230 ms, ordinary [[arithmetic]] can combine them: the count is
3, the total is 500 ms, and the mean is $500 / 3 \approx 166.7$ ms. The unit is
load-bearing because adding 120 milliseconds to 150 bytes would produce a number
with no coherent interpretation.

A measurement can describe a moment—“7 requests are active now”—or an interval—
“412 requests completed during this minute.” It does not by itself say why the
value changed. It supplies evidence that later telemetry concepts can aggregate,
correlate, and compare.

Consider a checkout service. At 10:00:00 it records CPU usage = 62 percent, active
requests = 7, and one request duration = 230 milliseconds. These are three
measurements because each attaches a numeric value to a named property and a
time. The first two describe state at an instant; the third describes the length
of a completed operation. All three can be processed because their values and
units make the observations explicit.

## Prerequisites

- [[arithmetic]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/metrics/
