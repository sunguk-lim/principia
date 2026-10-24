---
id: shared-retrieval-service
title: Shared Retrieval Service
summary: A shared retrieval service separates versioned ingestion and permission-scoped querying from individual applications so multiple callers can reuse one evidence infrastructure.
type: concept
tags: [ml/information-retrieval]
prereqs: [background-document-indexing, retrieval-authorization-boundary]
sources: [https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview, https://modelcontextprotocol.io/specification/2025-06-18/server/tools, https://learn.microsoft.com/en-us/azure/search/search-indexer-overview]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Shared Retrieval Service

## Meaning

A shared retrieval service is an application-independent boundary for ingesting and searching evidence. A chatbot and an agent can use the same query service without each owning another connector, chunking pipeline and index. The defining contribution is shared ownership and a stable contract, not a particular database or search algorithm.

## Mechanism

The ingestion plane uses [[background-document-indexing]] to extract, version and publish evidence. The query plane authenticates its caller, applies [[retrieval-authorization-boundary]], executes permitted search and returns evidence with source identity, version and location. [[dataset-lineage]] connects results to the source and transformation versions that created them. Query and ingestion failures have different effects: a delayed import can leave a healthy search endpoint returning stale evidence.

Specify corpus scope, freshness, supported filters, result limits, ordering, timeouts, version semantics and error states in the API contract. A tool protocol can expose that API to a model, but the model does not become the owner of permissions or consistency. A shared index also does not imply that every caller should see the same documents or use the same ranking configuration.

## Worked example

Application A and agent B query source D at version 7. When D changes to version 8, one ingestion pipeline stages the new chunks, validates completion and changes the active version. Both callers can then receive version 8 evidence without separately rebuilding connectors. If ingestion fails halfway, the service either retains complete version 7 with an explicit freshness boundary or exposes documented partial coverage. Mixing pages from versions 7 and 8 while claiming one coherent current document is not safe publication.

Centralization reduces duplicate work but creates a shared failure domain and can couple workloads through capacity or ranking changes. Compare with app-owned indexes on isolation, permitted recall, latency, cost, deployment independence and revocation delay. Test tenant-crossing queries, stale caches, document deletion, embedding migrations and ingestion backlogs. Hybrid search, reranking and iterative agent search can be layered on this boundary, but none is implied merely by extracting search into a service.

## Check your understanding

Does a working shared search endpoint prove fresh evidence? No. Query availability and ingestion freshness are separate service properties.

## Prerequisites

- [[background-document-indexing]]
- [[retrieval-authorization-boundary]]

## Sources

- <https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview>
- <https://modelcontextprotocol.io/specification/2025-06-18/server/tools>
- <https://learn.microsoft.com/en-us/azure/search/search-indexer-overview>
