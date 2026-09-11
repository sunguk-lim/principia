---
id: mixed-precision-training
title: Mixed-precision training
summary: Mixed-precision training uses lower-precision tensor operations where numerically safe while retaining selected higher-precision state and applying loss scaling to avoid underflowing gradients.
type: concept
tags: [ml/deep-learning]
prereqs: [gradient-descent, tensor]
sources: [https://docs.pytorch.org/docs/stable/amp.html]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Mixed-precision training

## Summary

**Mixed-precision training** combines lower-precision computation with selected higher-precision [[tensor]] state so hardware can reduce memory traffic and accelerate eligible operations without treating every numerical quantity as equally safe to narrow.

## Grounded explanation

Lower-precision floating-point formats represent fewer values than full precision. They can reduce memory use and can execute selected matrix operations faster on supported hardware, but their limited range can make small gradient values round to zero. Mixed precision therefore is a policy, not simply a global cast: an autocasting region chooses an eligible lower-precision dtype for supported operations, while operations that require a wider range remain in a safer dtype.

Gradient scaling protects an update from underflow. Before backpropagation, multiply the loss by a scale $s$; the resulting gradients are multiplied by the same $s$. Before the optimizer applies [[gradient-descent]], divide those gradients by $s$ to restore the intended update. If the scaled gradients contain non-finite values, a scaler can reduce $s$ and skip the unsafe update; scaling is an aid to numerical range, not a guarantee that every model is stable.

### Worked instance

Suppose an unscaled gradient for one parameter is $g=0.0005$ and a chosen scale is $s=1024$. Backpropagation carries $sg=0.512$, a value less likely to disappear in a narrow format. Before the optimizer update, unscaling returns $0.512/1024=0.0005$. With learning rate $\eta=0.1$, the intended update remains $w\leftarrow w-0.1(0.0005)$; scaling has changed representability during computation, not the mathematical target update.

Measure the result rather than assuming a universal speedup: supported hardware, operation mix, batch size, memory capacity, dtype choice, and numerical behavior determine the outcome. Keep validation metrics and finite-gradient checks alongside throughput measurements.

## Prerequisites

- [[gradient-descent]]
- [[tensor]]

## Sources

- [PyTorch Automatic Mixed Precision documentation](https://docs.pytorch.org/docs/stable/amp.html): documents `autocast` for per-operation dtype selection, `GradScaler` loss scaling, and the required scale-before-backward / unscale-before-step workflow.
