---
id: sparse-kv-outlier-storage
title: Sparse KV Outlier Storage
summary: Sparse KV outlier storage separates exceptional cache values and their coordinates from a low-bit dense representation so extremes do not coarsen every ordinary value.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-quantization]
sources: [https://arxiv.org/html/2401.18079v2]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Sparse KV Outlier Storage

## Meaning

Sparse outlier storage gives unusually large or otherwise sensitive KV values a separate representation while compressing the remaining dense data. It avoids forcing every ordinary value to share a coarse range with rare extremes. This complements [[kv-quantization]]; it is not merely keeping a whole recent suffix uncompressed.

## Mechanism

Choose a detection rule and its scope, such as each vector. Store exceptional values and their positions at higher precision. Build the dense quantized representation with a defined placeholder or residual convention. Reconstruction must specify whether the sparse value replaces a placeholder or adds a correction; mixing these conventions double-counts a value. The attention kernel must consume both parts consistently. KVQuant studies per-vector dense-and-sparse quantization; this does not imply that whole outlier channels are the only possible sparse unit.

The budget includes coordinate indices, counts, offsets, alignment, full-precision values and data-dependent execution. A threshold that produces many outliers can erase the expected capacity gain and create irregular work. Calibrate the rule without using final evaluation cases.

## Worked example

Take 100 cached values, with four designated outliers. A toy representation reserves a four-bit dense slot for every value, using zero placeholders for the outliers. Dense payload is 100×4=400 bits. Each sparse record stores an eight-bit coordinate and a 16-bit replacement, costing 4×24=96 bits. Total is 496 bits before scales and offsets, versus 1,600 bits for all 16-bit values. At 40 outliers it becomes 400+40×24=1,360 bits; sparse bookkeeping now consumes most of the saving. These chosen index widths describe the example, not every kernel.

Validate reconstruction at outlier locations and ordinary locations independently, including empty and unusually dense outlier sets. Compare quality and total memory at several thresholds, then measure tail latency, conversion cost and attention throughput under representative cache lengths. Low average error does not prove that a rare sensitive coordinate can be discarded safely.

## Check your understanding

Is storing only the exceptional values sufficient? No. Their positions and reconstruction convention must also be preserved.

## Prerequisites

- [[kv-quantization]]

## Sources

- <https://arxiv.org/html/2401.18079v2>
