---
id: cascaded-classification
title: Cascaded Classification
summary: Cascaded classification routes only selected examples through later decision stages, reducing expensive processing while making later errors conditional on earlier routing.
type: concept
tags: [ml/evaluation]
prereqs: [conditional-probability, precision-recall]
sources: [https://github.com/opencv/opencv/blob/4.x/doc/tutorials/others/cascade_classifier.markdown]
status: explained
created: 2026-11-23
updated: 2026-11-23
---

# Cascaded Classification

## Meaning

A classification cascade applies a sequence of decision stages, often rejecting easy negatives cheaply and evaluating survivors with a more expensive model or reviewer. It differs from running every model on every input and averaging results: routing changes which inputs later stages see. OpenCV's primary cascade tutorial illustrates early rejection in object detection; the architecture also provides a useful design pattern for other screened decisions.

## Mechanism

Let Y be the true binary label, with Y=1 positive and Y=0 negative. Let A mean that the first stage forwards an example, and B mean that the second stage accepts it as positive. When only forwarded examples can become final positives, final detection requires both A and B. By [[conditional-probability]],

$$P(A \cap B\mid Y=1)=P(A\mid Y=1)P(B\mid A,Y=1).$$

The analogous negative-label expression gives the final false-positive rate. No independence assumption is needed: the second factor is measured on the survivors. Multiplying two standalone full-population recall values would generally be wrong because stage one selects a different population for stage two.

Early negative decisions are irreversible in this topology. A perfect reviewer of forwarded cases cannot recover a positive rejected before review. If each example costs c_1 at stage one and each forwarded example costs c_2 at stage two, expected processing cost is c_1+P(A)c_2, before queueing and fixed overhead. This saving matters only alongside retained recall and [[precision-recall]] at the deployment prevalence.

## One example

Consider an invented batch with 100 positives and 9,900 negatives. Stage one forwards 90 positives and 990 negatives, so 1,080 cases reach review. The reviewer accepts 81 of those positives and 99 of those negatives. Final recall is 81/100=81%; equivalently 90/100 times 81/90. Final false-positive rate is 99/9,900=1%; final precision is 81/(81+99)=45%. A low false-positive rate is therefore not automatically high precision.

If stage-one cost is one unit and review costs ten units, the cascade uses 10,000+1,080×10=20,800 units. Reviewing every example at ten units would use 100,000 units under this simplified accounting. It saves work but misses nineteen positives, ten of them before review. These counts are illustrative, not measured performance.

## Validation and boundaries

Select stages and thresholds on development data, then evaluate the complete route on independent, time- and population-representative cases. Record early false negatives, survivor composition, reviewer errors, final precision and recall, review arrivals, latency and cost. A human queue needs a defined capacity and response policy; adding a reviewer without enough capacity can delay or abandon cases rather than improve outcomes.

Audit some early rejections to detect invisible misses and label-selection bias. Retraining the first stage changes the review population, so retest the second stage conditionally. Compare one-stage thresholding, full review and the cascade at matched error and resource constraints. A cascade does not enforce an immutable precision floor under distribution change.

**Check:** Why is 90% first-stage recall followed by a reviewer with 90% recall on survivors only 81% final recall? The reviewer sees only the 90% already forwarded, so the retained fractions multiply.

## Prerequisites

- [[conditional-probability]]
- [[precision-recall]]

## Sources

- <https://github.com/opencv/opencv/blob/4.x/doc/tutorials/others/cascade_classifier.markdown>
