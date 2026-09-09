---
id: llm-as-a-judge
title: LLM as a Judge
summary: LLM-as-a-judge evaluation asks a language model to score or compare generated outputs against a rubric, providing scalable but biased proxy labels that require human calibration.
type: concept
tags: [ml/evaluation]
prereqs: [transformer-attention, measurement, model-calibration]
sources: [https://arxiv.org/abs/2306.05685]
status: explained
created: 2026-09-09
updated: 2026-09-09
---

# LLM as a Judge

## Summary

**LLM-as-a-judge** evaluation uses one language model to score, rank, or critique outputs from another system. It scales qualitative evaluation beyond manual review, but its verdict is a proxy [[measurement]], not ground truth.

## Grounded explanation

A judging record should contain the task input, candidate output or pair, rubric, reference answer when available, judge model and version, prompt, decoding settings, and structured verdict. The judge processes these tokens through [[transformer-attention]] and may return a scalar score, categorical label, or pairwise preference.

Pairwise evaluation asks whether A or B is better. Reversing their order exposes position bias: if the verdict changes frequently, the evaluator is not stable enough for that use. Single-answer scoring avoids direct ordering but can drift in scale across judge versions and rubrics. Repeating evaluations can estimate variance but does not remove systematic bias.

Known failure modes include preference for longer answers, self-enhancement toward outputs resembling the judge, limited reasoning on difficult tasks, susceptibility to text inside candidates, and contamination from benchmark familiarity. Treat candidate text as untrusted data and delimit it from evaluator instructions.

Calibrate the judge against blinded human labels on the target task. Report agreement and confusion by rubric dimension, model family, length, language, and difficulty; [[model-calibration]] matters when numeric judge confidence is used as a probability. Keep a human-reviewed sentinel set and revalidate whenever prompts, judge versions, or candidate distributions change.

Use deterministic rules or executable tests where correctness can be checked directly. Use judge models for dimensions such as helpfulness or style that require interpretation, ideally alongside references and human audits. Never let a high aggregate agreement conceal a slice where the judge systematically rewards the wrong behavior.

## Prerequisites

- [[transformer-attention]]
- [[measurement]]
- [[model-calibration]]

## Sources

- [Zheng et al., “Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena”](https://arxiv.org/abs/2306.05685): pairwise and single-answer judging, human-agreement evaluation, and position, verbosity, self-enhancement, and reasoning biases.
