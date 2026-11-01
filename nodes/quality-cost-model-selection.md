---
id: quality-cost-model-selection
title: Quality–Cost Model Selection
summary: Quality–cost model selection chooses a deployment configuration against task utility and measured resource constraints rather than ranking models by one benchmark or parameter count.
type: concept
tags: [ml/evaluation]
prereqs: [paired-benchmark-uncertainty, evaluation-slices, measurement]
sources: [https://www.anthropic.com/research/demystifying-evals-for-ai-agents, https://scikit-learn.org/stable/modules/model_evaluation.html]
status: explained
created: 2026-11-02
updated: 2026-11-02
---

# Quality–Cost Model Selection

## Meaning

A model is not simply better because it has lower validation loss or more parameters. Quality–cost selection chooses a model and deployment configuration for a declared task population, acceptance rule and resource budget. Quality is an outcome to measure, not a synonym for model size.

## Mechanism

Define required success, critical-slice quality and latency or memory limits before comparing candidates. [[evaluation-slices]] prevents an aggregate improvement from concealing unacceptable regressions. [[paired-benchmark-uncertainty]] distinguishes an observed matched-task difference from evidence strong enough to guide deployment. Lack of a detectable difference is not a proof of equality.

Measure the actual configuration through [[measurement]]: hardware, precision, batch policy, prompt, adaptation and retry policy all affect cost and quality. Remove configurations violating hard constraints. Among the rest, retain trade-offs rather than silently collapsing unrelated units. One candidate dominates another only if it is no worse on every declared objective and strictly better on at least one. A nondominated candidate can still be unsuitable for an unmeasured critical requirement.

## Worked example

A deployment requires at least 90% valid completion and a measured 95th-percentile latency below 2 seconds. On a held-out cohort, A records 92%, 1.5 seconds and $0.02 per attempt; B records 93%, 2.4 seconds and $0.04; C records 89%, 1.2 seconds and $0.01. B violates latency and C violates quality, so A is the only observed feasible candidate. If A's uncertainty interval crosses the quality threshold, gather more representative evidence rather than certifying it from the point estimate.

If the latency limit later changes, repeat the decision; the selected model is conditional on the contract. Values here are an invented decision example, not empirical model results.

## Boundaries and validation

Keep development tuning separate from final held-out acceptance. Compare paired outcomes, workload slices, tails and billed resources under matched traffic. Parameter doubling does not imply exactly doubled serving cost. Aggregate token loss can guide training without deciding a downstream cost–utility trade-off. Record the selection rule, uncertainty, configuration and rollback condition so the decision can be revisited when traffic or prices change.

## Prerequisites

- [[paired-benchmark-uncertainty]]
- [[evaluation-slices]]
- [[measurement]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://scikit-learn.org/stable/modules/model_evaluation.html>
