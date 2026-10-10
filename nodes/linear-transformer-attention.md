---
id: linear-transformer-attention
title: Linear Transformer Attention
type: concept
summary: Linear Transformer attention factors a kernel similarity into query and key feature maps so attention aggregation can be reordered through a fixed-size state.
tags: [ml/llm/architecture]
prereqs: [transformer-attention, matrix-multiplication, measurement]
sources: [https://arxiv.org/abs/2006.16236]
status: explained
created: 2026-10-11
updated: 2026-10-11
---

# Linear Transformer Attention

## Summary

A kernelized similarity can be written as `sim(q,k) = φ(q)ᵀφ(k)` instead of explicitly forming every query–key score. [[matrix-multiplication]] associativity then lets a model aggregate key–value contributions first and apply each query afterward. This changes the sequence-length scaling but also changes the attention function unless the feature map accurately represents the desired kernel.

## Mechanism

For feature dimension `m`, accumulate `S = Σ φ(k_j)v_jᵀ` and `z = Σ φ(k_j)`. A query's normalized output is `φ(q_i)ᵀS / (φ(q_i)ᵀz)`, assuming the denominator is nonzero and the chosen feature map keeps weights meaningful. For causal autoregressive attention, update `S` and `z` only with keys and values available up to the current position; the state can be carried forward recurrently. With fixed feature and value widths, work and state avoid an `n × n` attention matrix, but the feature-width products and memory traffic still matter.

This formulation is not merely a faster implementation of softmax attention. A deterministic positive feature map generally defines a different similarity; changing it can alter sharp selectivity and long-range behavior. Numerical stability matters when the denominator is small. The paper describes linear sequence complexity and recurrent implementation, but its reported acceleration is workload-specific. Compare full attention, optimized exact kernels, and this approximation on quality, throughput, latency, and memory across sequence lengths using [[measurement]]. Include causal leakage and adversarial long-range retrieval tests.

## Prerequisites

- [[transformer-attention]]
- [[matrix-multiplication]]
- [[measurement]]

## Source

- [Katharopoulos et al., “Fast Autoregressive Transformers with Linear Attention”](https://arxiv.org/abs/2006.16236).
