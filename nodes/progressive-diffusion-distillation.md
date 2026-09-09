---
id: progressive-diffusion-distillation
title: Progressive Diffusion Distillation
summary: Progressive diffusion distillation repeatedly trains a student sampler to replace two deterministic teacher steps with one, halving required model evaluations at each stage.
type: concept
tags: [ml/llm/inference]
prereqs: [denoising-diffusion-probabilistic-model, inference-cost-break-even]
sources: [https://arxiv.org/abs/2202.00512]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Progressive Diffusion Distillation

## Summary

**Progressive diffusion distillation** compresses a deterministic diffusion sampler's trajectory. Each stage teaches a student update to match the result of two teacher updates, then treats that student as the next teacher.

## Grounded explanation

If a teacher sampler requires $N$ neural-network evaluations, one stage targets $N/2$ evaluations; repeated stages produce $N/4,N/8,\ldots$. The progressive construction keeps each student's local target closer to its teacher than directly asking a one-step model to reproduce a long trajectory.

Salimans and Ho combine this process with parameterizations designed to remain stable at few steps and report four-step image sampling on their benchmarks with little perceptual-quality loss. That result is experiment-specific. Distillation changes the learned sampler and can alter density estimates, diversity, guidance behavior, and robustness outside the training distribution.

Model width and step count are separate cost axes. Fewer evaluations attack sequential latency; smaller or quantized networks attack per-evaluation memory, throughput, and arithmetic. The dominant term depends on latent resolution, guidance passes, decoder cost, batch size, hardware, and compilation, so profile before selecting either intervention.

Compare teacher and students at every stage using end-to-end latency, number of evaluations, device utilization, peak memory, cost, quality, diversity, and prompt adherence. Include equal-latency baselines with better solvers or fewer undistilled steps, and account for distillation training cost through [[inference-cost-break-even]]. Stop before cumulative approximation error crosses the deployment quality bound.

## Prerequisites

- [[denoising-diffusion-probabilistic-model]]
- [[inference-cost-break-even]]

## Sources

- [Salimans and Ho, “Progressive Distillation for Fast Sampling of Diffusion Models”](https://arxiv.org/abs/2202.00512): repeatedly halves deterministic sampling steps and studies stable few-step parameterizations and quality.
