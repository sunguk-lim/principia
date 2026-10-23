---
id: retrieval-evidence-gate
title: Retrieval Evidence Gate
summary: A retrieval evidence gate evaluates whether retrieved passages support an answer before generation, while keeping relevance, sufficiency, and authorization as separate checks.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, measurement]
sources: [https://arxiv.org/abs/2005.11401, https://learn.microsoft.com/en-us/azure/search/semantic-search-overview]
status: explained
created: 2026-10-01
updated: 2026-10-24
---

# Retrieval Evidence Gate

## Summary

A retrieval system may find passages about the query without finding evidence for the requested answer. A **retrieval evidence gate** asks two questions between retrieval and generation: which candidates actually support the question, and whether the retained set is sufficient to answer it. It is a quality-control stage, not an authorization or prompt-injection boundary.

## Grounded explanation

In [[retrieval-augmented-generation]], lexical or dense retrieval returns a candidate set. Its first-stage score expresses matching under that retriever; it is not a probability that the passage entails an answer. A reranker can reorder candidates using the query and passage jointly. A separate sufficiency check asks whether the retained passages jointly contain enough evidence; one passage may be relevant but incomplete. If no candidate contains the needed fact, reranking cannot recover it. Diagnose first-stage recall before tuning later gates.

Define a judgment contract such as `supports_query(question, passage)` and `answerable(question, retained_passages)`, with an uncertain option. Calibrate any claimed probabilities on adjudicated examples. Use the application to decide thresholds, context budget, and abstention. For example, a user asks for a product's cancellation deadline. A page mentioning cancellations generally is topically relevant; only the policy page specifying the deadline is evidentially useful. If the policy's effective date is missing, the correct downstream behavior may be to ask for clarification rather than generate a date.

Evaluate with [[measurement]] on a corpus of questions with labeled supporting passages and answerability. Measure candidate recall, reranker precision/recall, false exclusions of decisive evidence, answer faithfulness, abstention, latency, and cost. Compare against no reranking and a conventional cross-encoder under the same context limit. Batch scoring may reduce request overhead, but the latency claim must be measured. A prompt-injection score on a passage is at most one signal: retrieved text still remains untrusted, and resource authorization must be enforced before it reaches this stage.

## Modality-aware decisions

Text passages and rendered pages may have different score distributions and failure modes. Preserve source document, page, modality, and version when merging candidates; merging the same page can avoid duplicated context without discarding complementary text and visual evidence. Fit separate modality thresholds only when held-out labels and workload justify them. The same numeric threshold does not establish equal error rates across modalities.

Evaluate answerable-from-text, answerable-only-from-image, mixed-evidence, and unsupported cases separately, including questions containing screenshots. Inspect both false acceptance of insufficient evidence and false exclusion of a decisive page. A bounded wider-search retry may recover missing recall; repeating a low-quality candidate set cannot manufacture missing facts. If evidence remains insufficient, persist the question, permitted evidence identifiers, and reason for human review rather than generating a confident unsupported answer. Threshold fitting and final evaluation need separate data; a small demonstration table is not a general reliability guarantee.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[measurement]]

## Sources

- [Lewis et al., Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401): retriever-generator architecture.
- [Azure AI Search semantic ranking](https://learn.microsoft.com/en-us/azure/search/semantic-search-overview): documented reranking over an initial result set.
