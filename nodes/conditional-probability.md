---
id: conditional-probability
title: Conditional Probability
summary: Conditional probability restricts the possible outcomes to those where the conditioning event occurred, then measures the target event inside that reduced world.
type: concept
tags: [math/probability]
prereqs: [probability]
sources: [https://www.stat.berkeley.edu/~stark/Teach/S240/Notes/ch4.pdf]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Conditional Probability

## Summary

**Conditional probability** asks how likely event $A$ is after learning that event $B$ occurred. It uses [[probability]] inside the reduced world selected by $B$ rather than across all outcomes.

## Grounded explanation

Let $A$ and $B$ be events and suppose $P(B)>0$. The definition is

$$P(A\mid B)=\frac{P(A\cap B)}{P(B)}.$$

Here $A\cap B$ means that both events occur. Dividing by $P(B)$ renormalizes the part of the original world that remains possible after observing $B$, so the conditional probabilities inside $B$ again total $1$.

### Worked example

Out of 100 recorded days, 40 were rainy. On 30 of those rainy days the road was wet. Let $B$ be “rain” and $A$ be “wet road.” Then $P(B)=40/100$ and $P(A\cap B)=30/100$, so

$$P(A\mid B)=\frac{30/100}{40/100}=\frac{30}{40}=0.75.$$

The denominator is 40 rainy days, not all 100 days: once rain is known, only those 40 days form the relevant world. Reversing the condition asks a different question; $P(B\mid A)$ would use wet days as its denominator.

Conditional probability is the building block for statements such as “the event rate among predictions with score 0.8” and “the distribution of a label given an input.”

## Prerequisites

- [[probability]]

## Sources

- Philip B. Stark, *Statistics 240 Notes*, conditional probability section.
