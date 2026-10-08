---
id: residual-connection
title: Residual Connection
summary: "A residual block adds its input to a learned transformation, preserving an identity route for signals and gradients."
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, gradient-descent]
sources: [https://arxiv.org/abs/1512.03385, https://arxiv.org/abs/1706.03762]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Residual Connection

## Summary

A **residual connection** computes $y=x+F(x)$, after matching shapes. The identity path lets a block learn a correction to its input rather than requiring every layer to reconstruct the input. In Transformers it wraps attention and feed-forward sublayers, often with normalization; exact pre-norm versus post-norm placement changes training behavior.

## Grounded explanation

In a deep [[neural-network]], repeated transformations can make it hard to preserve useful information and train early layers. The additive path carries $x$ forward even if $F$ initially contributes little. During backpropagation, the derivative includes an identity term as well as the derivative of $F$, offering a direct route for gradient signals. This does **not** guarantee stable gradients: normalization, initialization, scale, depth, and optimizer still matter. If feature widths differ, a projection or other shape adjustment is needed before the addition.

For a Transformer layer, one sublayer computes an attention update and another a position-wise feed-forward update. Each can be wrapped by a residual path. The original Transformer paper used residual addition followed by layer normalization; many later variants normalize before the sublayer. Treat those as architectural alternatives, not interchangeable prose. In a small ablation, hold width, depth, training budget, and data fixed, then compare loss curves and gradient norms with the same optimizer and normalization placement. Verify that the skip branch really implements an identity or documented projection.

## Prerequisites

- [[neural-network]]
- [[gradient-descent]]

## Sources

- [He et al., Deep Residual Learning](https://arxiv.org/abs/1512.03385): original residual-learning formulation.
- [Vaswani et al., Attention Is All You Need](https://arxiv.org/abs/1706.03762): residual paths around Transformer sublayers.
