---
id: agent-workflow-graph
title: Agent Workflow Graph
summary: An agent workflow graph makes task state, permitted transitions, loops, checkpoints, and termination explicit while individual steps may be deterministic or model-driven.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-session-state, tool-call-execution-contract]
sources: [https://docs.langchain.com/oss/python/langgraph/overview, https://docs.langchain.com/oss/python/langgraph/persistence]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Agent Workflow Graph

## Summary

An **agent workflow graph** represents a task as state plus nodes that transform it and edges that choose what may run next. A node may call a model, run a deterministic check, invoke a tool, or wait for human input. The graph makes loops, termination, and checkpoint boundaries reviewable; it does not by itself prove task success.

## Grounded explanation

The [[agent-execution-harness]] owns permissions and effects around model calls. A workflow graph specifies how that harness advances: what state each step reads and writes, what conditions select an edge, and which paths terminate. LangGraph's official documentation describes mixing deterministic and LLM-driven steps, durable execution, and human-in-the-loop transitions. The same pattern can be implemented with plain code; a graph runtime is justified when explicit state and resumability outweigh its complexity.

For a research agent, a graph could route `draft query → retrieve → assess evidence → either retrieve again or synthesize`. The state should record query history, source IDs, remaining budget, and why a branch was selected. A retry edge must have a bound; a checkpoint must separate an attempted tool call from an observed effect. [[agent-session-state]] governs conversation continuity, while task-local graph state governs this run's progress. Collapsing the two can replay completed work on a later turn.

Visual composition tools can sketch the flow, libraries can connect model and tools, and tracing services can record what happened. These are roles, not mandatory product dependencies. A trace of a completed node shows execution, not that the external task succeeded. Compare a graph with a linear or plain-code baseline on task success, recovery after interruption, invalid transitions, state corruption, latency, and maintenance. Test cycles, partial failures, concurrent updates, and permission boundaries explicitly.

## Sources

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): stateful graph orchestration and deterministic/model-driven steps.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpoint and resume semantics.
