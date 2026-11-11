---
id: proximal-policy-optimization
title: "Proximal Policy Optimization"
summary: "PPO-Clip uses a pessimistic probability-ratio surrogate to remove incentives for excessive favorable movement on sampled actions."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [reinforce-policy-gradient]
sources: [https://arxiv.org/abs/1707.06347, https://spinningup.openai.com/en/latest/algorithms/ppo.html]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# Proximal Policy Optimization

## Meaning

Proximal Policy Optimization is a family of policy-update procedures. PPO-Clip, the variant developed here, reuses a collected batch while limiting the surrogate incentive for large favorable probability changes. It does not literally clamp every new probability or guarantee a maximum policy divergence.

## Mechanism

Following [[reinforce-policy-gradient]], collect actions y in contexts x from a frozen old policy pi_old. Let pi_theta be the policy being optimized, r=pi_theta(y|x)/pi_old(y|x) its sampled-action probability ratio, A a fixed estimated advantage, and epsilon a positive clipping width. Maximize the batch mean of

$$L(r,A)=\min(rA,\operatorname{clip}(r,1-\epsilon,1+\epsilon)A).$$

Here clip replaces numbers below the lower bound or above the upper bound with that bound. With A positive, increases beyond 1+epsilon stop improving this sample's objective. With A negative, decreases below 1-epsilon stop improving it. Movement in the unfavorable direction still receives a corrective gradient. A learned value function is a common way to estimate A, not a mathematical prerequisite of the clipped surrogate. A penalty against a separate reference policy is another independent choice.

## One example

Take epsilon=.2 and positive A=2. At r=1.1 the objective is min(2.2,2.2)=2.2; at r=1.4 it is min(2.8,2.4)=2.4, with no further favorable incentive. For A=-2 and r=.6 it is min(-1.2,-1.6)=-1.6, again flat in the favorable direction. But at A=-2 and r=1.4 it is min(-2.8,-2.4)=-2.8: increasing the probability of a bad action remains penalized. Clipping is sign-dependent pessimism, not symmetric gradient removal outside a band.

## Boundaries and check

Shared parameters couple samples, so flat contribution from one action does not freeze its probability. Repeated minibatch updates also move away from the sampling policy. Monitor actual divergence, ratio tails, clipped fractions by advantage sign, held-out task quality and total rollout cost; stop or refresh when the batch becomes stale. Does PPO-Clip guarantee monotonically improved real reward? No. Advantage error, reward flaws, finite samples and optimizer steps remain outside that guarantee.

## Prerequisites

- [[reinforce-policy-gradient]]

## Sources

- <https://arxiv.org/abs/1707.06347>
- <https://spinningup.openai.com/en/latest/algorithms/ppo.html>
