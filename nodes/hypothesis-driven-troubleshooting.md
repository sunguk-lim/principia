---
id: hypothesis-driven-troubleshooting
title: Hypothesis-Driven Troubleshooting
summary: Hypothesis-driven troubleshooting compares causal explanations through discriminating observations and bounded tests rather than equating correlated incidents with one proven cause.
type: concept
tags: [software/testing]
prereqs: [observability, measurement]
sources: [https://sre.google/sre-book/effective-troubleshooting/]
status: explained
created: 2026-10-20
updated: 2026-10-20
---

# Hypothesis-Driven Troubleshooting

## Meaning

A troubleshooting hypothesis proposes a mechanism connecting a change or failure to an observed symptom. The useful next step is evidence that separates that mechanism from plausible alternatives. A shared timestamp or agreement among investigators is a lead, not a causal proof.

## Mechanism

Stabilize the service first when necessary and preserve evidence. Use [[observability]] to locate the earliest bad boundary, record deployment and configuration versions, and list hypotheses with predicted observations. A good test changes one relevant factor or probes a component with known input, using [[measurement]] to compare the expected and observed outcomes. Bound production experiments, preserve rollback paths and avoid repeating harmful effects. A reversal can support causality but is not conclusive if load, dependencies or other variables changed at the same time. Negative results should narrow the search rather than be silently discarded.

## Worked example

An inference API starts failing and a training job stops progressing after a configuration rollout. One hypothesis is a shared credential change; another is two independent capacity failures. Check whether both processes read the same credential version, whether failures start at their next credential refresh, and whether an unaffected control still uses the old version. In a safe isolated reproduction, old credentials restore both paths while new credentials reproduce their distinct errors. That is stronger evidence than two linked incident chats mentioning the same deploy. If only the API recovers, revise the common-cause claim and investigate the training stall independently. Record exact interventions, observations, remaining uncertainty and a regression test for the proposed mechanism. Teams can share one evidence timeline without collapsing every symptom into a single root-cause label.

## Check your understanding

Does an incident disappearing after a rollback prove the rolled-back change caused it? It supports that hypothesis, but concurrent recovery, traffic changes or rollback side effects can confound the conclusion.

## Prerequisites

- [[observability]]
- [[measurement]]

## Sources

- <https://sre.google/sre-book/effective-troubleshooting/>
