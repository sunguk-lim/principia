---
id: llm-policy-optimization-method-selection
title: LLM Policy Optimization Method Selection
summary: PPO, DPO, and GRPO use different feedback and sampling contracts; choose among them by reward reliability, available preference data, rollout cost, and evaluation needs.
type: concept
tags: [ml/llm/training]
prereqs: [reinforcement-learning-from-verifiable-rewards, advantage-baseline, reward-hacking]
sources: [https://arxiv.org/abs/1707.06347, https://arxiv.org/abs/2305.18290, https://arxiv.org/abs/2402.03300]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# LLM Policy Optimization Method Selection

## Summary

PPO, DPO, and GRPO are not interchangeable labels for “train from feedback.” They assume different feedback and data flows. Choose a method only after specifying what is scored, how responses are collected, and what outcome will be measured independently.

## Grounded explanation

**PPO** uses sampled policy trajectories and an advantage estimate to constrain policy updates. In LLM applications it can optimize a learned reward model or an executable reward, but collecting current-policy rollouts and training a value estimator add cost. The [[advantage-baseline]] explains why the advantage differs from raw reward.

**DPO** fits a policy from pairs of preferred and dispreferred responses relative to a reference policy. It uses an offline preference dataset rather than an online reward call for each new sample. That is attractive when reliable comparison pairs exist, but the policy is limited by their coverage and preference quality. It is not the same feedback contract as [[reinforcement-learning-from-verifiable-rewards]].

**GRPO** samples groups of responses for the same prompt and uses relative group rewards, avoiding a separate learned value model. It still needs fresh rollouts, enough reward variation within groups, and a trustworthy scorer. Group normalization changes learning dynamics; a binary reward that is identical across a group supplies little contrast.

Start with a strong supervised or preference-data baseline. Compare methods at matched task set, sampled tokens, compute budget, reference policy, and inference budget. Report held-out success, invalid-output rate, reward–outcome divergence, diversity, training stability, and operational cost. [[reward-hacking]] can affect PPO or GRPO when the scorer is exploitable; preference noise and selection bias can affect DPO. A named optimizer cannot repair an incorrect reward or leaked evaluation set.

## Prerequisites

- [[reinforcement-learning-from-verifiable-rewards]]
- [[advantage-baseline]]
- [[reward-hacking]]

## Sources

- [PPO](https://arxiv.org/abs/1707.06347): clipped policy optimization with sampled trajectories.
- [DPO](https://arxiv.org/abs/2305.18290): direct policy fitting from preference pairs.
- [DeepSeekMath](https://arxiv.org/abs/2402.03300): group-relative policy optimization.
