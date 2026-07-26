---
id: chain-of-thought
title: Chain-of-Thought
summary: Chain-of-thought (CoT) is the practice of having a language model write out its intermediate reasoning steps as tokens before it commits to a final answer, rather than emitting…
type: concept
tags: [ml/llm/reasoning]
prereqs: [transformer-attention]
sources:
  - "Wei et al. 2022, Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (arXiv:2201.11903)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Chain-of-Thought

## Summary

**Chain-of-thought (CoT)** is the practice of having a language model write out its
**intermediate reasoning steps as tokens** before it commits to a final answer,
rather than emitting the answer directly. A *token* here is one discrete unit of
text the model reads and produces (a word or word-piece). The steps are not just
for the human reader: because the model generates one token at a time and each new
token uses [[transformer-attention]] to look back over *everything already
written* — including its own earlier steps — the written reasoning becomes a
**scratchpad the model attends to** when producing the answer. So CoT lets the
model condition its answer on its own step-by-step decomposition, and it spends
more computation (more generation steps) on a hard problem instead of cramming the
whole solution into a single shot.

## Grounded explanation

**What the model does, mechanically.** A language model generates text
**autoregressively**: it produces one token at a time, and to produce the next
token it runs a forward pass over the sequence built so far. (A *forward pass* is
one run of the network from input tokens to an output prediction.) The engine of
that pass is [[transformer-attention]]: every token forms a *query* and compares it
(via the query–key match described in [[transformer-attention]]) against the *keys*
of all earlier tokens, then takes a weighted average of their *values*. The
practical consequence is the one fact CoT is built on: **when the model picks token
number $t+1$, it can attend back over tokens $1 \dots t$ — and crucially, tokens
$1 \dots t$ include the tokens the model itself just generated.** The model's own
output is fed back in as input for the next step. Its prior words are part of its
own context.

**Why answering directly is hard.** Suppose we ask for the answer immediately. The
model must compute the entire result inside the forward pass that produces that one
answer token. But a single forward pass has a **fixed depth** — a fixed number of
attention-and-transform layers stacked one on top of the next. That depth is a hard
ceiling on how many sequential "thinking" operations can chain together before the
answer must come out. A multi-step problem (decompose, compute a sub-result, feed
it into the next computation) may need more sequential steps than the fixed depth
provides. The model is forced to guess in one leap.

**Why writing steps fixes it — the key insight.** Each generated token is *another*
forward pass. If the model first writes an intermediate result as tokens, that
result is now sitting in the context, and the *next* forward pass can attend to it
(again via [[transformer-attention]]) as a settled input rather than recomputing it.
So the model is no longer limited to the fixed depth of one pass: it **unrolls a
longer computation across many passes**, using the text it has written as the
memory that carries partial results from one pass to the next. Two things happen at
once:

1. **Conditioning on its own decomposition.** Because attention lets the answer
   token look directly at the written steps, the final answer is computed *from*
   those steps. The decomposition is not decoration; it is literally the input the
   answer attends to.
2. **More compute on demand.** Each extra step of reasoning is an extra forward
   pass. A hard problem gets more passes; an easy one gets fewer. CoT buys
   sequential computation by spending generation steps.

This is the whole mechanism: **attention-over-own-output turns generated text into
working memory.** The "magic" step — that writing reasoning improves the answer —
is justified entirely by the fact that the answer token attends to those written
reasoning tokens.

**Worked instance.** Take a small two-step problem:

> *Roger has 5 tennis balls. He buys 2 cans of tennis balls. Each can has 3 balls.
> How many tennis balls does he have now?*

The correct answer is $11$, and reaching it requires two operations in sequence:
first a multiplication ($2 \times 3 = 6$), then an addition that *depends on the
multiplication's result* ($5 + 6 = 11$). The second step cannot start until the
first is done — this is exactly the kind of sequential dependency that strains a
single fixed-depth pass.

*Direct path.* The context is just the question, and the very next token must be the
final number:

```
... How many tennis balls does he have now?  ->  [next token = answer]
```

To emit "11" here, the one forward pass producing that token must internally
perform both $2 \times 3$ and the dependent $5 + 6$ with no place to write the
intermediate $6$ down. The attention in that pass can look back at "2", "3", "5" in
the question, but the partial result $6$ exists only fleetingly inside the layers of
this single pass — it is never a token, so no later pass can attend to it. If the
problem's required step-count exceeds the pass's depth, the model misfires.

*Chain-of-thought path.* Now the model is prompted to reason first. It generates,
token by token:

```
... How many now?
2 cans × 3 balls = 6      <- step 1, written as tokens
5 + 6 = 11                <- step 2
Answer: 11                <- final answer
```

Trace the mechanism across the generation:

- Producing "**6**" is a forward pass whose attention reads "2", "cans", "3" from the
  text and computes one operation. The result $6$ is now **committed to the
  context as a token**.
- Producing the "**11**" in step 2 is a *later* forward pass. Its query attends back
  over the sequence and finds two settled inputs sitting right there as tokens: the
  "5" from the question and the "6" the model itself just wrote. The weighted
  average over their value vectors (per [[transformer-attention]]) delivers $5$ and
  $6$ into this pass, which only has to perform the single addition $5 + 6$.
- Producing the final "**Answer: 11**" attends back to the "11" already written in
  step 2 and copies it.

Notice what changed. Neither pass had to do two dependent operations alone; each did
one, and the bridge between them was a *token in the context that the next pass
attended to*. The intermediate $6$ went from being a hidden, un-attendable flicker
(direct path) to a written value the answer is computed from (CoT path). That is why
the steps help: not because the model "thinks out loud" in a human sense, but
because [[transformer-attention]] lets each forward pass read the partial results
the earlier passes deposited as text. Empirically, prompting large models to produce
such steps sharply raises accuracy on multi-step arithmetic and word problems (Wei
et al. 2022).

## Prerequisites

- [[transformer-attention]]

## Sources

- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q.,
  Zhou, D. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language
  Models.* arXiv:2201.11903.
