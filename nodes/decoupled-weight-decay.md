---
id: decoupled-weight-decay
title: Decoupled Weight Decay
summary: Decoupled weight decay shrinks parameters separately from an adaptive gradient transformation instead of passing an L2 penalty through that transformation.
type: concept
tags: [ml/deep-learning]
prereqs: [adam, regularization]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html, https://arxiv.org/abs/1711.05101]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Decoupled Weight Decay

## Meaning

Decoupled weight decay separates parameter shrinkage from the gradient transformation. AdamW applies this idea to [[adam]]. Although L2 penalties and multiplicative shrinkage can coincide for plain gradient descent under matched conventions, they generally differ when the optimizer rescales coordinates adaptively.

## Mechanism

Let theta be a parameter, eta the learning rate, lambda a decay coefficient and u the adaptive update direction formed only from data-loss gradients. A common step is theta_new=(1-eta*lambda)*theta-eta*u. The decay is applied directly, outside the moment buffers and coordinate denominator.

By contrast, adding lambda*theta to the loss gradient makes that penalty enter both Adam's first and second moment statistics. Its subsequent effect depends on gradient history. [[regularization]] defines the modeling objective, but implementing L2 in an adaptive gradient is not equivalent to a separate uniform shrinkage operation. State parameter exclusions and ordering: biases or normalization scales may use a different policy, and a decaying learning rate changes shrinkage per step under this convention.

## One example

Suppose theta has coordinates [2,4], eta=0.1, lambda=0.2 and a fixed data update u=[0.5,0.25]. Decoupled shrinkage produces 0.98*[2,4]-0.1*[0.5,0.25]=[1.91,3.895]. Both parameters shrink by the same fraction before the data update.

To isolate the distinction, imagine a fixed diagonal adaptive scaling [1,0.1] applied to an L2 gradient [0.4,0.8]. That penalty would produce decrements [0.04,0.008], not the decoupled [0.04,0.08]. This is a frozen-scaling illustration, not a full Adam trajectory: coupled Adam also changes its future buffers.

## Check your understanding

Can the same numeric lambda be transferred between coupled L2 and AdamW as if their effects were identical? No. Tune learning rate and decay jointly, specify exclusions and schedules, and evaluate held-out quality. Decoupling makes the shrinkage mechanism explicit; it does not remove interactions with training length, learning rate or other regularizers.

## Prerequisites

- [[adam]]
- [[regularization]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.optim.AdamW.html>
- <https://arxiv.org/abs/1711.05101>
