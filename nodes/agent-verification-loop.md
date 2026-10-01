---
id: agent-verification-loop
title: Agent Verification Loop
summary: An agent verification loop checks explicit completion criteria against evidence after each bounded step and chooses success, repair, replan, escalation, or stop.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, measurement, decision-score-action-gate]
sources: [https://docs.langchain.com/oss/python/langgraph/persistence, https://docs.langchain.com/oss/python/langgraph/interrupts]
status: explained
created: 2026-10-02
updated: 2026-10-02
---

# Agent Verification Loop

## Summary

An **agent verification loop** makes progress and completion testable. A model's statement that it is finished is a proposal, not proof: the application checks an explicit criterion against tool results and decides whether to continue, repair, escalate, or stop.

## Grounded explanation

Represent a plan step with a completion criterion and an evidence location. After execution, apply cheap deterministic checks first: was the required artifact produced, did a tool return success, did a test pass, and is the result authorized? When those checks cannot settle the question, a bounded classifier or independent reviewer can judge an uncertain case. The [[decision-score-action-gate]] keeps that judgment separate from the action policy and allows abstention. An independent LLM review is additional evidence, not an oracle.

Record the attempted approach and failure reason in [[agent-execution-harness]] state. Repeating the same call with unchanged inputs is not progress. A repair changes a bounded parameter or fixes a diagnosed failure; a replan selects another route; escalation asks for outside help; stop returns an explicit incomplete outcome when budget or evidence is exhausted. Persist the checkpoint before external side effects so a resumed run does not silently repeat them.

Consider a code-fix agent that edits a file and claims success. A build failure blocks completion. The next step may repair that specific error, but after repeated equivalent patches and no improvement it should stop or replan. Test success paths, false-positive completion, repeated-action detection, verifier disagreement, tool failures, and budget limits. Measure successful outcomes, mistaken acceptance, unnecessary replans, and latency/cost on held-out tasks using [[measurement]].

## Prerequisites

- [[agent-execution-harness]]
- [[measurement]]
- [[decision-score-action-gate]]

## Sources

- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence): checkpointing and recovery state.
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts): pausing before continuation.
