---
id: multi-model-inference-residency
title: Multi-Model Inference Residency
summary: Multi-model inference residency decides which model weights remain loaded on a finite GPU and when to load or evict them, balancing memory, cold-start latency, contention, and isolation.
type: concept
tags: [ml/llm/inference]
prereqs: [llm-inference-memory-budget, queue, load-balancing]
sources: [https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html, https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html]
status: explained
created: 2026-09-30
updated: 2026-10-24
---

# Multi-Model Inference Residency

## Summary

A GPU may serve several models whose combined weights and active-request memory do not all fit at once. **Multi-model inference residency** controls which models are loaded, when a request waits for a load, and which resident model is evicted when space is needed. It is a capacity and scheduling problem, not simply a model-routing API.

## Grounded explanation

For each model, account for loaded weights and runtime state plus request-dependent KV cache and workspace using an [[llm-inference-memory-budget]]. A model that fits alone may not fit alongside another model at peak concurrency. Sharing a server can reduce duplicated process overhead and place several request queues under one coordinator, but it also creates a shared failure domain and contention for memory and compute.

Consider two hot models A and B and a rarely used C. Keeping A and B resident avoids their repeated load latency; admitting C may require evicting one. A least-recently-used policy is easy to implement but can thrash if requests alternate among models larger than available capacity. Frequency estimates, pinned high-priority models, admission limits, and per-model memory reservations can help, at the cost of reduced flexibility. An independent-instance design isolates model lifecycles but may duplicate runtime allocations and require an external [[load-balancing]] router.

Separate the [[queue]] time from model load, prefill, and decode. A warm request behind another model's long run can be slower than a cold request on an idle dedicated endpoint. Report cold-start and warm p50/p95 latency, throughput, active models, load/eviction count, peak memory, OOMs, failures, and total cost under the same hardware, model versions, traffic mix, and quality. Benchmark concurrent as well as sequential requests; compare a shared resident pool with separate processes and an always-loaded baseline. A comparison that includes loading for only one side does not isolate serving-engine speed.

Triton's documented explicit load/unload control illustrates the mechanism, but it does not imply every serving engine implements the same eviction policy. Verify the target engine's model control, isolation, batching, and memory accounting before extrapolating.

## Compute-aware shared-device admission

Residency and execution admission are separate decisions. Two models may both fit in memory while their simultaneous work exceeds a latency target or temporary-workspace allowance. Keep separate per-model queues and batch only requests with compatible model, shapes, and execution contracts. Sharing one server does not turn an embedder and generator into one ordinary tensor batch with shared weights. Triton's architecture documentation illustrates per-model schedulers and configurable batching rather than one universal mixed-model batch.

A device coordinator can estimate the compute time and peak workspace of proposed per-model batches, then admit a compatible set within memory and service constraints. For a toy serialized 10 ms work window, estimated batches A and B costing 6 ms and 7 ms cannot both meet that window merely because both models are resident. The scheduler might run A now and B next, or reduce batch sizes; that introduces a fairness and waiting-time trade-off. If execution can overlap, summing estimates is not a calibrated model of interference: profile the actual pair and update the admission policy.

Benchmark model mixes, cold loads, eviction churn, competing workspaces, bursts, cancellation and starvation. Report per-model tail latency and useful throughput alongside aggregate throughput; a busy accelerator can still miss the important model's deadline. Compare with isolated instances and a simpler serialized policy under the same hardware, quality and demand. Model-load success and a failure-free finite request trace do not establish safe admission at arbitrary concurrency.

## Prerequisites

- [[llm-inference-memory-budget]]
- [[queue]]
- [[load-balancing]]

## Sources

- [NVIDIA Triton Inference Server model management](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_management.html): model-control modes and explicit load/unload semantics.

- <https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/architecture.html>
