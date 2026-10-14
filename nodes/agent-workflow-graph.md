---
id: agent-workflow-graph
title: Agent Workflow Graph
summary: An agent workflow graph makes task state, permitted transitions, loops, checkpoints, and termination explicit while individual steps may be deterministic or model-driven.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-session-state, tool-call-execution-contract]
sources: [https://docs.langchain.com/oss/python/langgraph/overview, https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/human-in-the-loop]
status: explained
created: 2026-10-08
updated: 2026-10-15
---

# Agent Workflow Graph

## Summary

An **agent workflow graph** represents a task as state plus nodes that transform it and edges that choose what may run next. A node may call a model, run a deterministic check, invoke a tool, or wait for human input. The graph makes loops, termination, and checkpoint boundaries reviewable; it does not by itself prove task success.

## Grounded explanation

The [[agent-execution-harness]] owns permissions and effects around model calls. A workflow graph specifies how that harness advances: what state each step reads and writes, what conditions select an edge, and which paths terminate. LangGraph's official documentation describes mixing deterministic and LLM-driven steps, durable execution, and human-in-the-loop transitions. The same pattern can be implemented with plain code; a graph runtime is justified when explicit state and resumability outweigh its complexity.

For a research agent, a graph could route `draft query → retrieve → assess evidence → either retrieve again or synthesize`. The state should record query history, source IDs, remaining budget, and why a branch was selected. A retry edge must have a bound; a checkpoint must separate an attempted tool call from an observed effect. [[agent-session-state]] governs conversation continuity, while task-local graph state governs this run's progress. Collapsing the two can replay completed work on a later turn.

Visual composition tools can sketch the flow, libraries can connect model and tools, and tracing services can record what happened. These are roles, not mandatory product dependencies. A trace of a completed node shows execution, not that the external task succeeded. Compare a graph with a linear or plain-code baseline on task success, recovery after interruption, invalid transitions, state corruption, latency, and maintenance. Test cycles, partial failures, concurrent updates, and permission boundaries explicitly.

## Durable transitions and releases

A pause is a persisted transition, not an in-memory wait. Store the thread identity, checkpoint, exact pending operation, approval scope, and deadline before waiting for human input. On resume, authenticate the actor and atomically choose one outcome—approve, reject, or expire—so competing responses cannot run the same effect twice. Reconcile an ambiguous external effect before retrying. LangGraph documents checkpoint-backed interrupts, but the application still owns expiry, identity, authorization, and idempotency policy.

A checkpoint also has a code-version boundary. If a graph deployment changes node names, state schema, or branch meaning, an old paused thread may not resume safely under new code. Version checkpoint schemas, test old-to-new resume fixtures, and either migrate or pin old runs to compatible code. Behavioral release evaluation should replay representative trajectories, interrupts, partial worker failures, and authorization cases; unit tests alone do not exercise every branch or model decision. Record model, prompt, graph, and tool versions with results so a regression can be attributed. A trace proves that a path ran, not that the resulting action was correct.

## Sources

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): stateful graph orchestration and deterministic/model-driven steps.
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpoint and resume semantics.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop): persisted pause and explicit resume flow.
