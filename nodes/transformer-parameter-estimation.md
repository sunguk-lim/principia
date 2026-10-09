---
id: transformer-parameter-estimation
title: Transformer Parameter Estimation
summary: Transformer parameter estimation sums tensor shapes by component, distinguishing embedding tables, attention projections, feed-forward layers, norms, and tied weights before approximating a model's size.
type: concept
tags: [ml/llm/architecture]
prereqs: [matrix-multiplication, transformer-attention, embedding]
sources: [https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Transformer Parameter Estimation

## Summary

A parameter count is a sum of stored trainable tensor elements, not a proxy for every compute or memory cost. It must be derived from the exact architecture and weight-sharing rules.

## Grounded explanation

For a simple dense block of width $d$ and feed-forward width $f$, four $d\times d$ attention projections contribute about $4d^2$ weights; two feed-forward matrices contribute about $2df$. Biases and normalization add smaller terms. Across $L$ identical blocks, a first estimate is $L(4d^2+2df)$, plus token and position [[embedding]] tables and any output head. This follows from [[matrix-multiplication]] tensor dimensions and the projection structure of [[transformer-attention]].

Do not multiply by head count again when the heads partition one total width $d$: the four projection matrices already include all heads. If the output projection shares the input embedding matrix, count that storage once. Grouped-query attention, gated MLPs, mixture-of-experts, adapters, and low-rank factors change the terms. A mixture-of-experts model may have many total parameters while activating only a subset per token; report both quantities.

For a worked check, with $d=1024$ and $f=4096$, the simplified per-block matrices contain roughly $4.19$ million attention and $8.39$ million feed-forward weights, before biases and norms. Validate a hand estimate against the implementation's named parameter tensors, deduplicating tied storage. Report whether embeddings, frozen parameters, adapters, and optimizer states are included; none is interchangeable with FLOPs or runtime memory.

## Sources

- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): original attention and position-wise feed-forward block shapes.
