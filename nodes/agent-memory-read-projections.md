---
id: agent-memory-read-projections
title: Agent-Memory Read Projections
summary: Agent-memory read projections derive different bounded views—facts, entities, episodes, outcomes, observations, or user context—from one provenance-preserving history according to the question being answered.
type: concept
tags: [ml/agents]
prereqs: [agent-memory, temporal-knowledge-graph, agent-session-state, measurement]
sources: [https://github.com/getzep/graphiti, https://arxiv.org/abs/2501.13956, https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/concepts/memory]
status: explained
created: 2026-10-10
updated: 2026-11-23
---

# Agent-Memory Read Projections

## Summary

One stored history can support several read views without creating six unrelated memory stores. The requested answer determines which representation and evidence granularity fit the context budget.

## Grounded explanation

[[agent-memory]] persists selected information across runs. A [[temporal-knowledge-graph]] can keep fact validity and provenance, while [[agent-session-state]] preserves ordered exchanges. A read projection reshapes these records for a task. “What is true now?” needs dated facts; “tell me about this entity” needs an assembled view of related facts; “what exactly was said?” needs the original episode; “how did that session end?” needs an outcome summary. A cross-session observation is a tentative pattern backed by multiple episodes, not a causal conclusion. A pre-query user summary is a bounded prior context view used before a precise retrieval query exists.

Each projection has different failure modes. A fact view may return stale validity; an entity summary may merge namesakes; an episode view may quote private detail unnecessarily; a thread outcome may omit an unresolved root cause; an observation may promote correlation to fact; a pre-query summary may over-personalize a trivial greeting. Retain source IDs, timestamps, access controls, and explicit uncertainty. Generated summaries should be invalidated or recomputed when underlying facts change; the original episode is not replaced by its summary.

For example, a service incident can be marked “restored” in a thread outcome while the root cause remains “unknown.” A later “why does this recur?” query should retrieve corroborated episodes, not silently elevate one thread summary into a diagnosis. Evaluate projection selection and answer quality on queries spanning each view at a fixed token budget. Measure freshness, exact-quote fidelity, provenance, privacy leakage, and unsupported inferences against a simple text-retrieval baseline. Graphiti provides a primary temporal-memory implementation; the six-view taxonomy here is an analytic design, not a measured product claim.

## Applicability scope before similarity ranking

A read view must be applicable as well as relevant. Derive trusted tenant, domain, environment and procedure-version constraints before semantic ranking, then search within the eligible namespace or filter. LangGraph's memory documentation provides namespaces and content filters as mechanisms; an application must still define their correctness and authorization contracts. A metadata match is not proof that a procedure works in that environment.

Suppose a store contains six similarly worded deployment procedures: three for environment A version 1, two for A version 2, and one for B version 2. A caller working in A version 2 should rank the two applicable procedures, not load all six and hope the model resolves conflicting commands. If a valid procedure has an incorrect version label, prefiltering can exclude the needed evidence; measure false exclusions as well as incorrect inclusions. A missing scope should trigger an explicit clarification or safe fallback, not a silent cross-scope search.

Use [[measurement]] to compare scoped and unscoped candidate recall, wrong-version activation, cross-tenant disclosure, task success and cost at the same final context budget. Include stale metadata and migrations. Authorization is a separate host-enforced boundary: user-supplied metadata cannot grant access, and relevant private text must not enter context just because a namespace query returned it.

## Sources

- [Graphiti repository](https://github.com/getzep/graphiti): temporal fact and episode storage mechanisms.
- [Zep temporal memory paper](https://arxiv.org/abs/2501.13956): temporal graph retrieval design.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointed state and history as a distinct lifecycle.

- <https://docs.langchain.com/oss/python/concepts/memory>
