---
id: transformer-flop-estimation
title: Transformer FLOP Estimation
summary: Transformer FLOP estimation counts arithmetic per operation and sequence position, separating projection and feed-forward matrix multiplies from sequence-length-dependent attention work.
type: concept
tags: [ml/llm/architecture]
prereqs: [matrix-multiplication, transformer-attention, measurement]
sources: [https://arxiv.org/abs/1706.03762, https://arxiv.org/abs/1904.10509]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Transformer FLOP Estimation

## Summary

A FLOP estimate is an accounting model for arithmetic, not a latency prediction. State whether multiply-add counts as one or two operations, and distinguish prefill, incremental decode, and training.

## Grounded explanation

Using two FLOPs per multiply-add, one dense layer with sequence length $n$, width $d$, and feed-forward width $f$ has approximately $8nd^2$ FLOPs for Q/K/V/output projections and $4ndf$ for two feed-forward matrices. Dense attention score and value products add approximately $4n^2d$ FLOPs. These are leading terms from [[matrix-multiplication]] dimensions; [[transformer-attention]] also incurs softmax, normalization, and memory movement that the simple formula omits. Multiply by layer count only for blocks actually executed.

During incremental decoding with a KV cache, one new token attends to $n$ prior tokens, so attention work per step grows with context length rather than recomputing all $n^2$ pairs. Training includes backward operations and optimizer work, which must be accounted for separately; a universal multiplier is only an approximation. Sparse masks reduce arithmetic only if the implementation avoids masked products rather than computing dense matrices and discarding entries.

Validate against a profiler with matched shapes and precision. Compare predicted terms with measured kernel FLOPs, bytes moved, prefill latency, decode latency, and throughput under several sequence lengths. Memory bandwidth, launch overhead, padding, and accelerator utilization can dominate even when counted FLOPs fall. Label any estimate's architecture and counting convention before comparing models.

## Sources

- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): dense attention and block operations.
- [Child et al., Sparse Transformer](https://arxiv.org/abs/1904.10509): an example where restricted attention changes sequence scaling.
