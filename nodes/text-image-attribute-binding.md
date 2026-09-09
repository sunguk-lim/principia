---
id: text-image-attribute-binding
title: Text–Image Attribute Binding
summary: Text–image attribute binding is a generative model's ability to attach each requested property to the intended object or region rather than merely include the words and objects somewhere in the image.
type: concept
tags: [ml/evaluation]
prereqs: [transformer-attention, multi-head-attention]
sources: [https://arxiv.org/abs/2310.11513]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Text–Image Attribute Binding

## Summary

**Text–image attribute binding** asks whether generated objects receive the properties assigned to them by a prompt. “A brown bear beside a white wall” requires not only a bear, a wall, brown, and white, but the correct pairing.

## Grounded explanation

Holistic image quality or text-similarity scores can remain high when attributes are assigned to the wrong objects. Binding is therefore evaluated compositionally: detect or segment each requested object, then test color, count, position, or another property at the corresponding instance or region.

Conditioning architecture can influence binding. [[transformer-attention]] can let image locations interact selectively with text tokens, while pooled global modulation applies one shared condition to many locations. Yet architecture alone does not identify the cause. Ambiguous captions, missing relational examples, weak objectives, limited spatial representations, and the sampler can produce similar failures. [[multi-head-attention]] maps are supporting diagnostics, not proof that a token caused a region.

Use controlled prompt pairs that exchange one attribute or relation while holding everything else fixed. Score object presence separately from correct pairing, and report per-property accuracy rather than one aggregate. Human-check a sample of detector-based judgments because the evaluator may fail on the same unusual compositions.

An intervention is supported only when an ablation isolates it: compare caption or region supervision, conditioning architecture, objective, and sampling at matched data and compute. Joint or cross-attention may improve token–region interaction but costs compute and does not guarantee semantic grounding.

## Prerequisites

- [[transformer-attention]]
- [[multi-head-attention]]

## Sources

- [Ghosh et al., “An Object-Focused Framework for Evaluating Text-to-Image Alignment”](https://arxiv.org/abs/2310.11513): introduces GenEval tasks for object co-occurrence, position, count, color, and attribute binding, with object-focused automated evaluation.
