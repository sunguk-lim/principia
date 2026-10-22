---
id: transformer-flop-estimation
title: Transformer FLOP Estimation
summary: Transformer FLOP estimation counts arithmetic per operation and sequence position, separating projection and feed-forward matrix multiplies from sequence-length-dependent attention work.
type: concept
tags: [ml/llm/architecture]
prereqs: [matrix-multiplication, transformer-attention, measurement, arithmetic-intensity]
sources: [https://arxiv.org/abs/1706.03762, https://arxiv.org/abs/1904.10509, https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html]
status: explained
created: 2026-10-10
updated: 2026-10-23
---

# Transformer FLOP Estimation

## Summary

A FLOP estimate is an accounting model for arithmetic, not a latency prediction. State whether multiply-add counts as one or two operations, and distinguish prefill, incremental decode, and training.

## Grounded explanation

Using two FLOPs per multiply-add, one dense layer with sequence length $n$, width $d$, and feed-forward width $f$ has approximately $8nd^2$ FLOPs for Q/K/V/output projections and $4ndf$ for two feed-forward matrices. Dense attention score and value products add approximately $4n^2d$ FLOPs. These are leading terms from [[matrix-multiplication]] dimensions; [[transformer-attention]] also incurs softmax, normalization, and memory movement that the simple formula omits. Multiply by layer count only for blocks actually executed.

During incremental decoding with a KV cache, one new token attends to $n$ prior tokens, so attention work per step grows with context length rather than recomputing all $n^2$ pairs. Training includes backward operations and optimizer work, which must be accounted for separately; a universal multiplier is only an approximation. Sparse masks reduce arithmetic only if the implementation avoids masked products rather than computing dense matrices and discarding entries.

Validate against a profiler with matched shapes and precision. Compare predicted terms with measured kernel FLOPs, bytes moved, prefill latency, decode latency, and throughput under several sequence lengths. Memory bandwidth, launch overhead, padding, and accelerator utilization can dominate even when counted FLOPs fall. Label any estimate's architecture and counting convention before comparing models.

## Matrix shape is not elapsed time

The same counted model work can execute differently when its matrix shape changes. [[arithmetic-intensity]] separates operations from bytes crossing a stated memory boundary. If many known token positions share one weight matrix, stacking their inputs can amortize that matrix read and expose larger tiled operations. Recurrent hidden-state dependencies constrain which positions can be stacked; independent batch examples and precomputed input projections remain possible.

For an illustrative FP16 multiply Y=XW, let W be 1024×1024 and X have M rows and 1024 columns. With two FLOPs per multiply-add, work is 2M×1024². Assume each input and weight is read once from device memory and each output written once, with two bytes per stored value. Traffic is 2(1024²+2M×1024) bytes. For M=1 the intensity is about 0.998 FLOP/byte; for M=128 it is 102.4 FLOPs/byte. These are idealized traffic calculations, not measured HBM traffic or a predicted hundredfold speedup. Reuse from cache, output accumulation precision, tile alignment and additional reads change the denominator.

NVIDIA's matrix-multiplication guide grounds the relationship among dimensions, arithmetic intensity, tile count and achieved throughput. Profile the actual shapes, launch gaps, memory transfers and end-to-end tokens/s with [[measurement]]. Larger batches can improve throughput while increasing request latency and activation memory. A recurrent model does not categorically leave all tensor cores idle, and adding devices can help independent or intra-step work without removing its temporal dependency. Hold model quality and workload constant before comparing costs.

## Sources

- [Vaswani et al., Transformer](https://arxiv.org/abs/1706.03762): dense attention and block operations.
- [Child et al., Sparse Transformer](https://arxiv.org/abs/1904.10509): an example where restricted attention changes sequence scaling.

- <https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html>
