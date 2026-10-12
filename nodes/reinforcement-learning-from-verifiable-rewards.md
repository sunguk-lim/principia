---
id: reinforcement-learning-from-verifiable-rewards
title: Reinforcement Learning from Verifiable Rewards
summary: RLVR updates a model from sampled outputs scored by executable checks rather than requiring a target reasoning trace for every prompt.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [model-free-learning, verifiable-reward-design]
sources: [https://arxiv.org/abs/2501.12948, https://arxiv.org/abs/2402.03300]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Reinforcement Learning from Verifiable Rewards

## Summary

**Reinforcement learning from verifiable rewards (RLVR)** samples responses to prompts, scores them with an executable checker, and updates the model to favor higher-scoring behavior. Training examples need a task and a way to check outcomes; they need not provide a complete ideal reasoning trace.

## Grounded explanation

In a math setting, a prompt and reference answer define a narrow check. The policy produces several candidate solutions; a [[verifiable-reward-design]] scores their final answers. A [[model-free-learning]] update uses sampled responses and rewards to change response probabilities. This can discover useful intermediate behavior, but it can also learn output formats or shortcuts that satisfy the checker. It does not prove that the generated reasoning is faithful.

RLVR describes the **feedback source**, not a unique optimizer. Group-relative policy optimization, PPO-like methods, or other policy updates can use verifiable rewards. Supervised fine-tuning instead imitates target responses; DPO uses labeled preference pairs. Which approach is appropriate depends on feedback quality, available compute, exploration needs, and whether reliable executable checks exist. The training procedure should include a reference-policy or update-size control when needed to avoid destabilizing large shifts.

Freeze a task-separated held-out set before reward tuning. Compare baseline and trained models at matched inference budgets, report accuracy, invalid-format rate, reward–accuracy divergence, latency, and evaluation contamination checks. Vary prompt wording and task difficulty to test transfer. A vendor workshop run, single benchmark, or rising training reward alone does not demonstrate general reasoning improvement.

## Prerequisites

- [[model-free-learning]]
- [[verifiable-reward-design]]

## Sources

- [DeepSeek-R1 technical report](https://arxiv.org/abs/2501.12948): describes reinforcement learning with rule-based rewards on verifiable tasks.
- [DeepSeekMath](https://arxiv.org/abs/2402.03300): introduces group-relative optimization for math reasoning.
