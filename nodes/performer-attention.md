---
id: performer-attention
title: Performer Attention
summary: Performer attention uses positive random feature maps to approximate the softmax attention kernel while permitting linear-sequence aggregation.
type: concept
tags: [ml/llm/architecture]
prereqs: [linear-transformer-attention, transformer-attention, measurement]
sources: [https://arxiv.org/abs/2009.14794]
status: explained
created: 2026-10-11
updated: 2026-10-11
---

# Performer Attention

## Summary

[[linear-transformer-attention]] gets linear sequence scaling by factoring a query–key similarity into feature maps. Performer asks a narrower question: can such a feature map approximate the exponential kernel used by softmax [[transformer-attention]] rather than replacing it with an unrelated similarity? Its FAVOR+ method uses positive orthogonal random features to estimate that kernel.

## Mechanism and trade-offs

Map each query and key into `m` nonnegative random features, then accumulate feature-weighted values and normalizers. The associative computation avoids materializing all `n²` scores when `m` stays fixed. Random features introduce approximation error; increasing `m` may improve fidelity but raises compute and memory. Positivity helps keep the normalization well behaved, but finite precision and small denominators still require care. A causal implementation must maintain prefixes rather than mix future tokens into the running summary.

Unlike Linformer's learned projection of the sequence axis, Performer approximates the attention kernel through a feature map. It does not assume the attention matrix is low rank in the same way. The paper provides theoretical and empirical support under its assumptions; a claim of uniform superiority over exact attention, sparse methods, or optimized GPU kernels would go beyond that evidence.

Evaluate feature counts on held-out tasks, especially exact-token retrieval and long contexts. Use fixed model quality and hardware conditions where possible, measure approximation error against exact attention on small analyzable inputs, and track training stability, throughput, peak memory, and tail latency with [[measurement]]. Compare both full attention and a simpler linear feature-map baseline.

## Prerequisites

- [[linear-transformer-attention]]
- [[transformer-attention]]
- [[measurement]]

## Source

- [Choromanski et al., “Rethinking Attention with Performers”](https://arxiv.org/abs/2009.14794).
