---
id: multi-model-inference-residency
title: Multi-Model Inference Residency
summary: Multi-model inference residency decides which model weights remain loaded on a finite GPU and when to load or evict them, balancing memory, cold-start latency, contention, and isolation.
type: concept
tags: [ml/llm/inference]
prereqs: [llm-inference-memory-budget, queue, load-balancing]
sources: [https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Multi-Model Inference Residency

## Summary

A GPU may serve several models whose combined weights and active-request memory do not all fit at once. **Multi-model inference residency** controls which models are loaded, when a request waits for a load, and which resident model is evicted when space is needed. It is a capacity and scheduling problem, not simply a model-routing API.

## Grounded explanation

For each model, account for loaded weights and runtime state plus request-dependent KV cache and workspace using an [[llm-inference-memory-budget]]. A model that fits alone may not fit alongside another model at peak concurrency. Sharing a server can reduce duplicated process overhead and place several request queues under one coordinator, but it also creates a shared failure domain and contention for memory and compute.

Consider two hot models A and B and a rarely used C. Keeping A and B resident avoids their repeated load latency; admitting C may require evicting one. A least-recently-used policy is easy to implement but can thrash if requests alternate among models larger than available capacity. Frequency estimates, pinned high-priority models, admission limits, and per-model memory reservations can help, at the cost of reduced flexibility. An independent-instance design isolates model lifecycles but may duplicate runtime allocations and require an external [[load-balancing]] router.

Separate the [[queue]] time from model load, prefill, and decode. A warm request behind another model's long run can be slower than a cold request on an idle dedicated endpoint. Report cold-start and warm p50/p95 latency, throughput, active models, load/eviction count, peak memory, OOMs, failures, and total cost under the same hardware, model versions, traffic mix, and quality. Benchmark concurrent as well as sequential requests; compare a shared resident pool with separate processes and an always-loaded baseline. A comparison that includes loading for only one side does not isolate serving-engine speed.

Triton's documented explicit load/unload control illustrates the mechanism, but it does not imply every serving engine implements the same eviction policy. Verify the target engine's model control, isolation, batching, and memory accounting before extrapolating.

## Prerequisites

- [[llm-inference-memory-budget]]
- [[queue]]
- [[load-balancing]]

## Sources

- [NVIDIA Triton Inference Server model management](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html): model-control modes and explicit load/unload semantics.
