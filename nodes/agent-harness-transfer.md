---
id: agent-harness-transfer
title: Agent Harness Transfer
summary: Agent harness transfer tests behavioral compatibility when either a model or its surrounding prompts, tools, observations and runtime controls change.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, tool-call-execution-contract, measurement]
sources: [https://docs.langchain.com/oss/python/langchain/overview, https://docs.langchain.com/oss/python/langgraph/overview, https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm]
status: explained
created: 2026-10-08
updated: 2026-11-22
---

# Agent Harness Transfer

## Summary

A model trained on agent trajectories learns conditional behavior under a particular [[agent-execution-harness]], not a harness-independent task policy by definition. The surrounding prompt, tool names and argument schemas, observation encoding, action space, and stop conventions are part of its input/output distribution. Moving the same weights to a different runtime is therefore a transfer test. The inverse test changes the model beneath a retained runtime.

## Grounded explanation

A [[tool-call-execution-contract]] defines how a proposed action becomes an executable call and how its result returns. LangChain's official overview describes an agent as a model plus a harness of prompts, tools, and middleware; LangGraph documents stateful orchestration as a separate layer. Those are interface facts, not evidence for a universal transfer failure rate.

Consider a training trace where the model calls `edit_file(path, patch)` and receives a line-numbered diff. A target harness might offer `apply_patch(diff)` and return a structured JSON error. Even if both solve the same coding task, the first generated call can be invalid, and the next observation can fall outside the training examples. Teacher-forced next-action loss on the original traces does not test recovery after such a mismatch.

Represent a trajectory with explicit task state, observation type, allowed-action schema, action arguments, result, and effect evidence. An intermediate representation can reduce conversion work, but it cannot erase semantic differences: two tools with similar names may have different permissions or side effects. Validate every adapter against real execution contracts. Alternatives include prompt/schema adapters, retraining on diverse harnesses, or retaining the original harness. More varied data costs annotation and may not help when target tools are genuinely different.

Hold task instances and weights fixed while varying one harness feature at a time, then test on a harness excluded from training. Measure schema-valid calls, task completion, invalid actions, recovery after unfamiliar observations, cost, and safety violations with [[measurement]]. Compare against the original harness and a simple adapter baseline. Distinguish model generalization from a stronger target harness's own error handling; no single-source newsletter claim establishes the size or cause of a transfer gap.

## Swapping the model under an evolved harness

Transfer can also run in the other direction: keep a harness artifact while replacing its model. A prompt, retry rule or completion check optimized for one model may interact differently with another model's tool calling, observation handling or stopping behavior. An unchanged schema is not evidence that the behavioral contract still holds. Distinguish portable invariants, such as verified effect completion, from model-specific heuristics added during optimization.

For an invented comparison, model X scores 80 tasks with the original harness and 90 with an evolved version. Model Y scores 85 with the original and 75 with that evolved version. The edit helps X but harms Y; inheriting the 90-task result would hide the interaction. Run both harness versions with each model on the same independent cases before attributing a difference to the harness or model alone. Include schema-valid actions, verified outcomes, premature stopping, loops, permission failures and total cost.

Preserve the exact edit, targeted failure, pre-test prediction, observed fixes and regressions, model and benchmark version. That provenance can help a new optimizer decide what to retest, but it cannot make an old result current. Reject changes that weaken the acceptance oracle or remove an invariant simply to improve the score. Primary harness documentation establishes the runtime boundary; the crossed comparison and record fields here are independent evaluation design, not a claim to reproduce a particular transfer study.

## Sources

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview): identifies the agent harness's prompt, tools, and middleware.
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview): documents stateful orchestration as a runtime concern.

- <https://www.itl.nist.gov/div898/handbook/pri/section3/pri333.htm>
