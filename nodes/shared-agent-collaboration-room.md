---
id: shared-agent-collaboration-room
title: "Shared Agent Collaboration Room"
summary: "A shared agent collaboration room exposes durable, addressed human-agent conversation while keeping message identity, execution authority, task state and disclosure scope distinct."
type: concept
tags: [ml/agents]
prereqs: [multi-agent-orchestration, durable-agent-task-board, agent-workload-identity]
sources: [https://spec.matrix.org/v1.16/client-server-api/, https://www.anthropic.com/engineering/multi-agent-research-system]
status: explained
created: 2026-11-15
updated: 2026-11-15
---

# Shared Agent Collaboration Room

## Meaning

A collaboration room is a shared conversational interface to agents, not a requirement that all agents run inside the messaging server. Humans can address an agent, inspect relevant history and continue a task without one person relaying terminal output. Adding a room changes the product's audience and disclosure paths, not just its chat layout.

## Mechanism

Keep four identities distinct: human requester, room, logical agent and current execution attempt. A stable handle routes follow-ups to a logical agent; it does not identify which process or model invocation completed the work. The actual software principal follows [[agent-workload-identity]]. A room message should retain its sender, message ID, task reference and any artifact revision needed to interpret the result.

Addressed inbox delivery needs an explicit duplicate and recovery policy. Receiving or acknowledging a message means it reached a stage of delivery, not that the requested external effect succeeded. [[durable-agent-task-board]] records accepted ownership, dependencies and verified completion outside optimistic chat prose. [[multi-agent-orchestration]] governs what evidence a worker must pass to the next role and when work terminates.

The room service can store messages and shared files while worker processes and working directories stay elsewhere. Model-provider calls and external tools create further data paths. Local execution therefore does not imply that room content or attached files remain local. Inventory which component stores each class of data and which identity can read or act on it.

Membership, permission to send, history visibility, artifact access and tool authority are separate checks. A worker allowed in both a private and public room can accidentally relay private evidence. Check the destination audience before forwarding content; a private label is not an information-flow proof. Matrix's client-server specification supplies concrete room, event, membership and transaction-identifier contracts; the design here does not claim every agent product implements Matrix.

## One example

Researcher R receives task T in room A and produces artifact revision 4. Reviewer V accepts that revision and an operations agent posts an authorized summary in room B. If B has a broader audience, the dispatcher checks that summary's disclosure scope rather than forwarding A's entire transcript. A repeated delivery of T must not silently start a second owner. A message saying “posted” is reconciled against the observed destination event before T becomes complete.

## Validation

Test revoked membership, stale history access, wrong-room attachments, duplicate messages, worker reconnects and mismatched artifact versions. Compare a direct single-agent interface with the room at matched tasks: measure handoff loss, false completion, unauthorized disclosure, cost and latency. A room improves accessibility to work only if these contracts survive real failures.

## Prerequisites

- [[multi-agent-orchestration]]
- [[durable-agent-task-board]]
- [[agent-workload-identity]]

## Sources

- <https://spec.matrix.org/v1.16/client-server-api/>
- <https://www.anthropic.com/engineering/multi-agent-research-system>
