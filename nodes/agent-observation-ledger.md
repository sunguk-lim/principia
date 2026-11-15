---
id: agent-observation-ledger
title: Agent Observation Ledger
summary: An agent observation ledger preserves action outcomes, unresolved state and recoverable evidence references so prompt compaction does not erase what was observed.
type: concept
tags: [ml/agents]
prereqs: [agent-session-state, agent-memory, agent-verification-loop]
sources: [https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts, https://www.anthropic.com/research/effective-context-engineering-for-ai-agents]
status: explained
created: 2026-10-06
updated: 2026-11-16
---

# Agent Observation Ledger

## Summary

A computer-use agent should not confuse an old screenshot with the current screen or an attempted click with a completed effect. An **observation ledger** records what the agent has tried, what was observed afterward, which subgoals are complete, and what remains uncertain. Recent pixels remain available for perception; durable progress lives in structured [[agent-session-state]].

## Grounded explanation

The ledger is a compact, inspectable state record, not a transcript summary claiming perfect recall. Each step has an action identifier, expected state change, observed evidence, outcome (`confirmed`, `failed`, or `unknown`), and next check. A screenshot is evidence of one moment; it should have a timestamp or step ID so a later agent cannot mistake it for the live screen. A tool result or screenshot after a click can support a transition, but neither a model's plan nor the click request alone proves the effect.

For example, an agent filling a spreadsheet might record `row 18 amount = 42.10, verified in screenshot 81` and `row 19 pending`. It can drop most earlier near-identical frames while retaining the last few for spatial continuity. If a later frame contradicts the ledger, the agent must inspect and reconcile rather than blindly trusting either. [[agent-memory]] covers general storage and retrieval; the observation ledger is narrower: it is the task-specific account of actions and current progress. [[agent-verification-loop]] decides when evidence is sufficient to commit a state transition or when to replan.

Compression trades token cost against omitted details. A checkpoint should retain identifiers and uncertainty, not only a fluent narrative. A repeated action against an unchanged observed state should trigger diagnosis: the original action may have failed, the observation may be stale, or the task may be looping. A larger context window does not by itself determine which of those occurred.

Evaluate on long tasks with repeated-looking screens. Measure task completion, duplicate actions, false completion, recovery after compaction, context size, and cost. Compare full-history, recent-frame-only, and recent-frame-plus-ledger policies under identical tasks. Inspect individual failures before attributing them to attention or model training.

## Tool-result receipts after masking

The same ledger principle applies beyond screenshots. A compact receipt identifies a tool call, its safe input fingerprint, completion state, observation time, task-relevant facts and a resolvable reference to the retained output. A placeholder saying only “output omitted” records neither what was learned nor whether the action succeeded. Keep a model's interpretation distinct from the actual observation; a stored tool response remains untrusted data.

For example, call C17 queried inventory version v6 for item Q and observed 12 units at 10:00. Its receipt can retain those facts and artifact A17 while the full 8,000-token response leaves the active prompt. A later question about a returned warehouse field can read A17 rather than rerun the original query. A question about current stock at 11:00 may need a fresh query instead. A hash can detect changed stored bytes, but it does not prove the original response was true or remains current.

A receipt reference is useful only if the active runtime can resolve it with the correct access scope. Test a successful read, missing artifact, denied access, partial response and contradictory later observation. Keep incomplete calls unknown until reconciled. These fields are an independently designed ledger application, not a standardized provider schema or evidence that one particular compression policy always saves money.

## Prerequisites

- [[agent-session-state]]
- [[agent-memory]]
- [[agent-verification-loop]]

## Sources

- <https://www.anthropic.com/research/effective-context-engineering-for-ai-agents>: lightweight references and on-demand context retrieval; receipt fields are an independent application.

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointed agent state.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): resumable execution and state inspection.
