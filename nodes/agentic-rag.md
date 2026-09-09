---
id: agentic-rag
title: Agentic Retrieval-Augmented Generation
summary: Agentic RAG lets a controller decide whether, when, and how to retrieve evidence, possibly iterating over retrieval, evaluation, and generation rather than always executing one fixed retrieval pass.
type: concept
tags: [ml/agents]
prereqs: [retrieval-augmented-generation, multi-agent-orchestration, llm-as-a-judge]
sources: [https://arxiv.org/abs/2310.11511]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Agentic Retrieval-Augmented Generation

## Summary

**Agentic retrieval-augmented generation** adds control decisions around [[retrieval-augmented-generation]]: whether retrieval is needed, which source or query to use, whether evidence is sufficient, and whether to retrieve again or answer.

## Grounded explanation

A minimal controller can follow this state machine:

1. inspect the request and choose no retrieval, internal retrieval, or an authorized external source;
2. form a query and retrieve evidence;
3. assess relevance and support;
4. revise the query or choose another source when evidence is insufficient;
5. generate with citations or abstain.

Self-RAG is one researched instance: a language model learns special reflection tokens that control on-demand retrieval and critique retrieved passages and generations. Other systems implement the controller with prompts, code, or [[multi-agent-orchestration]]. Splitting “retriever” and “writer” into named agents does not itself make retrieval more capable; the durable mechanism is conditional, observable control over the retrieval loop.

Each extra decision can improve hard queries but adds latency, cost, nondeterminism, and new failure paths. An external fallback also changes freshness, trust, privacy, and prompt-injection exposure. Evidence assessment by an [[llm-as-a-judge]] can be wrong or biased, so it needs labeled calibration and deterministic checks where possible.

Compare with a retrieve-once baseline. Measure task success, retrieval calls per request, retrieval recall, claim-level citation support, correct abstention, source-policy violations, injected-document resistance, latency, and cost. Include cases where retrieval is unnecessary, the internal corpus suffices, only an external source suffices, sources conflict, and tools fail. Ensure retries are bounded and read-only retrieval cannot silently become action execution.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[multi-agent-orchestration]]
- [[llm-as-a-judge]]

## Sources

- [Asai et al., “Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection”](https://arxiv.org/abs/2310.11511): introduces adaptive on-demand retrieval and reflection over passages and generations.
