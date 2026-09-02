---
id: conditional-independence
title: Conditional Independence
summary: Conditional independence means that once a conditioning variable is known, learning one of two other variables does not change the conditional distribution of the other.
type: concept
tags: [math/probability]
prereqs: [conditional-probability]
sources: [https://www.statlect.com/fundamentals-of-probability/conditional-independence]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Conditional Independence

## Summary

Two uncertain quantities are **conditionally independent given** a third when, inside every case selected by the third quantity, observing either one supplies no further information about the other. Conditioning can remove an apparent association by fixing their shared explanation, or create an association that was absent before conditioning.

## Grounded explanation

Let $X$, $Y$, and $Z$ be uncertain quantities. Write $X\perp Y\mid Z$ when, for every value $z$ with positive probability,

$$
P(X=x,Y=y\mid Z=z)=P(X=x\mid Z=z)P(Y=y\mid Z=z).
$$

This factorization uses [[conditional-probability]]. An equivalent form, whenever its terms are defined, is

$$
P(X=x\mid Y=y,Z=z)=P(X=x\mid Z=z).
$$

The second equation states the operational meaning: after $Z$ is known, learning $Y$ does not update the probability of $X$. Conditional independence is stronger than zero correlation and is not the same as ordinary independence, because the claim is explicitly restricted to each conditioned subpopulation.

### Worked example

A fair coin $Z$ chooses one of two bags. Bag $0$ contains only red balls and bag $1$ only blue balls. After choosing a bag, draw two balls with replacement; let $X$ and $Y$ record whether the first and second balls are blue.

Before the bag is revealed, $P(X=1)=P(Y=1)=1/2$, but $P(X=1,Y=1)=1/2$, not $(1/2)(1/2)=1/4$: the draws are associated because both expose the hidden bag. Given $Z=1$, however, $P(X=1,Y=1\mid Z=1)=1$ and the product is $1\cdot1=1$. Given $Z=0$, both sides are $0$. Thus $X\perp Y\mid Z$ even though $X$ and $Y$ are not independent without conditioning.

The conditioning set matters. Adding or removing a variable can change the truth of the factorization; conditional independence is therefore always a statement about a particular triple of variable sets, not a permanent relation between two names.

## Prerequisites

- [[conditional-probability]]

## Sources

- StatLect, “Conditional independence” — factorization definition, equivalent conditional form, and distinction from unconditional independence.
