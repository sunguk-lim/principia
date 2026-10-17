---
id: query-key-normalization
title: Query-Key Normalization
summary: Query-key normalization applies a chosen normalization to projected queries and keys before their dot products to control attention-logit scale and training instability.
type: concept
tags: [ml/deep-learning]
prereqs: [transformer-attention, layer-normalization]
sources: [https://arxiv.org/html/2302.05442]
status: explained
created: 2026-10-18
updated: 2026-10-18
---

# Query-Key Normalization

## Summary

Query-key normalization applies a chosen normalization to projected queries and keys before their dot products to control attention-logit scale and training instability.

## Grounded explanation

A large query or key magnitude can create extreme attention scores. After softmax, one position may receive nearly all the weight, making attention insensitive to alternatives. Dividing by the square root of feature width does not by itself control learned vector magnitudes. Query-key normalization changes the projected vectors before their dot products.

For an input state matrix $X$, query and key projection matrices $W_Q,W_K$, and query/key width $d$, the ViT-22B formulation computes

$$Q=\operatorname{LN}(XW_Q),\qquad K=\operatorname{LN}(XW_K),\qquad A=\operatorname{softmax}(QK^\top/\sqrt d).$$

Here $\operatorname{LN}$ denotes [[layer-normalization]] across the selected feature axis, and $A$ is the attention-weight matrix used by [[transformer-attention]]. The change is specifically on queries and keys; normalizing the input state before the projections is not the same operation. Values are not automatically normalized by this rule.

Why does this help? Layer normalization removes a vector's common offset and controls its spread before the score product. In a simplified two-coordinate vector $q=[10,20]$, ignoring the small stabilizer and using unit learned gain and zero offset, centering and scaling produces $[-1,1]$. Multiplying both original coordinates by ten still produces the same normalized vector. A purely magnitude-driven growth in this direction therefore no longer multiplies its dot products by ten. Learned gains, offsets, epsilon, and the key vector still matter: this is not a universal bound on attention scores.

ViT-22B reports training instability associated with growing logits and low attention entropy, and uses query/key LayerNorm to mitigate it. Other architectures use other normalizers, but these are not identical: centering, scale parameters, axis selection, and interaction with position transforms can change the function. State the exact variant rather than treating every `qk_norm` option as interchangeable.

Diagnose with maximum logits, attention entropy, loss, gradients, and numerical errors across training. Ablate normalization under matched architecture and optimization settings, and assess final task quality and runtime overhead. Peaky attention is not inherently wrong; the target is uncontrolled instability, not forced uniform attention. Query-key normalization does not establish calibrated classification confidence and is not a replacement for evaluation on the actual task.

## Prerequisites

- [[transformer-attention]]
- [[layer-normalization]]

## Sources

- <https://arxiv.org/html/2302.05442>
