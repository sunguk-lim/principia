---
id: speculative-decoding
title: Speculative Decoding
summary: Generating text one token at a time runs the big "target" model once per token, and that pass is memory-bound — most of the time goes to streaming the model's weights and the…
type: concept
tags: [ml/llm/inference]
prereqs: [transformer-attention, kv-cache, softmax, probability-distribution]
sources:
  - "Leviathan, Kalman & Matias, *Fast Inference from Transformers via Speculative Decoding*, ICML 2023 (arXiv:2211.17192)"
  - "Chen et al., *Accelerating Large Language Model Decoding with Speculative Sampling*, 2023 (arXiv:2302.01318)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Speculative Decoding

## Summary

Generating text one token at a time runs the **big "target" model once per
token**, and that pass is **memory-bound** — most of the time goes to streaming
the model's weights and the [[kv-cache]] through memory, not to arithmetic, so
scoring one token costs almost as much as scoring several. **Speculative
decoding** exploits this slack. A small, cheap **draft** model proposes the next
$k$ tokens; the target model then runs **one** pass that scores **all $k$
positions in parallel**; and a **probabilistic acceptance rule** decides how many
of the draft's tokens to keep. The rule is built so the tokens that come out are
distributed **exactly** as if the target model had generated them alone — same
quality, but often $k$ tokens per target pass instead of one.

## Grounded explanation

**The setup and notation.** We have two models over the same vocabulary. The
**target** model $T$ is the one we actually want to sample from; running its
forward pass is expensive. The **draft** model $D$ is small and fast (e.g. a
model with far fewer layers). Both are ordinary transformers, so for any prefix
of tokens each one produces, via its final [[softmax]] inside
[[transformer-attention]], a [[probability-distribution]] (a discrete pmf over the vocabulary) for the next
token. Write $p(x)$ for the target's probability of token $x$ and $q(x)$ for
the draft's probability of the same token, always conditioned on whatever prefix
is current.

**Why decoding is slow, and where the slack is.** With a [[kv-cache]], producing
token $t$ costs *one* target forward pass: project the single new token to its
query/key/value, append $k_t,v_t$ to the cache, and attend over the cache. That
is already minimal in *arithmetic*. But each pass must read the model's entire
weight set (and the cache) out of memory, and a modern target model is large, so
the pass is **memory-bound**: the hardware finishes the few multiplications long
before the memory traffic is done. Crucially, that memory traffic is **nearly the
same whether the pass scores one token position or several** — the weights are
read once either way. Sequential decoding wastes this: it pays full memory cost
for a single token, $n$ times for $n$ tokens.

**The parallel-scoring trick (why one target pass scores $k$ tokens).** Suppose
the current prefix is $x_{1:m}$ and the draft has cheaply proposed
$\tilde x_{m+1}, \tilde x_{m+2}, \dots, \tilde x_{m+k}$ by running itself $k$
times. Now feed the target model the concatenation
$x_{1:m},\tilde x_{m+1},\dots,\tilde x_{m+k}$ as a **single** input. Because
[[transformer-attention]] is **causal** — position $i$ attends only to positions
$\le i$ — the target's output row at each position $j$ is the next-token
distribution given exactly the prefix up to $j$. So in **one** pass the target
produces $k+1$ distributions at once:

$$p(\cdot \mid x_{1:m}),\quad p(\cdot \mid x_{1:m},\tilde x_{m+1}),\quad \dots,\quad p(\cdot \mid x_{1:m},\dots,\tilde x_{m+k}).$$

This is the same fact the [[kv-cache]] rests on (each row is the distribution for
its own prefix), used in the other direction: instead of feeding one token and
reading one row, we feed $k$ guessed tokens and read $k$ rows — for essentially
the cost of a single pass, since the pass was memory-bound anyway. The KV-cache
also lets us keep the prefix $x_{1:m}$'s keys/values and only pay for the $k$ new
columns. Call the target distribution at the position **after** $\tilde x_{m+i}$
by the shorthand $p_i = p(\cdot \mid x_{1:m},\dots,\tilde x_{m+i-1})$, so $p_1$
scores the first draft token, $p_2$ the second, and so on; and let
$q_i = q(\cdot \mid x_{1:m},\dots,\tilde x_{m+i-1})$ be the draft's distribution
that *proposed* token $\tilde x_{m+i}$.

**The acceptance rule (the one non-obvious step).** We now walk left to right
through the $k$ draft tokens. For draft token $\tilde x_{m+i}$, with the value it
was proposed under, $q_i(\tilde x_{m+i})$, and the target's verdict on it,
$p_i(\tilde x_{m+i})$:

- **Accept** $\tilde x_{m+i}$ with probability
  $$a_i = \min\!\left(1,\ \frac{p_i(\tilde x_{m+i})}{q_i(\tilde x_{m+i})}\right).$$
  (Draw a uniform $r\in[0,1)$; accept iff $r < a_i$.) If accepted, move to the
  next draft token.
- **Reject** otherwise. Stop the walk and **resample** the token at this position
  from the **residual** distribution
  $$p'_i(x) = \frac{\big(p_i(x) - q_i(x)\big)_+}{\sum_{x'}\big(p_i(x') - q_i(x')\big)_+},$$
  where $(z)_+ = \max(0, z)$ is the positive part. Discard the rest of the draft.

