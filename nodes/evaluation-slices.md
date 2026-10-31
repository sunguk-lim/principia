---
id: evaluation-slices
title: Evaluation Slices
summary: Evaluation slices measure the same prediction task on explicitly defined input subpopulations so aggregate quality cannot hide localized failures.
type: concept
tags: [ml/evaluation]
prereqs: [confusion-matrix, conditional-probability, loss-function]
sources: [https://scikit-learn.org/stable/modules/model_evaluation.html, https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html, https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html]
status: explained
created: 2026-10-20
updated: 2026-11-01
---

# Evaluation Slices

## Meaning

An evaluation slice is a documented subset of examples selected by a property relevant to service behavior. Slices can expose an important weakness even when the overall score improves. They do not create new ground truth, and their membership rule must not change between compared systems.

## Mechanism

Define a membership rule before comparing predictions: for instance human-annotated negation scope, language, input length or customer environment. Use the same labeled examples and metric within each slice. A [[confusion-matrix]] separates false alarms from missed cases; [[conditional-probability]] expresses error given membership. Slices may overlap and need not partition the dataset, so their counts cannot always be summed. Report denominator and label mix beside each score. Choosing slices after looking at failures is useful discovery, but requires confirmation on fresh held-out examples rather than treating a selected surprise as an unbiased test.

## Worked example

Suppose 100 of 1,000 labeled cases contain negation. A baseline makes 30 errors on those 100 and 45 on the other 900: total error is 75/1,000=7.5%. A replacement makes 40 and 20 respectively: total error improves to 6%, while negation error worsens from 30% to 40%. The aggregate is not wrong; it answers a different population question. If negation examples were artificially oversampled in a test suite, use the real traffic proportions for a deployment aggregate and still show slice results. Include uncertainty, paired per-example changes and important intersections. A broad slice can hide a rarer subgroup; tiny slices cannot support precise conclusions. Decide fixes by error cost and prevalence, not merely the largest percentage.

## Check your understanding

Can improving aggregate accuracy certify improvement on every slice? No. A weighted aggregate can improve while an operationally important subset deteriorates.

## Domain-sliced validation likelihood

The same slicing principle applies to a probabilistic [[loss-function]], not only hard-label errors. State the valid-token denominator, weighting and scoring units. Let a fixed validation mix contain 80% code tokens and 20% reasoning tokens. A model with losses 1.0 and 2.0 has aggregate 0.8×1.0+0.2×2.0=1.2. A replacement with 0.8 and 2.4 has aggregate 1.12, even though reasoning loss worsens. The overall improvement does not certify improvement on that domain.

Keep the mix fixed when comparing models, and report slice losses and counts. Distinguish a changed mixture from changed within-slice performance. Per-token losses across incompatible tokenizers do not have matching units; declare a justified common normalization before comparing them. Overlapping slices do not necessarily reconstruct an overall weighted mean. Finally, a lower domain loss is still not proof of better top-choice decisions or task utility; evaluate those outcomes independently.

## Prerequisites

- [[loss-function]]
- [[confusion-matrix]]
- [[conditional-probability]]

## Sources

- <https://scikit-learn.org/stable/modules/model_evaluation.html>
- <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html>

- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html>
