---
id: contrastive-search-decoding
title: "Contrastive Search Decoding"
summary: "Contrastive search selects a high-probability next-token candidate while penalizing similarity between its contextual hidden state and earlier token states."
type: concept
tags: [ml/llm/inference]
prereqs: [decoder-only-transformer, cosine-similarity]
sources: [https://arxiv.org/html/2202.06417v1]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Contrastive Search Decoding

## Meaning

Contrastive search is a next-token selection rule combining model probability with a contextual repetition penalty. It does not merely count repeated words. Nor is it the same as contrasting the logits of a large model and a second smaller model: the original rule compares hidden representations within one language model.

## Mechanism

A [[decoder-only-transformer]] supplies next-token probabilities for the current prefix. Let C be the k most probable candidates, p(v) the probability of candidate v, h_v its hidden state after appending it to the prefix, and h_j a prior token's hidden state. Choose alpha between zero and one and define

$$D(v)=\max_j \operatorname{cos}(h_v,h_j),\qquad S(v)=(1-\alpha)p(v)-\alpha D(v).$$

The function cos is [[cosine-similarity]]. Select the candidate in C with largest S. The probability term favors a plausible continuation; the penalty discourages a representation extremely close to one already present. The top-k restriction limits candidate evaluations and prevents the diversity term from searching the whole low-probability vocabulary. Candidate states depend on the prefix; static word embeddings are not a drop-in replacement.

This is a deterministic scoring decision under fixed execution and tie rules, not multinomial sampling from S. At alpha=0 the rule chooses the most probable eligible candidate. Positive alpha changes the objective and can discourage legitimate repeated names or technical terms.

## One example

Use two toy candidates, A and B, with probabilities .50 and .30; other vocabulary tokens hold the remaining .20 and are outside C. Their maximum contextual similarities are .90 and .20. For alpha=.4, A scores .6×.50-.4×.90=-.06, while B scores .6×.30-.4×.20=.10. B wins despite lower probability. At alpha=.1, A scores .45-.09=.36 and B .27-.02=.25, so A wins. Both components matter.

## Boundaries and validation

The SimCTG paper introduces contrastive representation training and this search procedure; training and decoding are different operations. Its experimental gains do not prove universal superiority or factuality. Test probability/top-k construction, contextual-state alignment, penalty axes, tie handling and numerical agreement. Compare repetition, coherence, legitimate repetition, task correctness, latency and memory over k and alpha at a fixed model and output budget. Candidate evaluation adds work.

**Check:** Can an API exposing only next-token probabilities implement the exact rule? Not without also obtaining the required candidate and prior contextual states.

## Sources

- <https://arxiv.org/html/2202.06417v1>
