---
id: group-sequence-policy-optimization
title: "Group Sequence Policy Optimization"
summary: "GSPO clips a length-normalized sequence-likelihood ratio so response-level reward and the policy update share a sequence-level control signal."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [proximal-policy-optimization, group-relative-policy-optimization, logarithm, likelihood]
sources: [https://arxiv.org/abs/2507.18071]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# Group Sequence Policy Optimization

## Meaning

Group Sequence Policy Optimization (GSPO) controls the update of a complete sampled response with one sequence-level ratio. This differs from independently clipping each token's probability ratio while broadcasting the same final reward to every token.

## Mechanism

Let T be response length, rho_t the current-policy probability of sampled token t divided by its sampling-policy probability at the same prefix, and A the group's fixed response advantage. GSPO uses

$$s=\exp\left(\frac1T\sum_{t=1}^T\log\rho_t\right),\qquad L=\min(sA,\operatorname{clip}(s,1-\epsilon,1+\epsilon)A).$$

The [[logarithm]] makes the sequence likelihood product numerically manageable. The T-th root is a chosen normalization of that product, not the ordinary unnormalized importance weight for an entire sequence. [[group-relative-policy-optimization]] supplies A; [[proximal-policy-optimization]] explains which side becomes flat for each advantage sign.

Because s depends on all tokens, the active surrogate gives them a coherent shared factor. If the sequence hits the favorable-side cutoff, that surrogate's contribution becomes flat for the entire response. A few extreme tokens can affect whether many otherwise ordinary tokens contribute.

This is a [[likelihood]] ratio for a fixed observed response as policy parameters vary, before the length-root normalization.

## One example

For two tokens with ratios 1.44 and 1.00, s=sqrt(1.44)=1.2. With A=2 and an illustrative band [.9,1.1], the positive objective is min(2.4,2.2)=2.2 and is locally flat beyond the upper bound. Independent token clipping at 1.1 would flatten the first token's positive contribution while leaving the second active. These invented wide bounds make the contrast visible; they are not a recommended GSPO configuration.

## Boundaries and check

Sequence-root normalization changes the objective and does not establish an unbiased full-trajectory importance estimator. Small average log-ratio changes can also conceal individual token extremes. Compute ratios from compatible rollout/trainer probabilities, exclude padding consistently, and test long responses, positive and negative advantages, and zero-length rejection. Compare quality, divergence, clip fractions and useful gradient tokens at equal compute. Does sequence-level control guarantee stable training of every mixture-of-experts model? No: the primary paper's reported improvements do not remove routing, numerical and reward failure modes.

## Prerequisites

- [[proximal-policy-optimization]]
- [[group-relative-policy-optimization]]
- [[logarithm]]

- [[likelihood]]

## Sources

- <https://arxiv.org/abs/2507.18071>
