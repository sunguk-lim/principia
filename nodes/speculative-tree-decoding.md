---
id: speculative-tree-decoding
title: Speculative Tree Decoding
summary: "A draft tree offers alternate token paths for one target verification pass; useful work depends on acceptance and correct state commitment."
type: concept
tags: [ml/llm/inference]
prereqs: [speculative-decoding, transformer-attention]
sources: [https://arxiv.org/abs/2305.09781, https://arxiv.org/abs/2401.10774]
status: explained
created: 2026-10-09
updated: 2026-10-09
---

# Speculative Tree Decoding

## Summary

**Speculative tree decoding** extends [[speculative-decoding]] from one proposed chain to several alternative next-token paths. A target model verifies candidate nodes under the correct ancestor context and commits only the accepted output path. Draft breadth can rescue an early mistaken proposal, but tree construction and verification have costs.

## Grounded explanation

A conventional draft chain proposes $k$ tokens. If the target rejects an early token, later proposals in that chain cannot be used. A tree carries alternatives at selected positions, so one target pass can score multiple continuations if its attention mask ensures each node sees only its own ancestors. The candidate budget must be allocated: a wider tree covers alternatives while a deeper one gambles on a long accepted prefix. Parallel predictions for several future positions may be individually plausible yet mutually inconsistent because later positions did not condition on earlier sampled choices. A sequential short-list selector is one possible repair; this is a design option, not a universal requirement.

Stateful model layers add a separate constraint. Verifying candidate branches must not accidentally advance the *live* generation state down rejected branches. An implementation may stage branch-specific state and commit only accepted transitions, or use another mathematically equivalent verification scheme. The exact method depends on the model architecture; an attention-only target uses a causal mask and KV state, while recurrent/state-space layers need an explicit branch-state contract. Calling a particular kernel rollback-free does not prove it is faster or distribution-preserving.

Compare equal target-model checkpoints, draft compute budgets, prompts, and sampling settings. Measure accepted output tokens per target pass, total wall time, draft and verification overhead, memory, output-distribution agreement with ordinary decoding, and quality on code as well as open-ended text. An apparent token-per-pass gain can vanish when the drafter or state handling dominates latency.

## Prerequisites

- [[speculative-decoding]]
- [[transformer-attention]]

## Sources

- [SpecInfer](https://arxiv.org/abs/2305.09781): speculative inference with token trees.
- [Medusa](https://arxiv.org/abs/2401.10774): multi-head candidate generation and tree attention.
