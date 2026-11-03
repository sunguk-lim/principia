---
id: ml-task-specification
title: ML Task Specification
summary: An ML task specification connects a prediction to an operational decision, admissible data, measurable outcomes and a non-ML baseline before model development.
type: concept
tags: [ml/systems]
prereqs: [measurement, loss-function]
sources: [https://developers.google.com/machine-learning/guides/rules-of-ml]
status: explained
created: 2026-11-04
updated: 2026-11-04
---

# ML Task Specification

## Meaning

An ML task specification defines what decision a system should improve before choosing a model. It names the prediction unit, information available at decision time, desired outcome, costs of mistakes and operating constraints. A metric that is easy to optimize is not automatically the outcome users need.

## Mechanism

Start with the action and its owner. Define the population, prediction time, label meaning, observation delay and conditions under which the prediction is used or ignored. Separate the training [[loss-function]] from the operational success metric. Then use [[measurement]] to establish a simple non-ML or fixed-rule baseline and the evidence needed to justify added complexity. Google’s Rules of ML explicitly recommends considering a launch without ML, establishing metrics and beginning with a simple pipeline; these are engineering practices, not guarantees for every application.

Check feasibility: can required information be collected legitimately before the decision, can outcomes be observed, and can the service meet latency, reliability and maintenance needs? If labels arrive weeks later, an immediate dashboard proxy cannot silently certify the actual goal. Write stop conditions and who can revise the task contract when costs or user needs change.

## One example

An invented support queue receives 100 cases daily. The decision is which cases a human should review within an hour, not merely which category a case belongs to. Suppose missing an urgent case costs 20 units and reviewing a nonurgent one costs 1. A classifier’s 95% accuracy does not specify either cost: five missed urgent cases cost 100 units, while five needless reviews cost 5. Record those outcomes and review capacity, compare with the current rule, and choose acceptance limits before tuning.

## Check your understanding

Can a lower training loss prove that automation is worth deploying? No. It may not improve the decision outcome or satisfy operating constraints. Preserve the baseline, denominators, delayed-label policy and action boundaries. Model selection is a later conditional decision, not a substitute for specifying the problem.

## Prerequisites

- [[measurement]]
- [[loss-function]]

## Sources

- <https://developers.google.com/machine-learning/guides/rules-of-ml>
