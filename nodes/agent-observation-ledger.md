---
id: agent-observation-ledger
title: Agent Observation Ledger
summary: An agent observation ledger keeps verified action outcomes, completed subgoals, and unresolved state separate from the latest visual observation so long-running computer-use tasks do not depend on replaying every screenshot.
type: concept
tags: [ml/agents]
prereqs: [agent-session-state, agent-memory, agent-verification-loop]
sources: [https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Agent Observation Ledger

## Summary

A computer-use agent should not confuse an old screenshot with the current screen or an attempted click with a completed effect. An **observation ledger** records what the agent has tried, what was observed afterward, which subgoals are complete, and what remains uncertain. Recent pixels remain available for perception; durable progress lives in structured [[agent-session-state]].

## Grounded explanation

The ledger is a compact, inspectable state record, not a transcript summary claiming perfect recall. Each step has an action identifier, expected state change, observed evidence, outcome (`confirmed`, `failed`, or `unknown`), and next check. A screenshot is evidence of one moment; it should have a timestamp or step ID so a later agent cannot mistake it for the live screen. A tool result or screenshot after a click can support a transition, but neither a model's plan nor the click request alone proves the effect.

For example, an agent filling a spreadsheet might record `row 18 amount = 42.10, verified in screenshot 81` and `row 19 pending`. It can drop most earlier near-identical frames while retaining the last few for spatial continuity. If a later frame contradicts the ledger, the agent must inspect and reconcile rather than blindly trusting either. [[agent-memory]] covers general storage and retrieval; the observation ledger is narrower: it is the task-specific account of actions and current progress. [[agent-verification-loop]] decides when evidence is sufficient to commit a state transition or when to replan.

Compression trades token cost against omitted details. A checkpoint should retain identifiers and uncertainty, not only a fluent narrative. A repeated action against an unchanged observed state should trigger diagnosis: the original action may have failed, the observation may be stale, or the task may be looping. A larger context window does not by itself determine which of those occurred.

Evaluate on long tasks with repeated-looking screens. Measure task completion, duplicate actions, false completion, recovery after compaction, context size, and cost. Compare full-history, recent-frame-only, and recent-frame-plus-ledger policies under identical tasks. Inspect individual failures before attributing them to attention or model training.

## Prerequisites

- [[agent-session-state]]
- [[agent-memory]]
- [[agent-verification-loop]]

## Sources

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointed agent state.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): resumable execution and state inspection.
