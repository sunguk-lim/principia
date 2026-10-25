---
id: rag-latency-budget
title: RAG Latency Budget
summary: A RAG latency budget attributes first-token and completion delay to the actual retrieval, context, queueing and generation critical path rather than assuming one universal bottleneck.
type: concept
tags: [ml/information-retrieval]
prereqs: [retrieval-augmented-generation, prefill-vs-decode, trace-span, latency-percentile]
sources: [https://docs.langchain.com/oss/python/langchain/retrieval, https://opentelemetry.io/docs/concepts/signals/traces/]
status: explained
created: 2026-10-26
updated: 2026-10-26
---

# RAG Latency Budget

## Meaning

A RAG latency budget explains where time goes on the path from question arrival to usable output. It distinguishes time to the first usable token from full completion and counts only elapsed critical-path work, not the sum of overlapping child durations. Saying that RAG is always a prefill problem or always a retrieval problem hides the workload that determines the answer.

## Mechanism

[[retrieval-augmented-generation]] can include query encoding, remote search, evidence ranking, context assembly and model inference. [[prefill-vs-decode]] separates processing the assembled prompt from emitting subsequent tokens. Each stage can also wait for a worker, network or provider. An agentic controller may repeat retrieval and add model calls, so its path is not the same as a retrieve-once pipeline.

Instrument a root [[trace-span]] for the request and child spans for bounded operations, with first-output and last-output timestamps. A parent duration already includes its children. Do not add both the parent and child as separate elapsed work. When lexical and vector searches run concurrently and both results are required, completion waits for the slower branch, not the sum of both branch durations. Shared-resource contention and launch delays can change that overlap; observe start/end times rather than inferring it from a diagram.

## Worked example

Assume a hypothetical request waits 20 ms, spends 10 ms encoding the query, then starts two searches together. Their durations are 30 and 50 ms. Fusion/reranking takes 40 ms, context assembly 10 ms, and model prefill plus delivery of the first usable token 120 ms. First-token time is 20+10+max(30,50)+40+10+120=250 ms. The two searches contribute 50, not 80. If the remaining streamed response takes 600 ms, completion time is 850 ms.

A perfect elimination of the 50-ms search interval would reduce first-token time from 250 to 200 ms, but completion from 850 to 800 ms. Reducing prefill by 30 ms instead yields 220 and 820 ms. These original toy numbers explain attribution, not measured hardware performance. If a remote database stalls for 800 ms or an iterative controller retrieves again, the bottleneck changes. More retrieved evidence can also increase prefill and improve answer support simultaneously, so a faster prompt assembled by deleting necessary evidence is not an equivalent success.

## Validation

Measure [[latency-percentile]] over complete requests, not sums of component p95 values: the slow tails need not occur on the same request. Slice by input/output length, retrieval rounds, corpus/route, concurrency, cache hits, failures and accepted answer quality. Report first usable output and completion separately, including retries and rejected requests. Compare candidate optimizations on the same task set and evidence requirements. A warm prefix cache, fewer passages, parallel retrieval and graph replay affect different parts of the path; optimize the observed constrained stage and retest correctness.

## Check your understanding

**Question:** Can a sum of child spans exceed end-to-end latency? **Answer:** Yes, when children overlap; the root interval measures elapsed time. That does not prove telemetry is wrong or mean every operation was serialized.

## Prerequisites

- [[retrieval-augmented-generation]]
- [[prefill-vs-decode]]
- [[trace-span]]
- [[latency-percentile]]

## Sources

- <https://docs.langchain.com/oss/python/langchain/retrieval> — retrieval architectures and variable retrieval/inference latency.
- <https://opentelemetry.io/docs/concepts/signals/traces/> — request traces and nested operation intervals.
