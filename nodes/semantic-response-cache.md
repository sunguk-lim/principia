---
id: semantic-response-cache
title: "Semantic Response Cache"
summary: "A semantic response cache reuses a stored answer for a sufficiently similar request only when authorization, dependency versions and freshness policy also permit reuse."
type: concept
tags: [ml/agents]
prereqs: [embedding, cosine-similarity, ml-system-freshness, retrieval-authorization-boundary]
sources: [https://github.com/redis/redis-vl-python/blob/main/redisvl/extensions/cache/llm/semantic.py]
status: explained
created: 2026-11-20
updated: 2026-11-20
---

# Semantic Response Cache

## Meaning

A semantic response cache stores a request representation and its answer, then retrieves candidate answers for semantically similar requests. Unlike an exact-text cache, it may match paraphrases. [[cosine-similarity]] supplies a similarity score, not proof that the old answer is correct for a new request.

## Mechanism

Use an [[embedding]] for the request and store the answer with permitted identity scope, relevant inputs, model/prompt versions, source dependencies and creation time. Search within eligible records, apply a similarity threshold, then check the answer-reuse policy. RedisVL's primary implementation exposes vector-distance thresholds, filterable fields, per-entry expiry and deletion; the application must supply the meaning of those fields and invalidation rules.

[[ml-system-freshness]] matters when an answer depends on changing data. Expiry limits age but cannot guarantee that the fact stayed unchanged during that interval. Refreshing expiry on a cache hit can extend the lifetime of an obsolete answer unless separate dependency versions or invalidation constrain reuse. [[retrieval-authorization-boundary]] applies to the returned answer as well as the underlying documents: an old permitted answer must not bypass a later revocation or reveal another user's data.

Separate candidate matching from acceptance. Similar wording can refer to different orders, people, dates or required levels of certainty. Conversely, two different phrasings may genuinely share an immutable answer. Tune thresholds against costly false hits and false misses, including negation and changed identifiers. Exact keys or live reads can be simpler for correctness-sensitive cases.

## One example

At 09:00, a status answer says an order is being processed. At 09:10, the status changes. At 09:11, the same user asks a paraphrase. A strong similarity match and a 30-minute expiry do not make the 09:00 answer current. A version check could reject it; an invalidation event could remove it; or the system could retrieve only a response template and perform a fresh authorized read. Reusing the old answer without those conditions is a stale hit, not a successful cache optimization.

## Check your understanding

Does increasing hit rate necessarily improve the application? No. Measure valid-hit rate, wrong-answer reuse, cross-user leakage, revocation/dependency update behavior, latency and total cost on the same workload. Include cache lookup and invalidation overhead. A prefix attention-state cache reuses computation for identical token prefixes; it does not establish that a previously generated answer is still true. Reusing a procedure rather than an answer is another distinct design.

## Prerequisites

- [[embedding]]
- [[cosine-similarity]]
- [[ml-system-freshness]]
- [[retrieval-authorization-boundary]]

## Sources

- <https://github.com/redis/redis-vl-python/blob/main/redisvl/extensions/cache/llm/semantic.py>
