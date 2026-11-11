---
id: dynamic-reward-group-sampling
title: "Dynamic Sampling of Informative Reward Groups"
summary: "Dynamic group sampling replenishes a training batch after filtering prompt groups with no relative reward signal, changing both useful-batch size and the selected prompt distribution."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [group-relative-policy-optimization]
sources: [https://arxiv.org/abs/2503.14476]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# Dynamic Sampling of Informative Reward Groups

## Meaning

Dynamic group sampling tries to keep a group-relative policy update supplied with informative comparisons. It samples candidate prompt groups, drops groups whose rewards carry no within-group contrast, and generates more until an acceptance target or explicit budget is reached.

## Mechanism

In [[group-relative-policy-optimization]], a prompt's response rewards are centered against their group mean. A group with identical rewards has zero centered advantages; its reward-only relative term cannot distinguish the sampled answers. DAPO uses dynamic sampling to filter all-correct and all-incorrect groups in its correctness setting and replenish the batch. A general continuous reward requires a declared dispersion rule, not merely a binary correctness test.

This is not free variance reduction. It conditions training on which prompts currently yield varied outcomes. Easy prompts, very hard prompts and low-resolution scorers can all be removed. An all-equal group can still matter to a separate reference penalty or supervised term, and zero contrast does not prove that the prompt is useless forever.

## One example

Four prompts produce four binary rewards each: A=[1,1,1,1], B=[0,0,0,0], C=[1,0,1,0], D=[1,1,1,0]. A and B have zero centered signals. C's centered rewards are [.5,-.5,.5,-.5]; D's are [.25,.25,.25,-.75]. If the target is three accepted groups, this first attempt provides two and a further accepted group is needed. At a stationary acceptance probability .5, obtaining three accepted groups requires six proposed groups on average, not three. Real acceptance changes as the policy learns.

## Boundaries and check

Bound attempts and total generated tokens; a policy with nearly all-equal groups can otherwise generate indefinitely. Log proposed and accepted prompts, rejection reasons, reward variance, prompt coverage and rollout cost. Evaluate held-out easy and hard slices as well as the accepted middle. Compare fixed proposed-token budgets, not only equal accepted batch size. Does filtering all failures teach the model how to solve impossible prompts? No: it changes which comparisons enter the update and may starve those prompts without another exploration mechanism.

## Prerequisites

- [[group-relative-policy-optimization]]

## Sources

- <https://arxiv.org/abs/2503.14476>
