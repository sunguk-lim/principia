---
id: multi-agent-state-reduction
title: Multi-Agent State Reduction
summary: Multi-agent state reduction combines concurrent worker updates through an explicit merge operation so shared state remains valid and reproducible under parallel execution.
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration, agent-workflow-graph]
sources: [https://docs.langchain.com/oss/python/langgraph/graph-api#reducers]
status: explained
created: 2026-10-15
updated: 2026-10-15
---

# Multi-Agent State Reduction

## Summary

When specialists run concurrently, each may produce an update to the same shared field. A **state reducer** specifies how those updates combine. Without a merge contract, the result can depend on completion order or one worker can overwrite another's evidence.

## Grounded explanation

In [[multi-agent-orchestration]], give each worker private scratch state and a narrow output schema. Shared state should receive validated deltas, not arbitrary replacement snapshots. The [[agent-workflow-graph]] determines which workers run in a parallel step and which downstream node receives the combined state. LangGraph's Graph API documents per-key reducers for applying node updates; it does not make every reducer appropriate for a particular application.

Suppose two workers return findings with stable IDs. A map union that rejects conflicting values for the same ID can merge them regardless of arrival order. List concatenation can preserve all findings but may produce a different order across runs, so sort by a stable key before presenting or hashing the result. A numeric sum is associative for exact integers, but floating-point sums can vary slightly with grouping. A “last writer wins” rule is not a deterministic review decision unless the winner is chosen by an explicit, stable ordering.

Define the reducer's identity value, conflict policy, duplicate policy, and ordering rule. For parallel replay, associative merging permits different grouping; commutative merging permits different completion order; idempotence helps when an update may be delivered twice. Not every field needs all three properties, but exceptions must be deliberate. Preserve each worker's provenance so a final reviewer can attribute evidence and failures. A failed worker should be represented as a partial result with a reason, not silently removed from the denominator.

Test permutations of worker order, duplicate delivery, conflicting IDs, timeouts, and partial failure. Assert both the merged value and the provenance record. Compare parallel execution with a sequential baseline for correctness, latency, and cost; concurrency is useful only when its speed benefit exceeds coordination and verification overhead.

## Prerequisites

- [[multi-agent-orchestration]]
- [[agent-workflow-graph]]

## Sources

- [LangGraph Graph API, reducers](https://docs.langchain.com/oss/python/langgraph/graph-api#reducers): state schema and per-key update reduction semantics.
