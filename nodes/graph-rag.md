---
id: graph-rag
title: GraphRAG
summary: GraphRAG builds a knowledge-graph index and hierarchical community summaries so retrieval-augmented generation can answer corpus-wide questions that are poorly served by a few independently retrieved chunks.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, knowledge-graph]
sources: [https://arxiv.org/abs/2404.16130]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# GraphRAG

## Summary

**GraphRAG** extends [[retrieval-augmented-generation]] for global questions over a corpus. It extracts entities and relationships into a [[knowledge-graph]], groups related entities, prepares summaries of those communities, and combines community-level partial answers for a query.

## Grounded explanation

Ordinary RAG is effective when a question has a few locally relevant passages. A query such as “What themes recur across this collection?” may depend on evidence spread across many documents, so returning only the top few independent chunks can omit entire regions.

GraphRAG adds an offline index-building phase. First, a model extracts entity and relationship claims from source text to form a [[knowledge-graph]]. A community-detection procedure groups densely related entities. The system then prepares a summary for each community, often at several hierarchy levels. At query time, relevant community summaries produce partial responses, and a final reduction combines them.

Suppose a corpus has 1,000 reports in four topic communities. A chunk retriever returns five passages concentrated in the community whose wording most resembles “risk.” A global GraphRAG pass can instead obtain one partial account from each relevant community and reduce those accounts into a broader answer. That improves coverage only if extraction, grouping, summaries, and reduction preserve the evidence.

The graph is generated evidence, not ground truth. Missed entities remove paths; merged identities create false relationships; community summaries can omit minority evidence; and the extra indexing and model calls increase cost and update latency. A local factual question may still be better served by ordinary chunk retrieval.

Evaluate global and local questions separately. Measure claim coverage, citation support, contradiction rate, latency, index cost, and update behavior against chunk-RAG and long-context baselines. Trace final statements back through partial answers to source passages. Rebuild or incrementally validate affected graph regions when documents change rather than assuming an old summary remains current.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[knowledge-graph]]

## Sources

- [Edge et al., “From Local to Global: A Graph RAG Approach to Query-Focused Summarization”](https://arxiv.org/abs/2404.16130): entity graph construction, community summaries, map-reduce answering, and evaluation on global corpus questions.
