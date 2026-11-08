---
id: task-underspecification
title: "Task Underspecification"
summary: "Task underspecification leaves outcome-relevant choices open, allowing incompatible solutions to satisfy the same stated brief."
type: concept
tags: [ml/agents]
prereqs: [ml-task-specification]
sources: [https://www.anthropic.com/research/demystifying-evals-for-ai-agents, https://arxiv.org/abs/2011.03395]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Task Underspecification

## Meaning

A task is underspecified when its instructions and acceptance criteria do not settle decisions that matter to the intended result. This is not merely a short prompt: a concise contract can be sufficient, while a long document can leave the decisive population or objective undefined.

## Mechanism

Use an [[ml-task-specification]] to separate the requested action, admissible information, population, outcome and constraints. Enumerate remaining choices and ask whether reasonable alternatives produce materially different results. Resolve high-impact ambiguity through clarification, an explicit assumption or a bounded design proposal; keep low-impact implementation freedom. More detailed instructions help only if they settle the relevant ambiguity.

The ML-pipeline underspecification studied by D'Amour and colleagues is a related but narrower technical result: predictors with similar in-domain held-out performance can behave differently under deployment tests. It is not a claim that every ambiguous natural-language brief has that paper's formal definition. Both motivate [[measurement]] of properties the current acceptance rule leaves unconstrained.

## One example

An invented brief asks for a study of whether a tutoring tool improves grades. Analyst A compares users with nonusers; analyst B compares each user's before-and-after grades. Both can produce valid-looking tables, yet answer different questions with different confounders. Neither table alone identifies a causal improvement. Clarifying the target population, intervention, comparison and outcome timing changes the task before another model or longer prompt is tried. A simulation with known effects can then test the proposed estimator.

## Check your understanding

Does adding a reference answer remove all ambiguity? No. It may constrain presentation while leaving data access, methodology or permitted side effects open. Test alternate reasonable interpretations and record assumptions. Separate errors in following a settled contract from failures to notice that the contract itself was incomplete; otherwise an execution benchmark can silently reward one arbitrary default.

## Prerequisites

- [[ml-task-specification]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://arxiv.org/abs/2011.03395>
