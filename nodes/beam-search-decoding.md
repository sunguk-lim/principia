---
id: beam-search-decoding
title: "Beam Search Decoding"
summary: "Beam search retains a bounded frontier of high-scoring partial token sequences, approximating sequence search while making pruning, length scoring and stopping explicit."
type: concept
tags: [ml/llm/inference]
prereqs: [probability-chain-rule, logarithm]
sources: [https://huggingface.co/docs/transformers/generation_strategies]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Beam Search Decoding

## Meaning

Beam search keeps several possible token continuations alive instead of committing immediately to one. At every step it expands retained prefixes, scores their children and prunes back to a fixed width. It is a bounded search procedure, not a guarantee of the most probable sequence or a verifier of task correctness.

## Mechanism

Let b be the positive beam width and y_1 through y_t a candidate's first t tokens. The [[probability-chain-rule]] gives its probability as the product of p(y_i|y_1,...,y_(i-1)) over positions i. Its log score is the corresponding sum of [[logarithm]] values. Expand every retained prefix with eligible next tokens and keep the best b unfinished candidates under the declared scoring rule; manage completed candidates separately according to the stopping policy.

A width-one version under the same local score and simple stopping reduces to greedy continuation. Larger widths preserve more alternatives, but any pruned prefix is unavailable later. Length normalization, completion penalties and constraints change the objective. Scores from different lengths are not automatically comparable: multiplying another probability no greater than one cannot increase a raw path probability.

## One example

Assume exactly two output positions, so all completions have equal length. First tokens have probabilities A=.6 and B=.4. After A, x and y each have probability .5; after B, x has .9 and y .1. Greedy takes A and then x under a specified tie rule, producing probability .6×.5=.30.

A width-two beam retains A and B after the first position. Their four children score Ax=.30, Ay=.30, Bx=.36 and By=.04. The best completion is Bx. The initial lower-probability B survives long enough for its stronger continuation to win. All four probabilities sum to one. This small success does not prove optimality at longer depths: a good future path may have been pruned earlier.

## Boundaries and validation

Inspect candidate ancestry, cumulative scores, masks, completed-sequence handling and length penalties against small enumerated examples. Compare width, latency, memory and independently assessed quality. A wider beam can optimize a model's likelihood more effectively while making the answer less useful. Unlike a general reasoning search, ordinary likelihood beam search need not use a separate verifier; its score is the model's sequence probability or a declared modification.

**Check:** Does b=10 ensure the global optimum? No. It explores only prefixes that survived every earlier prune.

## Sources

- <https://huggingface.co/docs/transformers/generation_strategies>
