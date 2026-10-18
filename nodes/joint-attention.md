---
id: joint-attention
title: Joint Attention
summary: Joint attention computes attention over tokens from multiple modalities together, permitting cross-modal interactions while optionally retaining modality-specific projections and feed-forward networks.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, multi-head-attention, text-image-attribute-binding, softmax]
sources: [https://arxiv.org/abs/2403.03206, https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/model.py, https://raw.githubusercontent.com/black-forest-labs/flux/main/src/flux/modules/layers.py]
status: explained
created: 2026-09-10
updated: 2026-10-19
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

### Double-stream to single-stream layouts

Joint interaction and parameter sharing are separate axes. In the released FLUX implementation, early double-stream blocks keep separate text/image modulation, projections, and feedforward paths, while concatenating their projected query/key/value sequences for a shared attention operation. Both modalities can therefore interact before their parameter paths are unified. After those blocks, the model concatenates the text and image hidden sequences, then processes them through single-stream blocks with a shared block computation. At the output, it slices away the text prefix and predicts image states.

For two text tokens and four image tokens, each double-stream attention operates on six projected tokens, but splits its output into two text and four image states for their separate updates. The transition produces one six-token hidden sequence; a later image output slices positions two through five. A wrong boundary can silently mix text conditioning and image outputs. A single shared stream is not six independent token models, and a double stream is not two isolated models: joint attention already couples them. This is an architectural layout change, not a speed-preserving rewrite that arbitrary trained separate projections can always undergo. Compare training quality, capacity, modality statistics, activation memory, and latency under controlled depth and width; do not infer a gain from the stream count alone.

## Prerequisites

- [[transformer-attention]]
- [[multi-head-attention]]
- [[text-image-attribute-binding]]
- [[softmax]]

## Sources

- [Esser et al., “Scaling Rectified Flow Transformers for High-Resolution Image Synthesis”](https://arxiv.org/abs/2403.03206): presents an architecture with modality-specific weights and bidirectional interaction between image and text tokens.

- [FLUX model and blocks](https://github.com/black-forest-labs/flux/tree/main/src/flux): released double-stream/single-stream transition and shared projection implementation.
