---
id: progressive-model-rollout
title: Progressive Model Rollout
summary: Progressive model rollout limits initial exposure of a candidate model, evaluates it under production traffic, and expands or reverses exposure using predefined safety and quality gates.
type: concept
tags: [ml/evaluation]
prereqs: [multi-armed-bandit, load-balancing, concept-drift]
sources: [https://sre.google/sre-book/reliable-product-launches/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Progressive Model Rollout

## Summary

A **progressive model rollout** sends a controlled portion of production workload to a candidate model, observes predefined metrics, and increases exposure only when gates pass. It limits blast radius; it does not make production experimentation risk-free.

## Grounded explanation

Several patterns answer different questions:

- **Shadow evaluation** duplicates requests to the candidate but suppresses candidate responses. It reveals compatibility, latency, and candidate outputs without changing user-visible predictions. It can still consume resources, expose data to another path, and trigger side effects unless tools and writes are disabled.
- **Canary rollout** exposes a small, stable cohort to the candidate and expands gradually. Automated rollback should use reliability and safety guardrails, not only an average model score.
- **Randomized A/B test** assigns comparable experimental units to legacy and candidate behavior to estimate a causal product effect. Assignment, sample size, interference, and multiple testing matter.
- **Interleaving** mixes ranked outputs from alternatives in one experience to obtain sensitive preference evidence, but attribution requires an interleaving method designed for ranking.
- A [[multi-armed-bandit]] adapts allocation toward better observed rewards, trading clean fixed-allocation inference for lower regret.

Route by user or another persistent unit when repeated interactions could cross-contaminate behavior. [[load-balancing]] alone is not experimental randomization. Define primary outcomes, guardrails, minimum duration, ramp stages, stop conditions, and rollback before exposure. Monitor delayed labels and slices because [[concept-drift]] or selection can invalidate an early aggregate win.

Google SRE describes canaries as early rollout stages observed under real traffic, followed by broader stages only after validation, with automatic rollback when validation fails. For models, pair service health with prediction quality, fairness, safety, and business outcomes. A shadow result cannot establish user impact, while a canary without a valid comparator cannot by itself estimate causal lift.

## Prerequisites

- [[multi-armed-bandit]]
- [[load-balancing]]
- [[concept-drift]]

## Sources

- [Google SRE, “Reliable Product Launches at Scale”](https://sre.google/sre-book/reliable-product-launches/): documents staged canaries, observation periods, gradual expansion, feature-flag routing, and rollback requirements.
