---
id: retrieval-index-amortization
title: Retrieval Index Amortization
summary: Retrieval index amortization separates reusable preprocessing from recurring query work and update cost so a fast warm lookup is not mistaken for low total system cost.
type: concept
tags: [ml/information-retrieval]
prereqs: [background-document-indexing, measurement]
sources: [https://learn.microsoft.com/en-us/azure/search/search-indexer-overview, https://docs.streamlit.io/develop/concepts/architecture/caching]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Retrieval Index Amortization

## Meaning

Indexing pays some computation before a query arrives. The benefit is reuse: many later queries can search stored representations instead of repeating decoding, extraction and embedding. The saving depends on query volume, corpus changes and invalidation rules, not on labeling one measured step “one-time.”

## Mechanism

[[background-document-indexing]] separates ingestion from search and binds stored representations to source and transformation versions. A query still needs parsing, query encoding, candidate lookup, optional rescoring and result delivery. Updates need detecting, rebuilding and safely publishing changed evidence. Encoder replacement can invalidate all vectors even if source bytes are unchanged.

Define I as initial indexing cost, U as total maintenance cost over a declared period, Q as the positive number of queries and S as average query-service cost in that period. Average cost per query is (I+U)/Q + S. Use one unit consistently, such as seconds of work or money; do not add bytes to milliseconds. This model omits parallelism and contention, so it is accounting rather than a latency predictor. [[measurement]] keeps warm lookup latency separate from cold start and end-to-end behavior.

A cache can avoid repeated work only when its key and invalidation reflect the inputs that matter. Streamlit's caching documentation gives a primary example of input-driven reuse and expiry controls. Azure indexing documentation warns that indexing competes with query resources. Moving work off the request path does not make it free or guarantee independent compute.

## One example

An invented corpus takes 120 seconds to index, needs 30 seconds of updates in a day and serves 50 queries at 0.2 seconds of work each. Total work is 120+30+10=160 seconds, or 3.2 seconds per query when amortized. The warm query still takes 0.2 seconds in this simplified example. With 1,000 queries and the same I, U and S, average work is 0.35 seconds per query. Neither number establishes tail latency, concurrent throughput or retrieval quality.

## Check your understanding

Is the break-even point fixed once an index is built? No. Churn, cache expiry, model revisions and required freshness change maintenance and reuse. Benchmark cold and warm paths, source-to-search delay, corpus size, recall, storage and concurrency; disclose whether initial indexing and updates are included. A fast average over a handful of queries is not a universal serving guarantee.

## Prerequisites

- [[background-document-indexing]]
- [[measurement]]

## Sources

- <https://learn.microsoft.com/en-us/azure/search/search-indexer-overview>
- <https://docs.streamlit.io/develop/concepts/architecture/caching>
