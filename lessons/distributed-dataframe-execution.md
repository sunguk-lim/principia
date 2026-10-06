# Distributed Dataframe Execution

## Meaning

A distributed dataframe spreads tabular operations across workers. Its scalability comes from a partitionable execution plan, not from a familiar dataframe API or a larger cluster by itself. The expensive boundary is often moving data between workers for operations that need global coordination.

## Mechanism

A filter can run independently on each partition. A [[reduction-operation]] can combine compact local summaries when its state is mergeable. Joins, global sorts, and some grouped computations may need a shuffle so matching keys meet on the same worker. Shuffling consumes network bandwidth, serialization time, and memory. Skew can overload one partition even when total data is spread across many machines. [[out-of-core-processing]] keeps each worker's live set bounded; adding workers does not excuse an unbounded intermediate result.

Input file size is a poor memory estimate. Selected columns, decoded types, joins, grouping cardinality, temporary buffers, and output size determine what must fit. Decide batch versus streaming from the delivery deadline and update semantics, not from an arbitrary data-volume threshold.

## One example

A daily feature job reads a large log and computes counts by account. Each worker can count locally, then merge counts by account. If one account owns most rows, it may become a hot key and dominate the shuffle. Measure partition sizes and spill; consider a two-stage aggregation rather than merely increasing worker count.

## Check your understanding

**Question:** Why does containerizing a pandas script not automatically make it distributed?

**Answer:** The script may still materialize all data and execute global operations in one process. A distributed plan must partition data and handle joins, reductions, and state explicitly.
