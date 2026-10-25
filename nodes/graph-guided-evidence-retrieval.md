---
id: graph-guided-evidence-retrieval
title: Graph-Guided Evidence Retrieval
summary: Graph-guided evidence retrieval uses entity identities and typed relationships to select source-grounded context while bounding traversal, freshness and authorization.
type: concept
tags: [ml/information-retrieval]
prereqs: [knowledge-graph, retrieval-augmented-generation, retrieval-authorization-boundary]
sources: [https://microsoft.github.io/graphrag/query/local_search/, https://microsoft.github.io/graphrag/index/default_dataflow/]
status: explained
created: 2026-10-26
updated: 2026-10-26
---

# Graph-Guided Evidence Retrieval

## Meaning

Graph-guided evidence retrieval uses linked entities to find the evidence needed for an answer, including bridge facts that a single similarity query may rank poorly. Its output is a bounded, authorized evidence set, not a graph path accepted as unquestionable truth. This is a retrieval architecture, not just a graph storage format.

## Mechanism

A [[knowledge-graph]] represents stable entities and directed, typed relation claims. During indexing, connect each extracted entity and relation to its supporting text unit and source revision. Resolve identities carefully: two people with the same name are not automatically one entity. Retain conflicting or uncertain claims with provenance rather than merging them into an invented fact.

At query time, resolve one or more starting entities using exact identifiers, search, or semantic matching. Select relevant relation types and expand a bounded neighborhood or explicit path pattern. Recover the source passages for the candidate entities and relationships, rank/filter them, and fit supported evidence into the generator's context. This composes with [[retrieval-augmented-generation]]: embedding similarity can find the starting entities, and ordinary passages can complement the structured evidence. Microsoft's GraphRAG local search is one primary example combining entity, relationship and text-unit context; it is not a claim that every graph retriever uses the same traversal algorithm or always finds all relevant paths.

Apply the [[retrieval-authorization-boundary]] before exposing restricted entities, edges, passages, counts or derived answers. An allowed start and end do not authorize a hidden bridge. A bounded hop count and relation whitelist limit expansion but do not by themselves enforce access policy. Track source updates and deletions so a cached path does not outlive its supporting records.

## Worked example

Use three fictional records: D1 states that vendor V supplies component C; D2 states that product P contains C; D3 states that P has a pending audit. The question asks which vendors supply components in products with pending audits. Start from the pending product P, follow its component relation to C, then the inverse of the supplier relation to V. The answer cites D1, D2 and D3, so the bridge in D2 remains visible instead of disappearing behind a confident conclusion.

If the user cannot access D2, that path is not available evidence for this caller. If D2 is stale and P no longer contains C, the old path is invalid. If D1 merely says V *might* supply C, do not upgrade it to a confirmed supplier. These are distinct failures even though the same three graph vertices exist.

## Validation and alternatives

Evaluate entity resolution, edge extraction, bridge recall, complete-path support, permission leakage, freshness, context size and end-to-end answer faithfulness separately. Include missing edges, ambiguous identifiers and contradictory revisions. Compare with lexical/vector retrieval plus bounded query expansion and with a structured database query when the required relations are already authoritative. A graph can improve access to relationships; it cannot manufacture absent evidence or prove causation from connectivity. Global community-summary GraphRAG and an agent choosing several retrieval tools solve different control/coverage problems and can be combined with this local retrieval design.

## Check your understanding

**Question:** Two authorized endpoint entities are connected only by a restricted document. Can the generator use that path? **Answer:** No. Authorization applies to the evidence supporting the relationship, not merely the endpoint labels.

## Prerequisites

- [[knowledge-graph]]
- [[retrieval-augmented-generation]]
- [[retrieval-authorization-boundary]]

## Sources

- <https://microsoft.github.io/graphrag/query/local_search/>
- <https://microsoft.github.io/graphrag/index/default_dataflow/>
