---
id: on-policy-optimal-baseline
title: "On-Policy RL with Optimal Reward Baseline"
summary: "OPO couples fresh data for each policy update with a practical length-weighted approximation to the variance-minimizing reward baseline."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [reinforce-policy-gradient]
sources: [https://arxiv.org/abs/2505.23585, https://raw.githubusercontent.com/verl-project/verl/main/docs/algo/opo.md]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# On-Policy RL with Optimal Reward Baseline

## Meaning

On-Policy RL with Optimal Reward Baseline (OPO) changes both data freshness and baseline construction. It generates new responses for each policy-gradient step rather than performing many steps on a fixed old-policy batch. Its practical baseline weights sampled response rewards by length under a stated approximation.

## Mechanism

In [[reinforce-policy-gradient]], define g(y)=gradient_theta log pi_theta(y|x), R(y) its reward, and b a prompt-conditioned scalar baseline. Minimizing the estimator's total coordinate variance leads to b_star=E[||g||² R]/E[||g||²], where ||g||² is the sum of squared parameter-gradient coordinates. This weights rewards by gradient magnitude, not just by frequency.

Computing per-response gradient magnitudes is costly. OPO approximates ||g||² as proportional to response length when token-gradient directions are approximately orthogonal and their squared magnitudes have a similar distribution. The resulting population baseline is E[T R]/E[T], and a group implementation uses sum_i T_i R_i/sum_i T_i. This is a practical approximation, not a theorem that response length always measures gradient variance.

The documented recipe omits learned critic and reference models and explicit KL/entropy terms. Removing those components does not guarantee that task accuracy, diversity or safety will be preserved; those remain evaluation outcomes.

## One example

Two sampled responses have lengths 2 and 6, with rewards 1 and 0. The practical baseline is (2×1+6×0)/(2+6)=.25 rather than the ordinary mean .5. Centered rewards are .75 and -.25. A long low-reward response pulls the baseline downward more than a short one. If actual gradient magnitudes do not track lengths, that weighting need not minimize variance.

## Boundaries and check

A population baseline independent of the sampled action has the standard expectation property. A finite group estimate that includes the current response is data-dependent; do not transfer an exact unbiasedness claim without analyzing that estimator. Detach the baseline. One rollout batch followed by sequential minibatch parameter changes is not exact fresh sampling for every step merely because the first step was on-policy.

Verify rollout-policy versions, update count per batch, distributed global denominators and length-gradient correlation. Compare total generated tokens, gradient variance, entropy and held-out quality. Does fresh sampling alone prevent arbitrarily large parameter steps? No: optimizer scale and reward errors still matter.

## Prerequisites

- [[reinforce-policy-gradient]]

## Sources

- <https://arxiv.org/abs/2505.23585>
- <https://raw.githubusercontent.com/verl-project/verl/main/docs/algo/opo.md>
