---
id: latency-driven-inference-scaling
title: Latency-Driven Inference Scaling
summary: Latency-driven inference scaling selects ready prefill and decode capacity from workload-conditioned service measurements and explicit first-token and inter-token targets.
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-decode-disaggregation, inference-request-scheduling, measurement]
sources: [https://docs.nvidia.com/dynamo/dev/knowledge-base/modular-components/planner/planner-guide]
status: explained
created: 2026-10-31
updated: 2026-10-31
---

# Latency-Driven Inference Scaling

## Meaning

An inference scaling controller changes worker capacity to satisfy declared latency targets under a resource budget. Its target is useful ready capacity, not a GPU-utilization percentage or desired replica count. [[prefill-decode-disaggregation]] lets prompt and token-generation capacity change independently, but neither pool can complete a request alone.

## Mechanism

Use [[measurement]] of arrival rate, input/output lengths, prefix reuse, batch composition and per-iteration duration to estimate service under candidate replica counts. [[inference-request-scheduling]] couples queue delay, active sequences and cache pressure; requests per second alone therefore do not specify demand. Define time-to-first-token and inter-token objectives separately, including the percentile and measurement boundary.

A controller compares predicted or observed load with candidate capacities, selects feasible counts, requests the change, and observes readiness and resulting latency. Startup and weight-loading delays create a gap between desired and ready capacity. Forecasting can act before a burst, while reactive queue thresholds respond to current pressure. Neither guarantees a target under arbitrary demand. Dynamo's primary guide documents both threshold-oriented modes and a distinct performance-model-based SLA mode; this is not evidence that every mode profiles or predicts in the same way.

## Worked example

Suppose measurements show one prefill replica can sustain 40 requests per second for a fixed prompt mix while meeting the chosen first-token target. Arrivals rise to 90 per second. Two replicas provide a nominal 80, below demand; three provide 120 before coordination and imbalance costs. If each replica needs 20 seconds to become ready, the scale-up does not immediately deliver that capacity. Under a deliberately simplified constant-rate approximation, remaining at 80 for those 20 seconds accumulates `(90-80)*20=200` waiting requests. That backlog can violate the latency target even if three replicas are eventually sufficient.

The arithmetic is a planning illustration, not a linear scaling law. Re-measure the three-replica configuration. Longer outputs may independently saturate decode, and adding only prefill workers then leaves the generation bottleneck unchanged.

## Boundaries and validation

Use bounded count changes, readiness gates and a policy for stale metrics; measure oscillation, drain behavior, cold starts and overload. Compare fixed capacity, reactive thresholds and predictive control on the same arrival traces and hardware budget. Report latency-target attainment, rejected or timed-out work, ready GPU-seconds, queue depth and cost. Do not advertise an SLA merely because the controller accepted its configuration or proposed the desired worker count.

## Sources

- <https://docs.nvidia.com/dynamo/dev/knowledge-base/modular-components/planner/planner-guide>
