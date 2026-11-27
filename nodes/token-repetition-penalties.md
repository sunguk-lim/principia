---
id: token-repetition-penalties
title: "Token Repetition Penalties"
summary: "Token repetition penalties alter next-token logits according to prior token counts or presence, discouraging reuse without enforcing semantic novelty."
type: concept
tags: [ml/llm/inference]
prereqs: [softmax, subword-tokenization]
sources: [https://platform.openai.com/docs/api-reference/chat/create, https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/oai_docs/text-generation.txt]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Token Repetition Penalties

## Meaning

A repetition penalty changes the preference for a token because it has appeared before. A frequency penalty depends on how often it appeared; a presence penalty depends only on whether it appeared. These are distribution controls, not checks that an answer is nonredundant or correct.

## Mechanism

Let token index $i$ identify a vocabulary entry under [[subword-tokenization]], $z_i$ be its original next-token logit, and $c_i$ be its count in the history considered by the implementation. Let $a_f$ and $a_p$ be frequency and presence coefficients. An additive contract documented in OpenAI's text-generation reference is

$$z'_i=z_i-a_f c_i-a_p\mathbf{1}[c_i>0].$$

The indicator is one when the count is positive and zero otherwise. Applying [[softmax]] to the adjusted logits produces normalized probabilities. Positive coefficients reduce relative preference for previously seen tokens; negative coefficients can encourage reuse. This formula is one documented contract, not a definition of every provider's parameter called “repetition penalty.” Multiplicative penalties, counted-history scope and supported model settings can differ.

## One example

Three invented candidate tokens A, B and C have logits $[3,2,1]$ and counts $[3,1,0]$. With frequency coefficient $a_f=0.5$ alone, their adjusted logits are $[1.5,1.5,1]$: A loses 1.5 and B loses 0.5. With presence coefficient $a_p=0.5$ alone, the logits are $[2.5,1.5,1]$: both previously seen tokens lose the same 0.5. With both coefficients, they become $[1,1,1]$, so softmax gives equal probabilities in this three-token toy vocabulary. Counting repeated uses and detecting first use are visibly different operations.

## Boundaries and validation

A new token is not necessarily a new idea, and a repeated token may be essential in code, a name or a faithful quotation. Penalizing common fragments can distort wording without removing semantic repetition. It does not expand knowledge or enforce a diversity target.

Check the exact API's support, history window, tokenization, order of logit processors and parameter defaults. Compare count-based and presence-based changes independently on repetitive and repetition-required tasks. Measure correctness, faithfulness, useful diversity and malformed outputs across multiple trials, not only unique-token counts. Preserve a no-penalty baseline.

**Check:** If A occurred ten times and B once, does a presence penalty subtract ten times as much from A? No; the count-dependent frequency term does that, while presence applies once to each seen token.

## Prerequisites

- [[softmax]]
- [[subword-tokenization]]

## Sources

- <https://platform.openai.com/docs/api-reference/chat/create>
- <https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/data/oai_docs/text-generation.txt>
