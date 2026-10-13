---
id: inference-context-parallelism
title: Inference Context Parallelism
summary: Inference context parallelism partitions one request's token dimension across devices, with different prefill-compute and decode-KV objectives.
type: concept
tags: [ml/llm/inference]
prereqs: [prefill-vs-decode, context-parallelism, kv-cache, tensor-parallelism]
sources: [https://docs.vllm.ai/en/stable/serving/context_parallel_deployment/]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Inference Context Parallelism

## Summary

**Inference context parallelism** distributes the token dimension of one serving request across devices. Unlike a data-parallel replica, the devices cooperate on one long context. Prefill and decode use the partition for different reasons and require different communication.

## Grounded explanation

[[context-parallelism]] explains sequence sharding for training. During inference, [[prefill-vs-decode]] changes the objective. A long prefill has many new query tokens: split those queries across devices to reduce time to first token. If the entire key/value set fits on each device, a system can gather it and compute each query shard locally; if it does not, attention must stream key/value blocks, as in ring attention. The vLLM documentation describes both prefill approaches as under development, so do not infer production support from the design alone.

During decode, there are few new queries but a large retained [[kv-cache]]. Sharding the cache along the token axis can reduce per-device cache pressure and duplication, allowing more resident contexts. [[tensor-parallelism]] may first split KV heads; when head count is small relative to tensor-parallel degree, head-sharding alone can duplicate cache. Token-axis sharding adds a communication cost to combine partial attention results. More devices do not automatically improve token latency.

Choose prefill and decode layouts from measured bottlenecks. Compare time to first token, inter-token latency, throughput, cache occupancy, network traffic, and output equivalence under the same model and request distribution. The right partition depends on model head structure, hardware topology, context lengths, and concurrency; a newsletter's fixed strategy is not a universal deployment rule.

## Prerequisites

- [[prefill-vs-decode]]
- [[context-parallelism]]
- [[kv-cache]]
- [[tensor-parallelism]]

## Sources

- [vLLM, Context Parallel Deployment](https://docs.vllm.ai/en/stable/serving/context_parallel_deployment/): distinguishes long-prefill query sharding from decode KV-cache token sharding and their communication trade-offs.
