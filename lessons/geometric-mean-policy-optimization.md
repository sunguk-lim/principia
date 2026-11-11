# Geometric-Mean Policy Optimization

## Meaning

Geometric-Mean Policy Optimization (GMPO) changes how token surrogates are combined within a response. It takes a geometric rather than arithmetic mean while preserving the advantage's sign. It is not simply another label for GSPO: the clipping location differs.

## Mechanism

Let T be valid response length, A its fixed [[group-relative-policy-optimization]] advantage, rho_t a token probability ratio, and c_t=min(rho_t A,clip(rho_t,a,b)A) the [[proximal-policy-optimization]]-style token surrogate with positive bounds a and b. GMPO's response contribution is sign(A) times (product_t |c_t|)^(1/T). For zero A, define the contribution as zero rather than taking a logarithm of zero.

Compute positive magnitudes using the [[logarithm]]: exp(mean(log |c_t|)), then restore the sign. A negative advantage must not be passed directly into a fractional power. The geometric construction changes sensitivity and gradient weighting; a smaller scalar objective magnitude alone is not a proof of lower gradient variance or better generalization.

## One example

Take T=2, A=1, ratios [4,1], and token clipping bounds [.5,2]. Token surrogates are [2,1], so GMPO gives sqrt(2)≈1.414 rather than arithmetic mean 1.5. GSPO would first form the sequence root sqrt(4×1)=2, then clip that single number, giving 2 under the same illustrative band. The operations do not commute. For negative A, keep the same magnitude construction and restore its sign; the minimum also switches which clipping side is favorable.

Without clipping and with a constant nonzero response advantage, the geometric factor reduces to A times the geometric mean of the positive token ratios. This overlap does not make the complete clipped algorithms identical.

## Boundaries and check

Validate sign, zero-advantage handling, padding, log-space stability and the exact clipping order against a small reference calculation. Inspect gradients as well as objective values, including a single extreme token. Compare ratio distributions, held-out quality and total compute under matched reward and sampling settings. Does a geometric mean make the method immune to outliers? No: it changes their influence and still depends on all included factors and the clipping rule.
