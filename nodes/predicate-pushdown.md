---
id: predicate-pushdown
title: "Predicate Pushdown"
summary: "Predicate pushdown moves a row-selection condition toward its data source when the rewrite preserves results, reducing downstream intermediate work and sometimes source reads."
type: concept
tags: [databases/query-processing]
prereqs: [query-planning]
sources: ["https://duckdb.org/2024/11/14/optimizers.html"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Predicate Pushdown

## Meaning

A predicate is a condition deciding which rows to retain. Predicate pushdown places that condition earlier in an execution plan, as close to the data source as supported, instead of carrying rows through expensive operators only to discard them later. It changes execution order while preserving the query's meaning.

## Mechanism

[[query-planning]] chooses among equivalent plans. A row filter can often move before a transformation or join when the condition's required fields are already available and the rewrite is valid. [[column-pruning]] is complementary: it reduces fields rather than rows. A column used by the filter may need to be read even when it is absent from the final output.

Earlier filtering reduces downstream rows, but does not automatically reduce source bytes. A file or connector may need to read and decode all input before evaluating the condition. Source statistics or an index may permit skipping larger regions, while an opaque function can prevent pushdown entirely. Inspect the actual plan and storage metrics rather than inferring I/O savings from an API call's position.

Reordering is constrained by semantics. A filter on an aggregate result cannot generally be evaluated on individual input rows. Moving conditions across an outer join can change which unmatched rows survive. Expressions with side effects or nondeterministic behavior also need care. A selective condition does not justify an invalid rewrite.

## One example

An invented table contains 1,000 rows, of which 80 satisfy `region = 'west'`. A costly per-row transformation followed by that filter transforms 1,000 rows. If the filter depends only on the original region field and reordering is valid, filtering first transforms 80 rows. The retained result is the same, but 920 transformations are avoided. If all source bytes still must be scanned, the storage-read reduction may be zero despite that computation saving.

## Check your understanding

Is “filter first” always valid? No. State the condition's inputs and the intervening operator's semantics. Compare result equivalence, plans, rows per operator, source bytes and elapsed time under representative selectivity. Keep projection and row filtering distinct when diagnosing improvements.

## Prerequisites

- [[query-planning]]

## Sources

- <https://duckdb.org/2024/11/14/optimizers.html>
