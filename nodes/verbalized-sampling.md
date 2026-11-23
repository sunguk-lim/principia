---
id: verbalized-sampling
title: "Verbalized Sampling"
summary: "Verbalized sampling asks a model to generate multiple candidate responses with probability descriptions, separating a diverse proposal set from externally validated probabilities and selection."
type: concept
tags: [ml/llm/inference]
prereqs: [llm-sampling-controls, model-calibration, measurement]
sources: [https://arxiv.org/abs/2510.01171]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

# Verbalized Sampling

## Meaning

Verbalized sampling is a prompting strategy: ask for a set of candidate answers and associated probability descriptions instead of asking for only one answer. The candidates can expose alternatives that direct prompting repeatedly misses. The written numbers are model outputs, not direct access to a normalized probability over all complete responses.

## Mechanism

[[llm-sampling-controls]] changes token selection during generation. Verbalized sampling changes what the model is asked to generate: a distribution-shaped collection of responses, possibly with instructions about the requested region of probability mass. A separate application policy can select from that collection, ask a verifier to check it or request another proposal. Do not confuse generating the collection with sampling a final answer from a specified law.

Check format, duplicate candidates, nonnegative weights and the intended normalization rule. [[model-calibration]] concerns agreement with observed outcomes; a candidate's verbalized probability is not automatically calibrated truth confidence, actual sequence likelihood or empirical human preference. The paper studies an inference-time diversity intervention. Its explanation of typicality bias and its measured gains should not be generalized into guaranteed safety or quality on another workload.

## One example

An invented prompt asks for three coffee-joke ideas and their weights. The model returns A:0.2, B:0.1 and C:0.1. If the application chooses to treat these only as relative weights over the returned set, it normalizes by 0.4, giving 0.5, 0.25 and 0.25. That is a declared conditional selection policy over three candidates; it is not proof that A has probability 0.5 among every answer the model could produce.

If A and B are paraphrases, counting three strings overstates diversity. If C contains an unsafe suggestion, a small weight does not make it acceptable. Candidate validity and final selection remain separate contracts.

## Validation and check

Use [[measurement]] to compare direct prompting, repeated independent sampling and verbalized candidate generation at matched generated-token and task budgets. Evaluate semantic diversity, redundancy, task correctness, format failures, latency and selection quality. Use blinded human assessment where creative value is the target; lexical variation alone is not useful diversity. Assess factual and safety slices independently rather than importing reported research scores.

Vary candidate count and selection rules on development tasks, then report held-out performance. Retain failed or malformed candidate sets and account for verification cost. This method is not a replacement for authorization, calibrated abstention or an independently tested task oracle.

**Check:** Does a written 0.01 prove that a candidate is a calibrated rare but valid answer? No. It is generated metadata requiring its own interpretation and validation.

## Prerequisites

- [[llm-sampling-controls]]
- [[model-calibration]]
- [[measurement]]

## Sources

- <https://arxiv.org/abs/2510.01171>
