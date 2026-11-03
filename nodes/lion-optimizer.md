---
id: lion-optimizer
title: Lion Optimizer
summary: Lion uses the sign of a momentum–gradient blend for its update while retaining one momentum buffer rather than a second-moment buffer.
type: concept
tags: [ml/deep-learning]
prereqs: [momentum, decoupled-weight-decay]
sources: [https://arxiv.org/abs/2302.06675, https://github.com/google/automl/tree/master/lion]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# Lion Optimizer

## Meaning

Lion changes the magnitude rule of [[momentum]] optimization. Its data update uses only the sign of a blend of current gradient and remembered direction. Removing a second-moment buffer can save state, but taking a sign changes the geometry and effective step size.

## Mechanism

Let m be the old momentum, g the current gradient, beta_1 and beta_2 two averaging coefficients, eta the learning rate and lambda the decay coefficient. First form c=beta_1*m+(1-beta_1)*g. Update each parameter by theta_new=(1-eta*lambda)*theta-eta*sign(c), where sign gives -1, 0 or +1. Then store m_new=beta_2*m+(1-beta_2)*g for the next step. The blend used for this update and the buffer retained for later steps use different coefficients.

[[decoupled-weight-decay]] remains a separate shrinkage term. Within a parameter group, nonzero data-update coordinates have magnitude eta, regardless of the magnitudes of c. Thus copying a learning rate from an adaptive optimizer is not a fair comparison. The authors recommend retuning learning rate and weight decay; their workload-specific advantages are not universal guarantees.

## One example

Take old momentum [2,-1], current gradient [-1,3], beta_1=0.8 and beta_2=0.9. The update blend is [1.4,-0.2], whose sign is [1,-1]. With eta=0.05, the data update subtracts [0.05,-0.05], even though the second current gradient is positive. The new stored momentum is [1.7,-0.6]. These are distinct blend and storage results; replacing one coefficient with the other changes the algorithm.

## Check your understanding

Does one buffer imply half the total training memory? No. It can halve moment-buffer storage relative to two equally represented buffers, not weights, gradients or activations. Measure tuning cost, held-out quality, update stability, state bytes and wall-clock time. A sign-only step is neither universally more robust nor numerically interchangeable with AdamW.

## Prerequisites

- [[momentum]]
- [[decoupled-weight-decay]]

## Sources

- <https://arxiv.org/abs/2302.06675>
- <https://github.com/google/automl/tree/master/lion>
