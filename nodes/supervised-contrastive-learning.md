---
id: supervised-contrastive-learning
title: Supervised Contrastive Learning
summary: Supervised contrastive learning trains embeddings by attracting examples with the same label and repelling examples with different labels within a comparison batch.
type: concept
tags: [ml/deep-learning]
prereqs: [embedding, softmax, loss-function]
sources: [https://arxiv.org/abs/2004.11362]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Supervised Contrastive Learning

## Summary

**Supervised contrastive learning** uses labels to shape an [[embedding]] space. For each anchor, other examples with the same class are positives and examples with different classes are negatives.

## Grounded explanation

Let $z_i$ be a normalized embedding for anchor $i$, $P(i)$ its positive indices, $A(i)$ all other compared examples, and $\tau>0$ a temperature. A common supervised contrastive [[loss-function]] is

$$L_i=-\frac{1}{|P(i)|}\sum_{p\in P(i)}\log\frac{\exp(z_i^\top z_p/\tau)}{\sum_{a\in A(i)}\exp(z_i^\top z_a/\tau)}.$$

The denominator is a [[softmax]] over similarities. Minimizing the loss raises similarity to every same-label positive relative to different-label examples. Unlike ordinary cross-entropy on classifier logits, the objective directly organizes representation geometry and can use multiple positives per anchor.

Batch composition is part of the objective. An anchor with no same-label peer cannot contribute in this form, while few negatives make the comparison weak. Augmentations must preserve labels, and class imbalance can make some anchors or classes dominate the available pairs.

Same-label attraction can also erase useful within-class structure. Noisy labels create false positives; semantically related classes create false negatives. The method does not inherently prevent catastrophic forgetting when old examples or anchors disappear from a sequential stream.

Compare it with cross-entropy at matched architecture, augmentations, tokens or images, and optimization budget. Evaluate linear-probe or fine-tuned task quality, retrieval structure, robustness slices, calibration, batch-size sensitivity, and old/new-task retention when used in continual learning.

## Prerequisites

- [[embedding]]
- [[softmax]]
- [[loss-function]]

## Sources

- [Khosla et al., “Supervised Contrastive Learning”](https://arxiv.org/abs/2004.11362): extend batch contrastive objectives to labels by attracting same-class embeddings and separating different-class embeddings.
