---
id: local-feature-attribution
title: Local Feature Attribution
summary: Local feature attribution decomposes one model output into a baseline plus per-feature contributions under a specified masking and background-data convention.
type: concept
tags: [ml/evaluation]
prereqs: [expectation, set, arithmetic]
sources: [https://arxiv.org/abs/1705.07874]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# Local Feature Attribution

## Summary

**Local feature attribution** explains one model output by assigning numerical contributions to that input’s features. An additive explanation has the form

$$f(x)=\phi_0+\sum_{i=1}^{M}\phi_i,$$

where the baseline $\phi_0$ is a reference output and each $\phi_i$ is the contribution assigned to feature $i$ under a stated missing-feature convention.

## Grounded explanation

Global importance averages behavior across many examples; local attribution concerns one $x$. SHAP constructs local additive attributions from Shapley values. For a feature $i$, it averages the change in a value function when $i$ is added to every possible subset of the other features, weighting subset sizes so each ordering contributes fairly. The subsets form a [[set]], and the calculation uses ordinary [[arithmetic]].

Take a two-feature model $f(a,b)=2a+b$, with the zero input as baseline. For input $(a,b)=(3,4)$, the baseline is $0$, feature A contributes $6$, and B contributes $4$; the attributions add to the output $10`. This example is exact because the model is additive. With interactions, the averaging rule distributes shared effects according to the chosen coalition-value definition.

For real models, “feature missing” is not literal. A method may replace absent features using an [[expectation]] over background data. Different background populations or assumptions about dependence can therefore change the attributions. Correlated inputs are especially delicate: independently masking one can create combinations that never occur, and attribution is not a causal effect.

An audit-ready decision record must preserve the model version, exact input snapshot, threshold and policy path in addition to any attribution. Validate local faithfulness by comparing the explanation’s reconstructed output, perturbing features within plausible constraints, and checking stability across equivalent inputs. Evaluate whether reason codes are understandable and whether explanation errors concentrate in important slices.

Local attribution answers “how did this explanation method allocate this model output under these conventions?” It does not prove why the real-world event occurred, guarantee legal sufficiency, or replace reproducible decision logs.

## Prerequisites

- [[expectation]]
- [[set]]
- [[arithmetic]]

## Sources

- [Lundberg and Lee, “A Unified Approach to Interpreting Model Predictions”](https://arxiv.org/abs/1705.07874): additive feature attribution, SHAP, local accuracy, and feature-level values for individual predictions.
