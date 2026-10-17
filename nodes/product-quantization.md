---
id: product-quantization
title: Product Quantization
summary: Product quantization splits a vector into subvectors and encodes each with a learned subspace codebook, enabling compact storage and approximate distance evaluation.
type: concept
tags: [databases/vector]
prereqs: [k-means-clustering, tensor, quantization]
sources: [https://faiss.ai/cpp_api/struct/structfaiss_1_1ProductQuantizer.html]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Product Quantization

## Summary

Product quantization splits a vector into subvectors and encodes each with a learned subspace codebook, enabling compact storage and approximate distance evaluation.

## Grounded explanation

Scalar [[quantization]] replaces each coordinate with a code. Product quantization instead replaces each *group of coordinates* with the index of a representative subvector. The vector is a one-dimensional [[tensor]]. Split its $d$ coordinates into $M$ equal groups of length $d/M$, assuming divisibility. Train a separate codebook of $K$ representative subvectors for each group, commonly using [[k-means-clustering]]. An encoded vector stores the $M$ selected codebook indices rather than its original coordinates.

Let $x_m$ denote group $m$, and let $c_{m,k}$ be representative $k$ in that group's codebook. Choose index $a_m$ minimizing the squared coordinate differences between $x_m$ and $c_{m,k}$. Reconstruction concatenates $c_{1,a_1},\ldots,c_{M,a_M}$. There are $K^M$ possible combinations, but only $MK$ representatives are stored. This product structure avoids learning one enormous codebook containing all combinations.

For an illustrative four-coordinate vector, use two groups and two representatives per group. If $x=[1,2,8,9]$ is assigned representatives $[1,1]$ and $[8,10]$, it reconstructs as $[1,1,8,10]$ and stores just two binary indices. The sum of squared reconstruction differences is $0^2+1^2+0^2+(-1)^2=2$. Those two bits exclude the cost of storing the shared codebooks and any per-vector identifiers or metadata.

Search need not reconstruct every vector. For a query, precompute its squared distance to each representative in each group. Approximate distance to an encoded database vector is the sum of $M$ table lookups, one per stored index. This works because squared Euclidean distance is additive across disjoint coordinate groups. Keeping the query uncompressed avoids adding query quantization error, but database distances remain approximate and can change neighbor rankings.

More bits per group increase representational capacity, codebook storage, and training requirements. The grouping can lose correlations between groups. Measure search recall against exact distances, memory including codebooks, build time, and query latency on held-out data. A codebook trained for squared Euclidean reconstruction need not optimize another similarity measure equally well. Product quantization is a vector coding mechanism, not a promise that any low-bit neural-network weight format will execute efficiently on a particular device.

## Prerequisites

- [[k-means-clustering]]
- [[tensor]]
- [[quantization]]

## Sources

- <https://faiss.ai/cpp_api/struct/structfaiss_1_1ProductQuantizer.html>
