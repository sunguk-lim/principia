---
id: factorial-agent-evaluation
title: "Factorial Agent Evaluation"
summary: "Factorial agent evaluation crosses harness and model choices on matched tasks to distinguish runtime effects, model effects and their interaction."
type: concept
tags: [ml/evaluation]
prereqs: [agent-execution-harness, paired-benchmark-uncertainty]
sources: ["https://www.anthropic.com/research/demystifying-evals-for-ai-agents", "https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Factorial Agent Evaluation

## Meaning

A factorial evaluation runs combinations of several independently chosen factors. For agents, a model and its surrounding harness are separate factors: an expensive model inside one runtime and a cheap model inside another cannot isolate which difference caused the observed outcome. The [[agent-execution-harness]] defines the surrounding runtime controls, tools and state whose effects the experiment compares.

## Mechanism

Cross two harnesses with two models, rather than measuring only two diagonal combinations. Use the same task instances, initial files, allowed tools, success checks and resource policy in every cell. Pin each component's version and record unavoidable capability differences. Repeated trials should use separate clean environments; randomize order to reduce time-dependent infrastructure effects. Matching inputs does not make the runtime the only difference if the model also changes.

The harness effect is a comparison while holding the model fixed. The model effect holds the harness fixed. An interaction means one factor's measured effect depends on the other factor. Use [[paired-benchmark-uncertainty]] on per-task outcomes; do not treat many correlated retries of one issue as many independent tasks. A task-pass rubric, infrastructure-failure category and complete cost trace are necessary before interpreting scores.

## One example

Invented mean task-success rates are: harness A with model X, 80%; A with Y, 60%; B with X, 70%; B with Y, 90%. Switching A to B changes X by minus 10 percentage points but Y by plus 30. The difference of these differences is 40 points. That interaction contradicts the claim that B has one model-independent advantage. Comparing only A/X with B/Y would hide it.

Report the four cells, task-level differences, repeats and uncertainty, alongside latency and total resource use. Small samples or incomparable vendor credit units cannot establish a universal ranking. Additional factors increase experimental cost, so a small deliberate cross is often more useful than an uncontrolled leaderboard.

## Check your understanding

If B/Y beats A/X, did B cause the improvement? Not identified: both factors changed. Measure the other combinations before attributing the difference.

## Prerequisites

- [[agent-execution-harness]]
- [[paired-benchmark-uncertainty]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm>
