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
updated: 2026-11-05
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

## Usage signals and composite router scores

A token-volume ranking describes the selected platform traffic, not a random sample of users or a held-out measure of task quality. A workflow generating 1,000 tokens per attempt contributes ten times the volume of one generating 100, even if both are invoked equally often. Prices, routing defaults, customer mix and output length can change the order. Use popularity for discovery, then evaluate the actual task; token share is not accuracy, unique-user preference or causal evidence of superiority.

A composite router index also makes a choice of priorities. State the normalization, workload weights and direction of each metric before combining them. Suppose A has normalized quality 0.9 and normalized cost 0.8, while B has quality 0.8 and cost 0.2, with lower cost preferred. The invented score quality−0.1×cost gives A=0.82 and B=0.78; changing the cost weight to 0.3 gives A=0.66 and B=0.74, reversing the rank. The measurements did not change: the objective did. Normalization changes can also reverse a ranking.

Keep hard constraints outside a compensating score: an unsafe or ineligible endpoint cannot buy eligibility with low cost. Compare a router with fixed-model and simple-policy baselines on held-out requests, including routing overhead, retries, cache effects and per-slice failure. Freeze the benchmark and tuning boundary; show uncertainty and the separate quality, latency and cost outcomes alongside any aggregate index. An aggregate task suite cannot certify all future workloads.

## Prerequisites

- [[paired-benchmark-uncertainty]]
- [[evaluation-slices]]
- [[measurement]]

## Sources

- <https://www.anthropic.com/research/demystifying-evals-for-ai-agents>
- <https://scikit-learn.org/stable/modules/model_evaluation.html>
