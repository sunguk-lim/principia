---
id: bellman-equation
title: Bellman Equation
summary: A Bellman equation expresses a state's value as its expected immediate reward plus the discounted value of the next state, turning a long-horizon decision problem into a one-step recursion.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [markov-decision-process, expectation]
sources: [https://incompleteideas.net/book/the-book-2nd.html]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Bellman Equation

## Summary

A **Bellman equation** decomposes the value of a state in a [[markov-decision-process]] into one reward now plus the discounted value expected after one transition. The recursion is valid because the Markov state makes the distribution of that next transition depend only on the current state and action.

## Grounded explanation

Fix a policy $\pi$, a rule that selects an action in each state of a [[markov-decision-process]]. Let $v_\pi(s)$ mean the expected discounted return when starting in state $s$ and then following $\pi$. The return is a reward now plus the remaining return, so its value obeys

$$v_\pi(s)=\mathbb{E}_\pi[R_{t+1}+\gamma v_\pi(S_{t+1})\mid S_t=s].$$

Here $R_{t+1}$ is the reward produced by the next transition, $S_{t+1}$ is the next state, and $\gamma$ is the MDP's discount factor. The equation does not assume that one sample transition reveals the value. Its [[expectation]] averages over the possible actions and environment outcomes prescribed by the policy and transition model.

The useful step is the decomposition. A long return might contain indefinitely many rewards, but after one transition the remainder is the same question again at a new state. Repeatedly applying the equation can evaluate a fixed policy. Choosing the action with the largest one-step expectation instead gives the optimality form:

$$v_*(s)=\max_a\mathbb{E}[R_{t+1}+\gamma v_*(S_{t+1})\mid S_t=s,A_t=a].$$

That maximum is a planning condition, not an instruction to greedily choose the largest immediate reward: each candidate action includes its next state's future value.

### Worked example

Consider a state `start` with two actions and discount $\gamma=0.9$. Action `safe` gives reward 2 and always moves to `terminal`, whose value is 0. Action `risky` gives reward 0, then moves to `good` with probability 0.5 and `bad` with probability 0.5. Suppose following the fixed policy from `good` has value 10 and from `bad` has value 0. The Bellman backup for `safe` is

$$2+0.9\times0=2.$$

For `risky`, first take the expected next value: $0.5\times10+0.5\times0=5$. Its backup is

$$0+0.9\times5=4.5.$$

Although `risky` pays less immediately, its value is larger because the future `good` outcome offsets the risk. If the probability of `good` fell to 0.1, the same calculation would be $0.9\times(0.1\times10)=0.9$, so `safe` would become preferable. This is exactly the trade-off the Bellman equation exposes: immediate rewards and uncertain downstream consequences appear in one comparable quantity.

Value iteration and policy evaluation differ in how they use this equation: the former repeatedly applies the maximum backup to seek an optimal policy, while the latter repeatedly applies the fixed policy's expectation. Both require a Markov model (or estimates of its transitions) and can be inaccurate when the state omits decision-relevant history.

## Prerequisites

- [[markov-decision-process]]

## Sources

- Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed., Chapter 4 — Bellman expectation and optimality equations, policy evaluation, and value iteration. Official author-hosted book page: https://incompleteideas.net/book/the-book-2nd.html
