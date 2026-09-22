---
id: fixed-choice-logit-scoring
title: Fixed-Choice Logit Scoring
summary: Fixed-choice logit scoring reads a language model's next-token scores for a declared label set and renormalizes only those scores to rank bounded application choices without generating an answer string.
type: concept
tags: [ml/llm/inference]
prereqs: [softmax, model-calibration]
sources: [https://docs.sglang.io/docs/basic_usage/native_api.md#v1score-decoder-only-scoring]
status: explained
created: 2026-09-23
updated: 2026-09-23
---

# Fixed-Choice Logit Scoring

## Summary

**Fixed-choice logit scoring** turns a language model into a bounded decision scorer when an application already knows every allowed outcome. The prompt assigns each outcome a verified one-token label, the model produces its usual next-token logits, and the serving layer selects only the label logits and applies [[softmax]] to them. The result ranks the offered choices without an autoregressive loop or a generated JSON string. It is a conditional distribution over the offered labels, not automatic evidence that the winning choice is correct or [[model-calibration|calibrated]].

## Grounded explanation

### The mechanism

Suppose an application must route a ticket to `billing`, `technical`, or `account`. It renders the ticket and descriptions of those choices into the model's own chat template, maps the choices to labels `A`, `B`, and `C`, and ends the prompt immediately before the answer label. The model evaluates that prompt once and produces one logit for every vocabulary token at the next position.

Let $z_A$, $z_B$, and $z_C$ be the logits at the token IDs for the three labels. Instead of sampling from the full vocabulary, the scorer extracts the vector

$$z_L=[z_A,z_B,z_C]$$

and computes

$$p_i=\frac{e^{z_i}}{e^{z_A}+e^{z_B}+e^{z_C}}$$

for each offered label $i$. This is ordinary [[softmax]] over a subset. The application maps the largest score back to its semantic choice and may apply a policy such as “accept only when the top probability exceeds a threshold and leads the runner-up by a required margin.” The model supplies scores; application code owns authorization, abstention, and downstream action.

This differs from structured output. A grammar-constrained decoder still generates the braces, field name, and label value token by token while preventing malformed syntax. Fixed-choice scoring stops after the first evaluated answer position because the outcomes were enumerated before inference. It therefore fits classification or routing, not tasks whose valid answer must be newly written.

### Worked example

For the three ticket labels, suppose the selected logits are

$$[z_A,z_B,z_C]=[8.2,5.5,4.8].$$

Subtracting the maximum for numerical stability gives $[0,-2.7,-3.4]$. Exponentiating gives approximately $[1,0.0672,0.0334]$, whose sum is $1.1006$. Normalizing yields

$$[p_A,p_B,p_C]\approx[0.909,0.061,0.030].$$

The scorer therefore ranks `billing` first. But $0.909$ means only that `A` receives about 90.9% of the probability mass **after every token except A, B, and C has been removed**. If the true ticket is a security incident and no `security` or `other` choice exists, the procedure still distributes all mass among three wrong choices. An explicit reject option and threshold can reduce that failure, but only labeled target-domain data can determine whether a threshold has acceptable risk.

### Conditions and failure modes

Each label must identify the intended answer position unambiguously. A visible letter can tokenize differently with a leading space or under another chat template, and a multi-token label needs sequence scoring rather than one logit. Pin the model, tokenizer, template, and serving revision; verify labels after rendering the complete prompt.

The label token itself can carry a prior unrelated to the semantic description. Randomize label-to-choice mappings and choice order during evaluation to reveal token and position bias. Compare the bounded scorer with a simple classifier, constrained generation, and ordinary generation under the same examples and error costs.

Finally, restricted normalization does not create real-world probabilities. Use [[model-calibration]] on held-out labeled examples, inspect classwise errors and reliability, and measure selective risk when abstention is allowed. Revalidate after changing the model, prompt, labels, template, or traffic distribution.

## Prerequisites

- [[softmax]]
- [[model-calibration]]

## Sources

- [SGLang Native APIs, `/v1/score` decoder-only scoring](https://docs.sglang.io/docs/basic_usage/native_api.md#v1score-decoder-only-scoring) — official API contract for selecting label token IDs and optionally applying softmax to obtain normalized scores.
