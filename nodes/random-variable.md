---
id: random-variable
title: Random Variable
summary: A random variable is a rule that attaches a number to each possible outcome of a random experiment.
type: concept
tags: [math/probability]
prereqs: [probability]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Random Variable

## Summary

A random variable is a rule that attaches a **number** to each possible outcome of a random experiment. A [[probability]] model on its own only tells us how likely each outcome is, but the outcomes themselves may be things we cannot add, average, or compare numerically (heads/tails, a card, a winner's name). A random variable fixes that: it is a *function* from outcomes to numbers, so the question "how likely is outcome ω?" becomes "how likely is it that the number equals (or lies near) some value x?". Because each number is just a relabelling of outcomes, it automatically carries a probability — the total [[probability]] of all the outcomes that the rule sends to that number. This repackaging of a probability model as a numeric quantity-with-probabilities is the object that every later notion (distributions, averages, estimators) is built on.

## Grounded explanation

**Starting point (from [[probability]]).** Assume we already have a random experiment with a set of possible outcomes — call the set $S$ (the "sample space") — and a [[probability]] that assigns to each event (each subset of $S$) a number in $[0,1]$, where the probability of all of $S$ is $1$ and the probability of a collection of disjoint outcomes is the sum of their individual probabilities. We write $P(\text{event})$ for this number. That is the entire inheritance from [[probability]]; we will not re-derive it.

**The gap a random variable fills.** The probability model talks about *outcomes and events*, which need not be numbers. If I toss a coin, the outcomes are "heads" and "tails" — there is nothing to add or average. Yet we constantly want to do arithmetic on random results: "how many heads in ten tosses?", "what total did the dice show?", "how much did I win?". To ask such questions we first need a *number* pinned to every outcome. That pinning is exactly what a random variable is.

**Definition.** A **random variable** is a function $X$ that takes each outcome and returns a real number:
$$ X : S \to \mathbb{R}, \qquad \omega \mapsto X(\omega), $$
where $\omega$ (the Greek letter omega) denotes one outcome in the sample space $S$, and $X(\omega)$ is the number the rule assigns to it. Note three things. (1) $X$ is **not** random in itself — it is a fixed, deterministic rule; the randomness lives in *which* outcome $\omega$ occurs. (2) Many different outcomes may be sent to the *same* number; $X$ need not be one-to-one. (3) The capital letter $X$ names the rule; a lowercase $x$ names a particular value it might take.

**Why each value carries a probability — the key step.** Once $X$ is fixed, the statement "$X = x$" is just shorthand for an *event*: the set of all outcomes that $X$ maps to $x$. Write that set as
$$ \{\, \omega \in S : X(\omega) = x \,\}. $$
Being a subset of $S$, it is something the underlying [[probability]] already knows how to score. So we *define*
$$ P(X = x) \;=\; P\big(\{\, \omega \in S : X(\omega) = x \,\}\big), $$
the total [[probability]] of all outcomes the rule sends to $x$. This is the one "magic-looking" move, and it is justified entirely by the additivity we inherited from [[probability]]: the outcomes sending to $x$ are distinct outcomes, so the probability of the whole bundle is the sum of their individual probabilities — no new assumption is needed. The number $x$ thus *inherits* a probability from the outcomes hiding behind it. Doing this for every value gives us a numeric quantity with a probability attached to each value: that bundle is what makes $X$ useful.

**Two kinds, by what the values look like.** If the set of values $X$ can take is *countable* — a finite or step-by-step list like $0,1,2,\dots$ — we call $X$ **discrete**, and $P(X=x)$ is meaningful for each individual value. If instead $X$ can take any value in a continuous range (a length, a waiting time), then any *single* exact value typically has probability $0$, and the probability lives in *ranges*: we ask for $P(a \le X \le b)$, the [[probability]] of the event $\{\omega : a \le X(\omega) \le b\}$. The same definition is at work — an event of outcomes, scored by the underlying [[probability]] — only the grain (a point vs. an interval) differs. The worked example below is discrete.

**Worked instance: $X$ = the sum of two fair dice.**

*The model (from [[probability]]).* Roll two fair, distinguishable dice (say a red one and a blue one). An outcome is an ordered pair $(r, b)$ with $r$ the red die and $b$ the blue die, each from $1$ to $6$. The sample space therefore has $6 \times 6 = 36$ outcomes, e.g. $(1,1), (1,2), \dots, (6,6)$. "Fair" means every one of the $36$ outcomes has the same [[probability]], $\tfrac{1}{36}$ (they are equally likely and must sum to $1$).

*The random variable.* Define the rule
$$ X(r, b) = r + b. $$
This is a genuine function from the $36$ outcomes to numbers — for example $X(3,4) = 7$ and $X(1,1) = 2$. Several different outcomes land on the same number: $(3,4)$, $(4,3)$, $(2,5)$, $(5,2)$, $(1,6)$, $(6,1)$ all map to $7$. The possible values of $X$ run over the integers $2, 3, 4, \dots, 12$ (smallest sum $1+1=2$, largest $6+6=12$), so $X$ is discrete with $11$ possible values.

*Deriving the probabilities by counting.* By the definition above, $P(X=x)$ is the [[probability]] of the event consisting of all outcomes whose dice sum to $x$. Since each outcome has probability $\tfrac{1}{36}$, that probability is just (number of such outcomes) $\times \tfrac{1}{36}$.

- $X = 2$: only $(1,1)$ sums to $2$ — $1$ outcome — so $P(X=2) = \tfrac{1}{36}$.
- $X = 7$: the six outcomes $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ sum to $7$ — so $P(X=7) = \tfrac{6}{36} = \tfrac{1}{6}$.
- $X = 12$: only $(6,6)$ — $1$ outcome — so $P(X=12) = \tfrac{1}{36}$.
- A range, to show the continuous-style question on a discrete variable: $P(2 \le X \le 3)$ collects the outcomes for $X=2$ ($(1,1)$) and $X=3$ ($(1,2),(2,1)$), i.e. $3$ outcomes, giving $\tfrac{3}{36} = \tfrac{1}{12}$.

Notice the asymmetry the example reveals: $7$ is six times as likely as $2$, not because any outcome is favored — every one of the $36$ is equally likely — but because *more outcomes are mapped to $7$*. That is precisely the effect of viewing the model through the lens of $X$: the numeric value reshuffles and bundles the flat outcome-probabilities into an uneven profile over $2,\dots,12$. As a sanity check, summing the counts over all values $2$ through $12$ gives $1+2+3+4+5+6+5+4+3+2+1 = 36$, so the probabilities sum to $\tfrac{36}{36} = 1$, exactly as the underlying [[probability]] requires.

**What we have, and what we have not, built.** We now have $X$: a fixed numeric rule on outcomes, together with a probability attached to each value (or range) of that rule, inherited cleanly from the [[probability]] on outcomes. We have deliberately *not* packaged the full list of value-probabilities into a single "distribution" object, nor computed any average ("expected value") of $X$ — those are separate concepts that take this node's $X$ as their starting material. The contribution of the random variable itself is the bridge: it turns a probability model over arbitrary outcomes into a numeric quantity we can later do arithmetic and inference on.

## Prerequisites

- [[probability]]

## Sources

_none_
