---
id: soft-moe-slots
title: "Soft Mixture-of-Experts Slots"
summary: "Soft MoE forms expert inputs as weighted token mixtures and reconstructs token outputs from processed slots rather than dispatching individual tokens to discrete experts."
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts, matrix-multiplication]
sources: [https://arxiv.org/html/2308.00951v2]
status: explained
created: 2026-11-08
updated: 2026-11-08
---

# Soft Mixture-of-Experts Slots

## Meaning

Soft MoE changes the unit processed by an expert. A slot is a weighted mixture of token representations, not an individual token selected by top-k. Experts process their assigned slots; a second set of weights combines slot outputs back into token positions.

## Mechanism

Let X be a matrix with m token rows and d features. Let there be s slots, each assigned to an expert transformation in [[mixture-of-experts]]. Learned token-slot scores form an m-by-s matrix. Normalize down each slot column so that its weights over tokens sum to one; call the resulting dispatch matrix D. Slot inputs are D-transpose times X, an s-by-d matrix computed by [[matrix-multiplication]]. Each assigned expert transforms its slot rows.

Normalize the same token-slot scores across slots for each token instead; call this m-by-s matrix C. If processed slots form an s-by-d matrix Z, output token representations are C times Z. The two normalizations have different axes and generally produce different weights. D builds slots; C reconstructs token outputs. Neither is a discrete per-token expert-selection mask.

## One example

Take two scalar token representations X=[2,8]. Two slots use token weights [.75,.25] and [.25,.75], giving slot inputs 3.5 and 6.5. These dispatch weights can arise from score ratios 3:1 and 1:3. Let expert one double its slot and expert two add one, giving processed slots [7,7.5]. For this symmetric illustrative score matrix, token one combines slots with [.75,.25], yielding 7.125; token two uses [.25,.75], yielding 7.375. Both outputs draw from both processed mixtures, not from an individually dispatched token. In a nonsymmetric score matrix the dispatch and combine coefficients need not numerically match.

## Check your understanding

Can this unmasked operation be dropped unchanged into a causal decoder? No. A slot containing a later token can reveal it to an earlier output. The primary Soft MoE paper focuses on visual recognition and explicitly identifies autoregressive decoding as a limitation requiring careful causal design. Expert memory also remains even when slot compute is bounded. Validate weight axes, shapes, causal visibility, quality, memory and full-path runtime; reported vision results are not general decoder-serving guarantees.

## Prerequisites

- [[mixture-of-experts]]
- [[matrix-multiplication]]

## Sources

- <https://arxiv.org/html/2308.00951v2>
