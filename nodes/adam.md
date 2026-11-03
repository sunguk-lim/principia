---
id: adam
title: Adam
summary: Adam combines bias-corrected exponential averages of gradients and squared gradients to form a directionally smoothed coordinate-adaptive update.
type: concept
tags: [ml/deep-learning]
prereqs: [momentum, rmsprop]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adam.html, https://arxiv.org/abs/1412.6980]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Adam

## Meaning

Adam combines the directional history of [[momentum]] with the squared-gradient scale history of [[rmsprop]]. Its two parameter-shaped buffers answer different questions: which direction persists, and how large have recent coordinate gradients been?

## Mechanism

Let g_t be a coordinate gradient, m_t the first average and v_t the square average. Let beta_1 and beta_2 lie between zero and one. From zero initial buffers, compute

$$m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,\quad
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2.$$

Define corrected estimates mhat_t=m_t/(1-beta_1^t) and vhat_t=v_t/(1-beta_2^t). With learning rate eta and positive epsilon, update theta_t=theta_previous-eta*mhat_t/(sqrt(vhat_t)+epsilon). The corrections counter the early downward bias caused by initializing averages to zero; they do not make noisy gradients exact population statistics. The second average is not a Hessian estimate.

## One example

Use eta=0.1, epsilon=0.01, beta_1=0.5 and beta_2=0.75. For gradients 2 then -1, the first step has m_1=1, v_1=1, corrected values 2 and 4, and decrement 0.2/2.01, about 0.09950. At step two, m_2=0 and v_2=1. The corrected first average is zero, so the adaptive update is zero although the current gradient is negative. The earlier positive direction and new negative direction canceled in momentum; scaling alone would not do this.

## Check your understanding

Does Adam always move against the current minibatch gradient? No: its remembered direction can differ. State epsilon placement, bias correction, weight-decay semantics and precision. Two FP32 moment arrays require eight bytes per parameter, excluding weights, gradients and workspace. Tune schedules and evaluate held-out quality and wall-clock cost; adaptive scaling does not guarantee best generalization or convergence on every objective.

## Prerequisites

- [[momentum]]
- [[rmsprop]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adam.html>
- <https://arxiv.org/abs/1412.6980>
