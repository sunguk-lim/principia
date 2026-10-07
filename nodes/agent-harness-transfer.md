---
id: agent-harness-transfer
title: Agent Harness Transfer
summary: Agent harness transfer tests whether a model's tool-use behavior survives changes to the prompts, action schemas, observations, and runtime controls surrounding it.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, tool-call-execution-contract, measurement]
sources: [https://docs.langchain.com/oss/python/langchain/overview, https://docs.langchain.com/oss/python/langgraph/overview]
status: explained
created: 2026-10-08
updated: 2026-10-08
---

# Agent Harness Transfer

## Summary

A model trained on agent trajectories learns conditional behavior under a particular [[agent-execution-harness]], not a harness-independent task policy by definition. The surrounding prompt, tool names and argument schemas, observation encoding, action space, and stop conventions are part of its input/output distribution. Moving the same weights to a different runtime is therefore a transfer test.

## Grounded explanation

A [[tool-call-execution-contract]] defines how a proposed action becomes an executable call and how its result returns. LangChain's official overview describes an agent as a model plus a harness of prompts, tools, and middleware; LangGraph documents stateful orchestration as a separate layer. Those are interface facts, not evidence for a universal transfer failure rate.

Consider a training trace where the model calls `edit_file(path, patch)` and receives a line-numbered diff. A target harness might offer `apply_patch(diff)` and return a structured JSON error. Even if both solve the same coding task, the first generated call can be invalid, and the next observation can fall outside the training examples. Teacher-forced next-action loss on the original traces does not test recovery after such a mismatch.

Represent a trajectory with explicit task state, observation type, allowed-action schema, action arguments, result, and effect evidence. An intermediate representation can reduce conversion work, but it cannot erase semantic differences: two tools with similar names may have different permissions or side effects. Validate every adapter against real execution contracts. Alternatives include prompt/schema adapters, retraining on diverse harnesses, or retaining the original harness. More varied data costs annotation and may not help when target tools are genuinely different.

Hold task instances and weights fixed while varying one harness feature at a time, then test on a harness excluded from training. Measure schema-valid calls, task completion, invalid actions, recovery after unfamiliar observations, cost, and safety violations with [[measurement]]. Compare against the original harness and a simple adapter baseline. Distinguish model generalization from a stronger target harness's own error handling; no single-source newsletter claim establishes the size or cause of a transfer gap.

## Sources

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview): identifies the agent harness's prompt, tools, and middleware.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): documents stateful orchestration as a runtime concern.
