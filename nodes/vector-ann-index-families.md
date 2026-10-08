---
id: vector-ann-index-families
title: Vector ANN Index Families
summary: "Flat, coarse-partition, graph, and compressed-vector indexes trade exactness, recall, memory, updates, and query work differently."
type: concept
tags: [ml/information-retrieval]
prereqs: [nearest-neighbor-search, quantization]
sources: [https://github.com/facebookresearch/faiss/wiki/Faiss-indexes, https://research.google/blog/announcing-scann-efficient-vector-similarity-search/]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Vector ANN Index Families

## Summary

A vector index chooses *which* stored embeddings to compare with a query and *how* to represent them. Flat search scores every vector exactly. Inverted-file (IVF) indexes probe selected coarse clusters. HNSW follows a navigable graph. Product quantization (PQ) replaces full vectors with compact codes; IVF-PQ combines partition pruning with those codes. ScaNN is an implementation family combining partitioning, quantized scoring, and rescoring. These are distinct mechanisms under the shared [[nearest-neighbor-search]] problem.

## Grounded explanation

A flat index is the correctness baseline: scan all $N$ vectors, compute the chosen metric, and take top $k$. Query work scales with $N$, but recall is exact for that metric. IVF first assigns database vectors to coarse centroids. At query time, search only a configurable number of nearby lists (`nprobe`). Too few probes can miss neighbors across a cluster boundary; more probes increase work and usually recall. HNSW instead organizes proximity links in layers: sparse upper-layer hops find a neighborhood and denser lower-layer traversal refines it. Search breadth improves recall at a memory and latency cost; graph construction and updates have their own costs.

PQ is not merely pruning: it uses [[quantization]] to encode subvectors with small codebooks, approximating distances without reading every full-precision coordinate. IVF-PQ narrows candidate lists *and* scores their compressed codes. A final rerank with original vectors can restore ranking quality if those vectors are retained. ScaNN's documented pipeline likewise partitions, scores compressed candidates, and reorders promising ones. The exact performance depends on metric, vector distribution, dimension, training set, filters, hardware, and update rate; no family universally dominates.

Measure recall@k against an exact flat index at a fixed embedding snapshot. Plot query latency and throughput versus recall, and include index-build time, peak memory, stored bytes per vector, insert/delete behavior, and post-filter recall. Tune each index to the same recall target before comparing latency. For RAG, also measure answer quality: nearest-vector recall is not the same as evidence sufficiency.

## Prerequisites

- [[nearest-neighbor-search]]
- [[quantization]]

## Sources

- [Faiss index catalog](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes): primary implementation descriptions of Flat, IVF, HNSW, PQ, and IVF-PQ.
- [Google Research ScaNN overview](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/): partition, approximate scoring, and rescoring design.
