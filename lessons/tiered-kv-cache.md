# Tiered Kv Cache

## Meaning

A **tiered KV cache** keeps frequently reused attention blocks near the GPU and evicts colder blocks to larger, slower memory instead of discarding them immediately. It expands the possible reuse window for repeated prompts, but a cache hit is valuable only when fetching the block is cheaper than recomputing it.

## Mechanism

[[kv-cache]] blocks occupy accelerator memory alongside weights and active requests. [[prefix-caching]] can reuse blocks across requests, yet a busy server eventually evicts them. A tiered design follows the [[memory-hierarchy]]: GPU memory for active blocks, CPU RAM for recently evicted blocks, and possibly local or network storage for colder ones. On a later matching prompt, the system checks whether a block still exists and fetches it back before continuing prefill.

Consider a long multi-turn conversation revisited after other users fill GPU memory. Without offload, its prior prefix must be recomputed. With CPU offload, a transfer may restore it faster. A short prefix may be cheaper to recompute; network storage might lose to recomputation even for a longer one under congestion. Eviction policy, block granularity, and request arrival patterns determine the trade-off. A cache index can be stale, and transfer bandwidth shared with other work may increase tail latency.

## One example

A long chat prefix is evicted from GPU RAM but retained in CPU RAM. A later request restores it if transfer costs less than prefill recomputation.

## Check your understanding

**Question:** Why is a cache hit not always a latency win?

**Answer:** Restore transfer and queueing may cost more than recomputing the prefix.
