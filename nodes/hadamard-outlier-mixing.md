---
id: hadamard-outlier-mixing
title: Hadamard Outlier Mixing for Quantization
summary: "Orthogonal sign-mixing redistributes large coordinates before group quantization while preserving the unquantized linear transform."
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, matrix-multiplication]
sources: [https://arxiv.org/abs/2404.00456]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Hadamard Outlier Mixing for Quantization

## Summary

Group quantization can waste integer levels when one unusually large coordinate sets a shared scale. **Hadamard outlier mixing** applies an orthogonal sign-mixing transform before quantization so the magnitude is spread across coordinates. In exact arithmetic, the transform and its inverse cancel; after rounding, quantization error and kernel cost determine whether it helps.

## Grounded explanation

Take a vector $x$ and a normalized Hadamard matrix $H$ with entries of equal magnitude and $H^TH=I$. For a linear map $Wx$, one can rewrite it as $(WH^T)(Hx)$ without changing the exact result. Random diagonal sign flips can reduce structured alignment with the transform. Mixing can replace a coordinate outlier with several moderate coordinates, improving a shared-scale codebook used by [[post-training-quantization]]. It does not guarantee lower error for every tensor: rotation can create new local peaks, and activation distributions may change with inputs.

The practical design couples transform block size, quantization group size, bit width, and kernel layout. They control different things: a transform block says which values mix, whereas a quantization group says which values share scales. A mathematically reversible transform is not free in a deployed kernel; a conversion may be fused into weights while dynamic activations still incur runtime work. Measure end-to-end latency and accuracy, not only the range of transformed values.

On a representative calibration and held-out set, compare the same checkpoint with no rotation, a rotation plus equal-bit quantization, and a higher-precision baseline. Report task loss, outlier distribution, per-layer error, bytes moved, kernel time, and energy. Avoid transferring a vendor's reported chip-specific speedup to unrelated devices.

## Prerequisites

- [[post-training-quantization]]
- [[matrix-multiplication]]

## Sources

- [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](https://arxiv.org/abs/2404.00456): primary rotation-based quantization method.
