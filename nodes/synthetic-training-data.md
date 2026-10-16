---
id: synthetic-training-data
title: Synthetic Training Data
summary: Synthetic training data is model- or program-generated examples used to expand a training set, with filtering, provenance, and independent evaluation needed to prevent generator artifacts from becoming the target.
type: concept
tags: [ml/training]
prereqs: [fine-tuning, dataset-lineage]
sources: [https://arxiv.org/abs/2212.10560]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Synthetic Training Data

## Summary

**Synthetic training data** is generated rather than directly labeled from the deployment population. It can cover rare formats or create more practice examples, but volume is not the same as diversity or truth. A model trained on its own plausible mistakes may learn the generator's style rather than the desired task.

## Grounded explanation

The Self-Instruct pipeline generates candidate instructions, inputs, and outputs, then filters invalid or near-duplicate items before [[fine-tuning]]. The durable pattern is generate → validate → deduplicate → version → train → evaluate. The generator, prompt, seed, filtering rules, and accepted examples belong in [[dataset-lineage]] so a later result can be traced to a particular synthetic distribution.

Several failure modes differ. Wrong labels teach wrong behavior; repeated templates inflate apparent data size; near-duplicate test examples leak the answer; simulated users may omit difficult real-world ambiguity. A verifier can reject some invalid examples, but it may share blind spots with the generator. Human review or executable tests are useful where available, especially for high-cost labels.

## Validation

Compare a real-data baseline with matched-budget additions of filtered synthetic examples. Keep an independent, time- or source-separated real-world test set untouched by generation and filtering. Report task slices, error severity, calibration, diversity, duplicate rate, and performance under distribution shift. Ablate filtering and synthetic proportion to identify whether gains come from useful coverage rather than more training steps.

## Prerequisites

- [[fine-tuning]]
- [[dataset-lineage]]

## Sources

- [Wang et al., *Self-Instruct: Aligning Language Models with Self-Generated Instructions*](https://arxiv.org/abs/2212.10560).
