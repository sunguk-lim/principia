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
updated: 2026-10-20
---

# Tiered KV Cache

## Summary

A **tiered KV cache** keeps frequently reused attention blocks near the GPU and evicts colder blocks to larger, slower memory instead of discarding them immediately. It expands the possible reuse window for repeated prompts, but a cache hit is valuable only when fetching the block is cheaper than recomputing it.

## Grounded explanation

[[kv-cache]] blocks occupy accelerator memory alongside weights and active requests. [[prefix-caching]] can reuse blocks across requests, yet a busy server eventually evicts them. A tiered design follows the [[memory-hierarchy]]: GPU memory for active blocks, CPU RAM for recently evicted blocks, and possibly local or network storage for colder ones. On a later matching prompt, the system checks whether a block still exists and fetches it back before continuing prefill.

Consider a long multi-turn conversation revisited after other users fill GPU memory. Without offload, its prior prefix must be recomputed. With CPU offload, a transfer may restore it faster. A short prefix may be cheaper to recompute; network storage might lose to recomputation even for a longer one under congestion. Eviction policy, block granularity, and request arrival patterns determine the trade-off. A cache index can be stale, and transfer bandwidth shared with other work may increase tail latency.

Do not confuse tiering with adding GPU capacity: offloaded blocks are not ready for immediate decode until restored. Nor is tiering a universal performance gain. Evaluate GPU and host memory occupancy, cache-hit and restore rates, bytes moved, restore latency, time to first token, throughput, and p95 latency across repeated-prefix and unique-prefix mixes. Compare no offload, CPU tier, and storage tier under identical hardware, model, and load. Verify the benchmark's total memory and storage costs.

## Retention, restoration and recomputation

A retention policy chooses not only where a block goes, but how long keeping it is worth the opportunity cost. For one returning request, compare measured recomputation time with restore time: bytes divided by effective transfer bandwidth, plus lookup, setup, queueing and contention. Transfer overlap helps only when it actually shortens the critical path. Retaining a cold prefix in GPU memory can displace several active requests; a high hit rate can therefore coexist with worse useful throughput.

For a hypothetical 2 GiB prefix, a path sustaining 8 GiB/s needs at least 250 ms to move the state. Add 30 ms of setup and waiting to obtain 280 ms. If recomputation takes 180 ms under the same load, discard-and-recompute is faster for this request. At 32 GiB/s the transfer floor becomes 62.5 ms; with the same 30 ms overhead, 92.5 ms restoration can win. These are illustrative measured-path assumptions, not device peak predictions. Long queues can reverse either choice. Choose retention duration using reuse likelihood, capacity pressure and restore/recompute cost; test stale indexes, eviction, cold starts and incompatible model versions. Keeping bytes is not sufficient if the corresponding request state cannot safely be resumed.

## Prerequisites

- [[kv-cache]]
- [[prefix-caching]]
- [[memory-hierarchy]]

## Sources

- [llm-d tiered prefix cache](https://llm-d.ai/docs/well-lit-paths/foundations/tiered-prefix-cache): GPU, CPU, and storage tiers.

- <https://llm-d.ai/docs/well-lit-paths/foundations/tiered-prefix-cache>
