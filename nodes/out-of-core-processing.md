---
id: out-of-core-processing
title: Out-of-Core Processing
summary: Out-of-core processing computes over data larger than memory by bounding the live working set and reading or writing partitions incrementally.
type: concept
tags: [databases/storage]
prereqs: [memory-hierarchy, reduction-operation]
sources: [https://pandas.pydata.org/docs/user_guide/scale.html]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Out-of-Core Processing

## Summary

The full dataset stays in slower storage while a bounded portion occupies working memory. The challenge is not dividing the input file alone: intermediate state and the final result must also fit or be partitioned.

## Grounded explanation

The [[memory-hierarchy]] trades fast limited memory against larger slower storage. Read a partition, compute its contribution, release it, and continue. A [[reduction-operation]] with mergeable state lets partition results combine without collecting all rows.

### Original example: a mean without all the rows

Two partitions contain values `[2, 4, 6]` and `[8, 10]`. Their sufficient state for a mean is `(sum, count)`: `(12, 3)` and `(18, 2)`. Merge by componentwise addition to get `(30, 5)`, then divide once: mean 6. Averaging the partition means instead gives `(4+9)/2=6.5`, which is wrong because the partitions have different sizes.

The operation, not merely the chunk size, determines whether this works. An exact median cannot generally be computed from partition medians. A join can generate far more output than input if keys repeat, and per-key aggregation state can grow with the number of distinct keys. Partition those operations by a suitable key or use an engine that writes intermediate state to disk when memory fills.

### Budget the live set

Let $M$ be available memory, $B$ an input partition's decoded size, $T$ temporary computation storage, and $S$ retained state/output. All are measured in bytes. A necessary working-set condition is

$$B+T+S < M,$$

with headroom for runtime overhead. For an 8 GiB budget, a 2 GiB partition, 3 GiB of temporary buffers and 1 GiB of retained state use 6 GiB. Increasing the input partition to 4 GiB exhausts the budget even though that partition alone appears to fit. On-disk compression makes file size an unreliable substitute for decoded memory.

### Choosing an execution engine

pandas supports smaller data types, loading selected columns, chunked processing where operations permit it, and integration with larger-scale execution tools. It is not inherently prohibited in production, and there is no universal memory amplification multiplier. Containerizing an existing script does not make its operations partitionable.

Before changing engines, compare representative outputs, peak memory, intermediate size, data skew, and elapsed time. A distributed execution plan additionally moves data between workers; more machines need not help an operation dominated by that transfer or a single oversized partition. Record which operations genuinely require global information instead of treating every daily dataset as a low-latency stream.

## Sources

- [pandas, Scaling to large datasets](https://pandas.pydata.org/docs/user_guide/scale.html): selective loading, memory reduction, chunking and alternative execution tools. Worked calculations above are independent examples.
