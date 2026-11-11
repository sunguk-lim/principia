---
id: generalized-advantage-estimation
title: "Generalized Advantage Estimation"
summary: "GAE estimates an action advantage by exponentially weighting successive value-prediction residuals, trading reliance on a critic against sampled-return variance."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [bellman-equation, advantage-baseline, variance]
sources: [https://arxiv.org/abs/1506.02438]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# Generalized Advantage Estimation

## Meaning

Generalized Advantage Estimation (GAE) constructs a policy-learning signal from rewards and a value estimator. It combines short, bootstrapped estimates with longer sampled outcomes instead of choosing only one horizon.

## Mechanism

Let t index a step, s_t be its state, r_t the reward after its action, V(s_t) an estimated future discounted return, gamma in [0,1] a discount factor, and lambda in [0,1] a trace-decay setting. The [[bellman-equation]] motivates the temporal residual delta_t=r_t+gamma V(s_(t+1))-V(s_t). For a finite trajectory ending at T, define

$$\hat A_t=\sum_{l=0}^{T-t-1}(\gamma\lambda)^l\delta_{t+l}.$$

The index l counts steps after t. The equivalent backward recursion is A_t=delta_t+gamma lambda A_(t+1), with the terminal continuation set appropriately. At lambda=0 only one residual matters. At lambda=1 the value terms telescope to a sampled discounted return minus the initial value, provided the terminal boundary is correct. The [[advantage-baseline]] gives the interpretation of this subtraction.

A smaller lambda reduces dependence on distant noisy rewards but places more trust in the value estimator. A larger lambda carries distant reward farther and can raise variance. Neither direction is universally superior, especially for long responses and inaccurate critics.

Here [[variance]] concerns repeated reward trajectories, not simply changing the output length.

## One example

Consider two steps, rewards [0,1], values [.4,.7,0], gamma=1 and lambda=.8. Residuals are .7-.4=.3 and 1-.7=.3. The final advantage is .3 and the first is .3+.8×.3=.54. With lambda=0 the first is .3; with lambda=1 it becomes .6, exactly final return 1 minus initial value .4. Thus the value at the intermediate step matters when lambda is less than one.

## Boundaries and check

An actual terminal state has no future value; a time-limit cutoff may still require bootstrapping. Padding is neither a transition nor a reward. Test the backward recursion against the explicit sum, including unequal lengths, masks, terminal states and truncations. Compare critic calibration and outcome quality across length slices, not just average advantage magnitude. Does setting lambda=1 make every part of a clipped off-policy training update unbiased? No: this is a statement about the estimator under its boundary and sampling assumptions.

## Prerequisites

- [[bellman-equation]]
- [[advantage-baseline]]

- [[variance]]

## Sources

- <https://arxiv.org/abs/1506.02438>
