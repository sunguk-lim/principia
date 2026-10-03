---
id: heterogeneous-treatment-effects
title: Heterogeneous Treatment Effects
summary: Heterogeneous treatment effects describe how a causal intervention's outcome difference varies across units or covariate-defined subgroups, subject to identification and overlap assumptions.
type: concept
tags: [ml/evaluation]
prereqs: [hypothesis-testing, conditional-probability]
sources: [https://www.pywhy.org/EconML/spec/estimation/dml.html]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# Heterogeneous Treatment Effects

## Summary

An average treatment effect can hide that an intervention helps some users and harms others. **Heterogeneous treatment effects** ask how the causal difference between treatment and control outcomes changes with observed characteristics.

## Grounded explanation

For a recommendation policy, define treatment as an exposure rule and outcome as delayed retention. Randomization identifies subgroup effects when assignment and follow-up are valid; in observational logs, treatment selection may depend on user traits and prior behavior. Estimators such as double machine learning model treatment and outcome nuisance functions, but require observed confounders, overlap, and sufficiently accurate estimation. [[conditional-probability]] and a prediction of retention alone do not identify a treatment effect.

Predefine consequential subgroups where possible, report uncertainty with [[hypothesis-testing]], and examine overlap and attrition. Split data so the same sample does not both discover and validate a subgroup. Compare a heterogeneous policy with the simpler uniform policy in a randomized test before using estimated uplift for targeting. An impressive subgroup plot from passive logs is a hypothesis, not proof of personalized benefit.

## Prerequisites

- [[hypothesis-testing]]
- [[conditional-probability]]

## Sources

- [EconML double machine learning](https://www.pywhy.org/EconML/spec/estimation/dml.html): identification assumptions and heterogeneous-effect estimation.
