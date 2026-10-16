---
id: retrieval-chunking
title: Retrieval Chunking
summary: Retrieval chunking divides source documents into indexed evidence units, trading passage precision against context loss, duplication, metadata integrity, and recall.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation]
sources: [https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Retrieval Chunking

## Summary

A [[retrieval-augmented-generation]] system rarely indexes a long document as one indivisible vector. **Chunking** chooses the units that retrieval can find and the generator can cite. Too-large chunks dilute a specific answer and consume context; too-small chunks separate facts from their qualifiers. The right boundary depends on the query and document structure, not one universal token count.

## Grounded explanation

A chunk must preserve its source document ID, version, access scope, position, and enough neighboring context to interpret it. Fixed-size windows are simple and predictable; sentence, heading, or layout-aware splits may preserve meaning better but can create variable lengths. Overlap repeats boundary text to reduce split facts, at the cost of larger indexes and duplicate retrieval hits. For example, splitting a policy's refund deadline from its jurisdiction exception can yield an apparently relevant but misleading passage. Parent-document expansion can retrieve a small matching chunk, then pass a larger authorized section for answer construction.

A chunk boundary is also an authorization boundary. If one source contains material with different permissions, attaching only document-level metadata can leak restricted text. Version and citation metadata must follow the chunk through indexing, retrieval, reranking, and prompt assembly.

## Validation

Compare chunk sizes and structural splitting on labeled questions at the same embedding model, candidate budget, and context limit. Measure supporting-passage recall, answer faithfulness, citation correctness, duplicate-hit rate, index size, latency, and unauthorized retrieval. Test table rows, headings, and cross-boundary conditions, not just plain paragraphs. Tune overlap with measured boundary failures rather than assuming more duplication always helps.

## Prerequisites

- [[retrieval-augmented-generation]]

## Sources

- [Azure AI Search, chunking documents for vector search](https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents).
