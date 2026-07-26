---
id: neural-network
title: Neural network
summary: A neural network maps inputs to outputs by alternating linear transformations with simple nonlinearities, stacked into layers.
type: concept
tags: [ml/deep-learning]
prereqs: [matrix-multiplication, softmax]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Neural network

## Summary

A **neural network** maps inputs to outputs by alternating linear transformations
with simple nonlinearities, stacked into layers.

## Grounded explanation

Each layer multiplies its input by a weight matrix ([[matrix-multiplication]]),
adds a bias, and applies a nonlinearity $\sigma$:

$$h^{(l)} = \sigma\!\big(W^{(l)} h^{(l-1)} + b^{(l)}\big)$$

Stacking layers composes these maps; the output layer often uses [[softmax]] to
produce probabilities. The weight matrices $W^{(l)}$ are the **parameters** learned
during training — and they are exactly what transformer-attention is built
from and what lora adapts.

## Prerequisites

- [[matrix-multiplication]]
- [[softmax]]

## Sources

_none_
