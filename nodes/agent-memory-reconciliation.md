---
id: agent-memory-reconciliation
title: Agent-Memory Reconciliation
summary: Agent-memory reconciliation compares new candidate facts with scoped existing facts and publishes a validated current-state change without confusing temporal change with historical falsity.
type: concept
tags: [ml/agents]
prereqs: [agent-memory, agent-memory-entity-resolution, temporal-knowledge-graph, transaction, optimistic-concurrency-control]
sources: [https://arxiv.org/html/2504.19413v1, https://docs.mem0.ai/core-concepts/memory-operations/add, https://www.postgresql.org/docs/current/transaction-iso.html]
status: explained
created: 2026-11-14
updated: 2026-11-14
---

# Agent-Memory Reconciliation

## Meaning

Reconciliation is the write-path decision that turns new evidence into a coherent current view of [[agent-memory]]. Extraction asks which facts a message supports. Reconciliation asks how those candidate facts relate to facts already stored. Similarity retrieval alone answers neither question.

## Mechanism

First establish scope and identity with [[agent-memory-entity-resolution]]. Retrieve possible conflicts using stable entity and attribute identifiers, supplemented by semantic search. A top-K list can omit the one fact needing correction; a fluent model cannot resolve a conflict it never sees. Compare candidate evidence, applicability time and certainty before proposing an operation.

A useful operation vocabulary is ADD for a distinct fact, UPDATE for a revised representation, DELETE for removal under a defined policy, and NOOP for no change. These names need explicit semantics: supplementing an incomplete fact, correcting a false one and ending a previously true relationship are different transitions. Use [[temporal-knowledge-graph]] validity intervals for historical change rather than assuming every later assertion makes the past false. Ambiguous evidence can remain unresolved instead of forcing a destructive choice.

Treat the proposed operation as data. Validate the target ID, owner, evidence and resulting invariants outside the proposing model. Publish related changes as a [[transaction]] and use [[optimistic-concurrency-control]] when the compared state may have changed. Preserve authorized provenance; history retention is not a substitute for an erasure policy.

## One example

At revision 8, person P has employment at A from January onward. A March message states that P left A in February and also consults for B. Retrieve P's employment relations, close A's applicable interval in February, and add the consulting relation with the dates actually supported. Do not invent that consulting began in February. A repeated paraphrase need not add a second relation. If revision 9 changed the dates while this proposal was being computed, re-read and revalidate instead of overwriting that change.

## Validation and implementation boundary

Evaluate candidate-conflict recall, operation confusion counts, false removals, missed updates and downstream stale answers separately on time-ordered, adjudicated conversations. Include concurrent corrections, namesakes, repeated events, concurrent jobs and uncertain dates. Compare rule-based entity/attribute handling with model-assisted decisions, allowing abstention.

The 2025 Mem0 paper describes a four-operation update architecture. The current official add documentation inspected on this node's update date instead describes additive-only storage; its current repository likewise uses an additive extraction flow. The historical design is evidence for a reconciliation pattern, not proof that today's default add API performs every operation automatically. Pin an implementation version before making product-specific claims.

## Prerequisites

- [[agent-memory]]
- [[agent-memory-entity-resolution]]
- [[temporal-knowledge-graph]]
- [[transaction]]
- [[optimistic-concurrency-control]]

## Sources

- <https://arxiv.org/html/2504.19413v1>
- <https://docs.mem0.ai/core-concepts/memory-operations/add>
- <https://www.postgresql.org/docs/current/transaction-iso.html>
