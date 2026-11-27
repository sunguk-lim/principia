---
id: numeric-precision-formats
title: Numeric Precision Formats
summary: A numeric precision format specifies how bits represent values, trading range and resolution while leaving total model-memory and execution costs to a separate accounting contract.
type: concept
tags: [ml/llm/inference]
prereqs: [quantization]
sources: [https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html, https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/group__CUDA__MATH__INTRINSIC__BFLOAT16.html]
status: explained
created: 2026-06-23
updated: 2026-11-28
---

# Numeric Precision Formats

## Summary

A numeric precision format specifies what a bit pattern means. Floating-point formats divide bits among sign, exponent and fraction, while integer formats represent whole-number codes that can be interpreted through a separate [[quantization]] scale. Bit width determines nominal payload storage, not a universal speed or accuracy guarantee.

## Grounded explanation

For a normal binary floating-point number, write its value as $(-1)^s(1+f)2^e$. Here $s$ is the sign bit, $f$ the stored fractional contribution, and $e$ the decoded exponent after its bias is removed. The leading one is implicit for normal values. Zero, subnormal values, infinity and NaN require format-specific rules; this normal-value expression does not describe every bit pattern.

More exponent bits generally provide a wider magnitude range. More fraction bits provide finer local spacing. FP32 allocates 1 sign, 8 exponent and 23 fraction bits. FP16 uses 1, 5 and 10; BF16 uses 1, 8 and 7. Both latter formats use 16 bits, but BF16 exchanges fraction resolution for a much wider exponent range. That helps some training workloads avoid overflow while increasing rounding error; the correct choice depends on operation behavior and quality requirements.

INT8 and INT4 use 8-bit and 4-bit integer codes. An application may reserve a code or restrict the effective range. For example, symmetric quantization often uses INT4 codes -7 through 7 even though four bits can encode sixteen patterns. The represented real value depends on the stored scale and any zero point, not just the integer bit pattern. A format name does not specify tensor grouping, calibration or the arithmetic accumulation type.

Low-bit floating formats also differ in exponent, fraction and special-value conventions. Names such as E4M3 and E5M2 identify different allocations within an eight-bit container. Their exact finite ranges and overflow handling depend on the documented variant. Four-bit storage does not imply native four-bit arithmetic throughout an inference path: unpacking, scaling and accumulation can use wider values.

## Worked value: range versus resolution

Take 70000. FP16's maximum finite value is 65504, so a normal round-to-nearest conversion overflows to infinity for this value. BF16 can represent that magnitude. Around $2^{16}=65536$, seven fraction bits give a spacing of $2^{16}/2^7=512$. The two neighboring BF16 values are 69632 and 70144. Their distances from 70000 are 368 and 144, respectively, so round-to-nearest selects 70144. Range preserved the finite value, but resolution still introduced an error of 144. Equal bit count does not mean equal representable values.

## Worked storage: payload is not total memory

An invented billion-weight model needs $10^9\times16/8=2\times10^9$ payload bytes at 16 bits, versus $10^9\times4/8=0.5\times10^9$ at four bits: an ideal fourfold reduction in weight payload. That is 2.0 versus 0.5 decimal GB, or approximately 1.863 versus 0.466 GiB after division by $2^{30}$. Add scale metadata, unconverted tensors, temporary buffers and runtime state to obtain actual residency. Training additionally retains gradients and optimizer state; generation retains attention state. Those components do not all shrink by the weight-width ratio.

## Validation and boundaries

Supported kernels, shapes, memory movement, conversion overhead and the chosen workload determine execution time. Fewer stored bits can reduce traffic or enable more packed operations, but do not establish proportional throughput. Benchmark the actual backend with fixed shapes and quality criteria, separate payload from peak allocated and reserved memory, and report range failures and task-level error.

No format guarantees a universal sub-percent quality loss. Test rounding, overflow, underflow and representative end-to-end outputs under the deployed accumulation and scaling policy. A hardware support label is not evidence that every operation uses an efficient low-bit path.

## Prerequisites

- [[quantization]]

## Sources

- <https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html>
- <https://docs.nvidia.com/cuda/cuda-math-api/cuda_math_api/group__CUDA__MATH__INTRINSIC__BFLOAT16.html>
