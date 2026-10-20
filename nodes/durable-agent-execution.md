---
id: durable-agent-execution
title: Durable Agent Execution
summary: Durable agent execution reconstructs a task from committed checkpoints and reconciles uncertain external effects after worker or context loss.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-session-state, transaction]
sources: [https://adk.dev/runtime/resume/, https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-13
updated: 2026-10-21
---

# Durable Agent Execution

## Summary

A **durable agent** can continue the same task after a worker, model context, or execution environment ends. It does not achieve that by retaining a long transcript alone: its runtime must commit task progress, workspace references, approvals, and tool outcomes so the next worker can determine the next valid step.

## Grounded explanation

The [[agent-execution-harness]] owns control flow around the model. A checkpoint records a task identifier, accepted input, completed steps, current step, artifact versions, and pending external operations. A fresh worker reconstructs a bounded prompt from this durable evidence rather than asking the model to infer progress from a partial narrative. [[agent-session-state]] may preserve conversation context, but it is not the same as the interrupted run's execution position. A checkpoint must name which run is being resumed and which state version it observed.

The hardest boundary is an external side effect. The local checkpoint and a remote action normally cannot be one [[transaction]]. If an API call succeeds and the worker dies before recording its result, absence of a receipt means **unknown**, not failed. Persist an operation ID before dispatch; after restart, query the external system or use its idempotency semantics before retrying. An approval must bind the exact operation and arguments that were approved, and the resumed worker must not silently replace them. A workspace path alone is not enough if files changed; persist a commit or content hash when correctness depends on those bytes.

Crash-test the boundaries: before action dispatch, after dispatch before acknowledgement, after checkpoint commit, during an approval pause, and after model-context compaction. Require one coherent outcome and no duplicate consequential effect. Compare this machinery with a simpler queue and idempotent worker; a general agent runtime is justified when adaptive multi-step work really needs it.

## Re-entry is not exactly-once execution

ADK's resume documentation identifies a workflow by invocation and session, restores completed event results, and may rerun the interrupted tool. It explicitly warns that tools can execute more than once and that modifying a stopped workflow before resume is unsupported. A persistent session service is necessary for cross-process recovery but does not atomically bind remote effects to local event records.

Persist the exact evidence, draft, operation arguments and approval binding before a pause. Reusing the same logical operation must not silently retrieve new evidence or create a new draft under the old approval. Recheck current permissions and policy-critical freshness before dispatch; when a refreshed payload differs, obtain a decision for that payload rather than repurposing the old one.

A completed-table check followed by publication can race between workers, and a crash after publication can leave the completed table empty. An atomic local claim helps serialize workers but does not remove this remote ambiguity. Pair stable operation identity with provider deduplication or an outcome query; an outbox atomically commits local delivery intent but still requires duplicate-safe delivery and consumption. Test concurrent duplicate approvals and every crash boundary, not only one sequential replay.

## Prerequisites

- [[agent-execution-harness]]
- [[agent-session-state]]
- [[transaction]]

## Sources

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): documents thread checkpoints, durability, replay, and state recovery.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): documents durable pause/resume points for human input.

- <https://adk.dev/runtime/resume/>
