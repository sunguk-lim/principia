---
id: agent-harness-interoperability
title: Agent Harness Interoperability
summary: Agent harness interoperability requires a shared task interface plus tested semantics for sessions, streaming, files, cancellation, errors, and authority across runtimes.
type: concept
tags: [ml/agents]
prereqs: [agent-harness-transfer, tool-call-execution-contract, agent-session-state]
sources: [https://agentclientprotocol.com/overview/introduction, https://modelcontextprotocol.io/specification/2025-06-18/server/tools, https://agentclientprotocol.com/protocol/session-setup, https://agentclientprotocol.com/protocol/prompt-turn]
status: explained
created: 2026-10-14
updated: 2026-10-26
---

# Agent Harness Interoperability

## Summary

A common API can let one client work with multiple coding-agent runtimes, but matching method names is only surface compatibility. **Agent harness interoperability** means the same task can be started, observed, interrupted, resumed, and completed with the promised semantics across implementations.

## Grounded explanation

[[agent-harness-transfer]] explains why a model's learned behavior can change when prompts, tools, and observations change. An interoperability layer addresses the application side: define how a task begins, which session owns it, how partial events stream, how files or workspaces are referenced, how cancellation is acknowledged, and how errors or unknown side effects are reported. A [[tool-call-execution-contract]] still validates and authorizes each tool operation; a portable API must not silently widen permissions. [[agent-session-state]] must distinguish reconnecting to a prior task from starting a new run.

The Agent Client Protocol is a primary example of a shared editor–agent interface, not proof that all agent harnesses have equivalent behavior. An adapter may translate events yet lose ordering, omit a partial file update, or treat cancellation as completion. Expose such limitations instead of claiming transparent interchangeability.

Run conformance tests across at least two runtimes: start, stream, cancel, resume, file mutation, malformed input, tool refusal, timeout, and crash recovery. Compare the resulting artifacts, effect logs, latency, and permissions. A success on one happy-path task does not establish substitutability.

## Native runtimes, artifact handoffs, and cancellation

A coordinator can keep one conversation while worker A and worker B execute in their own harnesses. That is not the same as changing the coordinator's model or serializing one live execution into another runtime. Preserve a mapping from coordinator task to worker runtime, session and attempt. Capability negotiation must precede optional operations: a runtime that can create a session does not necessarily support loading it. ACP's session-load path can replay history, while a supported resume path can reconnect without replaying it. Neither promises that a native tool process or arbitrary interpreter state moved between runtimes.

The artifact contract is equally important. Suppose worker A produces revision `r7` of `analysis.json`, then worker B builds a report from it. The handoff should identify the producer, attempt, immutable content digest, revision, media type and permitted location. B verifies those properties and its allowed read scope before consuming the file. A local path in A's workspace is not automatically meaningful or authorized in B's. If A later writes `r8`, it is a new candidate input, not an invisible mutation of B's already accepted evidence. Separate workspaces reduce edit collisions; they do not create a security sandbox or revoke shared credentials.

Cancellation is a request-and-observation protocol, not proof of rollback. ACP illustrates the distinction: the client sends a cancellation notification, the agent attempts to abort ongoing work, and the original prompt response eventually reports a cancelled stop reason after pending updates. Updates can arrive after the request but before that response. An adapter must still reconcile them. If an artifact or external side effect completed just before cancellation, cancelling does not erase it; inspect the observed receipt and mark an unobserved outcome unknown instead of inventing failure.

A conformance fixture starts task T in runtime A, receives two partial events, sends cancel, then receives a completed-file event before the terminal cancelled response. The correct result retains the file's observed revision and records that the turn was cancelled; it must not label the file nonexistent or silently resume T in B. Test duplicate events, lost terminal responses, permission-request cancellation, missing artifacts and incompatible resume capabilities. A common transport only helps if these semantic distinctions survive translation.

## Prerequisites

- [[agent-harness-transfer]]
- [[tool-call-execution-contract]]
- [[agent-session-state]]

## Sources

- [Agent Client Protocol introduction](https://agentclientprotocol.com/overview/introduction): primary editor–agent interoperability contract.
- [Model Context Protocol tools specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): a separate tool-discovery and invocation boundary.

- <https://agentclientprotocol.com/protocol/session-setup>

- <https://agentclientprotocol.com/protocol/prompt-turn>