If *all* $k$ are accepted, we additionally sample one bonus token straight from
$p_{k+1}$ — already available for free from the same target pass. So one target
pass yields **somewhere between 1 and $k+1$** correct tokens.

**Why this is EXACT — the justifying identity.** The magic-looking claim is that
the accepted-or-resampled token at each position is distributed *exactly* as
$p_i$, the target's own distribution — despite having been proposed by the wrong
model $q_i$. Drop the subscript $i$ and check the probability that the final token
equals some value $x$. It can arrive two ways:

1. The draft proposed $x$ (prob $q(x)$) **and** we accepted it (prob
   $\min(1, p(x)/q(x))$). Contribution:
   $$q(x)\cdot\min\!\Big(1,\tfrac{p(x)}{q(x)}\Big) = \min\big(q(x),\,p(x)\big).$$
2. We rejected whatever was proposed (overall prob
   $1-\sum_{x'}\min(q(x'),p(x')) = \sum_{x'}(p(x')-q(x'))_+$) **and** the residual
   resample landed on $x$ (prob $p'(x)$, whose denominator is exactly that same
   sum). Contribution:
   $$\Big(\textstyle\sum_{x'}(p(x')-q(x'))_+\Big)\cdot\frac{(p(x)-q(x))_+}{\sum_{x'}(p(x')-q(x'))_+} = (p(x)-q(x))_+.$$

Adding the two: $\min(q(x),p(x)) + (p(x)-q(x))_+$. If $p(x)\ge q(x)$ this is
$q(x) + (p(x)-q(x)) = p(x)$; if $p(x)<q(x)$ it is $p(x) + 0 = p(x)$. **Either way
the total is $p(x)$.** So every emitted token — accepted or resampled — is a true
sample from the target. Speculative decoding changes *how fast* tokens come out,
never *which distribution* they come from. (The draft only affects the
acceptance *rate*: the closer $q$ is to $p$, the more tokens survive per pass.)

**Worked instance (2 accepted, 1 rejected).** Tiny vocabulary
$\{A, B, C\}$. The draft proposes $k=3$ tokens; one target pass gives us $p_1,p_2,p_3$.
Suppose the draft proposed and the two models assign:

| pos $i$ | draft proposed $\tilde x$ | $q_i(\tilde x)$ | $p_i(\tilde x)$ | $a_i=\min(1,p_i/q_i)$ | drawn $r$ | outcome |
|---|---|---|---|---|---|---|
| 1 | $A$ | $0.50$ | $0.60$ | $\min(1, 1.20)=1.00$ | $0.31$ | **accept** ($r<1.00$) |
| 2 | $B$ | $0.80$ | $0.40$ | $\min(1, 0.50)=0.50$ | $0.22$ | **accept** ($r<0.50$) |
| 3 | $C$ | $0.90$ | $0.30$ | $\min(1, 0.333)=0.333$ | $0.71$ | **reject** ($r\ge0.333$) |

Position 1: target likes $A$ even more than the draft did ($0.60>0.50$), so the
ratio exceeds 1 and acceptance is certain — keep $A$. Position 2: target likes $B$
*less* than the draft ($0.40<0.80$), acceptance probability $0.50$; the draw
$0.22<0.50$, so we still keep $B$. Position 3: ratio $0.30/0.90=0.333$, but the
draw $0.71\ge0.333$, so $C$ is **rejected** — and we stop here, discarding nothing
further (there was nothing after it that matters).

Now **resample** position 3 from the residual $p'_3$. Suppose at that prefix the
full distributions are

$$p_3 = (A{:}0.50,\ B{:}0.20,\ C{:}0.30),\qquad q_3 = (A{:}0.05,\ B{:}0.05,\ C{:}0.90).$$

Positive parts $(p_3-q_3)_+ = (A{:}0.45,\ B{:}0.15,\ C{:}0.00)$ — note $C$'s part
is $0$, exactly the token the draft over-proposed. The normalizer is
$0.45+0.15+0.00 = 0.60$, so

$$p'_3 = \big(A{:}0.45/0.60,\ B{:}0.15/0.60,\ C{:}0\big) = (A{:}0.75,\ B{:}0.25,\ C{:}0).$$

We sample from $p'_3$ and emit, say, $A$. **Net result of this round:** the
sequence grew by $A, B, A$ — **3 correct target tokens from a single target
forward pass**. The naive method would have spent **3** target passes for the
same 3 tokens. (Had all 3 been accepted, we'd have taken a 4th free token from
$p_4$, getting 4 tokens for one pass.) Every emitted token is a genuine target
sample, by the identity above — so quality is untouched while target passes drop
from 3 to 1.

## Prerequisites

- [[transformer-attention]]
- [[kv-cache]]
- [[softmax]]
- [[probability-distribution]]

## Sources

- Leviathan, Kalman & Matias, *Fast Inference from Transformers via Speculative Decoding*, ICML 2023 (arXiv:2211.17192).
- Chen et al., *Accelerating Large Language Model Decoding with Speculative Sampling*, 2023 (arXiv:2302.01318).
