---
id: telemetry-signal
title: Telemetry Signal
summary: A telemetry signal is an emitted system output that carries either discrete events or measurements so activity inside an application can be inspected from outside; traces, metrics, and logs are complementary signal forms.
type: concept
tags: [observability/fundamentals]
prereqs: [event, measurement]
sources: [https://opentelemetry.io/docs/concepts/signals/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Telemetry Signal

## Summary

A **telemetry signal** is an output a running system emits so an observer can
learn about activity that would otherwise remain internal. Its payload is built
from a discrete [[event]], a numeric [[measurement]], or a combination of both.

## Grounded explanation

Signals provide different views of the same execution. A point-in-time record
answers “what happened?”; a series of values answers “how much, and how is it
changing?”; a correlated path answers “which operations led here?” OpenTelemetry
names the dominant forms logs, metrics, and traces. They are not interchangeable:
each deliberately preserves different information.

Suppose a checkout request begins at 10:00:00, calls an inventory service, and
finishes 230 ms later. One signal may carry an [[event]] saying “inventory lookup
failed” at 10:00:00.180. Another may carry the [[measurement]] “checkout duration
= 230 ms.” A third may preserve the two operations and their parent-child
relationship. Together they reveal the occurrence, the quantity, and the causal
path.

The word *telemetry* emphasizes transport from the observed system toward an
observer. Producing a signal is not the same as storing or visualizing it: the
application can emit the data, an intermediate component can process it, and a
separate backend can retain and query it. That separation lets one application
produce standard signals without being coupled to one analysis vendor.

## Prerequisites

- [[event]]
- [[measurement]]

## Sources

- https://opentelemetry.io/docs/concepts/signals/
