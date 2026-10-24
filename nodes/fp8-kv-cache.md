---
id: fp8-kv-cache
title: FP8 KV Cache
summary: An FP8 KV cache stores attention keys and values in scaled eight-bit floating-point form under an explicitly compatible attention-kernel contract.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, numeric-precision-formats]
sources: [https://raw.githubusercontent.com/vllm-project/vllm/main/docs/features/quantization/quantized_kvcache.md]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# FP8 KV Cache

## Meaning

An FP8 KV cache reduces the storage precision of the request-dependent [[kv-cache]]. It is independent of the precision of model weights. FP8 is a floating-point family with exponent and fraction fields, not the same grid as an eight-bit integer; [[numeric-precision-formats]] explains that distinction.

## Mechanism

Let x be a cached value, s a positive scale and round_FP8 the conversion to a chosen FP8 format. Store y=round_FP8(x/s) and interpret it as x_hat=s×y. Choose the exact format, scale convention and grouping together with the attention implementation. Scales may be shared by a tensor or separated by head; finer grouping adds metadata and can better fit different ranges. Calibration data must represent the model and workload. A default scale of one is a configuration choice, not evidence of negligible error.

Storage precision does not uniquely determine compute precision. One kernel can dequantize into a wider calculation; another can operate with quantized queries and FP8 attention. The cited vLLM documentation distinguishes backend-dependent paths. Verify the deployed version, model and hardware rather than inferring a universal fast path from an FP8 storage flag.

## Worked example

A cache has 1,048,576 values. At two bytes per value, raw payload is 2,097,152 bytes. At one byte it is 1,048,576 bytes. If an illustrative implementation uses 64 four-byte scales, they add 256 bytes, giving 1,048,832 bytes before alignment and allocator overhead. That is about 50.012% of the original payload, not proof that total process memory or token latency halves. Weights, workspace and runtime remain.

For scale s=0.5 and value x=6, the normalized number is 12; if the selected format represents 12 exactly, reconstruction is 6. Nearby values can round and large values can overflow or clip according to conversion policy. Test saturation, per-head error, long-context task quality and cached/full-prefix consistency, as well as peak memory and prefill/decode latency. A smaller cache can improve capacity even when conversion costs prevent a latency improvement.

## Check your understanding

Do eight-bit cache entries prove eight-bit attention arithmetic? No. The kernel contract determines computation and conversion.

## Prerequisites

- [[kv-cache]]
- [[numeric-precision-formats]]

## Sources

- <https://raw.githubusercontent.com/vllm-project/vllm/main/docs/features/quantization/quantized_kvcache.md>
