---
id: cispo
title: "Clipped Importance-Sampling Policy Optimization"
summary: "CISPO clips and detaches importance weights multiplying token log probabilities, bounding their coefficient without using PPO\u2019s flat favorable-side token surrogate."
type: concept
tags: [ml/reinforcement-learning]
prereqs: [proximal-policy-optimization, group-relative-policy-optimization, token-sequence-loss-weighting]
sources: [https://arxiv.org/abs/2506.13585]
status: explained
created: 2026-11-12
updated: 2026-11-12
---

# Clipped Importance-Sampling Policy Optimization

## Meaning

Clipped Importance-Sampling Policy Optimization (CISPO) limits a token's importance-weight coefficient while retaining its log-policy gradient. The decisive operation is where clipping and gradient detachment occur, not merely choosing a larger clipping bound.

## Mechanism

Let rho_t=pi_theta(y_t|prefix)/pi_old(y_t|prefix), A_t a fixed advantage, and w_t=clip(rho_t,a,b) with positive weights and declared bounds. CISPO maximizes the sum of detach(w_t) A_t log pi_theta(y_t|prefix), divided by the valid-token count. “Detach” means treating the coefficient as a constant while differentiating. [[group-relative-policy-optimization]] supplies the published group advantage and [[token-sequence-loss-weighting]] its aggregation.

The parameter derivative is w_t A_t gradient_theta log pi_theta. Differentiating through w_t would add a term that is not this estimator. In contrast, a [[proximal-policy-optimization]] positive-advantage surrogate becomes flat when its ratio exceeds the upper favorable cutoff. A clipped but nonzero CISPO weight still permits a log-policy contribution beyond that boundary. Zero advantage or an explicitly applied mask can still remove a contribution.

## One example

For A=2, rho=1.5 and upper weight bound 1.2, the detached coefficient is 2.4. The token contributes 2.4 times its log-policy gradient. PPO with upper ratio 1.2 would have a locally flat positive surrogate there. For A=-2 and rho=.5 with lower weight bound .8, the coefficient becomes -1.6 rather than zero. The original MiniMax recipe did not impose a restrictive lower bound; a bounded illustration must not be confused with that experimental setting.

## Boundaries and check

Clipping importance weights introduces bias relative to the unclipped corrected estimator. Token ratios do not automatically perform full-trajectory distribution correction, and preserving a gradient does not prove the signal is useful. Test stop-gradient placement with analytic scalar derivatives, advantage signs, masks and extreme ratios. Monitor probability consistency between rollout and trainer, policy drift, token contribution counts and held-out quality. The primary report's efficiency results are workload-specific. Does “all tokens contribute” mean every token receives a nonzero parameter update? No: zero rewards, masks, cancellations and shared parameters remain.

## Prerequisites

- [[proximal-policy-optimization]]
- [[group-relative-policy-optimization]]
- [[token-sequence-loss-weighting]]

## Sources

- <https://arxiv.org/abs/2506.13585>
