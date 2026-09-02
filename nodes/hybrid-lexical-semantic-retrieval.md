---
id: hybrid-lexical-semantic-retrieval
title: Hybrid Lexical–Semantic Retrieval
summary: Hybrid lexical–semantic retrieval runs exact-term and embedding-based retrieval in parallel and fuses their rankings into one result list.
type: concept
tags: [ml/information-retrieval]
prereqs: [lexical-retrieval, nearest-neighbor-search, reciprocal-rank-fusion]
sources: [https://machinelearningmastery.com/implementing-hybrid-semantic-lexical-search-in-rag]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Hybrid Lexical–Semantic Retrieval

## Summary

**Hybrid lexical–semantic retrieval** combines [[lexical-retrieval]] with embedding-based [[nearest-neighbor-search]], then uses a fusion rule such as [[reciprocal-rank-fusion]] to produce one ranking.

## Grounded explanation

The two retrievers fail differently. [[lexical-retrieval]] is strong on exact identifiers and rare wording but misses paraphrases. [[nearest-neighbor-search]] finds nearby meanings but may blur exact constraints. Hybrid retrieval preserves candidates from both before fusion rather than forcing either mechanism to solve the other's problem.

### Worked example

For query “GPU out of memory error 137,” the lexical list is `[D1, D3, D5]`, where D1 contains the exact code. The semantic list is `[D2, D1, D4]`, where D2 explains memory exhaustion using different words. With RRF constant $k=10$, D1 scores $1/11+1/12\approx0.1742$, D2 scores $1/11\approx0.0909$, and D3 scores $1/12\approx0.0833$. D1 rises because both retrievers support it; D2 remains because semantic retrieval found the paraphrase.

Fusion should occur over sufficiently large per-retriever windows and be evaluated on judged queries. One aggregate metric can hide regressions, so inspect identifier-heavy, paraphrase-heavy, and mixed slices. Score-weighted fusion is another option, but it requires normalization because lexical and semantic scores have unrelated scales; rank fusion avoids that calibration problem.

## Prerequisites

- [[lexical-retrieval]]
- [[nearest-neighbor-search]]
- [[reciprocal-rank-fusion]]

## Sources

- Machine Learning Mastery, “Implementing Hybrid Semantic-Lexical Search in RAG” — BM25 plus semantic retrieval fused with RRF.
- Elastic documentation, “Reciprocal rank fusion.”
