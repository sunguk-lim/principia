---
id: gradient-descent
title: Gradient descent
summary: Gradient descent minimizes a loss by repeatedly stepping the parameters in the direction that reduces it fastest.
type: concept
tags: [ml/deep-learning]
prereqs: [gradient, loss-function]
sources: []
status: explained
created: 2026-06-18
updated: 2026-06-18
---

# Gradient descent

## Summary

**Gradient descent** minimizes a loss by repeatedly stepping the parameters in the
direction that reduces it fastest.

## Grounded explanation

Take the [[gradient]] of the [[loss-function]] with respect to the parameters, then
move a small step *against* it:

$$\theta \leftarrow \theta - \eta\,\nabla \mathcal{L}(\theta)$$

Because $-\nabla\mathcal{L}$ points toward the steepest decrease, each step lowers
the loss; repeating drives it toward a minimum. The scalar $\eta$ (the learning
rate) sets the step size — too large overshoots, too small crawls. This is the
optimizer that fine-tuning runs.

## Prerequisites

- [[gradient]]
- [[loss-function]]

## Sources

_none_
