---
id: adagrad
title: AdaGrad
summary: AdaGrad scales each gradient coordinate by the inverse square root of its cumulative squared-gradient history.
type: concept
tags: [ml/deep-learning]
prereqs: [gradient-descent]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adagrad.html]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# AdaGrad

## Meaning

AdaGrad changes [[gradient-descent]] so coordinates with large accumulated gradients receive smaller effective learning rates. This can help when rare and frequent features are updated at very different rates. It is a history-dependent diagonal scaling, not a measurement of curvature.

## Mechanism

For one coordinate, let theta be the parameter, g_t its gradient at step t, s_t the cumulative squared-gradient state, eta a positive learning rate, and epsilon a positive stabilizer. With a specified nonnegative initial s_0, use

$$s_t=s_{t-1}+g_t^2,\qquad \theta_t=\theta_{t-1}-\eta\frac{g_t}{\sqrt{s_t}+\epsilon}.$$

All coordinates follow this rule independently. Large past gradients increase the denominator, reducing later steps on that coordinate. Unlike an exponentially forgetting average, old observations never disappear. This is useful history on some sparse tasks but can make adaptation excessively slow after many updates. Some implementations add an explicit learning-rate decay or coupled L2 penalty; state those options rather than treating them as part of every AdaGrad run.

## One example

Take eta=0.1, epsilon=0.01, s_0=1 and theta_0=2. A gradient g_1=3 gives s_1=10 and a decrement 0.3/(sqrt(10)+0.01), about 0.09457, leaving theta_1 about 1.90543. A second gradient of -1 gives s_2=11 and an increment 0.1/(sqrt(11)+0.01), about 0.03006. The accumulator grows despite the sign reversal: squared history tracks scale, not direction.

## Check your understanding

Does the accumulator decrease when a gradient changes sign? No. Its increment is a square. Compare rare-coordinate behavior, stability, memory and time-to-quality with tuned alternatives; do not infer a universally superior optimizer from a sparse-feature example. Check initialization, epsilon placement, sparse-gradient support and runtime options against the actual implementation.

## Prerequisites

- [[gradient-descent]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adagrad.html>
