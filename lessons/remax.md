# ReMax

## Meaning

ReMax is a critic-free policy-gradient method for language-model alignment. For each prompt, it compares a sampled response's reward with the reward of a separate greedy response from the policy. The greedy answer is a reference outcome, not an automatically correct training label.

## Mechanism

Fix the current policy for data collection. Generate a response y by stochastic sampling, and generate g(x) by greedily choosing a token at each step. Score both. With R the reward function, use A=R(x,y)-R(x,g(x)) in the [[reinforce-policy-gradient]] term for y. Treat the greedy reward as a detached baseline. Conditional on the prompt and frozen policy, this baseline is not a function of the stochastic action y, so it can preserve the expected policy-gradient estimator under the required assumptions.

The greedy generation replaces value-model learning with a generation and scoring cost. It can be deterministic for a fixed implementation, but ties, numerical variation and decoding settings must be specified. The original ReMax alignment formulation also keeps a reference-model regularization component; critic-free does not mean reference-free.

## One example

For one prompt, the greedy response scores .4. Sampled responses score .9 and .1, giving centered weights .5 and -.3. The sampled better-than-greedy response is encouraged, and the worse one discouraged. If a second prompt's greedy response scores .95, a sampled score .9 instead receives -.05. The baseline changes which reward is surprising for each prompt, not the verifier's definition of correctness.

## Boundaries and check

A strong greedy baseline can reduce variance; a poor or noisy one may not. Greedy decoding does not find the globally most likely sequence or the best-reward answer in general. A baseline depending on policy parameters must not be differentiated as though it were an extra policy reward term. Reusing outputs after the policy changes creates a separate sampling mismatch.

Compare a no-baseline estimator, peer baseline and learned critic at matched generated-token and training budgets. Include the extra greedy pass, scorer latency, memory and any reference model in cost accounting. Does an author-reported reduction in training memory establish the same reduction for every hardware and optimizer configuration? No: model placement, optimizer state and batching determine the complete resource budget.
