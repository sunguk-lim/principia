---
id: agent-memory-read-projections
title: Agent-Memory Read Projections
summary: Agent-memory read projections derive different bounded views—facts, entities, episodes, outcomes, observations, or user context—from one provenance-preserving history according to the question being answered.
type: concept
tags: [ml/agents]
prereqs: [agent-memory, temporal-knowledge-graph, agent-session-state, measurement]
sources: [https://github.com/getzep/graphiti, https://arxiv.org/abs/2501.13956, https://docs.langchain.com/oss/python/langgraph/persistence]
status: explained
created: 2026-10-10
updated: 2026-10-10
---

# Agent-Memory Read Projections

## Summary

One stored history can support several read views without creating six unrelated memory stores. The requested answer determines which representation and evidence granularity fit the context budget.

## Grounded explanation

[[agent-memory]] persists selected information across runs. A [[temporal-knowledge-graph]] can keep fact validity and provenance, while [[agent-session-state]] preserves ordered exchanges. A read projection reshapes these records for a task. “What is true now?” needs dated facts; “tell me about this entity” needs an assembled view of related facts; “what exactly was said?” needs the original episode; “how did that session end?” needs an outcome summary. A cross-session observation is a tentative pattern backed by multiple episodes, not a causal conclusion. A pre-query user summary is a bounded prior context view used before a precise retrieval query exists.

Each projection has different failure modes. A fact view may return stale validity; an entity summary may merge namesakes; an episode view may quote private detail unnecessarily; a thread outcome may omit an unresolved root cause; an observation may promote correlation to fact; a pre-query summary may over-personalize a trivial greeting. Retain source IDs, timestamps, access controls, and explicit uncertainty. Generated summaries should be invalidated or recomputed when underlying facts change; the original episode is not replaced by its summary.

For example, a service incident can be marked “restored” in a thread outcome while the root cause remains “unknown.” A later “why does this recur?” query should retrieve corroborated episodes, not silently elevate one thread summary into a diagnosis. Evaluate projection selection and answer quality on queries spanning each view at a fixed token budget. Measure freshness, exact-quote fidelity, provenance, privacy leakage, and unsupported inferences against a simple text-retrieval baseline. Graphiti provides a primary temporal-memory implementation; the six-view taxonomy here is an analytic design, not a measured product claim.

## Sources

- [Graphiti repository](https://github.com/getzep/graphiti): temporal fact and episode storage mechanisms.
- [Zep temporal memory paper](https://arxiv.org/abs/2501.13956): temporal graph retrieval design.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointed state and history as a distinct lifecycle.
