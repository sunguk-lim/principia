---
id: decision-model-hierarchical-retrieval
title: Decision-Model Hierarchical Retrieval
summary: Decision-model hierarchical retrieval uses shared-context bounded judgments to select branches and passages without generating navigation text at every level.
type: concept
tags: [ml/information-retrieval]
prereqs: [hierarchical-document-retrieval, decision-score-action-gate]
sources: [https://arxiv.org/html/2610.35868v1]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Decision-Model Hierarchical Retrieval

## Meaning

A decision model can navigate a corpus hierarchy by returning scores over declared answers instead of generating a chain of navigation text. The contribution is a scoring-and-expansion procedure, not simply another name for flat reranking or for every hierarchical retriever.

## Mechanism

[[hierarchical-document-retrieval]] defines the branches and evidence expansion. At one level, present the query and candidate descriptions in a shared context. Ask a binary relevance question for each candidate and retain the highest-ranked branches. Expand their children and repeat toward passages. The [[decision-score-action-gate]] separates the learned judgment from application rules, including budget, authorization and abstention.

Parallel binary scores are each normalized over yes/no for that question; they need not sum to one across candidates. An optional multiple-choice judgment on a bounded shortlist is different: its options compete within one normalized distribution. Shared context allows each score to depend on alternatives, but does not prove probability calibration or comparability across different requests and pools.

## Worked example

Three document branches receive binary relevance scores 0.8, 0.7 and 0.2. Their sum is 1.7, which is valid because they answer different binary questions. With a branch budget of two, expand the first two. Suppose their passages score 0.6, 0.9 and 0.4; retain the highest two and optionally judge them as alternatives. A multiple-choice response of 0.65 and 0.35 then sums to one. The excluded third document remains unexamined: a later excellent passage score cannot rescue evidence there without a new expansion.

## Boundaries and validation

DecisionRAG is a primary example using joint candidate judgments and top-budget expansion. It avoids a separate first-stage retriever at query time; its hierarchy can still require offline grouping. Do not infer that it eliminates indexing work or that reported speed/quality comparisons transfer to another corpus.

Test shared versus independent scoring, batch/pool partitioning, hierarchy construction, branch budgets and fallback. Measure evidence containment before ranking conditional on containment, then final answer grounding and end-to-end cost. A fast scoring pass can still be expensive with a large context. Metadata, saved text and candidate instructions remain untrusted data, not authority to alter the search policy.

## Prerequisites

- [[hierarchical-document-retrieval]]
- [[decision-score-action-gate]]

## Sources

- <https://arxiv.org/html/2610.35868v1>
