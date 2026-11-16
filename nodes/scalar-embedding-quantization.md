---
id: scalar-embedding-quantization
title: Scalar Embedding Quantization
summary: Scalar embedding quantization encodes individual vector coordinates with calibrated finite levels while preserving an explicit query and distance contract.
type: concept
tags: [ml/information-retrieval]
prereqs: [quantization, embedding, nearest-neighbor-search]
sources: [https://github.com/facebookresearch/faiss/wiki/Faiss-indexes, https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html]
status: explained
created: 2026-11-17
updated: 2026-11-17
---

# Scalar Embedding Quantization

## Meaning

Scalar embedding quantization compresses an [[embedding]] by coding its coordinates separately. It changes the stored search representation rather than the model that produced it. The coordinate-wise decision distinguishes it from coding whole subvectors or retaining only signs.

## Mechanism

For coordinate j, choose a lower endpoint a_j, upper endpoint b_j greater than a_j, and an integer bit count B. There are L=2^B available codes, numbered zero through L-1. Set step s_j=(b_j-a_j)/(L-1). Encode x_j as round((x_j-a_j)/s_j), clipped into the code range; reconstruct code c_j as a_j+s_j c_j. This is [[quantization]] with coordinate-specific ranges. For an in-range value, nearest rounding has error at most s_j/2. Clipping an out-of-range value does not obey that bound. Constant-valued coordinates need a separate zero-range rule.

Calibrate ranges on representative indexing data, not one arbitrary query. Persist ranges, coordinate order, encoder version and normalization convention with the codes. Query scoring may decode documents, quantize the query compatibly, or use an asymmetric computation with an uncompressed query. These choices have different errors; treating packed integer coordinates as if they retained the original cosine geometry is not automatically valid.

## One example

Take two-coordinate vectors and two-bit unsigned codes. Ranges [-1,2] and [0,6] give steps one and two. Vector [0.6,5.1] encodes as [2,3] and reconstructs as [1,6], with errors [0.4,0.9], each below half its step. A later second coordinate of nine clips to code three and reconstructs as six: its error of three exceeds the in-range bound of one. That is a calibration-range failure, not an arithmetic contradiction.

Two-bit payload for a 768-coordinate vector is 192 bytes instead of 3,072 float32 bytes, before ranges, identifiers, index structure and retained originals. Faiss documents several scalar formats; this example defines an illustrative uniform scheme rather than claiming every format uses this exact range rule.

## Validation and check

Compare [[nearest-neighbor-search]] results against full-precision vectors on held-out queries. Inspect clipping frequency by coordinate and data slice, recall, final evidence quality, total memory and latency, including query conversion and rescoring. Recalibration requires coherent encoding of stored data. Can smaller reconstruction error guarantee unchanged nearest neighbors? No: two almost-tied candidates can swap even under small coordinate errors.

## Sources

- <https://github.com/facebookresearch/faiss/wiki/Faiss-indexes>
- <https://www.sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html>
