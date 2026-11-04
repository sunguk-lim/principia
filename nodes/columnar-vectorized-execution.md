---
id: columnar-vectorized-execution
title: Columnar Vectorized Execution
summary: "Columnar vectorized execution stores fields in typed arrays and applies operations to bounded batches, reducing per-row dispatch and unnecessary data movement without guaranteeing a universal speedup."
type: concept
tags: [databases/query-processing]
prereqs: [dynamic-array, memory-hierarchy, query-planning]
sources: [https://arrow.apache.org/docs/format/Columnar.html, https://duckdb.org/docs/stable/internals/vector]
status: explained
created: 2026-11-05
updated: 2026-11-05
---

# Columnar Vectorized Execution

## Meaning

Columnar layout and vectorized execution are complementary, not synonyms. Layout groups a field's values into arrays; execution applies an operator to a batch of values instead of repeatedly dispatching one operator call per row. A columnar file does not prove the whole query runs in batches, and a batch engine need not use one particular instruction set.

## Mechanism

An array provides ordered indexed values; [[dynamic-array]] explains contiguous storage and the difference between a container and its elements. A typed fixed-width column can store numeric values directly in a contiguous buffer rather than placing separately boxed row objects next to each other. Nullable or variable-width fields need extra information such as validity bits or offsets. Those buffers are part of the representation, not free metadata.

Batch execution passes a bounded group of values between operators. For an addition, the engine applies the same operation to that group in one operator invocation; it may exploit hardware instructions operating on several lanes, but batching does not guarantee that instruction choice. [[memory-hierarchy]] explains why adjacent required values and fewer object lookups can reduce traffic. [[query-planning]] determines which fields and operators are actually required before running them. Layout, selection and scheduling therefore contribute separately.

## One example

Consider rows `(price=3, count=2, label="a")`, `(5,4,"b")` and `(7,1,"c")`. To compute price×count, a columnar batch exposes price `[3,5,7]` and count `[2,4,1]`; applying the operator yields `[6,20,7]`. The label buffer is irrelevant to this operator. If each required numeric field uses 8 bytes, the two value buffers contain 3×2×8=48 bytes, excluding metadata and validity storage. Adding more unused fields need not widen this operator's input. Converting an existing row format, however, still requires reading and rearranging data before that saving appears.

## Check your understanding

Does a call that looks vectorized establish faster native batch execution? No: a library can hide a per-element interpreter loop. Compare identical results, data types, null semantics and batch sizes. Measure dispatch overhead, bytes read and materialized, conversion cost, peak working set and full query time. Large batches can improve amortization while consuming more memory; tiny batches restore overhead. Row-oriented mutation or point lookup can favor a different layout. Neither columnar layout nor moving a local dataframe program to a cluster automatically removes shuffles, skew or large intermediates.

## Prerequisites

- [[dynamic-array]]
- [[memory-hierarchy]]
- [[query-planning]]

## Sources

- <https://arrow.apache.org/docs/format/Columnar.html>
- <https://duckdb.org/docs/stable/internals/vector>
