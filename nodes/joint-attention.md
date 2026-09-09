---
id: joint-attention
title: Joint Attention
summary: Joint attention computes attention over tokens from multiple modalities together, permitting cross-modal interactions while optionally retaining modality-specific projections and feed-forward networks.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, multi-head-attention, text-image-attribute-binding, softmax]
sources: [https://arxiv.org/abs/2403.03206]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Joint Attention

## Summary

**Joint attention** places token sets from two or more modalities in one attention computation so interactions can flow in multiple directions. It differs from ordinary cross-attention, where one stream supplies queries and another supplies keys and values for that block.

## Grounded explanation

Given text states $T$ and image states $I$, a simple joint design forms a combined sequence $X=[T;I]$ and computes

$$\operatorname{Attention}(X)=\operatorname{softmax}(QK^\top/\sqrt d)V.$$

The [[softmax]] converts each query's scores into attention weights. Its attention matrix contains text–text, text–image, image–text, and image–image blocks unless masks remove some interactions. In cross-attention from image to text, only image queries receive the cross-modal output; text states remain unchanged by that block.

“Joint” does not require every weight to be shared. The MMDiT design in Stable Diffusion 3 uses separate weights for text and image modalities while enabling bidirectional information flow. Attention can be the communication step while modality-specific projections or feed-forward networks preserve specialization. Fully shared weights reduce parameters and may encourage transfer; separate weights increase capacity and cost. Adapters or partial sharing provide intermediate designs.

Joint interaction may help [[text-image-attribute-binding]], typography, or prompt comprehension, but it does not guarantee them. Longer combined sequences increase attention memory and operations, and observed gains may come from capacity, data, training objectives, or other architecture changes.

Compare cross, joint, and hybrid attention with parameters, operations, data, and training duration controlled. Ablate update directions and shared versus separate projections and feed-forward networks. Measure binding and relation accuracy, text and image activation statistics, throughput, memory, and human preference with uncertainty.

## Prerequisites

- [[transformer-attention]]
- [[multi-head-attention]]
- [[text-image-attribute-binding]]
- [[softmax]]

## Sources

- [Esser et al., “Scaling Rectified Flow Transformers for High-Resolution Image Synthesis”](https://arxiv.org/abs/2403.03206): presents an architecture with modality-specific weights and bidirectional interaction between image and text tokens.
