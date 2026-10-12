# Durable Agent Execution

## Meaning

Durable agent execution lets a task continue after its worker or model context ends. A long transcript is not enough; the runtime needs a committed record of which steps completed and what happened to external actions.

## Mechanism

The [[agent-execution-harness]] checkpoints task progress and references to artifact versions. The resumed worker loads those facts, then builds a bounded new prompt. [[agent-session-state]] preserves conversational meaning, while the checkpoint preserves the interrupted run's execution position. An external API call and the local record cannot usually share one [[transaction]], so a missing receipt means the outcome is unknown until reconciled.

## One example

An agent requests a refund, the service completes it, and the worker crashes before saving the response. On restart, the runtime queries the refund by operation ID. It records success if found; it does not issue another refund merely because the local result is missing.

## Check your understanding

**Question:** Why is a stored transcript insufficient? **Answer:** It may omit whether a side effect completed, which artifact version was used, or which exact operation was approved.
