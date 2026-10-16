---
id: classifier-serving-contract
title: Classifier Serving Contract
summary: A classifier's deployed behavior depends on feature and label mappings and the score-to-decision rule as well as its parameter checkpoint.
type: concept
tags: [ml/systems]
prereqs: [feature-hashing, model-calibration, concept-drift]
sources: [https://scikit-learn.org/stable/modules/compose.html#pipeline, https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html]
status: explained
created: 2026-10-16
updated: 2026-10-16
---

# Classifier Serving Contract

## Summary

An unchanged weights file does not imply unchanged predictions. The **serving contract** also includes preprocessing, feature order, vocabulary or hash mapping, score interpretation, class order, and the decision rule.

## Grounded explanation

A model receives a numeric representation, not the original request. A changed normalizer, tokenizer, missing-value imputer, or vocabulary index can turn the same input into a different vector before the checkpoint runs. For [[feature-hashing]], even changing the seed or width changes coordinate meanings. A class encoder can then map the same output index to a different label; a threshold or tie-break can change the decision while scores stay identical. scikit-learn's pipeline and label encoder document these separate transformations. Version them with the model, not only with the application release.

For example, a two-class model returns scores `[0.49, 0.51]`. Swapping the class-order mapping reverses the label without modifying either score. If the rule changes from `score > 0.5` to `score >= 0.5`, exactly tied examples change class. In a bag-of-words model, rebuilding the vocabulary in a different order can multiply each count by the wrong weight, even though vector dimensions and checkpoint bytes match.

Diagnose a sudden regression by replaying the same fixed requests through old and new versions. Compare raw input, normalized tokens, feature vector and indices, model scores, decoded labels, and final action in that order. This isolates the first divergence. Check schema defaults, dependency versions, and configuration as part of the contract. Aggregate accuracy alone cannot localize it; use slice-level disagreement and a confusion matrix.

If replay is identical but live outcomes deteriorate, examine input mix and delayed labels. [[concept-drift]] is a change in the target relationship, not a synonym for every traffic change; new categories may instead expose a coverage gap. Recalibration, better unknown handling, new data, or retraining are distinct remedies. Validate the selected remedy on time-held-out traffic and under the real latency budget. [[model-calibration]] helps distinguish stable ranking from a decision threshold that no longer matches error costs.

## Prerequisites

- [[feature-hashing]]
- [[model-calibration]]
- [[concept-drift]]

## Sources

- [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline): preprocessing and estimator as one fitted sequence.
- [scikit-learn LabelEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html): explicit class-to-integer mapping.
