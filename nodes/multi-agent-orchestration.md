---
id: multi-agent-orchestration
title: Multi-Agent Orchestration
summary: Multi-agent orchestration assigns bounded roles and communication paths to multiple model-driven workers while an explicit protocol coordinates state, tools, termination, and verification.
type: concept
tags: [ml/agents]
prereqs: [transformer-attention, structured-output, measurement]
sources: [https://arxiv.org/abs/2308.08155]
status: explained
created: 2026-09-10
updated: 2026-11-01
---

# Multi-Agent Orchestration

## Summary

**Multi-agent orchestration** decomposes a task among several model-driven workers and defines how they exchange messages, invoke tools, share state, and decide that work is complete.

## Grounded explanation

An orchestrated system needs more than role labels. Specify each worker’s input and output contract, allowed tools, private and shared state, routing rules, stopping condition, retry budget, and authority. [[structured-output]] can make handoffs machine-checkable instead of relying on prose conventions.

Common topologies include a sequential pipeline, a central coordinator with specialists, a critic–solver loop, and a group conversation. Each changes failure propagation. Pipelines make provenance clearer but can compound early errors; open conversation allows flexible recovery but increases message cost and makes termination harder to reason about.

Multiple workers do not create independent evidence when they use the same model, prompt assumptions, or retrieved source. Agreement can be correlated. A critic can improve results only when it has a useful verification signal, different information, or executable checks—not merely another opportunity to generate plausible text.

Tool access requires least privilege and explicit data boundaries. Treat scraped or retrieved content as untrusted, validate every handoff, cap recursion, and ensure that one worker cannot delegate broader authority than it received. Record the worker, prompt or policy version, tool call, inputs, outputs, and parent task for traceability.

Compare orchestration with a single-worker baseline at equal model and tool budgets. [[measurement]] should include task success, independently verified correctness, tool failures, handoff loss, latency, token and external-service cost, retries, and safety violations. Keep multiple workers only when decomposition improves these outcomes enough to justify added state and coordination risk.

## Separating strategy from search

A coordinator can be restricted to planning and worker dispatch while research workers alone have search access. This changes the permitted action space: the coordinator must formulate a self-contained brief rather than satisfy every subquestion through its own browsing. Enforce the restriction in tool exposure and authorization, not merely in a role prompt. It is a hypothesis about better task decomposition, not a theorem that coordinators must never search.

For example, dispatch separate evidence questions about mechanism, limitations and competing explanations. Each worker returns source identifiers, claims and unresolved gaps. A deterministic assembly step can renumber identifiers and remove duplicate references, but it cannot verify that a source entails a claim. Preserve that claim-to-evidence association when merging. A shallow topology limits the number of summaries passed between workers; it does not prevent every distortion. Compare tool-separated and search-capable coordinators at equal research and model budgets, checking completeness, evidence support, handoff loss and latency rather than a vendor leaderboard.

## Prerequisites

- [[transformer-attention]]
- [[structured-output]]
- [[measurement]]

## Sources

- [Wu et al., “AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation”](https://arxiv.org/abs/2308.08155): presents customizable conversational workers combining language models, human input, tools, and programmable interaction patterns.

- <https://arxiv.org/abs/2308.08155>
