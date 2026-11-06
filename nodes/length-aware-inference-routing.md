---
id: length-aware-inference-routing
title: "Length-Aware Inference Routing"
summary: "Length-aware inference routing places requests using estimated remaining work rather than treating request counts as equal service demand."
type: concept
tags: [ml/llm/inference]
prereqs: [inference-request-scheduling, load-balancing, prefix-caching, measurement]
sources: ["https://github.com/llm-d/llm-d-inference-scheduler/blob/main/docs/architecture.md"]
status: explained
created: 2026-11-07
updated: 2026-11-07
---

# Length-Aware Inference Routing

## Meaning

Length-aware routing uses request work estimates to choose a serving replica. It is distinct from local [[inference-request-scheduling]], which chooses work inside one replica, and from a policy that always chooses the fewest queued requests. A prompt-token count is an input feature, not an exact latency prediction.

## Mechanism

First enforce compatible model, modality and placement constraints. Then estimate each eligible replica's pending work and the new request's incremental cost. Uncached prompt length affects prefill; expected output length affects future decode work. [[prefix-caching]] means total prompt length can differ from prompt work that actually needs recomputation. Hardware, batching, current state and prediction uncertainty qualify every estimate.

[[load-balancing]] chooses among replicas, but counts alone ignore heterogeneous work. A hypothetical cost score can add estimated queue delay and incremental processing time, with units fixed and coefficients calibrated from [[measurement]]. This is an independent design example, not a claim that every router implements the same sum or that adding isolated request times exactly models continuous batching. The llm-d architecture supplies primary examples of separate filters, scorers and per-request data producers; its deployed plugin behavior must be checked separately.

## One example

Suppose compatible replica A has two queued requests estimated at 180 milliseconds each, while B has four estimated at 25 milliseconds each. A count-only rule chooses A. A serial additive workload estimate instead compares 360 with 100 milliseconds and prefers B. If the incoming prompt can reuse a prefix on A worth an estimated 300 milliseconds, that preference may reverse. These invented values expose the decision variables; actual overlapped execution needs a validated cost model.

## Check your understanding

Does input length reveal generation length? No. Length estimates can be wrong, cache directories stale and load telemetry delayed. Compare count-only, random/round-robin, estimated-work and cache-aware baselines on fixed arrival traces. Report TTFT, inter-token and completion tails, throughput, prediction errors and per-size fairness. Size-separated queues may isolate long jobs but also strand capacity; always favoring short work can starve long jobs, so age limits or explicit service classes may be necessary. Preserve eligibility constraints even when every candidate is busy.

## Prerequisites

- [[inference-request-scheduling]]
- [[load-balancing]]
- [[prefix-caching]]
- [[measurement]]

## Sources

- <https://github.com/llm-d/llm-d-inference-scheduler/blob/main/docs/architecture.md>
