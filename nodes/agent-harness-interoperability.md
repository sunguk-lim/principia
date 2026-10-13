---
id: agent-harness-interoperability
title: Agent Harness Interoperability
summary: Agent harness interoperability requires a shared task interface plus tested semantics for sessions, streaming, files, cancellation, errors, and authority across runtimes.
type: concept
tags: [ml/agents]
prereqs: [agent-harness-transfer, tool-call-execution-contract, agent-session-state]
sources: [https://agentclientprotocol.com/overview/introduction, https://modelcontextprotocol.io/specification/2025-06-18/server/tools]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Agent Harness Interoperability

## Summary

A common API can let one client work with multiple coding-agent runtimes, but matching method names is only surface compatibility. **Agent harness interoperability** means the same task can be started, observed, interrupted, resumed, and completed with the promised semantics across implementations.

## Grounded explanation

[[agent-harness-transfer]] explains why a model's learned behavior can change when prompts, tools, and observations change. An interoperability layer addresses the application side: define how a task begins, which session owns it, how partial events stream, how files or workspaces are referenced, how cancellation is acknowledged, and how errors or unknown side effects are reported. A [[tool-call-execution-contract]] still validates and authorizes each tool operation; a portable API must not silently widen permissions. [[agent-session-state]] must distinguish reconnecting to a prior task from starting a new run.

The Agent Client Protocol is a primary example of a shared editor–agent interface, not proof that all agent harnesses have equivalent behavior. An adapter may translate events yet lose ordering, omit a partial file update, or treat cancellation as completion. Expose such limitations instead of claiming transparent interchangeability.

Run conformance tests across at least two runtimes: start, stream, cancel, resume, file mutation, malformed input, tool refusal, timeout, and crash recovery. Compare the resulting artifacts, effect logs, latency, and permissions. A success on one happy-path task does not establish substitutability.

## Prerequisites

- [[agent-harness-transfer]]
- [[tool-call-execution-contract]]
- [[agent-session-state]]

## Sources

- [Agent Client Protocol introduction](https://agentclientprotocol.com/overview/introduction): primary editor–agent interoperability contract.
- [Model Context Protocol tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): a separate tool-discovery and invocation boundary.
