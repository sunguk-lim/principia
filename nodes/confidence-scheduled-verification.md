---
id: confidence-scheduled-verification
title: Confidence-Scheduled Verification
summary: Confidence-scheduled verification allocates target-model draft verification work using predicted useful acceptance and measured execution cost while preserving a separately checked sampling contract.
type: concept
tags: [ml/llm/inference]
prereqs: [speculative-decoding, inference-request-scheduling]
sources: [https://github.com/deepseek-ai/DeepInfer/blob/main/csrc/engine/mtp_varlen.hpp, https://github.com/deepseek-ai/DeepInfer/blob/main/deepinfer/model_executor/layers/tilelang_ops/cuda/schedule_mtp_varlen.py, https://arxiv.org/abs/2211.17192]
status: explained
created: 2026-10-21
updated: 2026-10-21
---

# Confidence-Scheduled Verification

## Meaning

Confidence-scheduled verification chooses how much draft work to send to the target model rather than verifying every proposed position. It optimizes useful accepted progress per unit execution time, not confidence for its own sake. It is distinct from a token-acceptance rule.

## Mechanism

[[speculative-decoding]] proposes tokens and uses target verification plus the appropriate acceptance or correction mechanism. [[inference-request-scheduling]] controls which positions share a target execution. Confidence estimates predict whether later draft positions will remain useful after earlier positions survive. Conditional acceptance estimates can be multiplied to estimate prefix survival; later tokens cannot bypass a rejected predecessor.

A scheduler compares candidate verification budgets using estimated progress divided by measured execution time, including sampling and scheduling overhead. DeepInfer's public CPU implementation combines confidence-derived rates with graph-size timing curves and runtime estimates. Its GPU implementation multiplies position rates and ranks cumulative values with deterministic tie breaking. These are inspectable scheduling mechanisms, not independently reproduced speed claims.

Selection can change output distributions if it depends on inappropriate future draft information. The CPU implementation explicitly separates older estimates for total budget from more recent estimates for per-request lengths to avoid later-token confidence influencing whether an earlier token is verified. Do not infer a general losslessness proof merely from the existence of target verification. Audit the complete proposal, selection, acceptance and correction contract.

## Worked example

Two requests each require one base target position. Request A has predicted draft-prefix survival probabilities 0.9 and 0.45; B has 0.8 and 0.2. With two extra positions, selecting A's first and B's first gives estimated progress 2+0.9+0.8=3.7 tokens. Verifying all four extras gives 2+0.9+0.45+0.8+0.2=4.35.

If the smaller execution takes 1 ms and the larger takes 1.5 ms, estimated rates are 3.7 versus 2.9 tokens/ms. Fewer verified positions can win. Different concurrency, timing, confidence calibration or overhead can reverse the choice. Sweep these conditions and test distributional correctness separately from throughput.

## Check your understanding

**Question:** Does high draft confidence authorize emission without target checks? **Answer:** No. Confidence schedules work; the sampling contract governs emitted tokens.

## Prerequisites

- [[speculative-decoding]]
- [[inference-request-scheduling]]

## Sources

- <https://github.com/deepseek-ai/DeepInfer/blob/main/csrc/engine/mtp_varlen.hpp>
- <https://github.com/deepseek-ai/DeepInfer/blob/main/deepinfer/model_executor/layers/tilelang_ops/cuda/schedule_mtp_varlen.py>
- <https://arxiv.org/abs/2211.17192>
