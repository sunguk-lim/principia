---
id: test-time-compute
title: Test-Time Compute
summary: Test-time compute is the idea that a model's accuracy can be raised by spending more computation at inference time — when it is actually answering a question — as a lever distinct…
type: concept
tags: [ml/llm/reasoning]
prereqs: [chain-of-thought]
sources:
  - "OpenAI 2024, Learning to Reason with LLMs (o1 system card / blog)"
  - "DeepSeek-AI 2025, DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning (arXiv:2501.12948)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Test-Time Compute

## Summary

**Test-time compute** is the idea that a model's accuracy can be raised by spending
**more computation at inference time** — when it is actually answering a question —
as a lever distinct from spending more during training. *Inference time* (also
called *test time*) is the moment the trained model is run on a new input;
*training time* is the earlier, one-off process that produced the model's fixed
weights. The training cost is paid once; the test-time cost is paid afresh on every
single query, and — this is the point — we can choose *how much* to pay per query.
The primary knob, grounded in [[chain-of-thought]], is simply **letting the model
generate more reasoning tokens before it answers**. Because each generated token is
another forward pass through the network, more tokens means literally more
sequential computation applied to that one problem. Harder problems are given more
of it; empirically, accuracy climbs smoothly as inference compute grows — a scaling
axis separate from making the model bigger.

## Grounded explanation

**The two budgets.** A deployed language model has its weights frozen by training.
There are then two separate places one can pour more computation to get better
answers. The first is **training-time compute**: a bigger model, or more training,
bakes more capability into those frozen weights — but it is paid once and fixed
thereafter. The second is **test-time compute**: at the moment of answering, we let
the model do *more work on this specific question*. The concept of test-time compute
is the recognition that this second budget is a real, tunable scaling axis on its
own — that you can hold the weights constant and still buy accuracy, per query, by
spending more inference computation.

**Why there is anything to spend — the ceiling we are lifting.** From
[[chain-of-thought]] we have the core fact: a single forward pass (one run of the
network from input tokens to one output prediction) has a **fixed depth** — a fixed
number of layers stacked one on the next. That depth is a hard ceiling on how many
sequential, dependent operations can chain together inside one pass. If we force the
model to answer immediately, the entire solution must be computed within that one
capped pass. A hard, multi-step problem may simply need more sequential steps than
the depth allows, and the model misfires. So the *amount of computation* a single
answer-pass can apply to a problem is bounded — and that bound is exactly what
test-time compute is invented to escape.

**The primary lever: generate more reasoning tokens.** Here is where
[[chain-of-thought]] supplies the mechanism. When the model writes intermediate
reasoning as tokens before answering, each generated token is *its own forward
pass*, and — because attention lets later passes read the tokens earlier passes
wrote — the model **unrolls a longer computation across many passes**, using the
written text as the memory that carries partial results forward. The decisive
reframing for test-time compute is this: **a fixed-depth network producing $N$
reasoning tokens is performing a variable-length computation whose length we
control by choosing $N$.** Tell the model to think briefly and it spends few passes;
tell it to think at length ("long CoT," the "thinking" regime) and it spends many.
Number of generated tokens *is* the quantity of test-time compute. So the knob is
concrete and continuous: we dial up compute by allowing — or training the model to
take — a longer chain of thought.

**Why more compute helps, and why it scales.** Two effects compound. First,
**ceiling-lifting**: a problem needing more dependent steps than one pass can hold
becomes solvable once those steps are spread across many passes, each depositing a
result the next attends to. Second, **matching effort to difficulty**: an easy
question is answered with a short chain (little compute), a hard one with a long
chain (much compute), so the budget flows to where it is needed. The striking
empirical regularity — reported for the o1 and R1 "reasoning" models — is that
accuracy on hard benchmarks rises *smoothly with the logarithm of inference
compute*: each doubling of reasoning tokens buys a roughly constant accuracy
increment, over orders of magnitude. That is the signature of a genuine scaling
axis, and it is orthogonal to model size — the *same* frozen weights get better the
more they are allowed to think.

