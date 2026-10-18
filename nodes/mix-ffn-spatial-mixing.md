---
id: mix-ffn-spatial-mixing
title: Mix-FFN Spatial Mixing
summary: Mix-FFN adds local spatial interaction inside a transformer feedforward block by applying a depthwise convolution on the token grid.
type: concept
tags: [ml/deep-learning]
prereqs: [position-wise-feed-forward-network, spatial-convolution]
sources: [https://arxiv.org/abs/2105.15203, https://raw.githubusercontent.com/NVlabs/SegFormer/master/mmseg/models/backbones/mix_transformer.py, https://arxiv.org/abs/2410.10629]
status: explained
created: 2026-10-19
updated: 2026-10-19
---

# Mix-FFN Spatial Mixing

## Meaning

A conventional position-wise feedforward block changes each token’s channels independently. Mix-FFN inserts a local grid operation so neighboring image tokens can exchange information inside that branch rather than relying exclusively on attention.

## Mechanism

After the first projection of a [[position-wise-feed-forward-network]], reshape the sequence into its known height-by-width spatial grid. A depthwise [[spatial-convolution]] filters each hidden channel using a local neighborhood, followed by activation and a final channel projection. SegFormer’s implementation uses a 3×3 depthwise layer between its linear maps. This preserves local structure without a full pairwise attention matrix. Padding and grid arrangement introduce spatial information; omitting an explicit positional table therefore does not make the model position-agnostic. Different variants place nonlinearities and gated paths differently, so “Mix-FFN” should be tied to an actual block definition.

## Worked example

For one hidden channel on a 3×3 grid with values 1 through 9 in row order, use a 3×3 all-ones depthwise kernel with zero padding. The center output is 45. The upper-left output sums 1+2+4+5=12 because five neighbors are outside the image. The same kernel has different boundary context, illustrating why zero padding can supply location cues. The output channel projection can mix channels after this spatial step. A flattened sequence with the wrong grid shape would mix unrelated tokens. Test non-square grids, boundary effects, padding masks, and changing resolution; compare local versus position-wise blocks at matched parameters and compute, with quality and runtime measurements.

## Check your understanding

Does removing an explicit position embedding remove every spatial prior? No. Convolutional neighborhoods, grid reshaping, patch extraction, and padding still encode structure.

## Prerequisites

- [[position-wise-feed-forward-network]]
- [[spatial-convolution]]

## Sources

- <https://arxiv.org/abs/2105.15203>
- <https://raw.githubusercontent.com/NVlabs/SegFormer/master/mmseg/models/backbones/mix_transformer.py>
- <https://arxiv.org/abs/2410.10629>
