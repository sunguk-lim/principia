---
id: rollout-trainer-probability-consistency
title: Rollout–Trainer Probability Consistency
summary: Rollout–trainer probability consistency checks whether the behavior policy that produced tokens matches the probabilities the trainer attributes to those tokens.
type: concept
tags: [ml/llm/training]
prereqs: [group-relative-policy-optimization, batch-invariant-inference, kl-divergence]
sources: [https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/, https://arxiv.org/abs/2402.03300]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Rollout–Trainer Probability Consistency

## Meaning

A rollout is a generated response used for a policy update. The behavior policy is the conditional distribution that actually generated it. Probability consistency asks whether the trainer evaluates that same conditional distribution at the same policy snapshot. Matching a model name or random seed is insufficient.

## Mechanism

[[group-relative-policy-optimization]] evaluates sampled responses and updates their probability relative to a sampled policy. An apparent policy change can instead come from different tokenization, logits processing, numerical kernels or policy versions between collection and training. [[batch-invariant-inference]] helps remove dependence on serving traffic, but does not synchronize weights or sampling transformations.

Separate three distributions: the behavior distribution used to sample, the old-policy distribution used in the update denominator, and the current policy being optimized. The current policy is expected to move during optimization. A reference-policy penalty is yet another comparison; its [[kl-divergence]] is not automatically the sampler/trainer mismatch.

## Worked example

At an unchanged weight snapshot, suppose a binary vocabulary has rollout probabilities 0.6 and 0.4. The trainer reconstructs 0.55 and 0.45. A sampled first token then has a trainer/behavior probability ratio of 0.55/0.6, approximately 0.917, despite no intended weight update. If top-k processing changed the actual behavior support, comparing only raw pre-processing logits can miss a still larger mismatch. For complete sequences, compare conditional probabilities along their actual prefixes, with identical masking and token accounting.

## Validation and boundaries

Record bounded versioned references for policy, tokenizer, template, numerical backend and sampling configuration. At a frozen checkpoint, compare stored token log probabilities against teacher-forced trainer values; inspect per-token differences, tails and support changes. Use full-distribution comparisons where available. Equality only on sampled tokens is not proof that every distribution matches.

An experiment may find numerical alignment stabilizes training, but that does not certify reward validity, useful exploration or generalization. Corrections for a deliberately different behavior policy are algorithmic choices that need their own derivation; silently relabeling inconsistent data on-policy is not one.

## Prerequisites

- [[group-relative-policy-optimization]]
- [[batch-invariant-inference]]
- [[kl-divergence]]

## Sources

- <https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/>
- <https://arxiv.org/abs/2402.03300>
