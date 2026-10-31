---
id: cross-entropy-versus-accuracy
title: Cross Entropy versus Accuracy
summary: Cross entropy evaluates probability assigned to a target whereas top-choice accuracy changes only when the selected answer changes.
type: concept
tags: [ml/evaluation]
prereqs: [loss-function, softmax, logarithm]
sources: [https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html]
status: explained
created: 2026-11-01
updated: 2026-11-01
---

# Cross Entropy versus Accuracy

## Meaning

Cross entropy and accuracy answer different questions. For a hard target label, cross entropy is the negative logarithm of the probability assigned to that target. Top-choice accuracy asks only whether the largest-score label is correct. Improvements in one need not change the other.

## Mechanism

A [[softmax]] turns logits into probabilities over a declared label set. With target probability p greater than zero, the per-example [[loss-function]] is -log(p), using the natural [[logarithm]] here. Averaging this value preserves information about probability changes even when the highest-scoring label stays the same. Accuracy replaces the distribution with a single decision and scores it zero or one.

Neither metric is inherently the final business objective. A model can improve probability on easy examples while worsening rare important cases. Cross entropy depends on target definition, weighting, smoothing and masking; a language-model per-token average also depends on tokenization. Raw per-token values across incompatible tokenizers are not a clean capability comparison.

## Worked example

The correct option is A. Model 1 assigns probabilities A=0.20, B=0.50, C=0.30; model 2 assigns A=0.35, B=0.40, C=0.25. Both choose B, so accuracy on this example remains zero. Their cross entropies are approximately 1.609 and 1.050, because -ln(0.20)=1.609 and -ln(0.35)=1.050. The target gained probability without becoming the top choice.

This does not prove model 2 learned a useful general capability: it is one example. Nor does unchanged accuracy mean nothing changed. Examine representative held-out cases and operational thresholds, not only an aggregate number.

## Validation

Use the same inputs, answer labels, scoring protocol, tokenizer where relevant, valid-token mask and weighting. Report paired item outcomes and domain slices alongside compatible likelihood measures. For open-ended generation, exact-answer probability is meaningful only after defining accepted variants and length handling. A lower validation loss is evidence about the measured distribution, not a universal ordering of models across every downstream task or serving cost.

## Prerequisites

- [[loss-function]]
- [[softmax]]
- [[logarithm]]

## Sources

- <https://docs.pytorch.org/docs/2.15/generated/torch.nn.CrossEntropyLoss.html>
