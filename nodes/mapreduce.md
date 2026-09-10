---
id: mapreduce
title: MapReduce
summary: MapReduce expresses a data-parallel computation as a map that emits intermediate key-value pairs and a reduce that combines all values for each key, while the runtime partitions work, moves grouped values, and recovers failed tasks.
type: concept
tags: [databases/distributed]
prereqs: [hash-map]
sources: [https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# MapReduce

## Summary

**MapReduce** separates a large batch computation into two functions: `map`, which emits intermediate `(key, value)` records, and `reduce`, which combines the values grouped under one key. The framework performs the partitioning, grouping, scheduling, and retry work around those functions.

## Grounded explanation

Suppose a corpus contains documents and the desired result is a word count. A mapper reads one document and emits `(word, 1)` for every word. The framework partitions intermediate records by a deterministic function of their key, so every occurrence of the same word reaches the same reducer. After the shuffle groups records, a reducer receives one word and its sequence of counts and emits their sum.

The grouping key is the essential contract. A [[hash-map]] is a familiar single-machine analogy: it associates each key with the values accumulated for that key. MapReduce makes that association distributed, so the implementation must transfer intermediate partitions between workers before reduction. The result is data parallelism for computations that can be represented as independent map operations followed by per-key aggregation.

The programming model does not make every workload suitable. A reducer cannot produce a final per-key result until its corresponding mapped values are available, and skewed keys can concentrate too much work on one reducer. Re-running work after a worker failure is practical only when map and reduce functions have controlled side effects or their output is written in an idempotent way. Prefer this pattern for large, finite batch jobs with a clear grouping key; use a different design when low-latency incremental state or cross-key coordination dominates.

## Prerequisites

- [[hash-map]]

## Sources

- [Dean and Ghemawat, *MapReduce: Simplified Data Processing on Large Clusters*](https://research.google/pubs/mapreduce-simplified-data-processing-on-large-clusters/): map/reduce functions, intermediate grouping, partitioning, scheduling, failure handling, and inter-machine communication.
