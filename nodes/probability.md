---
id: probability
title: Probability
summary: Probability is a number between 0 and 1 attached to an event — a yes/no question about the result of some uncertain situation, like "the die shows an even number." It measures how…
type: concept
tags: [math/probability]
prereqs: [arithmetic]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Probability

## Summary

Probability is a number between 0 and 1 attached to an *event* — a yes/no question about the result of some uncertain situation, like "the die shows an even number." It measures how strongly we expect that event to happen: 0 means never, 1 means always, and a value in between means sometimes. When every basic result is equally likely, the probability is just a counting ratio — the number of results that make the event true, divided by the total number of results — so it rests entirely on [[arithmetic]] (counting, then dividing). The frequentist reading makes this concrete: the probability is the long-run fraction of trials in which the event happens. Two further ideas, *conditional probability* (how a probability changes once you learn that some other event happened) and *independence* (two events that carry no information about each other), are built from the same ratios and are the workhorses for everything else.

## Grounded explanation

**The pieces, defined.** Start with one uncertain situation — say, rolling a die once. An **outcome** is one complete, indivisible result the situation can produce: for one die roll the outcomes are 1, 2, 3, 4, 5, 6. The **sample space** is the set of *all* possible outcomes — here `{1, 2, 3, 4, 5, 6}`, six outcomes in total. An **event** is any collection of outcomes, i.e. a yes/no question answered "yes" exactly when the actual outcome is one of the collection. "The roll is even" is the event `{2, 4, 6}`; "the roll is 2" is the single-outcome event `{2}`. We write `P(A)` for the probability of event `A` — a number we will assign and then compute.

**What the number must obey (the axioms, stated plainly).** Probability is not any arbitrary labeling of events with numbers; it must satisfy three rules so that the numbers behave like proportions of a whole:

1. **Non-negativity.** Every outcome gets a number that is at least 0. Nothing can happen a "negative amount."
2. **Total is 1.** Add up the numbers over *all* outcomes in the sample space and you get exactly 1. The whole of "something will happen" is the unit we are dividing up; 1 stands for certainty.
3. **Disjoint events add.** If two events share no outcome (they cannot both be true — they are *disjoint*), the probability that one *or* the other happens is the sum of their two probabilities.

From these three, the probability of any event is just the sum of the numbers on the outcomes it contains. These are exactly the rules of cutting a whole (1) into non-negative pieces — pure [[arithmetic]] of addition and division.

**Why a counting ratio.** Suppose we have a reason to call the outcomes *equally likely* — a fair die, a fair coin: no outcome is favored. Then by rule 1 they all carry the same number, say `p`, and by rule 2 those `p`'s add to 1. With `n` outcomes that means `n × p = 1`, so `p = 1/n` (divide both sides by `n` — [[arithmetic]]). Each outcome of a fair six-sided die therefore has probability `1/6`. By rule 3, an event made of `k` of those outcomes has probability `k × (1/n) = k/n`. So for equally-likely outcomes,

> probability of an event = (number of outcomes making it true) ÷ (total number of outcomes).

This is why probability "is" a counting ratio in the fair case: it is forced by the three axioms once equal likelihood is granted.

**The frequentist reading (why this matches reality).** Imagine repeating the situation many times — roll the die `N` times. Count how many of those rolls land in event `A`; call that count `m`. The *fraction* `m/N` is the proportion of trials where `A` happened. As `N` grows large, this observed proportion settles down toward the number `P(A)`. So a probability is the long-run fraction of trials in which the event occurs — again a count divided by a count, grounded in [[arithmetic]]. The axioms are exactly the properties any such fraction must have: it can't be negative (`m ≥ 0`), the fraction over the whole sample space is `N/N = 1`, and counts of disjoint events add (`m_A + m_B` rolls land in "A or B" when no roll lands in both).

**Conditional probability — updating once you learn something.** Often we get partial news: someone tells us the die came up even, and now we ask about a finer event. The **conditional probability of `A` given `B`**, written `P(A | B)`, is the probability of `A` once we *restrict attention to the trials where `B` happened*. The trick is renormalization: among the long run of trials, ignore every trial where `B` failed, and ask what fraction of the *remaining* (B-)trials also have `A`. In count terms that fraction is (trials with both `A` and `B`) ÷ (trials with `B`). Dividing top and bottom by the total number of trials `N` turns each count into a probability:

> `P(A | B) = P(A and B) ÷ P(B)`,

where "A and B" (written `A ∩ B`) is the event of outcomes in *both* `A` and `B`. We need `P(B) > 0` — you cannot condition on something that never happens (you'd be dividing by 0, which [[arithmetic]] forbids). The effect is to make `B` the new "whole": the probabilities of the outcomes inside `B` are scaled up by the same factor `1/P(B)` so they again sum to 1.

**Independence — when news tells you nothing.** Two events `A` and `B` are **independent** when learning that `B` happened leaves the probability of `A` unchanged: `P(A | B) = P(A)`. Substituting the definition above, `P(A) = P(A ∩ B) ÷ P(B)`, and multiplying both sides by `P(B)` gives the clean, symmetric test:

> `P(A ∩ B) = P(A) × P(B)`.

So for independent events the probability that both happen is just the *product* of their separate probabilities. This is the rule we lean on whenever a system is built from parts that don't influence each other (two separate coins, repeated fair trials).

**Worked instance — one fair die.** Sample space `{1, 2, 3, 4, 5, 6}`, `n = 6` equally-likely outcomes, each with probability `1/6`.

- Let `E` = "even" = `{2, 4, 6}`. It contains `k = 3` outcomes, so `P(E) = 3/6 = 1/2`. (Count 3, divide by 6.)
- Let `T` = "the roll is 2" = `{2}`, so `P(T) = 1/6`.
- Now the conditional `P(T | E)` — the chance the roll is a 2 *given* we already know it's even. The event "T and E" is `{2} ∩ {2,4,6} = {2}`, so `P(T ∩ E) = 1/6`. Then `P(T | E) = P(T ∩ E) ÷ P(E) = (1/6) ÷ (1/2) = (1/6) × (2/1) = 2/6 = 1/3`. Sanity check by direct counting: among the even outcomes `{2, 4, 6}` (now the whole, 3 of them), exactly 1 is a 2, and `1/3` matches. Knowing the roll is even *raised* the chance of a 2 from `1/6` to `1/3` — that is conditioning doing real work, not a degenerate no-op.

**Worked instance — two fair coins (independence).** Toss two coins; outcomes are the four pairs `{HH, HT, TH, TT}`, equally likely at `1/4` each. Let `A` = "first coin is heads" = `{HH, HT}` and `B` = "second coin is heads" = `{HH, TH}`. Counting: `P(A) = 2/4 = 1/2` and `P(B) = 2/4 = 1/2`. The event `A ∩ B` = "both heads" = `{HH}`, so `P(A ∩ B) = 1/4`. Test independence: `P(A) × P(B) = (1/2) × (1/2) = 1/4`, which equals `P(A ∩ B)`. The two coins are independent — knowing the first landed heads tells you nothing about the second, and indeed `P(B | A) = P(A ∩ B) ÷ P(A) = (1/4) ÷ (1/2) = 1/2 = P(B)`. Every number here came from counting outcomes and one division.

## Prerequisites

- [[arithmetic]]

## Sources

_none_
