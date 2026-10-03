---
id: llm-serving-metric-triangulation
title: LLM Serving Metric Triangulation
summary: LLM serving metric triangulation correlates queueing, first-token, inter-token, token-volume, and scheduler measures to localize a serving bottleneck before changing capacity or batching.
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-vs-decode, inference-request-scheduling, telemetry-metric]
sources: [https://github.com/vllm-project/vllm/blob/main/docs/usage/metrics.md]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# LLM Serving Metric Triangulation

## Summary

**LLM serving metric triangulation** compares several measurements from the same workload rather than treating GPU utilization or one latency number as a diagnosis. The phase, queue, and token mix determine which intervention might help.

## Grounded explanation

Time to first token (TTFT) spans the user's wait until the first streamed token; it may include queueing and [[prefill-vs-decode]] costs. Inter-token latency and time per output token describe the decode experience after the first token. Prompt and generation token counts describe workload mix, while request queue time and tokens per engine iteration help explain how the [[inference-request-scheduling]] layer is using capacity. In vLLM these are separately exposed metric families; confirm exact names and semantics against the version deployed.

Suppose TTFT rises with queue time while inter-token latency stays stable. Admission pressure or insufficient serving capacity is a candidate explanation. If queue time is stable but inter-token latency rises, investigate decode batch mix, memory bandwidth, KV-cache pressure, or contention instead. These patterns are hypotheses, not proofs: long prompts can raise TTFT without a queue, and changed output lengths can distort aggregate latency. Join signals by time window, model, request mix, and concurrency, then compare controlled traces.

Use [[telemetry-metric]] histograms to inspect p50 and tail latency alongside throughput, error and preemption rates, cache use, and token volume. Establish a baseline, change one scheduling or capacity parameter, and check task quality and cost as well as speed. A high GPU utilization reading alone cannot tell whether the service is meeting user latency objectives.

## Prerequisites

- [[prefill-vs-decode]]
- [[inference-request-scheduling]]
- [[telemetry-metric]]

## Sources

- [vLLM production metrics](https://github.com/vllm-project/vllm/blob/main/docs/usage/metrics.md): request-phase latency, token-volume, and engine-iteration metric families.
