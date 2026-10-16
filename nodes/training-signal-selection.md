---
id: training-signal-selection
title: Training-Signal Selection for Language Models
summary: Choose prompting, supervised tuning, preference fitting, or online policy optimization by the feedback actually available and the outcome to be validated.
type: concept
tags: [ml/llm/training]
prereqs: [fine-tuning, llm-policy-optimization-method-selection, verifiable-reward-design]
sources: [https://huggingface.co/docs/trl/sft_trainer, https://huggingface.co/docs/trl/grpo_trainer, https://arxiv.org/abs/2305.18290]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Training-Signal Selection for Language Models

## Summary

The first question in method selection is not which optimizer is newest. It is what feedback is available: paired demonstrations, ranked responses, an executable task score, or interaction with a stateful environment.

## Grounded explanation

Start with a prompt-only baseline. If inputs have trusted target outputs, [[fine-tuning]] can imitate them; its failure modes include coverage gaps, label noise, and near-duplicate evaluation leakage. A fixed number of examples is a data constraint, not a universal ceiling on model behavior. Split by task, source, and time when examples may share templates.

If pairs of responses are ranked, preference fitting can compare them without an online environment. Direct Preference Optimization is one example; it still depends on preference quality and coverage. If responses can be scored reproducibly, policy optimization becomes possible, but a scorer is not automatically a complete environment: sequential tasks additionally require state transitions, allowed actions, and a way to recover from invalid effects. [[verifiable-reward-design]] separates executable scoring from the desired downstream outcome. [[llm-policy-optimization-method-selection]] explains the different rollout and feedback contracts of PPO, DPO, and GRPO.

Consider 2,000 labeled input-output pairs, a six-week deadline, and no reliable task scorer. Build a prompt baseline and a supervised adapter first. Explore preference or online methods only after establishing a usable feedback signal and sufficient rollout/evaluation budget. This is a default under those constraints, not a rule that reinforcement learning always requires a simulator or that supervised tuning must win.

Compare methods at a matched data, token, and compute budget. Hold out task families, measure actual success, invalid outputs, calibration or abstention where relevant, safety failures, latency, and total training and evaluation cost. Inspect reward–outcome divergence and exploitability before trusting a high reward score. A method change is justified by independent task outcomes, not by the fact that an automatic score exists.

## Prerequisites

- [[fine-tuning]]
- [[llm-policy-optimization-method-selection]]
- [[verifiable-reward-design]]

## Sources

- [TRL SFT Trainer](https://huggingface.co/docs/trl/sft_trainer): supervised training data and workflow.
- [TRL GRPO Trainer](https://huggingface.co/docs/trl/grpo_trainer): grouped rollout and reward interface.
- [DPO paper](https://arxiv.org/abs/2305.18290): preference-pair fitting without online reward calls.
