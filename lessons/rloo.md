# REINFORCE Leave-One-Out

## Meaning

REINFORCE Leave-One-Out (RLOO) uses peer responses to estimate a prompt-specific reward baseline without training a critic. Its defining detail is excluding the current response from its own baseline.

## Mechanism

For a prompt x, sample K>1 responses independently from the same policy. Let R_i be response i's reward. Its baseline is b_i=sum_(j≠i) R_j/(K-1), and its centered signal is A_i=R_i-b_i. Apply A_i to that response's [[reinforce-policy-gradient]] term. Conditional on x and fixed policy parameters, independently sampled peers do not depend on the current sampled action, preserving the usual baseline argument. This requires detaching the baseline in the gradient computation.

A group mean including R_i is not identical: R_i-mean(R)=((K-1)/K) A_i. Without additional operations it shrinks all signals by a constant for fixed K; variable group sizes, normalization and clipping complicate that relationship. RLOO does not itself require dividing by within-group standard deviation.

## One example

Three responses receive rewards [1,0,1]. The first response compares against mean(0,1)=.5, giving A_1=.5. The second compares against mean(1,1)=1, giving A_2=-1. The third again receives .5. Subtracting the self-including group mean 2/3 instead gives [1/3,-2/3,1/3], exactly 2/3 of these leave-one-out values. Both include negative updates; neither is equivalent to retaining only successful outputs.

## Boundaries and check

The response is treated as an action with a final return, so applying one centered signal to all its token log probabilities does not locate the causal mistake inside it. K=1 is invalid for this peer estimator. Shared decoding randomness or conditional resampling can break the independent-peer assumption. A learned reward model or separate reference penalty remains a distinct system choice.

Test K=2, equal rewards, unequal group sizes and masked outputs. Compare variance, total sampled tokens and held-out task quality against a learned baseline and no baseline. Does removing a critic eliminate all extra generation cost? No: several responses per prompt are needed, and their quality and diversity determine the usefulness of the comparison.
