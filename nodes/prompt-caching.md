---
id: prompt-caching
title: Prompt Caching
summary: Prompt caching reuses the previously computed key–value state of an identical prompt prefix, reducing repeated prefill work while making prefix stability and cache-lifetime policy part of the request contract.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache]
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Prompt Caching

## Summary

**Prompt caching** lets a model provider retain the [[kv-cache]] computed for a
request's reusable beginning. A later request that presents the same cacheable
prefix can start after that prefix rather than recomputing its prefill, so the
caller pays less latency and input-processing work for context that genuinely
repeats.

## Grounded explanation

During prefill, a transformer turns each token in a prompt into keys and values
that later attention steps reuse. Those entries are the [[kv-cache]]. If two
requests begin with the same token sequence and use compatible model settings,
the entries for that shared prefix are the same computation. Prompt caching
keeps those already-computed entries temporarily, allowing a later request to
reuse them and process only the new suffix.

The cache is a **prefix** optimization, not a semantic search. It does not find
similar documents, repair a reordered prompt, or decide whether two instructions
mean the same thing. A caller must deliberately place stable material first—for
example, fixed instructions, tool definitions, or a versioned reference
document—and append per-request messages afterward. Changing a token before the
cache boundary can prevent reuse because the later attention state depends on
that earlier sequence.

A cache hit changes the cost of preparing a request; it does not change the
model's weights or guarantee an identical generated answer. The new suffix is
still prefixed by the cached state and decoding remains an autoregressive
process. Providers also define retention and invalidation policies, so an
application must treat a cache as an optional performance benefit rather than
its only copy of context.

### Worked instance

Suppose an assistant sends a 12,000-token stable policy-and-tools prefix followed
by a user-specific 300-token suffix. The first request prefills the entire
12,300-token prompt and may create a cache entry for the stable prefix. On a
later request with that exact prefix and a different 300-token suffix, a cache
hit can reuse the prefix's [[kv-cache]] and prefill only the new portion. If the
application inserts a timestamp near the beginning of the policy, the prefix is
no longer identical and it should expect a miss. Keeping volatile material at
the end preserves the reusable boundary.

## Prerequisites

- [[kv-cache]]

## Sources

- [Anthropic, “Prompt caching”](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): official API documentation on cacheable prompt prefixes, cache lifetime, and cache reads and writes.
