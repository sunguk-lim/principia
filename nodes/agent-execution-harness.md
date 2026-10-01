---
id: agent-execution-harness
title: Agent Execution Harness
summary: An agent execution harness is the application-owned control layer around model and tool calls that enforces permissions, budgets, state, recovery, and observability.
type: concept
tags: [ml/agents]
prereqs: [tool-call-execution-contract, agent-session-state, measurement]
sources: [https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Agent Execution Harness

## Summary

An **agent execution harness** surrounds a model with application-owned controls. The model proposes actions; the harness decides whether, when, and how to run them, records outcomes, and stops or recovers when a step fails. This is broader than a prompt or a tool schema.

## Grounded explanation

A [[tool-call-execution-contract]] defines one model-to-tool handoff. The harness composes many handoffs with budgets, identity and resource checks, retry policy, fallback, approval boundaries, and [[agent-session-state]]. It must distinguish read from write authority and never infer permission from a model's confidence. A classifier may flag risky calls, but deterministic authorization remains the enforcement boundary. Middleware can redact or inspect inputs, yet filters are fallible and cannot substitute for scoped credentials.

For example, a support agent may search orders and draft a refund. The harness bounds search calls, records tool IDs and outcomes, validates refund eligibility and amount, pauses for required approval, and resumes from a checkpoint. If a provider fails after a side effect, the harness reconciles the operation rather than blindly repeating it. LangGraph documents checkpointers and interrupts as concrete mechanisms for persistence and pause/resume; they do not make every application safe automatically.

Test the harness as a system: unauthorized writes, malformed calls, duplicate results, provider failures, timeouts, approval denial, crash recovery, and budget exhaustion. Compare with a simpler baseline under identical tasks. [[measurement]] should track task completion, escaped unauthorized effects, false blocks, recovery, latency, and cost. A large test count or a calibrated-looking score alone is not evidence of safe behavior.

## Prerequisites

- [[tool-call-execution-contract]]
- [[agent-session-state]]
- [[measurement]]

## Sources

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointed execution state.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): human-in-the-loop pause and resume.
