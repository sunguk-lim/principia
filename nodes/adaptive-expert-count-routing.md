---
id: adaptive-expert-count-routing
title: "Adaptive Expert-Count Routing"
summary: "Adaptive expert-count routing changes how many real expert transformations a token receives under a declared gating rule and quality-resource contract."
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts]
sources: [https://github.com/SJTU-DENG-Lab/AdaMoE, https://arxiv.org/html/2202.09368v2]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Adaptive Expert-Count Routing

## Meaning

A fixed top-k router assigns the same number of selected expert paths to each token. Adaptive expert count makes active real-expert work token-dependent. This is distinct from merely changing which fixed k experts win or balancing their placement.

## Mechanism

The gate in [[mixture-of-experts]] produces preferences. A policy must translate them into a variable set and define its combination weights, minimum and maximum work, and empty-set behavior. One illustrative policy sorts normalized probabilities and takes the shortest prefix whose cumulative mass reaches a threshold. This is a defined example, not a claim about every adaptive model or the AdaMoE implementation.

Another mechanism introduces null choices: a fixed number of routing slots can include options that perform no real expert transformation. AdaMoE's primary repository implements selection among real and null experts and executes only the real expert modules. Thus a fixed count of selected routing slots need not imply a fixed count of real expert evaluations. The exact treatment of null output, renormalization and balancing is part of that model, not a generic inference switch.

## One example

For an invented cumulative-mass policy with threshold .8, probabilities [.85,.10,.05] select one expert. Probabilities [.45,.35,.20] select two because .45 is insufficient and .45+.35=.80. Both vectors sum to one. If a maximum of one expert is also imposed, the second case cannot satisfy the threshold; the implementation must expose which rule wins rather than pretending both were met. Under a null-choice policy with two slots, [real A, null] instead triggers one real evaluation, while [real A, real B] triggers two.

## Check your understanding

Does a diffuse gate prove that an input is difficult? No. Gate confidence describes the router, not an independently calibrated task-difficulty score. More active experts can change output quality, batch sizes, imbalance and synchronization. Compare with fixed-k under the same data, model adaptation and quality target; measure actual expert calls, overflow, end-to-end latency and memory. Retrofitting variable compute into a checkpoint trained for fixed routing can change its learned function. Sparse operation counts are not a measured serving speedup.

## Prerequisites

- [[mixture-of-experts]]

## Sources

- <https://github.com/SJTU-DENG-Lab/AdaMoE>
- <https://arxiv.org/html/2202.09368v2>
