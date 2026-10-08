---
id: success-filtered-self-training
title: Success-Filtered Self-Training
summary: "A policy samples attempts, keeps successful trajectories, and imitates them; its selection bias and stale data set limits."
type: concept
tags: [ml/llm/training]
prereqs: [neural-network, loss-function, probability-distribution]
sources: [https://arxiv.org/abs/2308.08998]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Success-Filtered Self-Training

## Summary

**Success-filtered self-training** repeats generate → verify → keep successes → fit the model to kept trajectories. It is an inexpensive baseline when a [[neural-network]] already succeeds often enough for the filter to produce diverse examples. It is not automatically equivalent to online policy-gradient training.

## Grounded explanation

Let a model sample an output $y$ for task $x$ and let a test assign binary reward $r(x,y)$. The keep rule selects only examples with $r=1$; ordinary supervised fitting then increases their log-probability under a [[loss-function]] such as negative log-likelihood. ReST's original paper describes generating an offline dataset with the current policy and reusing it to improve the policy. The sampling policy, filter, and number of training epochs matter: fitting a static pile of old successes is not the same estimator as freshly sampling from the current policy at every update.

The selected dataset has a biased task distribution. An easy task may contribute many successes while a difficult task contributes none. Failed attempts provide no explicit counterexample, although increasing probability of successes changes normalized alternatives indirectly. A sparse binary test also collapses near-success and complete failure. Reuse of older outputs may narrow diversity and produce a mismatch between the current policy and the data-generating one. These are failure modes to diagnose, not universal ceilings. Reward weighting of log-probabilities resembles a score-function term under matched sampling assumptions; it does not erase the differences in data reuse, baselines, normalization, or optimizer.

For an agent with executable tests, start with a fixed task suite split by difficulty. Compare success filtering with on-policy optimization at equal generated trajectories, training tokens, and compute. Report held-out pass@1, pass@k, diversity of accepted solutions, per-task coverage, and reward exploitability. Rebalance tasks or refresh rollouts when coverage or freshness—not the optimizer—causes the plateau.

**Pass@k** asks whether at least one of $k$ sampled attempts passes a verifier; pass@1 measures a single attempt. If independent attempts each have success probability $p$, the idealized pass@k is $1-(1-p)^k$. Correlated samples and finite benchmark estimators break that shortcut, so report the sampling temperature, sample count, verifier, and uncertainty. A training loop may improve pass@1 while reducing solution diversity and thus harming pass@k, or vice versa.

## Prerequisites

- [[neural-network]]
- [[loss-function]]
- [[probability-distribution]]

## Sources

- [Gulcehre et al., Reinforced Self-Training](https://arxiv.org/abs/2308.08998): generate-and-improve loop with offline data reuse; its machine-translation results are not agent benchmark results.
