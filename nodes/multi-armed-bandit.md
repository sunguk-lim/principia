---
id: multi-armed-bandit
title: Multi-Armed Bandit
summary: A multi-armed bandit repeatedly chooses among actions with uncertain rewards, trading immediate exploitation against exploration that improves later choices.
type: concept
tags: [algorithms]
prereqs: [probability-distribution, expectation, measurement]
sources: [https://arxiv.org/abs/1204.5721]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Multi-Armed Bandit

## Summary

A **multi-armed bandit** is a sequential decision problem: at each round, choose one action and observe only that action’s reward. The central trade-off is exploiting an action with high observed reward versus exploring uncertain actions.

## Grounded explanation

For $K$ actions with reward [[probability-distribution]]s, a policy selects $A_t$ and observes reward $R_t$. In a stationary stochastic setting, expected cumulative regret through round $T$ is

$$\mathcal R_T=T\mu^*-\mathbb E\!\left[\sum_{t=1}^T R_t\right],$$

where $\mu^*$ is the best action’s [[expectation]]. Regret measures opportunity loss relative to repeatedly choosing the best fixed action in hindsight or under the assumed model.

A greedy policy can lock onto a noisy early winner. Exploration collects information that may improve later rewards, but it intentionally assigns some traffic to actions currently believed worse. Algorithms differ in how they represent uncertainty and schedule this cost; stochastic, adversarial, contextual, and nonstationary bandits make different assumptions.

Delayed rewards do not make bandits impossible, but they reduce the information available for updates and complicate attribution. Batched or asynchronous policy updates can remove a synchronous state lookup from the serving path, while increasing policy staleness. Long delays, interference between users, noncompliance risk, or a need for a simple unbiased causal estimate can make a fixed randomized experiment preferable.

Before deployment, define the reward window and unit of randomization, simulate delay and drift, and shadow the policy. Measure regret proxies, reward-delay coverage, action probabilities, policy age, serving latency, guardrail outcomes, and estimator bias. Log propensities so off-policy analysis remains possible.

## Prerequisites

- [[probability-distribution]]
- [[expectation]]
- [[measurement]]

## Sources

- [Bubeck and Cesa-Bianchi, “Regret Analysis of Stochastic and Nonstochastic Multi-Armed Bandit Problems”](https://arxiv.org/abs/1204.5721): formalizes bandits through action payoff processes, exploration–exploitation, and regret under stochastic and adversarial settings.
