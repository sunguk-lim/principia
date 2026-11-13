---
id: label-noise
title: Label Noise
summary: Label noise is disagreement between recorded training targets and the intended labeling rule, with error structure that can depend on class, input, annotator or policy version.
type: concept
tags: [ml/evaluation]
prereqs: [conditional-probability, loss-function, dataset-lineage]
sources: [https://arxiv.org/abs/1911.00068]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Label Noise

## Meaning

Label noise concerns the target, not merely the input format. A row can have the right columns and an admissible label while encoding a judgment inconsistent with the intended task. Genuine ambiguity, a changed task definition and an accidentally wrong label require different remedies.

## Mechanism

Let x be an input, y its intended class under a declared policy, and y_tilde its recorded class. A corruption rate is the [[conditional-probability]] P(y_tilde=j | y=i). A class-conditional model assumes this probability depends on the intended class, not further on x. Real errors can instead concentrate on a particular wording, source, annotator or difficult input; that assumption must be tested, not silently imposed.

The [[loss-function]] rewards agreement with recorded targets. When an annotation policy systematically reverses one subset, minimizing that objective can move predictions away from the intended rule on that subset. This does not imply every noisy dataset prevents useful training, or that a regression identifies label noise uniquely. Changed class proportions, input difficulty, leakage and optimization remain competing explanations.

## One example

An adjudicated audit contains 100 examples intended positive and 100 intended negative. The stored labels flip 20 positives to negative and five negatives to positive. Estimated directional flip rates are 20/100=.20 and 5/100=.05; collapsing them into 25/200=.125 hides asymmetry. If the twenty positive errors all come from one guideline version, treating .20 as a uniform corruption rate within positives also hides input/source structure. These are illustrative counts, not estimates about any real dataset.

## Validation and alternatives

Use [[dataset-lineage]] to stratify an independent audit by annotation source and policy version. Adjudicate disagreements under the target policy, preserving ambiguity rather than calling every disagreement an error. Out-of-sample model disagreement can prioritize inspection, but a confident model is not ground truth: rare valid examples can be exactly those it rejects. Compare original, corrected and selectively filtered data on the same independent target evaluation, reporting lost coverage as well as aggregate quality.

Confident Learning provides a primary method for estimating and ranking potential errors under stated noise assumptions. Its consistency conditions are not permission to delete all examples a classifier dislikes. Relabeling, additional adjudication, revised instructions or retaining uncertain labels can be safer than automatic pruning.

## Prerequisites

- [[conditional-probability]]
- [[loss-function]]
- [[dataset-lineage]]

## Sources

- <https://arxiv.org/abs/1911.00068>
