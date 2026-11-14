---
id: inter-annotator-agreement
title: "Inter-Annotator Agreement"
summary: "Inter-annotator agreement evaluates the reproducibility of a defined labeling task across independent raters while separating agreement, adjudication and correctness."
type: concept
tags: [ml/evaluation]
prereqs: [confusion-matrix, probability, dataset-lineage]
sources: [https://www.nltk.org/api/nltk.metrics.agreement.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Inter-Annotator Agreement

## Meaning

Agreement asks whether annotators applying a defined policy give compatible labels to the same items. It is evidence about reproducibility, not automatic evidence that their labels are correct. An agreement study is broader than selecting a single coefficient: task scope, independent rating, sampling and the handling of ambiguity determine what its result means.

## Mechanism

Use [[dataset-lineage]] to retain stable item identity, each annotator's original label and the instruction version. Have raters label shared items independently before discussing disagreements. Otherwise consensus can reflect influence rather than reproducibility. Specify whether labels are categorical, ordered or sets, which comparisons are eligible and how missing ratings affect the denominator.

For two categorical raters on the same items, a [[confusion-matrix]] records both agreement and its direction. Raw agreement is the diagonal count divided by eligible paired items, a [[probability]] estimated from the sample. A chance-adjusted coefficient specifies an additional baseline; its value is not interchangeable with the raw proportion. More raters, incomplete assignments and weighted disagreements require an estimator whose assumptions match that design rather than blindly reusing a two-rater formula.

Adjudication is a later decision under a stated target policy, ideally supported by independent evidence or a qualified resolver. Preserve the pre-adjudication labels: replacing them all with consensus and then measuring agreement would hide the uncertainty that motivated review. Report difficult slices, counts and label prevalence rather than an isolated percentage.

## One example

Two raters label 20 items accept or reject. They both accept eight, both reject seven, and disagree on five. Raw agreement is (8+7)/20=.75. If all five disagreements concern a new instruction's borderline cases, a single aggregate hides a policy-version problem. Rewriting the instructions and independently labeling fresh borderline examples tests the remedy; merely deciding the original five by discussion does not estimate improved reproducibility.

Both raters could also agree on the same wrong rule. An independent policy audit could find mistakes among the fifteen agreements, so .75 agreement neither equals accuracy nor establishes that the majority label is truth.

## Validation

Check duplicate items, mismatched label codes, rater leakage, missingness and sampling bias. Stratify by source or task difficulty when relevant, and quantify uncertainty with an appropriate sampling design. NLTK documents coder-item-label representations and several agreement estimators; scikit-learn documents two-rater kappa and its baseline. Choose the design first, then the statistic.

## Prerequisites

- [[confusion-matrix]]
- [[probability]]
- [[dataset-lineage]]

## Sources

- <https://www.nltk.org/api/nltk.metrics.agreement.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html>
