---
id: linformer-attention
title: Linformer Attention
summary: Linformer attention learns sequence-axis projections of keys and values, reducing attention cost when the projected length stays much smaller than the input length.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, low-rank-factorization, matrix-multiplication, measurement]
sources: [https://arxiv.org/abs/2006.04768]
status: explained
created: 2026-10-11
updated: 2026-10-11
---

# Linformer Attention

## Summary

[[transformer-attention]] forms interactions between all query and key positions, creating a quadratic sequence dimension. Linformer assumes that a much smaller projected sequence axis can retain enough information for the task. It projects keys and values from length `n` to length `k`, then lets each of the `n` queries attend to those `k` projected positions.

## Mechanism and limits

For one head, let queries, keys, and values each have `n` positions. Learned projection matrices map the key and value sequence axes to `k` positions. The score matrix is then `n × k`, and output aggregation also uses `n × k` weights. With fixed `k` and head width, the sequence-dependent attention work and score storage grow approximately linearly in `n`, instead of storing an `n × n` score matrix. The [[low-rank-factorization]] viewpoint motivates this compression, but it does not guarantee that every task's attention matrix is well represented at the chosen `k`.

This is an architectural approximation, unlike exact tiled attention. Compression can lose token-specific detail, and projection parameters or supported maximum lengths may complicate length extrapolation. The paper's reported quality and efficiency apply to its evaluated models and settings, not every modern decoder or hardware stack. The representation still needs a causal design for autoregressive use; one must not inadvertently mix future keys into a projected current state.

For a document model, vary `k` while holding training data, parameter budget, and input lengths comparable. Measure downstream quality, long-range retrieval probes, peak memory, throughput, and tail latency with [[measurement]]. Compare against full attention and a strong exact optimized baseline; theoretical score-matrix scaling alone does not prove wall-clock improvement.

## Prerequisites

- [[transformer-attention]]
- [[low-rank-factorization]]
- [[matrix-multiplication]]
- [[measurement]]

## Source

- [Wang et al., “Linformer: Self-Attention with Linear Complexity”](https://arxiv.org/abs/2006.04768).
