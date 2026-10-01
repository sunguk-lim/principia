---
id: user-data-rag-integration
title: User-Data RAG Integration
summary: User-data RAG integration connects delegated external sources to a per-user indexed corpus and enforces identity, freshness, and evidence quality throughout retrieval and generation.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, connector-oauth-scope-management, retrieval-authorization-boundary, ml-system-freshness]
sources: [https://arxiv.org/abs/2005.11401, https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search, https://developers.google.com/identity/protocols/oauth2/scopes]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# User-Data RAG Integration

## Summary

**User-data RAG integration** makes a user's external files searchable to an assistant without confusing connector access, indexing, retrieval, and generation. The integration is an end-to-end architecture; each stage has a different correctness and security contract.

## Grounded explanation

A user authorizes a source under [[connector-oauth-scope-management]] and selects its resources. The application imports content, preserves source ID, owner, revision, ACL, and fetch time, then parses and chunks it for [[retrieval-augmented-generation]]. An indexer may run asynchronously; a connected folder is not necessarily searchable yet. At query time, resolve the caller's identity, enforce [[retrieval-authorization-boundary]] before prompt assembly, retrieve candidate chunks, and ask the generator to ground claims in those chunks with source provenance.

A practical failure is revocation after indexing. The connector can lose access while old chunks remain searchable. A good design couples ACL updates and deletion/tombstones to index visibility and measures the lag as part of [[ml-system-freshness]]. Another failure is missing or poorly parsed content: no ranking or larger model can recover an unindexed page. Diagnose connector coverage, parse quality, index lag, authorized recall, answer support, and abstention separately.

For example, two coworkers connect folders with similarly named reports. The index may share infrastructure, but query-time filters must prevent one coworker from seeing the other's report. A successful demo on one folder does not establish this property. Test cross-user and cross-tenant queries, scope revocation, deletes, changed documents, malformed files, unsupported formats, and prompt injections in source text. Compare end-to-end latency, cost, and answer quality with a simpler single-source baseline.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[connector-oauth-scope-management]]
- [[retrieval-authorization-boundary]]
- [[ml-system-freshness]]

## Sources

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401): retrieval and generation separation.
- [Azure AI Search security trimming](https://learn.microsoft.com/en-us/azure/search/search-security-trimming-for-azure-search): identity-filtered retrieval.
- [Google OAuth 2.0 scopes](https://developers.google.com/identity/protocols/oauth2/scopes): delegated source permissions.
