# Asymmetric Policy-Ratio Clipping

## Meaning

Asymmetric clipping replaces one symmetric ratio width with separate lower and upper widths. It changes the update incentive for a sampled action, not the action's absolute probability or a guaranteed global trust region.

## Mechanism

Use the [[proximal-policy-optimization]] surrogate min(rA,clip(r,1-e_low,1+e_high)A). Here r is current over sampling-policy probability, A is a fixed advantage, and e_low and e_high are positive widths. With positive A, the upper bound ends the favorable increase incentive. With negative A, the lower bound ends the favorable decrease incentive. DAPO's Clip-Higher increases the upper width while keeping the lower relatively conservative.

A rare sampled token can experience a large relative probability increase while its absolute probability remains small. A larger upper width permits more of that favorable ratio movement, but also permits larger updates on noisy positive feedback. It does not specifically identify semantically exploratory tokens.

## One example

Choose e_low=.2 and e_high=.4. A positive-advantage action has old probability .01 and new probability .013, giving r=1.3. With A=2, this asymmetric objective is 2.6; a symmetric width .2 would cap its favorable term at 2.4. For A=-2 and r=.7, both settings give min(-1.4,-1.6)=-1.6 because their lower bound is .8. The wider upper side did not alter the negative-advantage cutoff. These are one-action computations, not a prediction of the complete parameter update.

## Boundaries and check

A flat surrogate contribution does not freeze a shared network, and unfavorable changes outside the band still receive corrective gradients. More permissive clipping cannot repair wrong rewards, poor group variation or numerical disagreement between rollout and trainer. Evaluate ratio tails, clipped fractions split by advantage sign, output diversity, held-out quality and compute. Change one bound at a time with the rest of the recipe fixed. Does raising the upper bound mean every token may increase by that exact percentage? No: it limits a particular sampled objective contribution, not all distribution coordinates.
