---
id: retrieval-augmented-generation
title: Retrieval-Augmented Generation
summary: Retrieval-augmented generation combines a generator's parametric model with evidence selected from an external index at query time.
type: concept
tags: [ml/information-retrieval]
prereqs: [vector-database, context-window, embedding]
sources: [https://arxiv.org/abs/2005.11401]
status: explained
created: 2026-06-23
updated: 2026-09-10
---

# Retrieval-Augmented Generation

## Summary

**Retrieval-augmented generation** (RAG) selects evidence from an external corpus and supplies it to a generator. It combines parametric model behavior with query-time access to non-parametric memory.

## Grounded explanation

A common pipeline has two phases:

1. **Indexing:** split source documents into addressable units, attach provenance, compute an [[embedding]] or lexical representation, and store searchable records.
2. **Query time:** transform the question into a retrieval query, rank candidate records, select evidence that fits the [[context-window]], generate an answer, and retain citations to the retrieved records.

Lewis et al. introduced RAG formulations that combined a pretrained sequence-to-sequence model with a dense Wikipedia index. One formulation conditioned the whole generated sequence on the same retrieved documents; another allowed the latent retrieved document to vary per generated token. Modern systems use many other retrievers and generators, so a [[vector-database]] is common but not definitional: lexical, hybrid, structured-record, or tool-based retrieval can also supply evidence.

Retrieval makes external information available; it does not guarantee that the selected passages contain the answer or that the generator follows them. Citations prove which records were presented only when the system preserves provenance, and they prove answer support only after checking that each claim is entailed by the cited evidence. Private knowledge is safe only when storage, retrieval filters, prompts, logs, caches, and model endpoints enforce the required boundary.

### Failure decomposition

Separate failures by stage:

- **Corpus and indexing:** missing documents, stale versions, bad parsing, unsuitable chunk boundaries, or lost metadata.
- **Query and retrieval:** vocabulary mismatch, embedding drift, weak recall, missing filters, or poor ranking.
- **Context assembly:** redundant evidence, conflicting versions, truncation, or instructions embedded in untrusted documents.
- **Generation:** unsupported synthesis, citation mismatch, refusal failure, or failure to acknowledge insufficient evidence.

Adding agent loops, query rewriting, reranking, or more retrieved passages can improve one stage while increasing latency, cost, attack surface, and error propagation. Compare every addition with a simpler retrieve-once baseline.

### Validation

Build an evaluation set with answer-bearing source records and time or access-control slices. Report retrieval recall at several cutoffs, ranking metrics, answer correctness, claim-level citation support, abstention when evidence is absent, freshness after updates, and authorization leakage tests. Measure end-to-end latency and cost as well as stage-level timings. Use counterfactual tests that remove or replace evidence to verify that answers actually depend on retrieval.

## Prerequisites

- [[vector-database]]
- [[context-window]]
- [[embedding]]

## Sources

- [Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”](https://arxiv.org/abs/2005.11401): formulates generation with parametric and dense non-parametric memory and evaluates sequence-level and token-level document conditioning.
