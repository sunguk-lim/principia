# Training Signal Selection

## Meaning

Training methods require different feedback. Demonstrations, pairwise preferences, executable scores, and stateful environments are not interchangeable data.

## Mechanism

Begin with a prompt baseline, then test supervised tuning when trusted input-output pairs exist. Preference fitting can use ranked outputs. Online policy optimization needs rollout and scoring contracts, and a scorer may be exploitable.

## Example

A team with 2,000 labeled examples and no reliable task scorer can evaluate a supervised adapter now while building a separate reward-validation study. A leaderboard name does not supply missing feedback.

## Boundaries and trade-offs

Supervised examples tell a learner what output to imitate; preference pairs say which of two outputs is better; a reward function scores sampled behavior. Those signals have different coverage and can contradict one another. In sequential tasks, a single final score does not describe legal intermediate actions or recovery after a failure. This is why “we have a scorer” is the start of a reward-design study, not proof that online policy training is ready.

## Validation

Use a held-out task set that a labeler or reward designer did not tune against. Compare the prompt baseline with a supervised model before spending the budget on online rollouts. For preference learning, inspect disagreements and minority-case quality. For reward optimization, deliberately probe loopholes and compare reward with real task success. Include inference-time behavior, because a training gain that raises latency or invalid actions may fail the deployment objective.

## Understanding check

Why does an automatic score not, by itself, prove that online reinforcement learning is the best next step?
