---
id: durable-agent-execution
title: Durable Agent Execution
summary: Durable agent execution reconstructs a task from committed checkpoints and reconciles uncertain external effects after worker or context loss.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-session-state, transaction]
sources: [https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Durable Agent Execution

## Summary

A **durable agent** can continue the same task after a worker, model context, or execution environment ends. It does not achieve that by retaining a long transcript alone: its runtime must commit task progress, workspace references, approvals, and tool outcomes so the next worker can determine the next valid step.

## Grounded explanation

The [[agent-execution-harness]] owns control flow around the model. A checkpoint records a task identifier, accepted input, completed steps, current step, artifact versions, and pending external operations. A fresh worker reconstructs a bounded prompt from this durable evidence rather than asking the model to infer progress from a partial narrative. [[agent-session-state]] may preserve conversation context, but it is not the same as the interrupted run's execution position. A checkpoint must name which run is being resumed and which state version it observed.

The hardest boundary is an external side effect. The local checkpoint and a remote action normally cannot be one [[transaction]]. If an API call succeeds and the worker dies before recording its result, absence of a receipt means **unknown**, not failed. Persist an operation ID before dispatch; after restart, query the external system or use its idempotency semantics before retrying. An approval must bind the exact operation and arguments that were approved, and the resumed worker must not silently replace them. A workspace path alone is not enough if files changed; persist a commit or content hash when correctness depends on those bytes.

Crash-test the boundaries: before action dispatch, after dispatch before acknowledgement, after checkpoint commit, during an approval pause, and after model-context compaction. Require one coherent outcome and no duplicate consequential effect. Compare this machinery with a simpler queue and idempotent worker; a general agent runtime is justified when adaptive multi-step work really needs it.

## Prerequisites

- [[agent-execution-harness]]
- [[agent-session-state]]
- [[transaction]]

## Sources

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): documents thread checkpoints, durability, replay, and state recovery.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): documents durable pause/resume points for human input.
