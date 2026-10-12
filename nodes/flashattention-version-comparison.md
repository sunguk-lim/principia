---
id: flashattention-version-comparison
title: FlashAttention Version Comparison
summary: FlashAttention versions preserve exact tiled attention while changing work partitioning and GPU pipeline overlap to fit different hardware bottlenecks.
type: concept
tags: [ml/llm/architecture]
prereqs: [flash-attention, memory-hierarchy, gpu-tile-programming]
sources: [https://arxiv.org/abs/2205.14135, https://arxiv.org/abs/2307.08691, https://arxiv.org/abs/2407.08608]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# FlashAttention Version Comparison

## Summary

The FlashAttention family keeps the core promise of [[flash-attention]]: compute exact attention without materializing the full score matrix in high-bandwidth memory. Later versions target different inefficiencies in the GPU implementation rather than changing the mathematical attention definition.

## Grounded explanation

The original algorithm tiles queries and keys, carries online softmax statistics, and exploits the [[memory-hierarchy]] to reduce HBM traffic. Its performance can still be limited by how much non-matmul work each block performs, how work is divided among warps or blocks, and whether the hardware pipeline sits idle. FlashAttention-2 revises work partitioning and parallelism to reduce such overhead and improve utilization. FlashAttention-3 targets Hopper-era execution features, overlapping matrix multiplication and softmax-related work more aggressively and exploiting asynchronous GPU mechanisms. These are implementation and hardware-scheduling differences; numerical error and supported precisions must be checked separately from the exact mathematical target.

A version number is not a universal speed ranking. Sequence length, head dimension, batch size, causal masking, dropout, precision, GPU generation, and forward versus backward pass change the bottleneck. [[gpu-tile-programming]] explains why a tile schedule that helps one shape can underutilize another. Kernels may also differ in supported features or fall back to another implementation.

Benchmark on the target device with pinned software versions, identical shapes, mask semantics, precision, and output checks. Measure end-to-end latency, kernel time, HBM traffic, occupancy or achieved throughput, peak memory, and forward/backward numerical deviation. Include a standard framework baseline and report unsupported configurations rather than inferring general superiority from one paper's headline result.

## Prerequisites

- [[flash-attention]]
- [[memory-hierarchy]]
- [[gpu-tile-programming]]

## Sources

- [FlashAttention](https://arxiv.org/abs/2205.14135): original IO-aware exact attention algorithm.
- [FlashAttention-2](https://arxiv.org/abs/2307.08691): revised parallelism and work partitioning.
- [FlashAttention-3](https://arxiv.org/abs/2407.08608): overlapping and asynchronous execution for Hopper GPUs.
