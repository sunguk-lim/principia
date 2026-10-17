---
id: activation-aware-weight-quantization
title: Activation-Aware Weight Quantization
summary: Activation-aware weight quantization uses representative activation statistics to rescale important input channels before low-bit weight quantization while preserving the unquantized layer function.
type: concept
tags: [ml/llm/inference]
prereqs: [post-training-quantization, matrix-multiplication]
sources: [https://arxiv.org/abs/2306.00978, https://github.com/mit-han-lab/llm-awq/blob/main/awq/quantize/auto_scale.py]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Activation-Aware Weight Quantization

## Summary

Activation-aware weight quantization uses representative activation statistics to rescale important input channels before low-bit weight quantization while preserving the unquantized layer function.

## Grounded explanation

Not every weight error has the same effect. A modest weight error multiplied by a frequently large input activation can dominate the output error. AWQ uses observed activations to guide a weight-only [[post-training-quantization]] transformation. “Activation-aware” does not mean every activation is stored at the same low precision as the weights.

Use a column input vector $x$ of length $d$ and a weight matrix $W$ of shape $r\times d$, producing $y=Wx$ by [[matrix-multiplication]]. Choose an invertible diagonal matrix $S$ with positive channel scales. Before quantization,

$$Wx=(WS)(S^{-1}x).$$

The larger a scale in $S$, the larger the corresponding weight column becomes and the smaller its matching input coordinate becomes. The exact unquantized product is unchanged. Quantization is applied to the transformed weights, producing the approximate output $Q(WS)S^{-1}x$, where $Q$ denotes the chosen rounding and dequantization operation. Its error depends on both the shared quantization ranges and the inverse-scaled activations.

AWQ uses representative activation statistics to choose channel scales and protect salient channels without requiring a separate high-precision weight path for each one. The reference implementation searches a bounded family of scales and measures the resulting output discrepancy on calibration inputs; this is not full-model gradient training. Scaling must be folded into compatible neighboring operations or otherwise executed correctly. Changing a weight column without the compensating input transformation changes the model even before rounding.

For intuition, suppose two input coordinates often have magnitudes near $10$ and $0.1$. An equal weight-rounding error of $0.02$ contributes about $0.2$ and $0.002$ respectively to the output. The first coordinate deserves attention, but increasing its weight scale can enlarge a quantization group's range and worsen other coordinates. Scale search balances this trade-off; it is not a rule to multiply the largest activation channel by an unlimited number.

Validate against unscaled rounding at equal bit width and group size, using held-out domains and realistic shapes. Check equivalence before quantization, reconstruction error afterward, task metrics, memory metadata, conversion cost, and target-kernel throughput. Representative calibration and compatible packing matter. Neither activation awareness nor a paper's reported speedup guarantees performance for another model or accelerator.

## Prerequisites

- [[post-training-quantization]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/abs/2306.00978>
- <https://github.com/mit-han-lab/llm-awq/blob/main/awq/quantize/auto_scale.py>
