# REINFORCE Policy Gradient

## Meaning

REINFORCE changes a stochastic policy so actions associated with higher sampled returns become more likely. It differentiates the policy's probability, not a discrete sampled action or a non-differentiable reward. This makes it a direct policy-optimization method within [[model-free-learning]].

## Mechanism

Let x be a context, y an action or complete response, theta the policy parameters, pi_theta(y|x) its probability, and R(x,y) a reward treated as fixed when differentiating. For samples drawn from the current policy, the expected reward gradient is

$$\nabla_\theta J=\mathbb E[(R(x,y)-b(x))\nabla_\theta\log\pi_\theta(y|x)].$$

The [[logarithm]] appears because differentiating a probability gives that probability times its log derivative. Sampling supplies the probability weighting in the expectation. An action-independent b(x) is an [[advantage-baseline]]: its expected contribution vanishes because the policy probabilities sum to one. A baseline fitted using the same action can invalidate this argument; detach the reward and baseline from the policy-gradient computation.

For a response, the log probability is the sum of conditional token log probabilities. Assigning one final reward to those terms does not identify which reasoning step caused success. Delayed feedback and variable response lengths remain important.

The [[derivative]] is taken with respect to policy parameters; sampled actions and reward labels are held fixed.

The [[variance]] of sampled gradients determines the precision of a finite batch; a baseline changes that spread rather than certifying a reward.

## One example

A policy chooses A with probability p=.25 and B with probability .75, with deterministic rewards 3 and 1. Parameterize p by a scalar logit z. The derivatives of log probabilities are 1-p=.75 for A and -p=-.25 for B. With baseline 1.5, the expected estimator is .25×(3-1.5)×.75 + .75×(1-1.5)×(-.25)=.375. Directly differentiating J=3p+1(1-p)=1+2p gives 2p(1-p)=.375 as well. The baseline changes sampled variance, not this expectation.

## Boundaries and check

Fresh sampling matters. Reusing old-policy responses without the appropriate correction estimates a different update. Clipping, reward normalization and repeated optimization are additional choices, not part of the bare estimator. Compare held-out reward and actual correctness, gradient spread and generated-token cost. Does a non-differentiable verifier prevent REINFORCE? No: the differentiated object is the policy probability; reward quality is a separate requirement.
