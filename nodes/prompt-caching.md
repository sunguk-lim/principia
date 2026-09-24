---
id: prompt-caching
title: Prompt Caching
summary: Prompt caching reuses key–value state for an identical eligible request prefix, reducing repeated prefill while making prefix construction, model settings, lifetime, and hit diagnostics part of the request contract.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache]
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
status: explained
created: 2026-09-12
updated: 2026-09-25
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

### Diagnose misses as request-prefix differences

A cache key is determined by more than the visible user text. Provider request construction can place tool definitions before the system prompt and message history, and model or serving settings can select a different cache namespace. A hit comparison must therefore use the **rendered eligible prefix** and the effective model/settings—not only the last user message.

When a hit rate drops, compare two requests from the beginning and find the first meaningful difference. Common causes are reordered or edited tools, a timestamp or request identifier inserted into stable instructions, history compaction that replaces earlier messages, a model change, a different cache breakpoint, or expiration. Put volatile data after the stable prefix; keep intentional semantic changes even when they reduce hits. A lower hit rate can be the correct result when compaction reduces total input work or a safety rule must change.

Record cache-read tokens, cache-write tokens, uncached input tokens, time to first token, total latency, and the effective model and breakpoint. Those fields distinguish a true reuse failure from a cheaper request that intentionally has less reusable input. Cache-hit rate alone is not the optimization objective; total latency, cost, and answer quality are.

### Worked instance

Suppose an assistant sends a 12,000-token stable policy-and-tools prefix followed
by a user-specific 300-token suffix. The first request prefills the entire
12,300-token prompt and may create a cache entry for the stable prefix. On a
later request with that exact prefix and a different 300-token suffix, a cache
hit can reuse the prefix's [[kv-cache]] and prefill only the new portion. If the
application inserts a timestamp near the beginning of the policy, the prefix is
no longer identical and it should expect a miss. Keeping volatile material at
the end preserves the reusable boundary. If a later deployment also reorders the tool list before that policy, the effective prefix changes earlier and the 12,000-token policy cannot be reused even though its text is unchanged. Comparing the fully rendered request exposes that first divergence.

## Prerequisites

- [[kv-cache]]

## Sources

- [Anthropic, “Prompt caching”](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): official API documentation on cacheable prompt prefixes, the `tools` → `system` → `messages` prefix order, cache breakpoints and lifetime, and cache-read/write usage fields.
