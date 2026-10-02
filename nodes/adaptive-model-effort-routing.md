---
id: adaptive-model-effort-routing
title: Adaptive Model-and-Effort Routing
summary: Adaptive model-and-effort routing selects a model and inference budget per request using expected quality, latency, cost, and switching penalties rather than one fixed model.
type: concept
tags: [ml/llm/inference]
prereqs: [decision-score-action-gate, inference-cost-break-even, prefix-caching, latency-percentile]
sources: [https://openrouter.ai/docs/guides/routing/routers/auto-router, https://openrouter.ai/typesafe/jev-router]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Adaptive Model-and-Effort Routing

## Summary

A routing layer can choose both *which* model handles a request and *how much* reasoning or compute budget it receives. The objective is to satisfy a task-quality target at acceptable latency and cost, not simply to select the cheapest model on every turn.

## Grounded explanation

A router observes permitted request features such as task type, input size, tool needs, and prior failures. A bounded decision then selects a model and effort tier. A [[decision-score-action-gate]] must convert uncertain model predictions into allowed choices and an abstain or fallback path. The routing policy should reject models lacking required modalities or tools before cost optimization.

The decision is sequential. In a continuing conversation, switching models can lose reusable prompt state and [[prefix-caching]] benefits; staying on a slightly more expensive model may cost less than a cold switch. Likewise, raising effort on the current model can improve a hard turn without a provider change. Compare expected gain against extra tokens, latency, cache loss, and the probability of retry or escalation. This is distinct from GPU model residency: routing chooses an endpoint or model policy, while residency manages loaded weights on serving hardware.

Build a fixed-model baseline on the same labeled task mix. Replay or randomize routing decisions with enough overlap to estimate task success, p50/p95 latency, accepted-answer cost, cache-hit rate, switching frequency, and failure rate. A router's explanation metadata is useful for debugging but not proof that its choice was optimal. Monitor distribution shift and keep explicit fallback behavior; a timeout or malformed routing answer needs a documented policy, not an implicit assumption that another router will intervene.

## Prerequisites

- [[decision-score-action-gate]]
- [[inference-cost-break-even]]
- [[prefix-caching]]
- [[latency-percentile]]

## Sources

- [OpenRouter Auto Router documentation](https://openrouter.ai/docs/guides/routing/routers/auto-router): public example of prompt-dependent model selection and cost tiers.
- [OpenRouter Jev Router API](https://openrouter.ai/typesafe/jev-router): documented model-and-effort routing surface; product-specific claims require workload testing.
