---
id: group-relative-policy-optimization
title: Group Relative Policy Optimization
summary: GRPO estimates each sampled response’s advantage relative to other responses for the same prompt, avoiding a separate learned value model.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [reinforcement-learning-from-verifiable-rewards, advantage-baseline]
sources: [https://arxiv.org/abs/2402.03300]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Group Relative Policy Optimization

## Summary

**Group Relative Policy Optimization (GRPO)** samples a group of outputs for one prompt and evaluates each against its peers. The group's reward mean and spread provide a relative advantage signal, so the method does not require a separately trained value model for each state.

## Grounded explanation

For one prompt, sample several completions from the current policy. Score each with a reward, which may come from [[reinforcement-learning-from-verifiable-rewards]]. Subtract the group mean reward and scale by the group's dispersion: a response above its peers gets positive relative advantage, and one below gets negative relative advantage. The [[advantage-baseline]] centers the reward signal so each completion is judged against peers for the same prompt. A clipped or otherwise constrained policy update limits how far the new policy moves from the sampled policy; a reference-policy penalty can limit drift further.

The group baseline removes a value-model training component but does not eliminate sampling cost, reward noise, or credit-assignment problems. If every candidate receives the same score, the group contains little relative signal. Group size, reward granularity, prompt distribution, length normalization, and clipping choices affect stability and cost. A verifier that rewards a shortcut can make GRPO optimize that shortcut efficiently.

Compare with supervised fine-tuning and an alternative policy update at matched rollout and compute budgets. Report held-out task accuracy, reward/accuracy divergence, response diversity, invalid-output rate, and sensitivity across random seeds. Do not infer superiority from one vendor recipe or a training curve without independent evaluation.

## Prerequisites

- [[reinforcement-learning-from-verifiable-rewards]]
- [[advantage-baseline]]

## Sources

- [DeepSeekMath](https://arxiv.org/abs/2402.03300): introduces GRPO and its group-relative advantage construction.
