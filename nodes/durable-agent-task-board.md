---
id: durable-agent-task-board
title: "Durable Agent Task Board"
summary: "A durable agent task board stores task identity, dependencies, ownership and evidence-backed transitions separately from conversational plans."
type: concept
tags: [ml/agents]
prereqs: [agent-workflow-graph, single-writer-state-coordination, agent-harness-interoperability]
sources: ["https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents", "https://docs.langchain.com/oss/python/langgraph/persistence"]
status: explained
created: 2026-11-06
updated: 2026-11-06
---

# Durable Agent Task Board

## Meaning

A durable task board is the shared account of work, not merely a list of intended steps. Each task has a stable identity, objective, dependencies, responsible attempt, current status, acceptance criterion and evidence references. A conversation saying “the endpoint is ready” does not establish which revision is ready or which tests ran.

## Mechanism

Use an [[agent-workflow-graph]] to define legal transitions such as `ready → running → verified`, with explicit failure and blocked states. A dependency becomes satisfied through accepted evidence, not because its owner disappeared or sent an optimistic summary. Keep proposed work, attempted actions and verified outcomes distinct. Persist the board so another session can reconstruct the next permitted task without replaying the entire chat.

Choose an authoritative update protocol. Under [[single-writer-state-coordination]], workers propose changes to a coordinator, which validates expected versions and evidence before accepting them. This is one policy, not a requirement that every implementation use a particular product. A transactional multi-writer store can implement a different deliberate policy; uncoordinated whole-file replacement is not equivalent.

Handoffs follow [[agent-harness-interoperability]]: name the producing worker, attempt, artifact revision or digest, interface contract and permitted location. Consumers confirm that the evidence they read matches the accepted revision. The board does not grant permissions beyond the surrounding execution system.

## One example

Backend task B produces API contract revision 6 and passes its contract checks. Frontend task F depends on that accepted revision. F claims work against board version 12. If B later produces revision 7 with an incompatible field, the board records a new dependency decision; it must not silently relabel F's old build as verified against revision 7.

If the backend only created a file but never ran the acceptance check, B remains prepared, not verified. If a test crashes, record the check as unknown or failed under its actual outcome rather than interpreting the artifact's existence as success.

## Check your understanding

Does a persisted checkbox prove completion? Only if its transition was validated against the declared criterion and the referenced evidence is still the relevant revision. Test stale handoffs, duplicate completions, owner failure and recovery from a partially written update.

## Prerequisites

- [[agent-workflow-graph]]
- [[single-writer-state-coordination]]
- [[agent-harness-interoperability]]

## Sources

- <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents>
- <https://docs.langchain.com/oss/python/langgraph/persistence>
