---
id: observability
title: Observability
summary: Observability is the ability to infer a running system's internal state from the telemetry signals it emits, using complementary outputs to answer new questions without adding a special probe for every possible failure.
type: concept
tags: [observability/fundamentals]
prereqs: [telemetry-signal]
sources: [https://opentelemetry.io/docs/what-is-opentelemetry/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Observability

## Summary

**Observability** is the ability to understand a running system's internal state
from its externally available [[telemetry-signal]] outputs. It is not merely
having data; the signals must let an operator form and test explanations for
behavior that was not fully predicted in advance.

## Grounded explanation

Monitoring often begins with a known question: alert when checkout failures
exceed a threshold. Observability becomes important when the question is unknown:
why did only mobile users in one region become slow after a deployment? Useful
signals preserve enough dimensions, timing, and correlation to narrow such a
new question without first changing the program and waiting for the failure to
happen again.

Suppose the outside symptom is a jump from 200 ms to 1.8 s. One
[[telemetry-signal]] view shows the increase began at 10:03; another reveals that
slow requests share `region=seoul`; another shows those requests waiting inside
one downstream operation. The internal hypothesis—one regional dependency is
slow—is inferred from outputs. No single signal carries the whole explanation;
their complementary preserved information does.

Observability is therefore a system capability, not a product name or dashboard.
Tools can collect, store, and visualize evidence, but the system must first emit
useful signals with consistent identity and context. More data alone does not
guarantee observability: noisy, uncorrelated outputs can make inference harder.

## Prerequisites

- [[telemetry-signal]]

## Sources

- https://opentelemetry.io/docs/what-is-opentelemetry/
