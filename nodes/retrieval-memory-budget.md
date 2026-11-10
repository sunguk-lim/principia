---
id: retrieval-memory-budget
title: Retrieval Memory Budget
summary: A retrieval memory budget accounts separately for encoder weights, stored vectors, search structure, rescoring data and runtime buffers so one compression ratio cannot stand in for total system memory.
type: concept
tags: [ml/information-retrieval]
prereqs: [binary-embedding-quantization, post-training-quantization]
sources: [https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html]
status: explained
created: 2026-11-11
updated: 2026-11-11
---

# Retrieval Memory Budget

## Meaning

A retrieval application stores more than the model that embeds a query. It may also keep many document vectors, a search structure, metadata, higher-precision rescoring data and temporary runtime buffers. Weight quantization and index quantization act on different terms of that budget and can affect quality in different ways.

## Mechanism

Let P be the number of encoder parameters, bw the effective bits per parameter, N the number of indexed vectors, d their dimension and bv the bits stored per vector coordinate. Ideal packed payloads are P×bw/8 bytes for weights and N×d×bv/8 bytes for vectors. Add quantization scales, alignment, identifiers, search-structure links, metadata, retained originals and runtime allocations separately. Effective bit rates and measured resident memory can differ from ideal payloads.

[[post-training-quantization]] changes the encoder and can change every new embedding. [[binary-embedding-quantization]] compresses the stored representation and changes candidate ranking. Its theoretical 32-fold vector-payload reduction from float32 to one bit says nothing by itself about model weights or a graph search structure. Retaining float32 vectors for rescoring can preserve a large storage term even when first-stage binary search is compact.

## One example

Use an invented encoder with 200 million parameters and an index of one million 768-dimensional vectors. At 16 bits per parameter, ideal weight payload is 400,000,000 bytes; four-bit weights reduce that term to 100,000,000 bytes, before quantization metadata. Float32 vectors require 1,000,000×768×4=3,072,000,000 bytes. Binary codes require 1,000,000×768/8=96,000,000 bytes.

Reducing only model weights leaves 3,172,000,000 bytes of these two ideal terms. Reducing only vectors leaves 496,000,000 bytes. Reducing both leaves 196,000,000 bytes. None is a measured complete application footprint. If the float32 vectors remain for rescoring, add their 3,072,000,000 bytes back where they are actually stored or loaded. Disk, RAM and accelerator memory are different budgets, even for the same data.

## Check your understanding

Can changing encoder precision leave the stored index untouched? Only when the resulting query-to-document geometry remains compatible and retrieval tests support that decision. Compare full-precision, weight-only, index-only and combined compression on the same held-out queries. Measure recall, downstream evidence quality, end-to-end latency, peak memory in each tier and rebuild cost. Compression is useful when the whole quality/resource frontier improves, not when one payload's ratio is largest.

## Prerequisites

- [[binary-embedding-quantization]]
- [[post-training-quantization]]

## Sources

- <https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html>
