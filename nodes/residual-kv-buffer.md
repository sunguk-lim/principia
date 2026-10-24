---
id: residual-kv-buffer
title: Residual High-Precision KV Buffer
summary: A residual KV buffer retains recent keys and values at high precision until a complete block can be quantized and appended to an older compressed cache.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-quantization]
sources: [https://arxiv.org/html/2402.02750v1]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Residual High-Precision KV Buffer

## Meaning

A residual high-precision KV buffer splits cached history into older compressed entries and a recent uncompressed suffix. It is one streaming strategy for [[kv-quantization]], not token eviction: both portions still participate in attention.

## Mechanism

Per-channel key quantization groups one coordinate across several tokens. During generation those tokens arrive one at a time, so the complete group is not yet available. Keep recent entries in a high-precision residual buffer. Once a configured block is complete, determine its quantization parameters, encode it and append the compressed block. The next suffix starts a new block. KIVI also retains a residual value portion to control quality.

The attention operation must read both portions in correct sequence order and combine their contributions under one normalization. Independently normalizing each portion and adding the two attention outputs is generally wrong: each local output has a different denominator. The buffer size also defines a memory and error trade, not an unlimited free accuracy improvement.

## Worked example

Use a toy block threshold of four tokens and two cached numbers per token, one key and one value. After six tokens, four older tokens are compressed and two recent tokens remain at 16 bits. With 4-bit compressed entries, payload is 4×2×4 + 2×2×16=96 bits. Keeping all six at 16 bits would use 6×2×16=192 bits. Scale and layout metadata are excluded from both toy totals. The recent suffix halves the ideal fourfold payload reduction in this state. After two more arrivals, the second block can be compressed, and memory changes again.

Track temporary coexistence during conversion, group padding and scales when measuring peaks. Sweep buffer and group sizes under fixed tasks; compare error, long-context correctness, kernel compatibility, token latency and throughput. A failure during block conversion must not lose or double-count a token. Validate around each block boundary rather than testing only a full compressed cache.

## Check your understanding

Are recent buffered tokens omitted from attention? No. They remain visible at higher precision until conversion.

## Prerequisites

- [[kv-quantization]]

## Sources

- <https://arxiv.org/html/2402.02750v1>
