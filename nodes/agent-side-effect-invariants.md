---
id: agent-side-effect-invariants
title: Agent Side-Effect Invariants
summary: Agent side-effect invariants specify state changes that must never occur while a task is completed, and are checked in evaluation and enforced at the action boundary for irreversible operations.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, agent-verification-loop, tool-call-execution-contract]
sources: [https://modelcontextprotocol.io/specification/2025-06-18/server/tools, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-06
updated: 2026-10-06
---

# Agent Side-Effect Invariants

## Summary

An agent can reach its requested goal and still violate a “do not” constraint. **Side-effect invariants** describe forbidden changes, such as “no order placed” while adding an item to a cart. Goal success and constraint preservation need separate evidence.

## Grounded explanation

Write the task as desired postconditions plus invariants. For a shopping task, `item in cart` is a postcondition; `orders unchanged`, `no payment attempt`, and `saved cards untouched` are invariants. In a controlled evaluation, compare relevant pre/post state and record the action-event log. A state diff alone can miss a transient side effect later reversed, while an event log alone may miss an uninstrumented external change. Both should be scoped to the task, because checking every unrelated field can create false failures.

At runtime, the [[agent-execution-harness]] must enforce high-impact constraints before an effect executes. The model's proposed tool name, reasoning, or click description is not authorization; the [[tool-call-execution-contract]] validates the actual target, arguments, and resource scope. Read-only actions, reversible writes, and irreversible commits can use different policies. A payment or external submission may require a deterministic deny rule or an approval bound to exact arguments. A later verifier cannot undo an already committed payment.

Coordinate-based interfaces add a grounding risk: the intended “Add to Cart” coordinate might resolve to another control after layout changes. When available, inspect the target element or accessibility identity before acting; otherwise use restricted capabilities or a safer tool surface. Do not assume DOM inspection works on every application. If the outcome is unknown after a timeout, reconcile it before retrying; duplicate effects are themselves invariant violations.

The [[agent-verification-loop]] reports goal success and invariant-violation rate separately. Test tempting forbidden controls, ambiguous coordinates, tool errors, delayed effects, and repeated requests. Measure false blocks too: a policy that prevents every action is safe but useless. This concept is broader than a single permission check because it combines specification, observation, and runtime enforcement over a whole task.

## Prerequisites

- [[agent-execution-harness]]
- [[agent-verification-loop]]
- [[tool-call-execution-contract]]

## Sources

- [MCP tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): tool requests and application-owned execution boundaries.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): pausing execution before consequential steps.
