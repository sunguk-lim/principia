---
id: reciprocal-rank-fusion
title: Reciprocal Rank Fusion
summary: Reciprocal rank fusion combines result lists by summing a decreasing reciprocal contribution from each list position, without requiring comparable scores.
type: concept
tags: [ml/information-retrieval]
prereqs: [arithmetic]
sources: [https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Reciprocal Rank Fusion

## Summary

**Reciprocal rank fusion (RRF)** merges several ranked result lists by giving a document the sum of reciprocal contributions based on its rank in each list, avoiding direct comparison of incompatible relevance scores.

## Grounded explanation

For document $d$, lists $R_1,\ldots,R_m$, and constant $k>0$,

$$\operatorname{RRF}(d)=\sum_{i:d\in R_i}\frac{1}{k+\operatorname{rank}_{R_i}(d)}.$$

Rank starts at 1. The [[arithmetic]] uses only order, so a cosine score of 0.8 need not be placed on the same scale as a lexical score of 12. The constant $k$ softens the gap between early and later positions.

### Worked example

Use $k=10$. Document A ranks 1st in list 1 and 5th in list 2, so its score is $1/11+1/15\approx0.1576$. Document B ranks 2nd only in list 1, scoring $1/12\approx0.0833$. A wins because independent lists support it, even though one list places it fifth.

RRF is robust and needs little tuning, but it discards score magnitude: a decisive first-place margin and a near tie look identical once converted to ranks. The result window must also be wide enough; a document absent from every retrieved window contributes zero.

## Prerequisites

- [[arithmetic]]

## Sources

- Elastic documentation, “Reciprocal rank fusion” — formula, rank constant, and multi-retriever use.
