# Soft Adaptive Policy Optimization

## Meaning

Soft Adaptive Policy Optimization (SAPO) uses smooth token-dependent update weights instead of a hard clipped surrogate. It aims to preserve near-on-policy signal while gradually attenuating large probability-ratio deviations. Its soft control is not a certified bound on global policy divergence.

## Mechanism

Let r be a sampled token's current over behavior-policy probability ratio, A its fixed advantage, and tau>0 a temperature parameter chosen separately for positive and negative A. Define the sigmoid sigma(z)=1/(1+exp(-z)) and f(r)=(4/tau) sigma(tau(r-1)). SAPO aggregates f(r)A across response tokens, using the group signal from [[group-relative-policy-optimization]].

Writing p=sigma(tau(r-1)), differentiation gives f'(r)=4p(1-p). Thus the log-policy gradient has coefficient 4p(1-p) r A. At r=1, p=.5 and the gate is one; away from one it decays smoothly. Larger tau narrows the ratio range receiving strong weight. Unlike the sign-dependent flat region of [[proximal-policy-optimization]], a finite ratio retains a smooth, potentially very small gradient. The objective value itself is not the same as the ordinary rA surrogate even when the local derivative matches at one.

## One example

Choose an illustrative tau=4. At r=1.5, p=sigma(2)≈.881 and the gate is 4×.881×.119≈.420. With A=2, the log-policy coefficient is about .420×1.5×2=1.26, compared with 3 for an unclipped ratio surrogate. At r=1, it is 2. Choosing tau=8 at r=1.5 gives p=sigma(4)≈.982 and a gate about .0707: stronger attenuation, not a wider permissive band.

## Boundaries and check

The paper discusses sequence-coherent behavior under assumptions on small updates and within-sequence ratio dispersion. That is not identical to applying one GSPO clip to every response or a guarantee for arbitrary ratio outliers. Implement the exact surrogate, not a detached gate substituted without a gradient analysis. Test derivatives numerically, positive/negative temperatures, extreme exponents, masks and numerical agreement across engines. Compare effective weighted tokens, divergence, quality and total training cost. Does a nonzero smooth gradient guarantee useful learning? No: a tiny weight, wrong reward or stale sample can still make it ineffective.
