---
id: cache-aware-inference-routing
title: Cache-Aware Inference Routing
summary: Cache-aware inference routing chooses an LLM-serving replica using both reusable prefix-KV residency and current load, trading saved prefill work against queueing and imbalance.
type: concept
tags: [ml/llm/inference]
prereqs: [prefix-caching, inference-request-scheduling, load-balancing]
sources: [https://llm-d.ai/docs/well-lit-paths/foundations/optimized-baseline, https://llm-d.ai/docs/well-lit-paths/foundations/precise-prefix-cache-routing]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Cache-Aware Inference Routing

## Summary

A load balancer that treats LLM replicas as interchangeable may send a repeated prompt to a replica without its cached prefix. **Cache-aware routing** estimates which replica can reuse the prefix and balances that benefit against the replica's current queue. It is a cluster-level choice, distinct from the [[inference-request-scheduling]] performed inside one server.

## Grounded explanation

[[prefix-caching]] stores KV blocks for identical token prefixes. Reuse is local to a replica unless blocks are shared or transferred. The router therefore needs an estimate of cache residency, request prefix identity, and server load. It can score a warm replica higher when saved prefill work exceeds the extra wait; when that replica is saturated, a cold replica may finish sooner despite recomputation. [[load-balancing]] is still necessary, but request count alone is a poor proxy when prompt lengths and cache states differ.

For example, two replicas serve a chat application. A returning conversation's system prompt and history are warm on A, while B has no matching blocks. Routing to A can reduce time to first token if A has headroom. If A already has a long queue, B may be preferable. The exact crossover depends on prefix length, model, batch composition, and queue dynamics. A router's cache index may lag eviction; it should tolerate stale entries and fall back safely rather than promising a hit.

A coarse scheme can use session affinity or approximate prefix scores. A finer scheme can consume cache creation and eviction events, at the cost of index traffic and operational complexity. Tiered cache offload is another mechanism: it expands the reusable working set but adds storage transfer cost. Prefill/decode disaggregation changes where KV state moves; it is related but not the same routing decision. Do not infer a universal throughput multiplier from one benchmark.

Replay repeated-prefix, unique-prefix, and mixed workloads under the same model and hardware. Compare load-only, affinity, and cache-plus-load policies. Report cache-hit and stale-index rates, queue wait, time to first token, inter-token latency, tail latency, throughput, and resource use. Include overload and eviction cases; a hit-rate improvement that worsens p95 latency is not automatically a win.

## Prerequisites

- [[prefix-caching]]
- [[inference-request-scheduling]]
- [[load-balancing]]

## Sources

- [llm-d optimized baseline](https://llm-d.ai/docs/well-lit-paths/foundations/optimized-baseline): prefix-aware and load-aware router design.
- [llm-d precise prefix cache routing](https://llm-d.ai/docs/well-lit-paths/foundations/precise-prefix-cache-routing): cache-state indexing variant.
