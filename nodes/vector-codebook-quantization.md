---
id: vector-codebook-quantization
title: "Vector Codebook Quantization"
summary: "Vector codebook quantization replaces a whole vector with the index of a learned representative, trading reconstruction error for compact codes."
type: concept
tags: [ml/representation-learning]
prereqs: [k-means-clustering]
sources: ["https://github.com/facebookresearch/faiss/wiki/Faiss-building-blocks:-clustering,-PCA,-quantization"]
status: explained
created: 2026-11-22
updated: 2026-11-22
---

# Vector Codebook Quantization

## Meaning

A vector codebook stores a finite set of representative vectors. Encoding replaces each original vector with the index of one representative; decoding retrieves that representative. This is not restricted to evenly spaced scalar levels or to separately coding coordinate groups.

## Mechanism

Choose a codebook with K centers of dimension d. Under squared-distance distortion, assign each input to its nearest center using the rule in [[k-means-clustering]]. Training can minimize the sum of reconstruction errors by updating the representatives. The code uses enough bits to identify one of K entries; storage also includes the shared codebook, vector identifiers and any alignment overhead. [[arithmetic]] gives both storage accounting and coordinatewise squared-error calculations.

At decoding, look up the selected representative. The original residual is lost unless stored separately. A learned codebook can match nonuniform data geometry better than a fixed evenly spaced grid, but its quality depends on the training distribution and distance metric. For search, distances to representatives approximate original distances and can change neighbor order.

## One example

Let a toy two-dimensional codebook contain [0,0] and [2,2]. Input [1.8,2.1] is encoded by index 1 and reconstructed as [2,2]. Its squared error is .2 squared plus -.1 squared, or .05. One binary index identifies the representative, but this does not mean the whole archive costs one bit: the two vectors in the shared codebook must also be stored.

## Boundaries and check

A single whole-vector codebook can need many representatives in high dimension. Factorized subspace codebooks offer another trade-off, not a definition of all vector quantization. Check final distortion, rare-region error, code utilization and distribution-shift sensitivity. For an index, evaluate recall against exact original vectors; for compressed training features, evaluate downstream quality. A low reconstruction error is not proof that label-relevant distinctions survived. Validate out-of-range indices and version codebooks with codes so old indices cannot silently decode under different representatives.

**Check:** Does assigning the same code imply two inputs were identical? No. It says they were mapped to the same representative under a lossy encoding.

## Prerequisites

- [[k-means-clustering]]
- [[arithmetic]]

## Sources

- <https://github.com/facebookresearch/faiss/wiki/Faiss-building-blocks:-clustering,-PCA,-quantization>
