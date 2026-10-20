---
id: vector-database
title: Vector Database
summary: A vector database stores vectors with provenance and metadata and supports similarity queries, persistence and updates using exact search or a measured approximate-index tradeoff.
type: concept
tags: [ml/information-retrieval]
prereqs: [embedding, nearest-neighbor-search]
sources: [https://github.com/pgvector/pgvector]
status: explained
created: 2026-06-23
updated: 2026-10-21
---

# Vector Database

## Summary

A vector database stores vectors together with source identifiers and metadata, then serves similarity queries under persistence, filtering and update requirements. It can be a specialized product or a capability inside a relational database. It is not synonymous with an approximate-nearest-neighbor index.

## Grounded explanation

An [[embedding]] maps an input into numeric coordinates according to a trained representation. [[nearest-neighbor-search]] ranks stored vectors using a declared distance or similarity. The database supplies the surrounding lifecycle: stable identifiers, source provenance, inserts, updates, deletions, persistence, access filtering and a query interface. Similarity is a learned geometric signal, not a guarantee that two documents mean the same thing or answer the same question.

Exact search computes the requested metric over eligible candidates and returns its true nearest neighbors, subject to the implementation's numeric contract. It can be a good baseline or production choice for small corpora, selective filters and efficient batched scans. A relational system can execute such calculations; pgvector explicitly supports both exact and approximate search inside PostgreSQL. A separate database product is not required merely because the data contains vectors.

Approximate indexes restrict the candidate search to trade some recall for lower cost. Graph traversal and partition-based indexes have different build, memory, update and query behavior. They do not guarantee a universal sublinear elapsed time or harmless ranking changes. Missing one decisive supporting passage can matter even when embedding distances are close. Measure recall against an exact-search baseline and evaluate the downstream task, rather than assuming approximation is nearly free.

## Worked example

Four documents have two-dimensional vectors A=(0,0), B=(1,0), C=(2,0), and D=(3,0). The query is q=(1.2,0). Their Euclidean distances are 1.2, 0.2, 0.8 and 1.8, so exact top-2 returns B and C.

Suppose A and C belong to the caller's permitted collection, while B and D do not. Exact top-2 within that collection returns C and A. Retrieving the global top-2 first and then filtering leaves only C; that is not equivalent to searching all permitted candidates. An approximate index may also miss C unless its search budget explores the relevant region. A query plan must state when filters apply and whether it can expand the search to return enough eligible results.

## Boundaries and validation

Record model and vector versions so queries remain comparable with stored embeddings. A source update needs coordinated replacement or invalidation of its vector and provenance; deletion and permission changes must propagate to every serving path. Persistence alone does not ensure these contracts.

Compare exact and approximate plans on representative collection sizes, filter selectivity and update rates. Report recall, downstream answer quality, p50/p95 latency, memory, build time, write cost and recovery behavior. Separate embedding-model quality from index approximation. Choose a specialized store only when its operational and query advantages justify another system boundary.

## Prerequisites

- [[embedding]]
- [[nearest-neighbor-search]]

## Sources

- <https://github.com/pgvector/pgvector> — documents exact and approximate SQL vector search, index tradeoffs and filtering behavior.
