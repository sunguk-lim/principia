---
id: query-by-committee
title: "Query-by-Committee Acquisition"
summary: "Query-by-committee acquisition selects unlabeled examples where a deliberately constructed ensemble disagrees, using the disagreement rule and committee diversity as explicit modeling choices."
type: concept
tags: [ml/training]
prereqs: [active-learning, bagging-variance-reduction, shannon-entropy]
sources: [https://modal-python.readthedocs.io/en/latest/content/query_strategies/Disagreement-sampling.html]
status: explained
created: 2026-11-26
updated: 2026-11-26
---

# Query-by-Committee Acquisition

## Meaning

Query by committee uses disagreement among several predictive hypotheses to decide what to label next. It is not asking one model to state its confidence, nor is it a majority-vote prediction rule. [[active-learning]] supplies the loop: acquire selected labels, update the learner or committee, and measure downstream improvement.

## Mechanism

Build a committee with a declared source of variation, such as resampled training sets or independently initialized models. [[bagging-variance-reduction]] explains why members can still share errors. Obtain each member's prediction for an unlabeled example and compute a disagreement score. One rule counts class votes, divides each count by committee size, and applies [[shannon-entropy]] to that vote distribution. An example with split votes ranks above unanimous votes under this rule.

The modAL documentation distinguishes vote shannon-entropy from shannon-entropy of averaged predicted class probabilities and from a member's divergence from the consensus. Those are different acquisition policies: uniformly uncertain members can produce high consensus shannon-entropy while agreeing with one another. No single disagreement statistic guarantees epistemic uncertainty or a useful annotation.

## One example

Take four hypothetical binary classifiers. On candidate A, votes are three positive and one negative, giving proportions 0.75 and 0.25. Using base-two shannon-entropy, its score is approximately 0.811 bits. On candidate B, votes split two and two, giving shannon-entropy 1 bit. On candidate C, all four vote positive, giving shannon-entropy zero. Vote-shannon-entropy acquisition selects B under equal cost, even if a confident shared error on C remains undiscovered.

If two members are identical copies, four nominal votes do not represent four independent views. Variation must affect plausible hypotheses rather than merely create different object instances.

## Validation and boundaries

Compare committee disagreement, single-model uncertainty and random selection at equal annotation plus model-training/scoring cost. Test correlated errors, rare classes, outliers and changing data. Evaluate on a representative untouched test set, not only the deliberately acquired sample. Retrain or refresh members under a stated policy as labels arrive; an obsolete committee can preserve disagreement unrelated to current learning needs.

## Check your understanding

Does unanimous agreement prove a label is known correctly? No. Every member can share the same misspecification or blind spot.

## Prerequisites

- [[active-learning]]
- [[bagging-variance-reduction]]
- [[shannon-entropy]]

## Sources

- <https://modal-python.readthedocs.io/en/latest/content/query_strategies/Disagreement-sampling.html>
