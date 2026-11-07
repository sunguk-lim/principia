---
id: request-token-budget
title: "Per-Request Token Budget"
summary: "A per-request token budget bounds admitted context and generated or iterative model work through externally enforced limits and explicit exhaustion outcomes."
type: concept
tags: [ml/llm/inference]
prereqs: [tool-call-execution-contract, multi-turn-token-accounting]
sources: [https://developers.openai.com/api/docs/guides/reasoning, https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Per-Request Token Budget

## Meaning

A token budget is a resource contract, not a promise that an answer will be correct or complete. Separate context admission, per-call output limits and an aggregate allowance across retries, reasoning and tool-driven turns. A prompt asking for brevity is not externally enforced control.

## Mechanism

Before dispatch, count the fully rendered model input with the supported tokenizer and reserve the allowed output under the endpoint's context rules. The [[tool-call-execution-contract]] checks tool and loop authority independently. Apply the endpoint's hard generation cap where supported, record its stop reason, and use [[multi-turn-token-accounting]] to reconcile actual usage across all calls belonging to the logical request.

An aggregate controller reserves allowance before concurrent calls and releases or reconciles it after observed completion. Otherwise two calls can each spend the same remaining budget. Provider caps differ in whether hidden reasoning is included; tool outputs and later prompts can consume additional context and billed input. Loop-count, wall-time and monetary limits remain separate controls because equal token counts need not imply equal runtime or cost.

## One example

An invented request permits at most 3,000 generated tokens across all model calls. After one call reports 1,100, the remaining allowance is 1,900. A retry requesting another 2,000 must be narrowed or rejected before dispatch. If two workers run concurrently, reserving 1,200 for one leaves only 700 for the other until reconciliation. A provider's per-call cap of 2,000 would not by itself enforce the 3,000 aggregate contract: two valid calls could otherwise generate 4,000. Input tokens are tracked separately in this example, not silently subtracted from an output-only allowance.

## Check your understanding

Does a limit stop always mean task completion? No. Preserve a truncation or budget-exhausted outcome and incomplete artifacts. A retry that merely reopens the full allowance can defeat the cap and amplify costs. Test exact boundaries, unknown usage after connection loss, parallel reservations, repeated tool calls and supported reasoning accounting. Compare success, truncation, latency and total cost over the same tasks. A documented provider field or recursion limit is one enforcement mechanism, not proof of a complete cross-call budget controller.

## Prerequisites

- [[tool-call-execution-contract]]
- [[multi-turn-token-accounting]]

## Sources

- <https://developers.openai.com/api/docs/guides/reasoning>
- <https://docs.langchain.com/oss/python/langgraph/errors/GRAPH_RECURSION_LIMIT>
