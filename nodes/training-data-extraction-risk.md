---
id: training-data-extraction-risk
title: Training-Data Extraction Risk
summary: Training-data extraction risk is the possibility that prompts elicit specific sensitive training examples from a model, which must be measured rather than inferred from general accuracy or refusal behavior.
type: concept
tags: [ml/evaluation]
prereqs: [neural-network, measurement]
sources: [https://arxiv.org/abs/2012.07805]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Training-Data Extraction Risk

## Summary

A trained model can sometimes reproduce fragments of its training data. **Training-data extraction risk** concerns whether an attacker can elicit specific information that should not be disclosed. It is not the claim that every training example is stored verbatim, nor that all remembered information is reachable by a prompt.

## Grounded explanation

Training changes a [[neural-network]]'s parameters to improve prediction on its data. Repeated, distinctive, or high-surprise strings can be learned in ways that allow later reproduction under some prompts. Carlini and colleagues demonstrated extraction attacks against language models and examined factors that make memorized sequences more likely to be emitted. Their experimental result establishes a possible failure mode, not a universal leakage rate for another model or dataset.

Separate three paths in a production diagnosis. A model may reproduce training data from weights; a retrieval system may place unauthorized content into its prompt; or a tool may return information outside the user's scope. A successful leak does not identify which path was responsible until inputs, retrieval decisions, tool results, and outputs are traced. Conversely, a model declining a standard prompt does not prove that a sensitive string was removed from its weights.

Use [[measurement]] with authorized synthetic canaries or an audited sensitive-data test set. Specify the attacker’s query budget and knowledge, prompt families, decoding settings, exact-versus-semantic match criteria, and false-positive review. Test role-crossing and adversarial paraphrases while protecting the real sensitive material in the evaluation process. Report extraction success with confidence bounds for the tested setting; do not use one clean benchmark to claim general immunity.

Data minimization and filtering before training reduce exposure at its source. Retrieval authorization and output detection are additional controls, but an output classifier can miss paraphrases and generate false alarms. If prohibited content was in the training set, a model release decision needs a measured remediation plan, not a belief that later refusal tuning erased it.

## Prerequisites

- [[neural-network]]
- [[measurement]]

## Sources

- [Carlini et al., “Extracting Training Data from Large Language Models”](https://arxiv.org/abs/2012.07805): primary extraction experiments and conditions for memorization risk.
