---
id: advantage-baseline
title: Advantage Baseline in Policy Optimization
summary: "Subtracting a state- or group-level reward baseline centers policy updates and can reduce variance while retaining useful negative signals."
type: concept
tags: [ml/llm/training]
prereqs: [expectation, probability-distribution, gradient-descent]
sources: [https://arxiv.org/abs/2402.03300]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Advantage Baseline in Policy Optimization

## Summary

A policy update need not treat every success as equally surprising. An **advantage baseline** compares a sampled reward with an expected or peer reward: $A=r-b$. A positive $A$ reinforces the sample; a negative $A$ can lower its probability. The baseline's construction and sampling distribution determine whether the update has the intended interpretation.

## Grounded explanation

For a policy $\pi_\theta(y|x)$, the score-function update weights $\nabla_\theta\log\pi_\theta(y|x)$ by reward. If $b(x)$ does not depend on the sampled action and the samples come from that policy, subtracting it leaves the [[expectation]] of the policy-gradient estimator unchanged because the expected score is zero. It can reduce variance, but a poorly chosen baseline can increase it. Group-relative methods such as GRPO use peer samples for one prompt to form a relative score; their exact normalization, clipping, and data-collection choices are additional algorithm details, not implied by the word baseline.

Suppose two tasks both yield a success with reward one. On a task usually solved by everyone, that success conveys less comparative information than a rare success on a hard task. Likewise a rare failure on an easy task may receive a negative update. This is a way to allocate learning signal, not proof that advantage optimization always beats success-filtered fitting. With an all-equal group or a noisy verifier, the comparison may be uninformative or harmful.

Use a held-out task distribution and log per-task reward mean, group variance, effective sample size, update magnitude, pass@1 and pass@k, and failures introduced by reward gaming. Compare raw reward weighting, a learned or running baseline, and group-relative normalization with matched rollout budgets. Never interpret one reported benchmark as a portable optimizer advantage.

## Prerequisites

- [[expectation]]
- [[probability-distribution]]
- [[gradient-descent]]

## Sources

- [DeepSeekMath](https://arxiv.org/abs/2402.03300): original GRPO proposal; specific benchmark gains are author-reported.