**Other levers (same currency, different shape).** Generating one long chain is not
the only way to spend test-time compute; it is just the one that follows directly
from [[chain-of-thought]]. A second way is to sample **several independent chains**
for the same question — each a fresh run of the reasoning process — and then
**aggregate** their answers, e.g. by taking the majority vote across them. This
spends compute "in parallel" (more chains) rather than "in series" (a longer single
chain), and it works because independent chains tend to make *different* mistakes
while agreeing on the correct answer, so the vote concentrates on the right one. A
third way is to generate many candidate solutions and have a separate scoring
process pick the best; the machinery of that search is left to its own node. All
three are the same idea — buy accuracy with inference computation — and all measure
their spend in tokens generated.

**Worked instance.** Take a problem that needs several dependent steps, so a single
capped pass is genuinely strained:

> *A store sells pens at \$3 each. Buy 4 or more and every pen is \$2. Sara buys 7
> pens and pays with a \$20 bill. How much change does she get?*

The correct answer is \$6, reached only through a chain of dependent decisions:
notice $7 \ge 4$, so the discounted price \$2 applies; multiply $7 \times 2 = 14$;
then subtract $20 - 14 = 6$. Each step needs the previous one's result.

*Low test-time compute — answer directly.* The context is just the question and the
next token must be the dollar figure:

```
... How much change does she get?  ->  [next token = answer]
```

Spend here: roughly **1 token** generated for the answer. That single forward pass
must, with no scratchpad, simultaneously decide the discount applies, multiply, and
subtract. A common failure is to miss the "4 or more" rule and use the \$3 price:
$7 \times 3 = 21$, which already exceeds \$20 — the model blurts an inconsistent
answer like "\$1" or "\$21". **Wrong**, because the dependent chain exceeded what one
pass could hold.

*Higher test-time compute — one long chain.* Now the model is allowed to reason:

```
7 pens, and 7 ≥ 4, so the price is $2 each.   <- step 1
7 × $2 = $14.                                  <- step 2 (attends to step 1's $2)
Change = $20 − $14 = $6.                        <- step 3 (attends to the $14)
Answer: $6                                       <- final
```

Spend here: about **30 tokens**. Each arithmetic step is its own pass that attends
back to the value the prior pass wrote, so no single pass carries the whole chain.
**Correct: \$6.** Going from ~1 token to ~30 tokens — roughly a 30× increase in
test-time compute — flipped the answer from wrong to right, on the *same* weights.

*Higher still — parallel chains plus majority vote.* Instead of trusting one chain,
sample $k = 5$ independent chains for the same question and vote. Suppose, with
independent sampling, the chains land:

| Chain | Reasoning sketch | Answer |
|-------|------------------|--------|
| 1 | $7\ge4 \Rightarrow \$2$; $7\times2=14$; $20-14$ | **\$6** |
| 2 | missed discount; $7\times3=21$; $20-21$ | \$-1 (junk) |
| 3 | $7\ge4 \Rightarrow \$2$; $7\times2=14$; $20-14$ | **\$6** |
| 4 | discount ok but $7\times2=15$ slip; $20-15$ | \$5 |
| 5 | $7\ge4 \Rightarrow \$2$; $7\times2=14$; $20-14$ | **\$6** |

Tally the final answers: \$6 appears **3** times, while the two error answers
(\$-1, \$5) appear once each and *disagree with each other*. Majority vote returns
**\$6**. Note the dynamics this exposes: the two wrong chains failed in *different*
ways, so they could not gang up, whereas the three correct chains all converged on
the same value — that is precisely why aggregation rescues the answer. Had we read
off only chain 4 (a 2-wrong-of-5 region of bad luck for a single sample), we would
have gotten \$5; the vote over five chains absorbs that. Spend here: about $5 \times
30 = 150$ tokens — five times the single-chain compute — trading still more
inference computation for still more reliability.

Across the three regimes the lesson is one quantity: **\~1 token (wrong) →
\~30 tokens (right) → \~150 tokens (right and robust)**. Compute spent at test time,
measured in generated tokens, is the dial; accuracy is what it buys. This is exactly
the regime the o1 and R1 reasoning models operate in — trained to emit long internal
chains of thought, and observed to get more accurate the more inference tokens they
are permitted to spend.

## Prerequisites

- [[chain-of-thought]]

## Sources

- OpenAI (2024). *Learning to Reason with LLMs* (o1 announcement / system card).
- DeepSeek-AI (2025). *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
  Reinforcement Learning.* arXiv:2501.12948.
