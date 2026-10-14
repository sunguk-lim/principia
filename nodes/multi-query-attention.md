---
id: multi-query-attention
title: Multi-Query Attention
summary: Multi-query attention lets many query heads share one key head and one value head, reducing per-token KV-cache traffic during incremental decoding at a possible quality cost.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, kv-cache]
sources: [https://arxiv.org/abs/1911.02150]
status: explained
created: 2026-10-15
updated: 2026-10-15
---

# Multi-Query Attention

## Summary

**Multi-query attention** (MQA) keeps multiple query projections but shares one key projection and one value projection across those query heads. Its purpose is to reduce the size of the [[kv-cache]] loaded at each decode step, not to remove the attention computation or guarantee faster end-to-end serving.

## Grounded explanation

In ordinary multi-head [[transformer-attention]], each of $H_q$ query heads has corresponding key and value heads. At a new token, the attention kernel reads earlier keys and values to compute each query head's result. With one key/value head shared by all queries, the cached state has roughly one head's key/value vectors per layer and token instead of $H_q$ heads' vectors, assuming equal head dimension and datatype. The query heads still differ, so they can apply different attention weights to the shared keys and values.

For $L$ layers, $T$ cached tokens, head width $d$, and $b$ bytes per element, an illustrative cache size is $2LTdb$ for MQA versus $2LTH_qdb$ for full multi-head attention. This ratio concerns KV storage and traffic, not all inference memory: model weights, activations, metadata, and scheduler overhead remain. The shared representation can also restrict how independently heads encode past tokens. The original MQA paper reports a quality/speed trade-off for its own models and hardware; that measurement is not portable to another checkpoint.

Compare matched architectures and training budgets before attributing quality differences to KV sharing. At serving time, measure cache bytes, achieved bandwidth, time to first token, inter-token latency, throughput, and quality across context lengths and concurrency. If decoding is limited elsewhere, a smaller cache may not improve latency. Grouping query heads into several KV groups is a separate middle-ground design rather than an MQA implementation detail.

## Prerequisites

- [[transformer-attention]]
- [[kv-cache]]

## Sources

- [Shazeer, “Fast Transformer Decoding: One Write-Head is All You Need”](https://arxiv.org/abs/1911.02150): proposes shared key/value heads for faster incremental decoding and reports model-specific trade-offs.
