---
id: usage-selection-bias
title: "Usage-Observation Selection Bias"
summary: "Usage-observation selection bias arises when platform participation and traffic mix determine which activity is visible, so observed volume cannot identify general model quality or adoption."
type: concept
tags: [ml/evaluation]
prereqs: [evaluation-slices]
sources: [https://developers.google.com/machine-learning/glossary#selection-bias]
status: explained
created: 2026-11-09
updated: 2026-11-09
---

# Usage-Observation Selection Bias

## Meaning

A platform's usage records describe activity selected into that platform. They do not automatically represent all users, tasks or available models. Token volume, request count and spending are different measures of that selected activity, not interchangeable votes for technical quality.

## Mechanism

Let S mean that a request appears in the observed service. A usage proportion is conditional on S; [[conditional-probability]] explains why it need not match the population proportion. Access, pricing, defaults, routing policies and which customers join can all change the observed mix. A before-and-after change can therefore reflect selection or workload changes rather than one model displacing another for identical tasks.

Use [[measurement]] to declare the denominator, time window and unit. Split new from returning users and compare stable cohorts where possible. [[evaluation-slices]] separates task and language mixtures that an aggregate can conceal. Usage data can show demand within its scope, but it does not identify a causal routing benefit without additional design and evidence. Google's glossary defines selection bias as a sampling process producing a sample unrepresentative of the population.

## One example

In an invented service, 100 returning users each generate one request: 60 use model A and 40 use B. Later those users make the same choices, while 100 newcomers all use B by default. B's share rises from 40/100=40% to 140/200=70%, even though no returning user switched. If B's outputs are twice as long, its token share differs again. Neither change alone establishes better answers or a causal effect of a routing launch.

## Check your understanding

Should usage rankings be ignored? No. They are useful evidence about observed demand and operational workload. Keep that conclusion separate from task quality, which needs controlled representative evaluations. Record missing populations, policy changes and billing units. A stable cohort reduces one source of selection but does not remove every confounder or make a popularity comparison a randomized experiment.

## Prerequisites

- [[evaluation-slices]]

## Sources

- <https://developers.google.com/machine-learning/glossary#selection-bias>
