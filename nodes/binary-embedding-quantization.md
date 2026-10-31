---
id: binary-embedding-quantization
title: Binary Embedding Quantization
summary: Binary embedding quantization maps each embedding coordinate to one bit and uses compact codes for approximate candidate retrieval with measured quality loss.
type: concept
tags: [ml/information-retrieval]
prereqs: [quantization, embedding, nearest-neighbor-search]
sources: [https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Binary Embedding Quantization

## Meaning

Binary embedding quantization stores one bit per coordinate instead of a floating-point value. It shrinks the vector payload and permits bitwise comparison, but discards magnitude information. It is not the same mechanism as low-bit model-weight quantization or product quantization.

## Mechanism

An [[embedding]] maps an item into a numeric vector. A simple [[quantization]] rule maps positive coordinates to one and nonpositive coordinates to zero; the exact threshold convention must match indexing and querying. Pack these bits into bytes. For two codes, Hamming distance is the count of differing bit positions. This provides an approximate [[nearest-neighbor-search]] ordering; it need not preserve the original cosine or dot-product ordering.

Retrieve a larger candidate set in the compact representation, then optionally rescore. Rescoring may compare a full-precision query with binary documents, or retain higher-precision document vectors for a different reranker. Those are different storage and compute budgets. A signed byte used to pack bits is a storage convention, not eight independent signed embedding coordinates.

## Worked example

A four-coordinate query [0.8,-0.2,0.1,-0.9] becomes 1010. Document A [0.7,-0.1,0.4,-0.8] also becomes 1010 and has Hamming distance zero. B [-0.1,-0.3,0.6,-0.7] becomes 0010 and differs at one bit. Code-based candidate ordering ranks A first here, but many distinct vectors share its code. Their magnitudes and within-region directions have been discarded.

For 1,024 coordinates, float32 payload is 1,024×4=4,096 bytes. A packed binary payload is 1,024/8=128 bytes, a 32-fold reduction for that payload. IDs, index structure, source documents, higher-precision rescoring data and generator state remain additional memory.

## Validation

Measure recall against a full-precision reference and downstream evidence grounding, including rare terms, languages and near-boundary coordinates. Vary candidate depth and rescoring budget under equal hardware. Report total resident/index storage, build cost and latency, not only bits per vector. One-bit codes are useful when the quality/cost frontier improves on the real corpus, not because 32-fold payload compression guarantees a 32-fold smaller or faster application.

## Prerequisites

- [[quantization]]
- [[embedding]]
- [[nearest-neighbor-search]]

## Sources

- <https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html>
