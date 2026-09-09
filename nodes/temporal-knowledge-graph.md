---
id: temporal-knowledge-graph
title: Temporal Knowledge Graph
summary: A temporal knowledge graph attaches validity or observation times to facts so queries can distinguish current relationships from historical states and later corrections.
type: concept
tags: [ml/agents]
prereqs: [graph, knowledge-graph, event, agent-memory]
sources: [https://arxiv.org/abs/2501.13956]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Temporal Knowledge Graph

## Summary

A **temporal knowledge graph** extends a [[knowledge-graph]]—and its underlying [[graph]] structure—with time-qualified facts. Instead of overwriting “Alice works at A” when a later assertion names B, it can preserve both claims with their applicable intervals and provenance.

## Grounded explanation

A temporal edge can be represented as $(s,p,o,[t_{from},t_{to}),t_{recorded})$: subject, predicate, object, valid-time interval, and the time the system recorded it. Valid time answers when the relationship held in the modeled world; recording or observation time answers when the system knew it.

Suppose one [[event]] records “Alice joined A in 2020,” and a later event says “Alice moved to B in 2023.” The graph can close the first edge at 2023 and open the second, while retaining both. A current-state query selects edges valid now; an as-of query reconstructs the state at a past valid or recorded time.

Temporal storage does not resolve truth automatically. Statements can conflict, extraction can be wrong, and later text can correct an earlier claim retroactively. Store source identity, confidence, extraction version, and supersession links; define whether queries return one selected belief or all competing evidence.

For [[agent-memory]], separate raw episodes from extracted entities and relations so answers can cite their evidence. Community summaries may speed broad retrieval, but they are derived artifacts that require timestamps and invalidation when underlying edges change.

Evaluate temporal retrieval with questions whose answers change over time. Measure fact extraction, interval accuracy, contradiction handling, as-of correctness, provenance coverage, update latency, and end-to-end answer faithfulness. Product-specific benchmark gains do not establish universal superiority over static retrieval.

## Prerequisites

- [[graph]]
- [[knowledge-graph]]
- [[event]]
- [[agent-memory]]

## Sources

- [Rasmussen et al., “A Temporal Knowledge Graph Architecture for Agent Memory”](https://arxiv.org/abs/2501.13956): describes Graphiti as a temporally aware graph that integrates ongoing conversational and structured data while maintaining historical relationships.
