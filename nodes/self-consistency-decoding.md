---
id: self-consistency-decoding
title: Self-Consistency Decoding
summary: Self-consistency decoding samples several reasoning paths and aggregates their normalized final answers rather than trusting one greedy path.
type: concept
tags: [ml/llm/reasoning]
prereqs: [chain-of-thought, llm-sampling-controls, measurement]
sources: [https://arxiv.org/abs/2203.11171]
status: explained
created: 2026-10-22
updated: 2026-10-22
---

# Self-Consistency Decoding

## Meaning

Self-consistency decoding samples multiple reasoning paths for the same problem, extracts their final answers, and selects the answer with the most support. It aggregates answers, not the words of the reasoning paths. The primary paper studies arithmetic and commonsense reasoning; applying agreement to a tool router is an additional application to validate, not an established safety guarantee.

## Mechanism

With [[chain-of-thought]], different generated paths can reach the same answer. [[llm-sampling-controls]] determines how paths are sampled. Normalize equivalent answers before counting: `0.5` and `1/2` should not be separate votes when the task treats them as equal. Let N be the number of samples, n(a) the count assigned to answer a, and f(a)=n(a)/N its observed frequency. Majority or plurality selection chooses the largest count under an explicit tie policy. This approximates aggregating probability mass over sampled paths that end at the same answer, instead of choosing one locally likely path.

The frequency f(a) is agreement among these samples, not the probability that a is true. Samples share weights, evidence and prompt biases. Repeated generation can therefore produce confident consensus on the same error. Disagreement is a candidate escalation signal; calibrate its relationship with actual errors on labeled held-out cases. Keep the effect executor outside this loop: sampling proposed actions must not execute them repeatedly.

## Worked example

Five sampled paths yield `12`, `12`, `8`, `12`, and `8`. The counts are 3 and 2, so plurality selects 12 with frequency 3/5=0.6. This says nothing about correctness until compared with evidence or an answer oracle. Five copies of the same flawed derivation can give frequency 1 while all are wrong.

If each path consumes 200 output tokens, five paths consume 1,000 rather than 200, plus aggregation work. Parallel requests may reduce elapsed time but not total generated tokens and can compete for capacity. Compare a fixed sampling budget with one greedy answer and a stronger single-pass alternative using [[measurement]]: correctness, disagreement, calibrated escalation, latency and cost. Include unanimous errors, ambiguous questions and distribution shift. For actions, also measure unsafe proposals and ensure independent authorization checks.

## Check your understanding

**Question:** Does unanimous agreement authorize a payment? **Answer:** No. It establishes only agreement under one sampling setup, not truth, permission or a safe external effect.

## Prerequisites

- [[chain-of-thought]]
- [[llm-sampling-controls]]
- [[measurement]]

## Sources

- <https://arxiv.org/abs/2203.11171>
