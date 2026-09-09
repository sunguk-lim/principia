---
id: column-pruning
title: Column Pruning
summary: Column pruning avoids reading or materializing fields that a computation does not require, reducing I/O, decoding, memory traffic, and intermediate width when the storage and execution path support projection.
type: concept
tags: [databases/storage]
prereqs: [query-planning, memory-hierarchy]
sources: [https://parquet.apache.org/docs/overview/motivation/, https://arrow.apache.org/docs/format/Columnar.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Column Pruning

## Summary

**Column pruning** carries the set of required fields backward through a computation and reads or materializes only those columns when possible.

## Grounded explanation

For a table with columns $C$ and a query that needs subset $R\subset C$, an ideal scan decodes only $R$. In columnar storage such as Parquet, values are organized by column, so an engine can often avoid the byte ranges for unused columns. Apache Arrow likewise stores each field as an array with a defined columnar layout, supporting sequential access and vectorized processing.

The [[query-planning]] stage derives required columns from output projections, filters, joins, grouping, sorting, and expressions. A column used only by a filter may be required at the scan but discarded afterward. `SELECT *`, opaque user-defined functions, schema-dependent code, or a connector that cannot push projections down can prevent pruning.

Benefits are workload-dependent. If a file has 100 similarly sized columns and a query needs 5, the upper-bound byte reduction is large, but metadata, row-group reads, decompression granularity, nested encodings, and remote request overhead prevent a universal 20× speedup. Row-oriented data may still read full records even when later operators discard fields.

Verify with an execution plan and storage metrics: projected schema, files and row groups touched, bytes read, bytes decoded, peak memory, transfer volume, and elapsed time. Compare identical results and warm/cold cache states. A library benchmark does not establish that one engine is generally faster than another; device transfer, lazy planning, data types, query shape, and manual versus automatic projection all matter through the [[memory-hierarchy]].

## Prerequisites

- [[query-planning]]
- [[memory-hierarchy]]

## Sources

- [Apache Parquet, “Motivation”](https://parquet.apache.org/docs/overview/motivation/): describes efficient compressed columnar representation and per-column encoding.
- [Apache Arrow Columnar Format](https://arrow.apache.org/docs/format/Columnar.html): specifies field arrays, contiguous buffers, sequential access, vectorization, and columnar locality trade-offs.
