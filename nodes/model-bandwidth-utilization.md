---
id: model-bandwidth-utilization
title: "Model Bandwidth Utilization"
summary: "Model bandwidth utilization compares a declared model-byte-per-decode-iteration estimate with elapsed iteration time and hardware bandwidth, without equating modeled traffic to measured memory-controller activity."
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-vs-decode, roofline-model, measurement]
sources: [https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Model Bandwidth Utilization

## Meaning

Model bandwidth utilization (MBU) is a model-based inference-efficiency metric. Estimate bytes a decode iteration must move, divide by its elapsed time, then divide by a declared peak memory bandwidth. It asks how the observed iteration compares with an idealized byte-delivery limit; it is not automatically a hardware-counter measurement of bus utilization.

## Mechanism

Define D as modeled bytes per iteration, t as iteration duration in seconds, and B as peak bytes per second across the stated hardware boundary. Then modeled bandwidth is D/t and MBU=D/(tB). The MosaicML team's primary article uses model parameter bytes plus KV-cache bytes as a simplifying estimate. [[prefill-vs-decode]] explains why weights can be reused across a batch and why retained attention state still incurs traffic. State whether time is one batch iteration or one request's token interval; aggregate token throughput is not an interchangeable denominator.

The [[roofline-model]] supplies a lower-bound interpretation: D/B is an ideal byte-transfer time under the assumed traffic model. Actual execution includes launches, synchronization, communication and arithmetic. Cache hits, sparsity, quantization, rereads and different memory tiers can make D differ from actual memory traffic. Consequently a modeled value above 100% can reveal a mismatched byte model or boundary, not impossible hardware. Compare it with profiler counters, not as a substitute for them.

## One example

For an invented dense decode iteration, count 12 GB of weight reads and 3 GB of KV/other modeled reads, giving D=15 GB. If t=0.020 seconds and B=1,500 GB/s, modeled bandwidth is 750 GB/s and MBU=0.5, or 50%. Ideal delivery time is 15/1,500=0.010 seconds. That leaves a gap to investigate, not proof that the other 10 ms is entirely idle memory time.

## Validation and boundaries

Use representative [[measurement]] with warm-up, synchronization, batch size, context lengths, precision and device topology fixed. Report the numerator's counting rules, effective traffic counters, inter-token latency and useful throughput. Sum device peak bandwidth only when the distributed traffic estimate and iteration time use the same boundary. A higher MBU need not improve user latency or total cost.

## Check your understanding

Does a higher modeled MBU prove more measured DRAM bytes were transferred? No. It depends on an explicitly chosen traffic estimate.

## Prerequisites

- [[prefill-vs-decode]]
- [[roofline-model]]
- [[measurement]]

## Sources

- <https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices>
