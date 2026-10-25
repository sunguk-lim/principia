---
id: cache-augmented-generation
title: Cache-Augmented Generation
summary: Cache-augmented generation preloads a bounded authorized corpus into a reusable model-context prefix, replacing per-query document selection with cache validity and long-context usage obligations.
type: concept
tags: [ml/information-retrieval]
prereqs: [prefix-caching, effective-context-utilization, retrieval-authorization-boundary]
sources: [https://arxiv.org/html/2412.15605v2]
status: explained
created: 2026-10-26
updated: 2026-10-26
---

# Cache-Augmented Generation

## Meaning

Cache-augmented generation (CAG) preloads a bounded collection of relevant documents into a reusable context prefix, then appends questions without selecting a new document subset for each question. The learned model weights need not change: the reused object is inference context state. It is a knowledge-provisioning architecture, broader than the caching mechanism that makes it economical.

## Mechanism

Choose a corpus snapshot, preserve document boundaries and citation identifiers, render it under a stable prompt, and compute the reusable prefix state. For each authorized question, adopt a compatible prefix, append the request and generate. Keep the shared prefix immutable and remove or isolate the question-and-answer suffix before the next independent request. Otherwise one caller's conversation can silently become another caller's evidence.

[[prefix-caching]] explains why compatible identical leading tokens can reuse attention state. A cache key must include the relevant model, rendering, position, mask and execution configuration, not just the visible document text. An update or deletion can invalidate the cached snapshot; a saved prefix cannot simply be assumed to reflect new facts. Loading a disk snapshot also has cost and requires a compatible runtime representation.

A capacity limit is not a usefulness guarantee. [[effective-context-utilization]] tests whether the model actually uses evidence across length, position and distractors. Reusing a prefix avoids redundant prefix prefill, but new suffix tokens and decoding still interact with the retained context. CAG removes a retrieval-selection step, not every source of latency, unsupported answers or memory cost.

The [[retrieval-authorization-boundary]] still applies to evidence even without a retriever. Scope preloaded corpora and cached state to callers permitted to see every included source, or build a separately authorized snapshot. Filtering only the final answer is too late to establish that the context boundary was respected. Revoking access may require invalidating shared state as well as preventing fresh reads.

## Worked example

Use a hypothetical endpoint with a 16,000-token combined context allowance. A stable instruction-and-document prefix occupies 10,000 tokens. Reserve 1,000 for a question/history suffix and 2,000 for output: the total is 13,000, leaving 3,000 tokens of headroom under this particular endpoint contract. This does not establish any real model's output limit or effective accuracy.

For 40 independent questions with that identical 10,000-token prefix, recomputing it each time processes 400,000 prefix token positions. Reusing it after the first processes 10,000, avoiding 390,000 repeated prefix positions. Those counts are not a 40-fold total-runtime claim: suffix work, cache loading, generation and attention to the long prefix remain. If a document changes before question 21, publish a new authorized snapshot and rebuild the affected reusable prefix rather than citing old state as current.

## Validation and alternatives

Chan and colleagues study CAG on bounded SQuAD and HotPotQA configurations. Their results motivate testing this design, not a universal instruction to replace retrieval. Compare a full-preload baseline, retrieve-once RAG and a hybrid on the same answerable corpus and quality target. Measure cold/warm first-output and completion times, total state bytes, update/revocation lag, citation support, missing-answer abstention and evidence-position slices. Count preparation and cache misses over the actual reuse lifetime. Query-time retrieval remains useful when the corpus is too large, changes frequently, needs narrow per-user access, or distracts the model; preloading can be simpler when a small stable corpus is genuinely reusable.

## Check your understanding

**Question:** Does a cache hit mean the model no longer reads the preloaded knowledge during generation? **Answer:** No. It skips redundant prefix computation; the retained state still participates in later attention and must remain current, compatible and authorized.

## Prerequisites

- [[prefix-caching]]
- [[effective-context-utilization]]
- [[retrieval-authorization-boundary]]

## Sources

- <https://arxiv.org/html/2412.15605v2> — Chan et al., cache-augmented generation with preloaded documents, reusable KV state and reset suffixes; results remain study-specific.
