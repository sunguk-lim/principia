---
id: kv-quantization
title: KV-Cache Quantization
summary: KV-cache quantization reduces the precision of request-dependent attention state while balancing reconstruction error, metadata, residual buffers and kernel cost.
type: concept
tags: [ml/llm/inference]
prereqs: [quantization, kv-cache]
sources:
  - "Liu et al., 'KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache' (2024), arXiv:2402.02750"
  - "Hooper et al., 'KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization' (2024), arXiv:2401.18079"
status: explained
created: 2026-06-23
updated: 2026-10-25
---

# KV-Cache Quantization

## Summary

KV-cache quantization stores request-dependent keys and values with fewer bits. It applies [[quantization]] to the [[kv-cache]], independently of model-weight precision. It can reduce memory traffic and increase capacity, but payload bit ratios are not guarantees about total memory, accuracy or decoding speed.

## Grounded explanation

An ordinary decoder retains keys and values for past tokens so they need not be recomputed. For fixed layers, KV heads and head width, stored values grow with retained tokens and concurrent sequences. Weight-only quantization changes learned parameter storage, not automatically the precision of these computed activations. Cache dominance depends on workload and architecture; it is not universal at every context or batch size.

For symmetric integer quantization, let x be a cached scalar, s a positive shared scale and q the nearest representable integer code. With no clipping, q=round(x/s) reconstructs x_hat=q×s and has error at most s/2. Four-bit symmetric codes might use -7 through 7; asymmetric schemes instead use a zero point. FP8 and codebook schemes use different reconstruction levels and cannot inherit this uniform-grid bound without checking their own conversion rule.

**Granularity and streaming.** Per-tensor scales are cheap but couple many values to the same range. Per-channel key scales group the same coordinate across tokens; per-token value scales group coordinates within a token. KIVI motivates this asymmetry from studied key outliers and value-error behavior, and keeps a recent high-precision residual cache until blocks can be quantized. These are tested design choices, not laws that every model has identical outlier structure. Per-channel grouping also needs tokens to arrive before a full block can be encoded.

### Worked example

Take two token key rows, each with two channels: [0.5,12] and [-0.8,9]. A single four-bit symmetric scale is 12/7≈1.714. The first channel's values both round to zero. With separate channel scales, the first uses 0.8/7≈0.1143: codes [4,-7] reconstruct [0.4571,-0.8]. The second uses 12/7≈1.714: codes [7,5] reconstruct [12,8.571]. Small-channel values survive, but reconstruction is not exact and two scales cost more than one. This groups actual tokens rather than assigning a separate scale to every isolated scalar.

A toy cache with 1,000 values requires 2,000 payload bytes at 16 bits. Four-bit codes require 500 bytes. If there are 20 four-byte scales, they add 80 bytes: 580 bytes before residual buffers, padding and allocator overhead. The fourfold payload reduction is only about 3.45-fold for these counted terms. Temporary conversion buffers can further increase the peak.

**Other error controls.** Non-uniform methods choose unequal reconstruction levels using calibration. KVQuant studies sensitivity-weighted levels, pre-rotation key quantization and per-vector dense-and-sparse outlier handling. Sparse values need their coordinates and a precise replacement/correction convention; they are not simply free high-precision channels. Each mechanism should be evaluated separately and in combination.

**Capacity is not latency.** The cache path can be bandwidth limited, but weight reads, launches, attention arithmetic, unpacking, conversion and scheduling can also matter. A compatible fused kernel can hide conversion work; an incompatible layout can erase the traffic benefit. Compare the same model, prompts, output lengths, concurrency and quality target. Measure peak allocated/reserved memory, cache bytes including metadata, prefill latency, token latency, throughput and long-context task quality. Include rare errors, saturation, block boundaries and shifted inputs. Neither almost-lossless accuracy nor speed proportional to bit width is a general guarantee.

## Prerequisites

- [[quantization]]
- [[kv-cache]]

## Sources

- <https://arxiv.org/html/2402.02750v1> — KIVI: per-channel keys, per-token values and streaming residual buffers.
- <https://arxiv.org/html/2401.18079v2> — KVQuant: non-uniform reconstruction, pre-RoPE keys and dense-and-sparse outliers.
