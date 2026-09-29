---
id: tool-call-execution-contract
title: Tool-Call Execution Contract
summary: A tool-call execution contract separates a model's proposed tool name and arguments from the application's validation, authorization, execution, and result reconciliation.
type: concept
tags: [ml/agents]
prereqs: [structured-output, agent-session-state]
sources: [https://developers.openai.com/api/docs/guides/function-calling, https://modelcontextprotocol.io/specification/2025-06-18/server/tools]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Tool-Call Execution Contract

## Summary

A model can propose a tool call, but the application owns the tool. The **tool-call execution contract** defines the handoff: expose a name and argument schema, receive a proposed call, validate and authorize it, execute at most the permitted effect, record an outcome, and return that outcome to the conversation. JSON-shaped output is an interface, not permission or proof of execution.

## Grounded explanation

The model receives a tool definition, often with a name, description, and input schema. It may return a call identifier, selected tool, and arguments. [[structured-output]] can constrain syntax but cannot establish that the arguments are true, safe, or within the user's authority. The application must parse against the actual schema, check resource and identity scopes, apply budgets and approvals where required, and reject unknown tools or extra arguments. A read-only search and a money-moving operation need different policies even if both take JSON.

For an example `search_books({"query":"..."})`, the application validates a bounded string and calls its own search implementation. A proposed `delete_book` is not executable merely because the model named it. The result should be associated with the original call ID and persisted in [[agent-session-state]] before the model is asked to continue. If the process crashes after a side effect but before recording the response, the outcome is *unknown* until reconciled; blindly retrying may duplicate it. Idempotency keys or status queries belong in the execution layer.

A common API shape can simplify adapters, but it does not make providers equivalent. Compare how each reports parallel calls, partial arguments, schema enforcement, tool errors, cancellation, stop reasons, and result ordering. Test malformed and unauthorized calls, duplicate IDs, interrupted execution, tool timeouts, and prompt-injection attempts in tool output. Measure task success, failure recovery, latency, and cost under a matched tool set. Only after these checks can an application claim meaningful portability rather than surface-level JSON compatibility.

## Prerequisites

- [[structured-output]]
- [[agent-session-state]]

## Sources

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling): model calls and application-supplied tools.
- [Model Context Protocol, Tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): schema-bearing tool discovery and invocation protocol.
