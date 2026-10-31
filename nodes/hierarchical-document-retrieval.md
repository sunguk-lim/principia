---
id: hierarchical-document-retrieval
title: Hierarchical Document Retrieval
summary: Hierarchical document retrieval selects promising document or section branches before expanding their evidence, exchanging exhaustive scoring for structured search and pruning risk.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, graph, retrieval-authorization-boundary]
sources: [https://github.com/VectifyAI/PageIndex, https://arxiv.org/html/2610.35868v1]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Hierarchical Document Retrieval

## Meaning

Hierarchical document retrieval organizes evidence into a tree of documents, sections or topic groups. A query-guided selector opens promising branches and expands them toward source passages. The architectural contribution is where the search goes, not whether one particular score uses embeddings or generated text.

## Mechanism

In [[retrieval-augmented-generation]], selected evidence limits what can ground an answer. A tree is a [[graph]] with parent/child structure; internal entries describe their descendants using titles, page ranges or summaries. Start at an appropriate root, score or reason over children, retain a bounded number, then read or expand only those branches. An evidence check may trigger additional expansion. The [[retrieval-authorization-boundary]] applies before exposing summaries as well as full passages; a hierarchy must not leak protected metadata.

Layout-based document trees and corpus-level semantic trees are different construction choices. An LLM can generate navigation choices, while a bounded scorer can choose among the same branches. Calling the system vectorless describes one implementation path, not a ban on embeddings in offline construction or a proof that parsing and partitioning disappeared.

## Worked example

A report has Finance, Operations and Risk branches. A debt question selects Finance, whose summary points to Appendix G under Risk. The search opens Finance and that referenced appendix, then reads the source table and its year label. If it kept Finance alone and irrevocably pruned Risk, a perfect passage scorer inside Finance could not recover the missing table. A bounded cross-reference expansion or fallback search addresses this architectural failure without assuming summaries are infallible.

## Trade-offs and validation

Trees can preserve useful document context but depend on faithful layout extraction, summaries and stable structure. Tables can still be split or misparsed. Measure answer containment at each expansion level, citations and source fidelity, build/update cost, calls, latency and fallback rate. Compare dense, lexical, hybrid and hierarchical methods on identical documents and equal budgets. Dense retrieval can also use metadata filters, contextualized chunks and iterative expansion; hierarchy is not automatically more accurate. Rebuild or invalidate stale tree descriptions after document revisions.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[graph]]
- [[retrieval-authorization-boundary]]

## Sources

- <https://github.com/VectifyAI/PageIndex>
- <https://arxiv.org/html/2610.35868v1>
