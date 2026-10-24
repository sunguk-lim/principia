---
id: retrieval-query-expansion
title: Retrieval Query Expansion
summary: Retrieval query expansion searches bounded variants of an original information need while preserving exact constraints and evaluating whether added recall outweighs drift and cost.
type: concept
tags: [ml/information-retrieval]
prereqs: [lexical-retrieval, reciprocal-rank-fusion, measurement]
sources: [https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-rewrite]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Retrieval Query Expansion

## Meaning

Query expansion adds or searches alternative expressions of the same information need. It can bridge a vocabulary mismatch between the question and indexed evidence. It is distinct from reranking an already retrieved set and from an agent deciding to search again after observing a failure.

## Mechanism

Keep the original query and its non-negotiable constraints. Produce a bounded set of variants through synonyms, spelling correction or a generative rewrite. Run [[lexical-retrieval]] for the original and selected variants, deduplicate results by stable evidence identity and combine rankings under a stated rule such as [[reciprocal-rank-fusion]]. More queries can find evidence absent from the original list, but they also spend search work and can drift to another meaning.

Do not delegate authoritative filters to a rewrite. Tenant identity, permissions, dates and exact product codes should remain application-enforced constraints. An expanded phrase is a proposal, not proof that it preserves intent. Retain original text for auditing and compare the generated variants against it. Azure's primary documentation describes searching original and rewritten queries and warns that rewrites can omit exact identifiers; its particular preview feature and API limits are implementation details, not the definition of the method.

## Worked example

The user asks for “XJ-42 repair.” A variant uses “XJ-42 servicing,” preserving the model identifier. Suppose the original list is [A] and the variant list is [B,A], where A and B are permitted documents for XJ-42. With fusion constant k=10, A receives 1/11+1/12≈0.1742 and B receives 1/11≈0.0909. The variant exposes B while original evidence remains preferred. A rewrite to “device servicing” could also retrieve XJ-24; a trusted exact-model constraint must not disappear just because that document ranks highly.

Use [[measurement]] to compare original-only and expanded retrieval at matched final context budgets. Report relevant-evidence recall, irrelevant additions, exact-identifier failures, latency and search/model cost on adjudicated queries. Include ambiguous wording, rare codes, negations and already-precise questions. Limit variants, per-query result windows and retries. More retrieved candidates can improve recall while harming the final answer through noise; evaluate both stages rather than calling every expansion useful.

## Check your understanding

Can reranking recover a document excluded by every first-stage query? No. Expansion changes candidate acquisition; reranking only orders acquired candidates.

## Prerequisites

- [[lexical-retrieval]]
- [[reciprocal-rank-fusion]]
- [[measurement]]

## Sources

- <https://learn.microsoft.com/en-us/azure/search/semantic-how-to-query-rewrite>
