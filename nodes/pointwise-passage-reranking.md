---
id: pointwise-passage-reranking
title: Pointwise Passage Reranking
summary: Pointwise passage reranking scores each query-passage pair independently and sorts those scores within an already retrieved candidate set.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-evidence-gate, transformer-attention]
sources: [https://sbert.net/examples/cross_encoder/applications/README.html, https://arxiv.org/abs/2306.17563]
status: explained
created: 2026-10-31
updated: 2026-10-31
---

# Pointwise Passage Reranking

## Meaning

Pointwise reranking judges one query-passage pair at a time and orders the candidate passages by their scores. The procedure is pointwise even if its model was trained using a different ranking loss. It does not retrieve missing evidence, and relevance does not by itself establish the sufficiency assessed by a [[retrieval-evidence-gate]].

## Mechanism

A cross-encoder is one implementation: it processes query and passage tokens jointly through [[transformer-attention]] and produces a scalar score. Another implementation asks a language model for a specified relevance judgment. The procedure and model architecture are separate choices; not every pointwise scorer is a cross-encoder.

Independent pairs can be batched because scoring passage A does not require the result for B. The scores must nonetheless be comparable within a query. A number called confidence is not automatically a calibrated probability. Ranking needs a useful relative order, while an absolute acceptance threshold additionally needs validation against labeled evidence. Prompt wording, truncation and inconsistent scoring scales can undermine comparisons.

## Worked example

A question asks for a return deadline. Retrieval supplies three passages: A describes company history, B states a 30-day deadline, and C describes return packaging. Suppose one fixed scorer produces A=0.2, B=0.9 and C=0.6. Sorting gives B, C, A; a context budget of two passages retains B and C. These illustrative scores are not measured probabilities. If retrieval never supplied B, sorting A and C would not recover the deadline.

If a fourth passage says a policy changed to 14 days, its date and source version matter. A generic relevance score may rate both policy passages highly while leaving their temporal conflict unresolved. Preserve provenance and apply the application's evidence policy rather than assuming the highest score establishes truth.

## Validation

Freeze the candidate set, model revision, input template and truncation policy when comparing rerankers. Assess whether decisive evidence survives the context cutoff, using judged questions and held-out evaluation. Measure ranking quality, final answer support, latency and total scoring cost; include missing-evidence and long-passage cases. Compare the initial ordering and alternative procedures under equal budgets. Parallelizable scoring does not imply constant latency at arbitrary candidate depth, and a documented model example is not evidence that all cross-encoders outperform every retriever.

## Sources

- <https://sbert.net/examples/cross_encoder/applications/README.html>
- <https://arxiv.org/abs/2306.17563>
