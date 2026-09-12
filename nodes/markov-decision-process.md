---
id: markov-decision-process
title: Markov Decision Process
summary: A Markov decision process models sequential choices by specifying states, actions, transition probabilities, rewards, and a discount factor whose next-step distribution depends only on the current state and action.
type: concept
tags: [ml/reinforcement-learning]
prereqs: [probability, set]
sources: [https://incompleteideas.net/book/the-book-2nd.html]
status: explained
created: 2026-09-12
updated: 2026-09-12
---

# Markov Decision Process

## Summary

A **Markov decision process** (MDP) is a model for a decision-maker that repeatedly observes a state, chooses an action, receives a reward, and reaches a next state. Its Markov condition makes the current state sufficient for predicting the next step: given the current state and action, earlier history does not change the next-state and reward distribution.

## Grounded explanation

An MDP packages a sequential decision problem as the tuple $(S, A, P, R, \gamma)$. $S$ is a [[set]] of states and $A$ is a set of actions. At time $t$, the agent observes state $S_t$, selects $A_t$, then the environment draws a next state $S_{t+1}$ and reward $R_{t+1}$. The transition model $P(s',r\mid s,a)$ is a [[probability]] distribution over the possible next-state and reward pairs after state $s$ and action $a$. The discount factor $\gamma$ is between 0 and 1 and weights rewards farther in the future.

The essential assumption is not that a state is a complete physical description. It is that the state representation retains every part of the past that matters for the distribution of the next step. Formally,

$$P(S_{t+1}=s', R_{t+1}=r \mid S_t=s, A_t=a, \text{earlier history}) = P(s',r\mid s,a).$$

This is what makes planning tractable: a policy can choose from the current state without carrying an unbounded transcript. If a representation omits relevant history, it is not Markov for that task; adding a sufficient variable, such as whether a door is already unlocked, can restore the property.

### Worked example

A robot has states $S=\{\text{dry},\text{wet}\}$ and actions $A=\{\text{wait},\text{walk}\}$. From `dry`, `walk` reaches `wet` with probability 0.8 and yields reward 3, while it remains `dry` with probability 0.2 and yields reward 3. From `wet`, `walk` reaches `dry` with probability 0.5 and reward 1, or remains `wet` with probability 0.5 and reward 1. The next outcome depends on the robot's present surface condition and choice, not on how many earlier walks produced that condition. With $\gamma=0.9$, a reward of 10 one step from now contributes $0.9\times10=9$ to the current return, whereas the same reward two steps away contributes $0.9^2\times10=8.1$. The discount makes a continuing task's total return finite under bounded rewards and expresses a preference for earlier reward.

An MDP is a modeling assumption, not a claim that every real environment is fully observed. A camera image or a short chat context can fail to contain the history needed to predict consequences. In that case, a policy based only on that observation can still be useful, but the MDP guarantees do not automatically apply.

## Prerequisites

- [[probability]]
- [[set]]

## Sources

- Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed., Chapters 3–4 — the MDP tuple, Markov property, returns, and discounting. Official author-hosted book page: https://incompleteideas.net/book/the-book-2nd.html
