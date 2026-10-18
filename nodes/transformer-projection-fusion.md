---
id: transformer-projection-fusion
title: Transformer Projection Fusion
summary: Transformer projection fusion combines compatible linear maps into larger matrix products without removing nonlinear or data-dependency boundaries.
type: concept
tags: [ml/llm/inference]
prereqs: [matrix-multiplication, transformer-attention, position-wise-feed-forward-network]
sources: [https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/modules/layers.py, https://huggingface.co/docs/diffusers/main/en/optimization/fp16]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Transformer Projection Fusion

## Meaning

Several transformer projections can share one input and be computed by one larger linear operation. This is an algebraic reorganization that may improve hardware utilization; it does not turn attention and a feedforward network into one linear function.

## Mechanism

For token matrix X, [[matrix-multiplication]] gives X[W_Q W_K W_V]=[XW_Q XW_K XW_V]. Bias vectors concatenate in the same order. The outputs are split into [[transformer-attention]] roles afterward. Self-attention shares one X; cross-attention generally has a different query input and can combine K/V but not arbitrarily all three. A parallel block can additionally compute a feedforward input projection from the same normalized X, then evaluate attention and the [[position-wise-feed-forward-network]] nonlinearity separately. If both branches produce outputs for a shared residual sum, their final projections can be represented by concatenating branch activations and stacking output weights. Serial blocks with different branch inputs do not satisfy that identity.

## Worked example

Use X=(2,3), W_Q=(1,0)ᵀ, W_K=(0,2)ᵀ, and W_V=(1,-1)ᵀ. Three scalar outputs are 2, 6, and -1; one 2×3 concatenated weight matrix yields exactly (2,6,-1). For a parallel feedforward input W_F=(2,1)ᵀ, the same multiply can also produce 7, but the subsequent activation and attention still run separately. Larger products can reduce repeated reads or dispatches, yet layout changes, concatenation, quantization scales, or activation memory may offset gains. Validate split order, bias placement, floating-point tolerance, gradients when training, peak memory, and latency across actual batch and sequence shapes.

## Check your understanding

Can a serial attention-then-MLP block be fused this way without changing its function? Not generally: the MLP receives the post-attention state, not the same input as Q/K/V.

## Prerequisites

- [[matrix-multiplication]]
- [[transformer-attention]]
- [[position-wise-feed-forward-network]]

## Sources

- <https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/modules/layers.py>
- <https://huggingface.co/docs/diffusers/main/en/optimization/fp16>
