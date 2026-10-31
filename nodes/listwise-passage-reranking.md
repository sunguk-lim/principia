---
id: listwise-passage-reranking
title: Listwise Passage Reranking
summary: Listwise passage reranking jointly orders a group of retrieved candidates and validates the resulting permutation under explicit context and window limits.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, structured-output, measurement]
sources: [https://arxiv.org/html/2304.09542]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Listwise Passage Reranking

## Meaning

Listwise passage reranking asks a model to order a group of candidates together. Unlike independently scoring each passage or aggregating pair preferences, the judgment can consider the full displayed group. The ranking procedure is separate from the model architecture and training loss.

## Mechanism

After [[retrieval-augmented-generation|retrieval]] supplies a candidate set, give each passage a stable identifier and ask for the identifiers in desired order. A [[structured-output]] contract checks that every expected identifier appears exactly once and that no unknown one is introduced. A syntactically valid permutation can still be irrelevant, position-biased or insufficient evidence.

Long lists can exceed context or attention-quality limits. A sliding window ranks overlapping groups, often from the tail toward the head so promising candidates can move forward. Window size, stride, initial ordering and number of passes determine which comparisons happen. This is not equivalent to one global omniscient ranking.

## Worked example

Candidates arrive as A,B,C,D,E,F. Rank the tail window C,D,E,F as E,C,F,D, giving A,B,E,C,F,D. Shift two places toward the head and rank A,B,E,C as E,B,A,C. The resulting list is E,B,A,C,F,D. E moved from the tail to the front, but F never shared a window with A or B in this pass. The procedure has not established every pairwise comparison implied by its final order.

## Validation

Use [[measurement]] to compare fixed candidate pools and budgets against the original order and other procedures. Check identifier validity, omissions, duplicates, token truncation and passage instructions treated as untrusted data. Permute input order and identifiers while keeping passage meaning fixed, then measure top-result agreement and evidence quality. Report candidate recall separately: no reordering can recover a missing passage without another retrieval step.

Relevant order can be measured with reciprocal rank or discounted gain under declared labels, but citation support and answer sufficiency are different outcomes. Include latency, token cost, long-list behavior and temporal conflicts. One benchmark improvement does not show general superiority of listwise over pointwise or pairwise methods.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[structured-output]]
- [[measurement]]

## Sources

- <https://arxiv.org/html/2304.09542>
