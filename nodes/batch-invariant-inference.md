---
id: batch-invariant-inference
title: Batch-Invariant Inference
summary: Batch-invariant inference preserves a request's numerical computation when unrelated requests change batch membership, distinct from fixed-batch repeatability.
type: concept
tags: [ml/llm/inference]
prereqs: [floating-point-reduction-order, continuous-batching, greedy-decoding-reproducibility]
sources: [https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/, https://docs.vllm.ai/en/latest/features/batch_invariance/]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Batch-Invariant Inference

## Meaning

Batch invariance asks whether one request receives the same numerical result when other requests are added, removed or reordered. Fixed-batch repeatability asks only whether rerunning the same complete batch gives the same result. The second does not imply the first.

## Mechanism

[[continuous-batching]] changes a request's neighbors over time. A kernel may change work partitioning with batch shape, altering [[floating-point-reduction-order]] even when the mathematical per-request function has no cross-request dependency. Fixing each request's reduction partition independently of unrelated batch members removes this cause of variation. The whole relevant path must meet the contract: normalization, matrix multiplication, attention, cache updates and any distributed reductions, not just the sampler.

By [[greedy-decoding-reproducibility]], a deterministic argmax can still choose a different token when nearly tied logits move. Batch-invariant arithmetic prevents this particular trigger; it does not repair changed prompts, model revisions or random sampling without a fixed random-number policy.

## Worked example

Request A has two top logits. In batch A+B the scores are 12.3417 and 12.3415; in batch A+C+D they are 12.3414 and 12.3416. Repeating either complete batch may reproduce its own result, yet A's winning token differs. A batch-invariant path must preserve A's values across those changes within its declared guarantee. It need not match a different device or software version.

## Contract and validation

Pin weights, tokenizer, rendered tokens, adapter, precision, runtime, hardware and decoding policy. Compare A alone, in multiple batch positions, with different neighbors and sequence lengths, and through admission/removal during decoding. Compare logits and first divergent token, not just visually similar strings. Test cached and uncached paths and supported distributed settings.

vLLM documents a beta mode with explicit platform, model and reduction-shape limits. Check the deployed version; a configuration flag is not proof that every custom kernel or unsupported model is covered. Measure throughput, tails and memory alongside numerical agreement. Fixed reduction choices can limit optimization, but no universal slowdown follows.

## Prerequisites

- [[floating-point-reduction-order]]
- [[continuous-batching]]
- [[greedy-decoding-reproducibility]]

## Sources

- <https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>
- <https://docs.vllm.ai/en/latest/features/batch_invariance/>
