---
id: structured-output
title: Structured Output
summary: Structured output (a.k.a.
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

![Static 7-panel walk of grammar-constrained decoding, grouped into 3 acts: a 4-state grammar automaton (S0→S3) as the spine, a 4-token vocabulary strip whose gold ring marks the current legal set, and a detail panel deriving one full digit decision — raw logits (2.0, 1.0, 3.0, 0.0) → unconstrained softmax favoring the illegal closer (0.644) → a dashed red counterfactual branch showing the invalid output it would produce → mask to −∞ → renormalized distribution (0, 1.000, 0, 0) → sampled token joining the growing output spine, which completes as valid JSON.|960](structured-output.svg)

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

Tiny vocabulary of 4 tokens: `{"x":`, the digit `7`, the brace `}`, and the word
`cat`. The required structure (our trivial grammar) is exactly three steps:

1. emit the opener `{"x":`
2. emit a single **digit**
3. emit the closer `}`

We're at **step 2** — the opener is already written, and the rule says the next
token *must be a digit*. Suppose the model's raw logits at this step are:

| token | logit $z$ |
|-------|-----------|
| `{"x":` | 2.0 |
| `7` | 1.0 |
| `}` | 3.0 |
| `cat` | 0.0 |

**Unconstrained [[softmax]].** Exponentiate: $e^{2.0}=7.389$, $e^{1.0}=2.718$,
$e^{3.0}=20.086$, $e^{0.0}=1.000$. Their sum is $31.193$. Dividing each by the
sum:

| token | probability |
|-------|-------------|
| `{"x":` | $7.389/31.193 = 0.237$ |
| `7` | $2.718/31.193 = 0.087$ |
| `}` | $20.086/31.193 = 0.644$ |
| `cat` | $1.000/31.193 = 0.032$ |

Left to itself the model would most likely emit `}` (0.644) — which is *illegal*
here (a digit is required), and would produce `{"x":}`, broken JSON. The
desired digit `7` has only an 8.7% chance. This instance is **non-degenerate**:
the illegal token is the *favorite*, so masking has real work to do.

**Mask.** The legal set at step 2 is just the digit `7`. The engine overwrites
the other three logits with $-\infty$:

| token | logit after mask |
|-------|------------------|
| `{"x":` | $-\infty$ |
| `7` | 1.0 |
| `}` | $-\infty$ |
| `cat` | $-\infty$ |

**Renormalized [[softmax]].** Now $e^{-\infty}=0$ for the three masked tokens,
and $e^{1.0}=2.718$ for `7`. The sum is $0+2.718+0+0=2.718$. Dividing:

| token | probability |
|-------|-------------|
| `{"x":` | $0/2.718 = 0$ |
| `7` | $2.718/2.718 = 1.000$ |
| `}` | $0/2.718 = 0$ |
| `cat` | $0/2.718 = 0$ |

The distribution collapsed onto `7` with probability 1. Sampling now *must* yield
`7`. Compare the before/after for the illegal favorite `}`: it fell from 0.644 to
exactly 0, and its mass was redistributed onto the lone legal token. (Had two
digits been legal, say `7` and `4`, masking would keep *both* and renormalize over
the pair — the model's preference between them surviving intact; here only `7` was
in the vocabulary, so it took all the mass.)

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
