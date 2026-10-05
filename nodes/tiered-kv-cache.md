---
id: tiered-kv-cache
title: Tiered KV Cache
summary: A tiered KV cache moves reusable attention state from scarce GPU memory to slower CPU or storage tiers, trading recomputation against transfer latency and working-set size.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, prefix-caching, memory-hierarchy]
sources: [https://llm-d.ai/docs/well-lit-paths/foundations/tiered-prefix-cache]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Tiered KV Cache

## Summary

A **tiered KV cache** keeps frequently reused attention blocks near the GPU and evicts colder blocks to larger, slower memory instead of discarding them immediately. It expands the possible reuse window for repeated prompts, but a cache hit is valuable only when fetching the block is cheaper than recomputing it.

## Grounded explanation

[[kv-cache]] blocks occupy accelerator memory alongside weights and active requests. [[prefix-caching]] can reuse blocks across requests, yet a busy server eventually evicts them. A tiered design follows the [[memory-hierarchy]]: GPU memory for active blocks, CPU RAM for recently evicted blocks, and possibly local or network storage for colder ones. On a later matching prompt, the system checks whether a block still exists and fetches it back before continuing prefill.

Consider a long multi-turn conversation revisited after other users fill GPU memory. Without offload, its prior prefix must be recomputed. With CPU offload, a transfer may restore it faster. A short prefix may be cheaper to recompute; network storage might lose to recomputation even for a longer one under congestion. Eviction policy, block granularity, and request arrival patterns determine the trade-off. A cache index can be stale, and transfer bandwidth shared with other work may increase tail latency.

Do not confuse tiering with adding GPU capacity: offloaded blocks are not ready for immediate decode until restored. Nor is tiering a universal performance gain. Evaluate GPU and host memory occupancy, cache-hit and restore rates, bytes moved, restore latency, time to first token, throughput, and p95 latency across repeated-prefix and unique-prefix mixes. Compare no offload, CPU tier, and storage tier under identical hardware, model, and load. Verify the benchmark's total memory and storage costs.

## Prerequisites

- [[kv-cache]]
- [[prefix-caching]]
- [[memory-hierarchy]]

## Sources

- [llm-d tiered prefix cache](https://llm-d.ai/docs/well-lit-paths/foundations/tiered-prefix-cache): GPU, CPU, and storage tiers.
