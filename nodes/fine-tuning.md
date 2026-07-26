---
id: fine-tuning
title: Fine-tuning
summary: Fine-tuning continues training an already-trained model on new data so it adapts to a specific task.
type: concept
tags: [ml/deep-learning]
prereqs: [gradient-descent, neural-network]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Fine-tuning

## Summary

**Fine-tuning** continues training an already-trained model on new data so it
adapts to a specific task.

## Grounded explanation

Start from a [[neural-network]] whose weights were already learned on a large
general corpus (pretraining). Then run more [[gradient-descent]] steps on
task-specific data, updating the weights:

$$\theta \leftarrow \theta - \eta\,\nabla \mathcal{L}_{\text{task}}(\theta)$$

*Full* fine-tuning updates **all** the weights — accurate but expensive: every
parameter is copied, stored, and optimized. This cost is exactly what lora
removes: it freezes the pretrained weights and learns only a small low-rank update
instead, so fine-tuning a huge model becomes cheap.

## Prerequisites

- [[gradient-descent]]
- [[neural-network]]

## Sources

_none_
