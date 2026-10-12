# Reinforcement Learning from Verifiable Rewards

## Meaning

RLVR trains a model from its sampled outputs and an executable outcome check. The training set supplies tasks and checkable answers or tests rather than an ideal reasoning trace for every sample.

## Mechanism

A model receives a math question, produces several solutions, and a [[verifiable-reward-design]] checks each final answer. A [[model-free-learning]] update increases the probability of rewarded behavior. The checker can still be exploited: a correct final number does not establish a sound reasoning path.

## One example

Train on arithmetic problems with a fixed answer parser. Before training, hold out problems and alternate wordings. After training, compare exact-match accuracy, invalid formats, and inference cost with the base model under the same sampling budget.

## Check your understanding

**Question:** Is RLVR the same as GRPO? **Answer:** No. RLVR names the verifiable source of reward; GRPO is one possible optimization method that can use it.
