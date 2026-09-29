---
id: model-unlearning
title: Model Unlearning
summary: Model unlearning attempts to reduce a trained model's dependence on specified data without full retraining, but behavioral refusal alone is not evidence that the data was removed.
type: concept
tags: [ml/training]
prereqs: [training-data-extraction-risk, measurement]
sources: [https://arxiv.org/abs/2310.02238, https://arxiv.org/abs/2012.07805]
status: explained
created: 2026-09-30
updated: 2026-09-30
---

# Model Unlearning

## Summary

**Model unlearning** seeks to make a trained model behave as though specified information had not influenced it, ideally without retraining from scratch. That is a stronger goal than teaching a model to refuse a question. A refusal can coexist with a retained capability to produce the answer under other prompts, and a failed extraction attempt cannot prove exact deletion.

## Grounded explanation

Define the deletion target first: a document, a user's records, a set of strings, or a category of facts. Define the reference behavior next, often a model retrained without those records. An approximate unlearning method may fine-tune, edit parameters, or distill behavior so the target is less likely to appear. The method can also damage neighboring legitimate knowledge or general capability. “Unlearned” therefore needs a specified evaluation and tolerance, not a generic success flag.

[[training-data-extraction-risk]] is one observable consequence to test, but it is only a slice of the objective. Probe diverse prompts and decoding settings, use authorized canaries and held-out paraphrases, and compare against both the original model and a retrained reference where feasible. Use [[measurement]] to report extraction, task quality, false refusal, calibration, and robustness after subsequent fine-tuning. State the attacker's query budget and what the test does not cover.

For example, a model trained on a fictional secret can be fine-tuned to reply “I cannot answer” to a direct question. A rephrased or translated request may still recover the string. This does not prove that *all* fine-tuning fails, only that the direct refusal benchmark does not establish deletion. A measured unlearning method may reduce extraction under the tested attacks without guaranteeing inaccessible information under every future attack.

Prefer preventing sensitive records from entering training data when possible. If removal is required, compare approximate unlearning with retraining, data versioning, access control around external context, and deployment risk. Output filtering is a fallible backstop, not a substitute for proving the required deletion property.

## Prerequisites

- [[training-data-extraction-risk]]
- [[measurement]]

## Sources

- [Eldan and Russinovich, “Who's Harry Potter? Approximate Unlearning in LLMs”](https://arxiv.org/abs/2310.02238): an approximate method and its evaluation scope.
- [Carlini et al., extraction attacks](https://arxiv.org/abs/2012.07805): why a refusal-only test is insufficient to evaluate residual disclosure risk.
