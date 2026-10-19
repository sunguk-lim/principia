---
id: linear-transformer-attention
title: Linear Transformer Attention
type: concept
summary: Linear Transformer attention factors a kernel similarity into query and key feature maps so attention aggregation can be reordered through a fixed-size state.
tags: [ml/llm/architecture]
prereqs: [transformer-attention, matrix-multiplication, measurement]
sources: [https://arxiv.org/abs/2205.14135, https://arxiv.org/abs/2006.16236, https://arxiv.org/abs/2410.10629]
status: explained
created: 2026-10-11
updated: 2026-10-20
---

# Linear Transformer Attention

## Summary

A kernelized similarity can be written as `sim(q,k) = φ(q)ᵀφ(k)` instead of explicitly forming every query–key score. [[matrix-multiplication]] associativity then lets a model aggregate key–value contributions first and apply each query afterward. This changes the sequence-length scaling but also changes the attention function unless the feature map accurately represents the desired kernel.

## Mechanism

For feature dimension `m`, accumulate `S = Σ φ(k_j)v_jᵀ` and `z = Σ φ(k_j)`. A query's normalized output is `φ(q_i)ᵀS / (φ(q_i)ᵀz)`, assuming the denominator is nonzero and the chosen feature map keeps weights meaningful. For causal autoregressive attention, update `S` and `z` only with keys and values available up to the current position; the state can be carried forward recurrently. With fixed feature and value widths, work and state avoid an `n × n` attention matrix, but the feature-width products and memory traffic still matter.

This formulation is not merely a faster implementation of softmax attention. A deterministic positive feature map generally defines a different similarity; changing it can alter sharp selectivity and long-range behavior. Numerical stability matters when the denominator is small. The paper describes linear sequence complexity and recurrent implementation, but its reported acceleration is workload-specific. Compare full attention, optimized exact kernels, and this approximation on quality, throughput, latency, and memory across sequence lengths using [[measurement]]. Include causal leakage and adversarial long-range retrieval tests.

## ReLU feature maps in image diffusion

A concrete nonnegative feature map is elementwise rectification: φ(x) keeps positive coordinates and replaces negative coordinates with zero. SANA uses ReLU-based linear attention in its image-generation architecture. The defining gain comes from reassociating the feature-map products, not from an exact softmax-kernel implementation. Local mixing and other architecture changes in that system must be evaluated separately; a combined benchmark does not isolate this attention choice.

For a one-query, two-key example, take q=(1,2), k₁=(2,1), k₂=(-1,2), and scalar values v₁=3, v₂=7. After rectification, k₂ becomes (0,2). Query–key weights are 4 and 4, so normalized attention returns (4×3+4×7)/8=5. The state formulation gives S=(6,17) and z=(2,3), so qᵀS/(qᵀz)=40/8=5 without forming a stored query-by-key matrix. Here S adds the outer products of each rectified key and value; z adds the rectified keys.

If all query features are zero, or query and keys have no overlapping positive coordinates, the denominator is zero. An epsilon or explicit fallback must be specified; it modifies the function and does not restore missing selectivity. Compare dense evaluation of the same ReLU similarity with reassociated evaluation for numerical agreement, then separately compare quality against softmax attention. Probe sharp retrieval, long-range interactions, feature sparsity, precision, memory, and full-image latency at matched resolution and compute.

## Exact attention kernels versus changed attention functions

FlashAttention changes how ordinary softmax attention is evaluated: tiled computation and online normalization avoid writing the full score matrix to slow memory. It retains the attention definition, up to floating-point differences, but dense prefill still has quadratic pair interactions. Kernelized linear attention changes or approximates the similarity so aggregation can be reassociated. Its linear sequence scaling is not an exact softmax implementation in general.

For N=4 positions, dense attention considers 16 query–key pairs; with N=8 it considers 64. An exact tiled implementation can avoid storing those 64 scores all at once, but it still evaluates their contributions. A fixed-width linear-attention state instead grows work roughly in proportion to N, with feature-width costs and a different similarity contract. Compare dense versus tiled evaluation of the same softmax operator for numerical agreement. Then compare linear attention against that operator separately for task quality, sharp retrieval and numerical stability. Lower activation memory, lower arithmetic and equivalent output are three distinct claims. “Linear memory” in an exact kernel description does not imply linear arithmetic or the same design as linear attention.

## Prerequisites

- [[transformer-attention]]
- [[matrix-multiplication]]
- [[measurement]]

## Source

- [Katharopoulos et al., “Fast Autoregressive Transformers with Linear Attention”](https://arxiv.org/abs/2006.16236).

- [SANA](https://arxiv.org/abs/2410.10629): ReLU linear attention within a redesigned image-generation system; performance claims are setting-specific.

- <https://arxiv.org/abs/2205.14135>
