---
id: tool-call-execution-contract
title: Tool-Call Execution Contract
summary: A tool-call execution contract separates a model's proposed tool name and arguments from the application's validation, authorization, execution, and result reconciliation.
type: concept
tags: [ml/agents]
prereqs: [structured-output, agent-session-state]
sources: [https://developers.openai.com/api/docs/guides/function-calling, https://developers.openai.com/api/docs/guides/function-calling, https://modelcontextprotocol.io/specification/2025-06-18/server/tools]
status: explained
created: 2026-09-30
updated: 2026-10-21
---

# Tool-Call Execution Contract

## Summary

A model can propose a tool call, but the application owns the tool. The **tool-call execution contract** defines the handoff: expose a name and argument schema, receive a proposed call, validate and authorize it, execute at most the permitted effect, record an outcome, and return that outcome to the conversation. JSON-shaped output is an interface, not permission or proof of execution.

## Grounded explanation

The model receives a tool definition, often with a name, description, and input schema. It may return a call identifier, selected tool, and arguments. [[structured-output]] can constrain syntax but cannot establish that the arguments are true, safe, or within the user's authority. The application must parse against the actual schema, check resource and identity scopes, apply budgets and approvals where required, and reject unknown tools or extra arguments. A read-only search and a money-moving operation need different policies even if both take JSON.

For an example `search_books({"query":"..."})`, the application validates a bounded string and calls its own search implementation. A proposed `delete_book` is not executable merely because the model named it. The result should be associated with the original call ID and persisted in [[agent-session-state]] before the model is asked to continue. If the process crashes after a side effect but before recording the response, the outcome is *unknown* until reconciled; blindly retrying may duplicate it. Idempotency keys or status queries belong in the execution layer.

A common API shape can simplify adapters, but it does not make providers equivalent. Compare how each reports parallel calls, partial arguments, schema enforcement, tool errors, cancellation, stop reasons, and result ordering. Test malformed and unauthorized calls, duplicate IDs, interrupted execution, tool timeouts, and prompt-injection attempts in tool output. Measure task success, failure recovery, latency, and cost under a matched tool set. Only after these checks can an application claim meaningful portability rather than surface-level JSON compatibility.

## Reducing and repairing the generated surface

Do not ask the model to regenerate arguments already fixed in application state. Define small semantic enums, explicit defaults and scoped object handles; resolve them in trusted code before policy checks. Shorter keys are not automatically fewer tokenizer units, and removing a disambiguating field can reduce correctness. A handle must be bound to the current request and resource scope, not treated as a globally authorized identifier.

Tool choice and argument filling can be staged, but their error and latency budgets compose. In a toy trace, a correct tool choice rate of 0.95 followed by an argument success rate of 0.9 conditioned on correct selection yields only 0.855 joint success. Compare staged and combined calls on the same held-out tasks rather than assuming two small decisions always win.

Before execution, validate syntax, types, resource identifiers, cross-field business invariants and authority. If a read-only proposal is invalid, return a bounded, sanitized field error and allow a limited repair attempt. Retain the original goal and reject attempts to repair by changing the requested action. For a write with an uncertain external outcome, reconcile before any repair or retry can trigger another effect. Output validity, semantic correctness, permitted action and observed completion remain separate metrics.

## Prerequisites

- [[structured-output]]
- [[agent-session-state]]

## Sources

- [OpenAI function calling guide](https://developers.openai.com/api/docs/guides/function-calling): model calls and application-supplied tools.
- [Model Context Protocol, Tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): schema-bearing tool discovery and invocation protocol.

- <https://developers.openai.com/api/docs/guides/function-calling>
