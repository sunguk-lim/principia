---
id: structured-output
title: Structured Output
summary: Structured output constrains token generation with a grammar by masking illegal logits to negative infinity and renormalizing probability over the legal tokens.
type: concept
tags: [ml/llm/reasoning]
prereqs: [softmax, probability-distribution]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Structured Output

## Summary

**Structured output** (a.k.a. constrained decoding, grammar-guided generation)
forces a language model's text generation to conform to a formal structure — a
JSON schema, a regular expression, a grammar. The trick: at every generation
step, before turning the model's scores into probabilities, a "constraint
engine" deletes every token that would break the structure by pushing its score
to $-\infty$. Because [[softmax]] sends a score of $-\infty$ to probability 0,
those tokens can never be picked, while the allowed tokens keep their *relative*
likelihoods. The result is **guaranteed-valid** output — never a parse failure —
without otherwise overriding the model's preferences.

![A grammar state expects a digit. Among five vocabulary tokens, the illegal closer has the largest raw probability. Masking leaves legal digits 7 and 4, whose probabilities renormalize to 0.622 and 0.378 while preserving their relative preference; sampling 7 advances the grammar toward valid JSON.](structured-output.svg)

## Grounded explanation

### The problem

A language model generates text one **token** at a time (a token is a chunk of
text — a word, a fragment, a punctuation mark — drawn from a fixed **vocabulary**,
the full list of tokens the model knows). At each step the model emits one real
number per vocabulary token, called a **logit** (an unbounded score: higher means
"more plausible here"). To turn those scores into a choice, we feed the whole
vector of logits through [[softmax]], which produces a [[probability-distribution]]
over the vocabulary — every token positive, the lot summing to 1 — and then we
**sample** a token from that distribution (draw one at random, each with its given
probability). The drawn token is appended to the text, and the loop repeats.

Left alone, this loop is free to emit *any* token at any step. If you need the
output to be valid JSON, a matching phone number, or a sentence from a fixed
grammar, "free to emit anything" is a liability: one wrong token — a letter where
a digit was required, a missing closing brace — and the whole thing fails to
parse. Re-prompting and hoping is unreliable.

### The mechanism: mask, then renormalize

Structured output attaches a **constraint engine** to the loop. The engine is a
small state machine that tracks *where in the required structure we currently
are*, and from that state it can compute the **legal set**: the subset of
vocabulary tokens that would keep the output on a valid path. (For JSON the state
might be "I have emitted `{` and a key, so the next thing must be `:`"; the legal
set is then just `{ : }`.)

The engine does **not** rewrite the model or its logits' meaning. It does exactly
one thing per step, slotted in between the logits and [[softmax]]:

> **Mask:** for every token *not* in the legal set, overwrite its logit with
> $-\infty$. Leave the legal tokens' logits untouched.

Why $-\infty$ specifically? Recall [[softmax]] exponentiates each logit and
divides by the total. The exponential of $-\infty$ is $0$. So a masked token
contributes $0$ to the numerator *and* $0$ to the sum — it vanishes from the
distribution entirely, getting probability exactly 0, and it can never be
sampled. Meanwhile the surviving (legal) tokens are exponentiated and divided by
their *new, smaller* total. This is the key invariant: **masking removes the
illegal tokens and redistributes their probability mass across the legal ones in
proportion to what they already had.** The model's ranking and relative
preference *among the allowed tokens* is preserved exactly; only the forbidden
options are erased. That is why constrained decoding rarely produces gibberish —
it isn't forcing arbitrary tokens, it is letting the model choose freely within
the legal set.

After a token is sampled, the engine **advances its state** to reflect that the
token was accepted (the `:` is now emitted, so next we expect a value), which
changes the legal set for the next step. Step by step, the state machine walks
the structure to completion, and *every* sampled token sits on a valid path — so
the finished string is guaranteed to parse. No structural error is possible,
because no structurally illegal token was ever reachable.

### A worked instance

Tiny vocabulary of 5 tokens: `{"x":`, the digits `7` and `4`, the brace `}`, and
the word `cat`. The required structure (our trivial grammar) is exactly three steps:

1. emit the opener `{"x":`
2. emit a single **digit**
3. emit the closer `}`

We're at **step 2** — the opener is already written, and the rule says the next
token *must be a digit*. Suppose the model's raw logits at this step are:

| token | logit $z$ |
|-------|-----------|
| `{"x":` | 2.0 |
| `7` | 1.0 |
| `4` | 0.5 |
| `}` | 3.0 |
| `cat` | 0.0 |

**Unconstrained [[softmax]].** Exponentiate: $e^{2.0}=7.389$, $e^{1.0}=2.718$,
$e^{0.5}=1.649$, $e^{3.0}=20.086$, $e^{0.0}=1.000$. Their sum is $32.842$. Dividing each by the
sum:

| token | probability |
|-------|-------------|
| `{"x":` | $7.389/32.842 = 0.225$ |
| `7` | $2.718/32.842 = 0.083$ |
| `4` | $1.649/32.842 = 0.050$ |
| `}` | $20.086/32.842 = 0.612$ |
| `cat` | $1.000/32.842 = 0.030$ |

Left to itself the model would most likely emit `}` (0.612) — which is *illegal*
here (a digit is required), and would produce `{"x":}`, broken JSON. The
preferred legal digit `7` has only an 8.3% chance. This instance is **non-degenerate**:
the illegal token is the *favorite*, so masking has real work to do.

**Mask.** The legal set at step 2 contains the digits `7` and `4`. The engine
leaves both legal logits untouched and overwrites the other three with $-\infty$:

| token | logit after mask |
|-------|------------------|
| `{"x":` | $-\infty$ |
| `7` | 1.0 |
| `4` | 0.5 |
| `}` | $-\infty$ |
| `cat` | $-\infty$ |

**Renormalized [[softmax]].** Now $e^{-\infty}=0$ for the three masked tokens,
while $e^{1.0}=2.718$ for `7` and $e^{0.5}=1.649$ for `4`. The legal total is
$2.718+1.649=4.367$. Dividing:

| token | probability |
|-------|-------------|
| `{"x":` | $0/4.367 = 0$ |
| `7` | $2.718/4.367 = 0.622$ |
| `4` | $1.649/4.367 = 0.378$ |
| `}` | $0/4.367 = 0$ |
| `cat` | $0/4.367 = 0$ |

The illegal favorite `}` falls from 0.612 to exactly 0. Its probability mass is
redistributed across the two legal digits, and their preference is preserved:
`7` remains more likely than `4`, with the ratio $0.622/0.378$ matching
$e^{1.0}/e^{0.5}$. Suppose sampling chooses the more likely digit `7`.

The engine then advances: digit emitted, so the legal set for step 3 becomes just
`}`. The output `{"x":7}` is assembled token by token and is valid by
construction.

### In practice

Real systems implement exactly this loop. **JSON mode** constrains decoding to a
JSON schema; libraries like **Outlines** compile a regex or schema into the state
machine that produces each step's legal set; **GBNF** (the grammar format used by
`llama.cpp`) lets you write a context-free grammar whose parser plays the same
role. All of them reduce to the same primitive shown above: track the state,
compute the legal set, mask illegal logits to $-\infty$, let [[softmax]]
renormalize over the survivors, sample, advance.

## Prerequisites

- [[softmax]]

## Sources

_none_
