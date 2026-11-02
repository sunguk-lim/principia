---
id: smoothquant
title: SmoothQuant Activation Smoothing
summary: SmoothQuant uses inverse input-channel rescaling to move activation outlier magnitude into weights before quantizing both operands of a linear layer.
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, matrix-multiplication]
sources: [https://arxiv.org/abs/2211.10438, https://github.com/mit-han-lab/smoothquant/blob/main/smoothquant/smooth.py]
status: explained
created: 2026-11-03
updated: 2026-11-03
---

# SmoothQuant Activation Smoothing

## Meaning

SmoothQuant prepares a trained linear layer for weight-and-activation quantization by redistributing channel magnitudes. Large activation channels can force a coarse shared rounding grid. The method shrinks those channels while enlarging matching weight columns, preserving the unquantized linear function before applying [[post-training-quantization]]. It is neither a file format nor a guarantee of lossless low-bit execution.

## Mechanism

Use column inputs. Let x be a d-element input vector, W an r-by-d weight matrix, and y=Wx the r-element output of [[matrix-multiplication]]. Let S be an invertible d-by-d diagonal matrix with positive channel scales s_j. Then

$$Wx=(WS)(S^{-1}x).$$

A large s_j divides input channel j and multiplies the corresponding weight column. The same factor cancels inside the exact product. Define Q_A and Q_W as quantization followed by reconstruction for activations and weights. The deployed approximation is Q_W(WS) Q_A(S^{-1}x), not the exact identity. Both rounding errors matter.

The paper chooses scales using calibration maxima. Let a_j be the maximum absolute input in channel j over calibration tokens, b_j the maximum absolute weight in column j, and alpha a smoothing parameter between zero and one. A representative rule is s_j=a_j^alpha / b_j^(1-alpha), with small positive floors in implementations for empty or zero-magnitude channels. Increasing alpha moves more difficulty from activations into weights. Shared scales, clipping and later operations mean balancing magnitudes alone is not an optimality proof.

## Worked example

Take x=[20,2] and W=[0.5,3], giving y=10+6=16. Choose S with diagonal [5,2]. The transformed input is [4,1], and weights become [2.5,6]; their product is still 10+6=16. The activation maximum dropped from 20 to 4 while the weight maximum rose from 3 to 6. This deliberately chosen example demonstrates the identity, not the calibration rule or a measured quality gain.

For an illustrative symmetric three-bit activation grid with codes -3 through 3, the original max-based scale is 20/3; input 2 rounds to zero. The transformed scale is 4/3; input 1 reconstructs as 4/3. Even with exact transformed weights, that reconstruction yields 2.5*4 + 6*(4/3)=18 rather than 16. Smoothing preserves the exact function, not every quantized value. W8A8 uses a much finer grid, but still requires validation.

## Boundaries and validation

Fold inverse scaling into compatible producer parameters where possible; shared consumers and residual branches must remain consistent. Check the unquantized transformed network first, then calibrated reconstruction error, held-out quality and domain shifts. Compare smoothing settings and unsmoothed equal-bit baselines. Record the actual activation, weight and accumulation formats and compatible kernels. Conversion metadata, workspace and dispatch can erase an apparent storage advantage. Report original-paper speedups only with their exact model, hardware and workload, not as method-wide promises.

## Prerequisites

- [[post-training-quantization]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2211.10438>
- <https://github.com/mit-han-lab/smoothquant/blob/main/smoothquant/smooth.py>
