# Group Relative Policy Optimization

## Meaning

GRPO compares several outputs from the same prompt and uses their relative rewards to update a policy. It avoids training a separate value model as a baseline.

## Mechanism

Sample a group of candidate completions, score each, subtract the group's mean, and normalize by its reward spread. A candidate that beats its peers receives positive advantage. In [[reinforcement-learning-from-verifiable-rewards]], an executable checker can supply those scores. The [[advantage-baseline]] explains why a completion is reinforced relative to other samples for that prompt.

## One example

For one arithmetic prompt, sample four answers. If two are correct and two are wrong, the group supplies a learning contrast. If all four get the same reward, it supplies little relative signal; more sampling or different tasks may be needed.

## Check your understanding

**Question:** What does GRPO save, and what does it still spend? **Answer:** It avoids a separate value model but still spends compute on multiple rollouts and remains dependent on reward quality.
