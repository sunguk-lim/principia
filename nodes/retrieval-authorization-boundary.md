---
id: retrieval-authorization-boundary
title: Retrieval Authorization Boundary
summary: A retrieval authorization boundary enforces a caller's document permissions before evidence enters a model context, independent of ranking or answer quality.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, measurement]
sources: [https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search]
status: explained
created: 2026-10-01
updated: 2026-10-02
---

# Retrieval Authorization Boundary

## Summary

A model cannot reliably ignore text it was not supposed to see. In a retrieval-backed application, the caller's access rights must filter documents *before* selected passages enter the model prompt. This boundary is independent of semantic relevance and output filtering: a highly relevant document may still be unauthorized.

## Grounded explanation

Associate each indexed document or chunk with an authoritative resource identity and access-control metadata. At query time, derive the caller identity from the application, not from model text, and apply a server-enforced filter or authorization check before returning content to [[retrieval-augmented-generation]]. If permissions vary within a document, a document-level label can be too coarse; chunk provenance and inherited permissions must match the actual disclosure unit. Revalidate when ACLs change, caches expire, or documents are reindexed.

Suppose employee A can see policy files but not another employee's payroll record. A vector search may rank the payroll record first for a benefits question. The authorization boundary removes it before prompt assembly. Asking the model to ignore it after retrieval is too late: the secret has crossed into context and may leak through paraphrase, tool calls, traces, or logs. Conversely, a permission filter is not a relevance ranker; it says what may be considered, not what answers the question.

Test the boundary with role-crossing queries, mixed-permission documents, revoked access, stale index/cache entries, and prompt-injection strings that claim higher authority. Measure unauthorized retrieval rate (the target is zero for tested scopes), permitted recall, latency, and audit completeness using [[measurement]]. Keep the output path and training-data governance as separate controls. An output detector cannot repair an authorization failure already visible to the model.

## Tenant-partitioned indexing

A shared index can carry tenant and resource identity on every chunk, with the search service enforcing an authenticated filter before candidates are returned. Separate indexes can reduce accidental cross-tenant mixing but add provisioning and operational overhead; neither layout is a substitute for query-time authorization and revocation handling. A partition key derived from model text or client-supplied metadata is not an authorization boundary. Test mixed-tenant batches, cache-key isolation, document moves, changed ACLs, and reindexing so no stale chunk crosses the caller's boundary. Compare permitted recall and latency as well as leakage across layouts.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[measurement]]

## Sources

- [Azure AI Search security trimming](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search): primary documentation for permission-filtered search results.
