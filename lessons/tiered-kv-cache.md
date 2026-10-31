# Tiered Kv Cache

## Meaning

A **tiered KV cache** keeps frequently reused attention blocks near the GPU and evicts colder blocks to larger, slower memory instead of discarding them immediately. It expands the possible reuse window for repeated prompts, but a cache hit is valuable only when fetching the block is cheaper than recomputing it.

## Mechanism

[[kv-cache]] blocks occupy accelerator memory alongside weights and active requests. [[prefix-caching]] can reuse blocks across requests, yet a busy server eventually evicts them. A tiered design follows the [[memory-hierarchy]]: GPU memory for active blocks, CPU RAM for recently evicted blocks, and possibly local or network storage for colder ones. On a later matching prompt, the system checks whether a block still exists and fetches it back before continuing prefill.

Consider a long multi-turn conversation revisited after other users fill GPU memory. Without offload, its prior prefix must be recomputed. With CPU offload, a transfer may restore it faster. A short prefix may be cheaper to recompute; network storage might lose to recomputation even for a longer one under congestion. Eviction policy, block granularity, and request arrival patterns determine the trade-off. A cache index can be stale, and transfer bandwidth shared with other work may increase tail latency.

## One example

For a hypothetical 2 GiB prefix, a restore path sustaining 8 GiB/s needs at least 250 ms to transfer it. Add 30 ms for setup and queueing: restoration takes 280 ms before any additional contention. If recomputation takes 180 ms, a hit on that slower tier is not the fastest path. At 32 GiB/s the transfer floor is 62.5 ms; with the same overhead, 92.5 ms restoration can win. Retaining the block on the GPU avoids the restore but consumes space other requests could use. Measure the full path and reuse probability before choosing how long to retain it.

## Shared transfer paths

Parallel storage reads do not bypass a shared bottleneck. Four 128 MiB blocks each read at 2 GiB/s could finish in 62.5 ms on independent paths; a common 4 GiB/s link raises the aggregate transfer floor to 125 ms. Queueing and stragglers add delay. Layerwise prefetch only hides transfer when required state arrives before use and staging lifetimes are correct. Measure the complete restore path, not the sum of device peak bandwidths.

## Check your understanding

**Question:** Why is a cache hit not always a latency win?

**Answer:** Restore transfer and queueing may cost more than recomputing the prefix.
