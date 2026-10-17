---
id: cross-attention
title: Cross-Attention
summary: Cross-attention updates one sequence using queries from that sequence and keys and values from a separate context sequence, allowing different sequence lengths and directional conditioning.
type: concept
tags: [ml/deep-learning]
prereqs: [transformer-attention]
sources: [https://arxiv.org/html/1706.03762]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Cross-Attention

## Summary

Cross-attention updates one sequence using queries from that sequence and keys and values from a separate context sequence, allowing different sequence lengths and directional conditioning.

## Grounded explanation

Self-attention draws queries, keys, and values from one sequence. Cross-attention uses two sources: a target sequence asks questions, while a context sequence supplies the items to retrieve. The same [[transformer-attention]] operation applies, but the provenance and shapes change. This distinction is architectural, not a different normalization formula.

Let $A$ be the target states with $n$ positions and $B$ the context states with $m$ positions. Learned projections produce target queries $Q$ of shape $n\times d$, context keys $K$ of shape $m\times d$, and context values $V$ of shape $m\times v$. Here $d$ is the query/key feature width and $v$ the value width. Then

$$O=\operatorname{softmax}(QK^\top/\sqrt d)V.$$

The score matrix is $n\times m$, and the output is $n\times v$: each target position receives a weighted combination of context values. There is no requirement that $n=m$. For two target positions and three context positions, each output uses its own three weights. If those rows are $[0.8,0.1,0.1]$ and $[0.1,0.2,0.7]$, the first output emphasizes the first context item while the second emphasizes the third. These are illustrative weights, not a training result.

In an encoder-decoder model, decoder states provide queries and encoder outputs provide keys and values. In image generation, image-state queries can read text-context keys and values. Only the target stream receives this block's output: the context is not automatically updated in the reverse direction. Bidirectional multimodal interaction requires additional operations or a joint attention design.

A context mask can prevent reading padding or unavailable positions. Its semantics and broadcasting must match the implementation; a dense mask alone does not guarantee skipped computation or lower memory use. Test unequal sequence lengths, padding, all-masked cases, and preservation of the intended information boundary. Compare conditioning quality and directional ablations as well as memory and latency. Context projections may be reusable when context is unchanged, but whether caching helps depends on execution and memory costs.

## Prerequisites

- [[transformer-attention]]

## Sources

- <https://arxiv.org/html/1706.03762>
