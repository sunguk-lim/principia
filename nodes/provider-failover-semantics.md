---
id: provider-failover-semantics
title: Provider Failover Semantics
summary: Provider failover defines when a model request can be retried or routed elsewhere while preserving policy, compatibility, cost, and side-effect boundaries.
type: concept
tags: [ml/llm/inference]
prereqs: [tool-call-execution-contract, load-balancing, measurement]
sources: [https://openrouter.ai/docs/guides/routing/provider-selection]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Provider Failover Semantics

## Summary

A model router may try another provider when the preferred endpoint is unavailable. **Provider failover semantics** specify the triggering failure, eligible alternatives, request compatibility, retry limit, and what the caller is told. “Automatic failover” does not mean the replacement model behaves identically or that a request can always be repeated safely.

## Grounded explanation

Choose an allowed provider set and order under [[load-balancing]], and apply data-policy, region, model, context, tool, and cost constraints before sending the request. OpenRouter's provider-selection documentation exposes fallback controls and preferred-provider ordering; those are routing features, not application-level guarantees of semantic equivalence. Test whether the router falls back on connection errors, timeouts, rate limits, and provider errors, and whether a partially streamed response is ever retried.

A plain inference call may be repeatable, but a model output that has already led to a tool effect is not. The [[tool-call-execution-contract]] requires the application to reconcile tool-call IDs and side effects before issuing any new call. Even without tools, a retry can double token charges or produce different text. Preserve a request ID and record provider, model revision, attempt count, latency, cost, and terminal error without logging private prompts unnecessarily.

For example, a primary endpoint times out after generating part of a streamed answer. A fallback might answer differently or repeat already emitted text. An application should define whether it stops, restarts a new response with a visible boundary, or asks the user to retry; silently concatenating two streams is incorrect. With [[measurement]], compare success rate, p95 latency, quality, policy compliance, and cost against no-fallback and single-provider baselines under controlled faults.

## Prerequisites

- [[tool-call-execution-contract]]
- [[load-balancing]]
- [[measurement]]

## Sources

- [OpenRouter provider selection](https://openrouter.ai/docs/guides/routing/provider-selection): provider preferences and fallback controls.
