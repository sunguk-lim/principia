---
id: model-alias-pinning
title: Model Alias Pinning
summary: Model alias pinning distinguishes a moving provider-selected model name from a fixed model revision, choosing controlled upgrades when reproducibility and compatibility matter.
type: concept
tags: [ml/model-portability]
prereqs: [provider-capability-matrix, progressive-model-rollout]
sources: [https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions, https://openrouter.ai/docs/guides/overview/models]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Model Alias Pinning

## Summary

A model name may identify a fixed revision or a **moving alias** that resolves to a different model later. **Model alias pinning** is the choice to use an explicit tested revision for reproducible production behavior, or to accept automatic movement and its operational risk. The syntax alone is not enough: providers differ, and even dateless identifiers can be fixed snapshots.

## Grounded explanation

A moving alias reduces manual migration but can change model behavior without an application code edit. Structured output, tool-call shape, latency, price, context limit, safety behavior, and availability may all differ after resolution changes. An explicit model revision makes comparisons and rollback easier, though it still needs lifecycle monitoring because fixed revisions can be retired. The [[provider-capability-matrix]] should record the requested string, resolved model identity where available, provider route, date, and observed behavior.

For example, an application using a vendor's “latest” alias might pass today's tool tests and fail after the alias points to a new model with different argument handling. Pinning a tested ID avoids that silent migration. A staging environment may instead deliberately follow the alias to detect upcoming changes. [[progressive-model-rollout]] can then compare the new revision with the current one on representative requests before promotion, with a rollback path.

Do not infer that every dateless ID moves. Anthropic documents dateless canonical IDs that are pinned snapshots for its newer generation, while earlier short aliases can resolve to dated snapshots. A router's `~` or other alias convention is its own contract. Verify the specific provider's primary documentation and, when possible, the resolved response metadata. Test at least output schema, tool semantics, safety boundaries, cost, and latency across the change. Track deprecation dates for the pinned revision so reproducibility does not become an unmaintained endpoint.

## Prerequisites

- [[provider-capability-matrix]]
- [[progressive-model-rollout]]

## Sources

- [Anthropic model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions): fixed IDs versus earlier aliases.
- [OpenRouter models guide](https://openrouter.ai/docs/guides/overview/models): model catalog and routing context.
