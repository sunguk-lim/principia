---
id: user-data-rag-integration
title: User-Data RAG Integration
summary: User-data RAG integration connects delegated external sources to a per-user indexed corpus and enforces identity, freshness, and evidence quality throughout retrieval and generation.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, connector-oauth-scope-management, retrieval-authorization-boundary, ml-system-freshness]
sources: [https://arxiv.org/abs/2005.11401, https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search, https://developers.google.com/identity/protocols/oauth2/scopes, https://docs.onyx.app/admins/connectors/overview]
status: explained
created: 2026-10-02
updated: 2026-10-22
---

# User-Data RAG Integration

## Summary

**User-data RAG integration** makes a user's external files searchable to an assistant without confusing connector access, indexing, retrieval, and generation. The integration is an end-to-end architecture; each stage has a different correctness and security contract.

## Grounded explanation

A user authorizes a source under [[connector-oauth-scope-management]] and selects its resources. The application imports content, preserves source ID, owner, revision, ACL, and fetch time, then parses and chunks it for [[retrieval-augmented-generation]]. An indexer may run asynchronously; a connected folder is not necessarily searchable yet. At query time, resolve the caller's identity, enforce [[retrieval-authorization-boundary]] before prompt assembly, retrieve candidate chunks, and ask the generator to ground claims in those chunks with source provenance.

A practical failure is revocation after indexing. The connector can lose access while old chunks remain searchable. A good design couples ACL updates and deletion/tombstones to index visibility and measures the lag as part of [[ml-system-freshness]]. Another failure is missing or poorly parsed content: no ranking or larger model can recover an unindexed page. Diagnose connector coverage, parse quality, index lag, authorized recall, answer support, and abstention separately.

For example, two coworkers connect folders with similarly named reports. The index may share infrastructure, but query-time filters must prevent one coworker from seeing the other's report. A successful demo on one folder does not establish this property. Test cross-user and cross-tenant queries, scope revocation, deletes, changed documents, malformed files, unsupported formats, and prompt injections in source text. Compare end-to-end latency, cost, and answer quality with a simpler single-source baseline.

## Pre-indexed and query-time source access

Pre-indexing performs ingestion and searchable representation work before a user asks. Query-time source access asks the upstream service when needed, possibly through a connector or a tool. A common tool protocol does not dictate which model is used: an MCP server can search its own persistent index or forward a live query. Hybrid systems can combine both. Pre-indexing can amortize repeated queries but adds storage, ingestion cost, deletion handling and freshness lag; live access depends on upstream authorization, API latency, rate limits and availability. Neither architecture is universally faster or more reliable.

Consider a source update at 10:00, an index refresh at 10:20 and a question at 10:10. The index can return its last revision, while a live query may see the new one if the source exposes it. A source outage can reverse the availability result: an authorized cached revision may remain useful while live access fails. State the revision and age rather than presenting stale content as current. Revocation is different from benign staleness: a previously indexed private document must not stay visible merely because refresh failed.

Onyx's primary connector documentation describes periodic indexing, separate refresh/prune controls and connector-specific permission-sync behavior. It also warns that a public connector can expose otherwise private source content to all application users. These are configuration-dependent contracts, not proof of universal permission inheritance or an edition-independent feature. Evaluate the chosen deployment's coverage, source revision, permission/deletion lag, permitted recall, answer support and end-to-end tail latency against a live-query baseline using the same corpus and queries.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[connector-oauth-scope-management]]
- [[retrieval-authorization-boundary]]
- [[ml-system-freshness]]

## Sources

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401): retrieval and generation separation.
- [Azure AI Search security trimming](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search): identity-filtered retrieval.
- [Google OAuth 2.0 scopes](https://developers.google.com/identity/protocols/oauth2/scopes): delegated source permissions.

- <https://docs.onyx.app/admins/connectors/overview>
