---
id: gptq
title: GPTQ Weight Quantization
summary: GPTQ quantizes trained layer weights while compensating later weights for earlier rounding errors using calibration-input curvature information.
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, hessian, matrix-multiplication]
sources: [https://arxiv.org/abs/2210.17323, https://github.com/IST-DASLab/gptq/blob/main/gptq.py]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# GPTQ Weight Quantization

## Summary

GPTQ quantizes trained layer weights while compensating later weights for earlier rounding errors using calibration-input curvature information.

## Grounded explanation

Ordinary weight rounding minimizes errors in stored numbers independently. GPTQ asks a different question: how much do those errors change a layer's outputs on representative inputs? It is a [[post-training-quantization]] method, not a new model architecture or ordinary gradient-based retraining of the whole model.

Let $W$ be a layer weight matrix with $r$ output coordinates and $d$ input coordinates. Let $X$ contain $n$ calibration input columns, so its shape is $d\times n$. The original layer output is $WX$, a [[matrix-multiplication]]. GPTQ seeks a quantized matrix $\widehat W$ whose output $\widehat WX$ stays close to $WX$. The local reconstruction objective sums the squares of all entries of $(W-\widehat W)X$.

The [[hessian]] of this quadratic objective with respect to one weight row is proportional to $XX^\top$. This matrix captures which input directions have large effects and which can compensate for one another. GPTQ rounds a weight column, then uses inverse-curvature information to adjust still-unquantized columns so they offset some of the resulting output error. Processing columns in blocks allows many such corrections to use efficient matrix operations. Damping adds a positive diagonal term before inversion or factorization to improve numerical robustness when calibration inputs do not span every direction.

A small example shows why compensation is possible. Suppose a layer output is $w_1x_1+w_2x_2$, and calibration inputs satisfy $x_2=x_1$. Rounding $w_1$ down by $0.1$ can be offset locally by increasing the still-free $w_2$ by $0.1$. If deployment inputs no longer have that relationship, the cancellation need not hold. Quantization of the second weight can also reintroduce error. The example explains the reconstruction principle, not a guarantee of zero final error.

Calibration inputs therefore matter even though the method does not require their task labels. Test held-out tasks and domain shifts; compare the same bit width and grouping against simple rounding. Record conversion memory and time as well as model size, task quality, and actual inference latency. The curvature is for a layer reconstruction surrogate, not the exact full-model task objective. A GPTQ-packed checkpoint also needs a compatible execution kernel; compression alone cannot guarantee a speedup.

## Prerequisites

- [[post-training-quantization]]
- [[hessian]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2210.17323>
- <https://github.com/IST-DASLab/gptq/blob/main/gptq.py>
