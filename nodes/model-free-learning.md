---
id: model-free-learning
title: Model-Free Learning
summary: Model-free learning improves a decision policy or estimates its values from sampled rewards and transitions without first estimating the environment’s transition probabilities and reward model.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [markov-decision-process, bellman-equation]
sources: [https://incompleteideas.net/book/the-book-2nd.html, https://doi.org/10.1007/BF00992698]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Model-Free Learning

## Summary

**Model-free learning** uses experience—observed states, actions, rewards, and next states—to estimate which actions have high long-run return, without first learning the complete transition-and-reward model of a [[markov-decision-process]]. It can therefore learn from interaction when planning with an accurate model is unavailable, but it trades that directness for statistical uncertainty, exploration requirements, and sensitivity to the data it actually observes.

## Grounded explanation

A [[markov-decision-process]] describes an environment through a transition-and-reward distribution. A model-based method estimates that distribution and plans with it. A model-free method instead receives transition samples such as `(state, action, reward, next state)` and updates an estimate of a value or a policy directly. “Model-free” does not mean assumption-free: the state representation, reward definition, policy class, data-collection process, and discount still determine what is learned.

The [[bellman-equation]] supplies the one-step target. If an estimate says that the next state is valuable, then a transition that reaches it with reward `r` should raise the current action’s estimated value toward `r + γ × next-value`; if the observed reward or continuation is worse, the estimate should fall. Repeated sampled updates replace an expectation over all possible transitions with experience from individual transitions. With enough representative data and suitable update conditions, those samples can estimate the same long-run quantities that a known model would make available for planning.

Two common forms differ in what they learn. **Value-based** methods estimate the return associated with states or state-action pairs, then choose an action with a high estimated value. **Policy-based** methods adjust a parameterized action-selection rule using returns from its sampled trajectories. Both must distinguish learning from using: a policy that always selects its current favorite action may never observe an alternative that is better. Exploration deliberately collects informative alternatives, while evaluation measures the behavior of the policy intended for deployment.

### Worked instance

Consider a delivery robot whose state records its location and battery level. At an intersection, `short-cut` may save time but can encounter a delay; `main-road` is slower but predictable. The robot does not know either transition distribution. On each trip it records the chosen action, the time penalty as a negative reward, and the next state. After a short-cut trip, it updates that action’s estimated long-run return toward the immediate penalty plus the discounted estimate for the resulting location and battery state. It need not first construct a table of every possible delay probability. But if it stops trying the short-cut after one bad trip, its estimate can remain wrong; if its state omits battery level, it can mix outcomes that require different decisions. Holdout episodes, repeated random seeds, safety limits during exploration, and comparison with a fixed baseline test whether the learned behavior is genuinely better.

## Prerequisites

- [[markov-decision-process]]
- [[bellman-equation]]

## Sources

- Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed., Chapters 5–6: Monte Carlo, temporal-difference, and control methods that learn from sampled experience. Official author-hosted book page: https://incompleteideas.net/book/the-book-2nd.html
- Watkins and Dayan, “Q-learning” (1992): model-free action-value learning and its convergence conditions. Author-hosted PDF: https://doi.org/10.1007/BF00992698
