---
id: late-interaction-retrieval
title: Late-Interaction Retrieval
summary: Late-interaction retrieval keeps multiple query and document embeddings separate until scoring, preserving fine-grained matches while allowing document representations to be computed before queries arrive.
type: concept
tags: [ml/information-retrieval]
prereqs: [embedding, vector-dot-product, nearest-neighbor-search]
sources: [https://arxiv.org/abs/2004.12832]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Late-Interaction Retrieval

## Summary

**Late-interaction retrieval** encodes a query and a document independently into multiple [[embedding]] vectors, then delays their interaction until ranking. It retains token-level matching signals without running one joint model over every query-document pair.

## Grounded explanation

A single-vector retriever compresses each document into one embedding before search. That makes [[nearest-neighbor-search]] efficient, but distinct clues inside a long document must share one vector. A fully joint reranker preserves detailed query-document interactions, but it must process each candidate together with the query and therefore cannot precompute the complete document-side representation.

Late interaction occupies the middle. Let query token $i$ have embedding $q_i$, and document token $j$ have embedding $d_j$. A ColBERT-style score is

$$
S(q,d)=\sum_i \max_j(q_i \cdot d_j).
$$

Here $q_i \cdot d_j$ is the [[vector-dot-product]] similarity between one query token and one document token. For each query token, the score keeps its strongest document-token match; summing those maxima rewards a document that covers multiple parts of the query. The document vectors $d_j$ do not depend on the query, so they can be computed and indexed in advance.

### Worked example

Suppose a two-token query is compared with three document tokens. Their dot-product similarities are

| | $d_1$ | $d_2$ | $d_3$ |
|---|---:|---:|---:|
| $q_1$ | 0.9 | 0.2 | 0.1 |
| $q_2$ | 0.1 | 0.3 | 0.8 |

The strongest match for $q_1$ is $0.9$, and the strongest for $q_2$ is $0.8$, so $S(q,d)=0.9+0.8=1.7$. The two clues can be found in different document positions; neither has to dominate one pooled document vector.

The retained detail has a cost. A document with 180 retained token vectors needs far more index space and query-time comparisons than one pooled vector. Compression, token pruning, and a cascade that first retrieves a small candidate set can reduce that cost, but each can discard the fine-grained evidence late interaction was meant to preserve. Evaluate ranking quality, index bytes, candidate recall, throughput, and tail latency together at the intended corpus size.

## Prerequisites

- [[embedding]]
- [[vector-dot-product]]
- [[nearest-neighbor-search]]

## Sources

- [Khattab and Zaharia, “ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT”](https://arxiv.org/abs/2004.12832): introduces independently encoded query/document representations and the late-interaction scoring architecture.
