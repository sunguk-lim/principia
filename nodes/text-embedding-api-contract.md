---
id: text-embedding-api-contract
title: Text-Embedding API Contract
summary: A text-embedding API contract binds each returned vector to its source input, encoder configuration and scoring geometry so batching and model changes cannot silently corrupt an index.
type: concept
tags: [ml/model-portability]
prereqs: [embedding, cosine-similarity, nearest-neighbor-search]
sources: [https://developers.openai.com/api/docs/guides/embeddings, https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html]
status: explained
created: 2026-10-26
updated: 2026-10-26
---

# Text-Embedding API Contract

## Meaning

A text-embedding API returns vectors, not generated answers. Its contract must preserve which input produced each vector, which encoder/configuration produced it, and how vectors may be compared. A successful JSON response or equal vector length is weaker than a compatible, useful search index.

## Mechanism

An [[embedding]] represents an input in learned coordinates. At the boundary, specify text normalization, token-length policy, empty-input handling, batch limits, requested dimensions if supported, numeric encoding and the returned input index. OpenAI's embedding response includes per-vector index and model/usage metadata; other endpoints have their own contracts. Preserve a stable document ID through batching and retries, and reconcile returned indices/counts before writing results. Do not silently assign the first vector to whichever document finished first.

Record the encoder revision, dimension, text processing, query/document task mode where required, normalization and scoring rule with the index. [[cosine-similarity]] compares directions; dot product agrees with it for unit-normalized vectors, not arbitrary vectors. The Sentence Transformers implementation supports multiple scoring metrics and documents normalized-vector equivalence. The score is not automatically a probability of relevance or a guarantee of factual agreement.

Changing the encoder can change the coordinate system even if the dimension remains identical. Do not mix new query vectors with an old corpus merely because the API request shape still works. Re-embed or use an explicitly documented compatible encoder pair, then compare [[nearest-neighbor-search]] results on judged queries before switching. A larger dimension can increase storage and search work without guaranteeing a better task result.

## Worked example

A batch sends document IDs D1 and D2. Its two returned records have indices 1 and 0. Store each by that index-to-ID mapping, not response arrival order. Suppose D1's illustrative unit vector is (0.8,0.6), D2's is (-0.8,0.6), and a compatible query is (0.6,0.8). The coordinate products sum to 0.48+0.48=0.96 for D1 and -0.48+0.48=0 for D2, so D1 ranks first. These are toy coordinates, not a claim about real text semantics.

If only the query encoder rotates its axes to produce (-0.8,0.6), the vectors still have dimension two and length one, but the old D1 score becomes -0.64+0.36=-0.28 and D2's becomes 0.64+0.36=1. The ranking reverses. Type/shape checks pass while geometry compatibility fails.

## Validation

Check vector count, input identities, dimensions and finite values; reject or quarantine incomplete batches. Test long and empty inputs, duplicate retries, model revision changes and encoded-versus-float responses. On held-out queries, compare ranking recall, hard negatives, language/domain slices, latency, bytes and cost. Verify privacy/retention before submitting text. A general model benchmark does not certify a particular retrieval task, and a same-size embedding does not certify a safe index migration.

## Check your understanding

**Question:** Is an old index safe when a replacement endpoint returns the same number of floats? **Answer:** No. Coordinate semantics, input processing and scoring must be compatible and task-tested.

## Prerequisites

- [[embedding]]
- [[cosine-similarity]]
- [[nearest-neighbor-search]]

## Sources

- <https://developers.openai.com/api/docs/guides/embeddings>
- <https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html>
