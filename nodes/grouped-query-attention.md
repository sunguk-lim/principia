---
id: grouped-query-attention
title: Grouped-Query Attention
summary: Grouped-query attention assigns several query heads to each key/value head, choosing a tunable point between full multi-head attention and single-KV-head multi-query attention.
type: concept
tags: [ml/llm/architecture]
prereqs: [multi-query-attention, kv-cache]
sources: [https://arxiv.org/abs/2305.13245]
status: explained
created: 2026-10-15
updated: 2026-10-15
---

# Grouped-Query Attention

## Summary

**Grouped-query attention** (GQA) uses fewer key/value heads than query heads, but more than the single shared pair in [[multi-query-attention]]. It trades cache traffic and capacity against representation flexibility.

## Grounded explanation

Let $H_q$ be the number of query heads and $H_{kv}$ the number of key/value heads, with query heads assigned to KV groups. Full multi-head attention has $H_{kv}=H_q$; MQA has $H_{kv}=1$; GQA selects an intermediate value. Each query head computes its own attention weights but reads the key/value sequence of its group. The [[kv-cache]] therefore scales approximately as $2LTH_{kv}db$ for $L$ layers, $T$ cached tokens, head width $d$, and bytes per element $b$. This is a cache-size relationship, not a universal latency formula.

A smaller $H_{kv}$ can reduce memory bandwidth and serve more concurrent sequences within capacity. It can also constrain the distinct past representations available to query heads. More KV groups may preserve quality better, but can increase cache traffic. Hardware memory-level parallelism and kernel implementation can make the latency curve nonlinear: twice as many groups need not mean twice the decode time. Compare several group counts on the same checkpoint family, precision, batch, sequence distribution, and hardware.

Ainslie et al. describe converting an existing multi-head checkpoint by pooling key and value projections within each group and continuing pretraining. That is a documented adaptation recipe, not a guarantee that an arbitrary model can be converted with the same compute or quality outcome. Validate conversion on held-out tasks and test long-context quality as well as first-token latency, inter-token latency, throughput, cache bytes, and peak memory. Distinguish a model trained with GQA from a converted checkpoint when interpreting results.

## Prerequisites

- [[multi-query-attention]]
- [[kv-cache]]

## Sources

- [Ainslie et al., “GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints”](https://arxiv.org/abs/2305.13245): defines grouped KV heads and studies checkpoint conversion.
