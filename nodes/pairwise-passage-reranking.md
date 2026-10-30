---
id: pairwise-passage-reranking
title: Pairwise Passage Reranking
summary: Pairwise passage reranking aggregates query-conditioned preferences between candidate pairs while explicitly handling ties, cycles and comparison cost.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-evidence-gate]
sources: [https://arxiv.org/abs/2306.17563]
status: explained
created: 2026-10-31
updated: 2026-10-31
---

# Pairwise Passage Reranking

## Meaning

Pairwise reranking asks which of two passages better serves a query. The comparison is local; turning many local judgments into an ordered list requires an aggregation policy. It remains bounded by the candidate set of the [[retrieval-evidence-gate]], not a substitute for retrieval.

## Mechanism

Compare a query with passages A and B under a fixed instruction and return a preference or tie. Reverse their presentation order to expose position sensitivity. Qin and colleagues' Pairwise Ranking Prompting uses two orders, reconciles inconsistent judgments as ties, and studies all-pair aggregation, comparator-based sorting and bounded sliding passes. Those are different cost/quality choices, not an assertion that every pairwise ranker must use one algorithm.

In an all-pair policy, assign one point for a win and half a point for a tie. Sort total points and use a declared tie-breaker, such as the original retrieval order. For n candidates there are n(n-1)/2 unordered pairs; checking both orders makes n(n-1) model judgments. These are logical comparisons, not necessarily one network request each.

## Worked example

Three candidate passages have preferences A over B, B over C, and C over A. All three receive one win and one loss, so each scores one point. The judgments form a cycle, not a unique consistent order. An initial-order tie-breaker produces a deterministic output but does not prove that its first passage is objectively best.

Now keep A over B and B over C, but treat A versus C as a tie after the two presentation orders disagree. Scores are A=1.5, B=1 and C=0.5, giving A, B, C. There are three unordered pairs and six order-reversed judgments. This small example exercises ties as well as aggregation rather than assuming a perfectly transitive comparator.

## Trade-offs and validation

All-pair judgments can be independently batched but grow quadratically. Sorting-based schemes inspect fewer pairs, yet a noisy non-transitive comparator need not satisfy the assumptions of ordinary sorting. Limited passes can improve the head of a list while leaving unexamined comparisons sensitive to the initial order. Specify the algorithm, comparison budget, tie policy and invalid-output behavior.

Evaluate against the unchanged retrieval order and a pointwise baseline using the same candidates, context budget and query labels. Measure order-reversal consistency, ties, cycles, evidence retention, final answer support, latency and total model work. Retrieved passage text is untrusted reference data; it must not alter the ranking instruction or invoke tools.

## Sources

- <https://arxiv.org/abs/2306.17563>
