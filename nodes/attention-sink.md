---
id: attention-sink
title: Attention Sink
summary: When you run sliding-window-attention for very long, streaming generation and evict the oldest tokens as the window slides forward, generation quality can collapse — the model's…
type: concept
tags: [ml/llm/architecture]
prereqs: [sliding-window-attention, softmax]
sources:
  - "Xiao, Tian, Chen, Han, Lewis. Efficient Streaming Language Models with Attention Sinks (StreamingLLM), 2023. arXiv:2309.17453"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Attention Sink

## Summary

When you run [[sliding-window-attention]] for very long, streaming generation and
**evict the oldest tokens** as the window slides forward, generation quality can
collapse — the model's predictions become garbage almost the moment the very first
tokens fall out of the cache. The culprit is the [[softmax]] sum-to-1 rule: every
query's attention weights are *forced* to total 1, so even when no key is a good
match, the model must still dump that leftover probability somewhere. During
training it learns to dump the excess onto the **first few tokens** of the sequence,
using them as a constant "no-op" parking spot — an **attention sink**. Evicting
those initial tokens destroys the parking spot, forcing the excess mass onto recent,
semantically irrelevant tokens and corrupting every output. The fix is tiny: always
**keep the first few tokens** in the cache alongside the sliding window.

## Grounded explanation

### Setup: the streaming regime

Recall from [[sliding-window-attention]] that we cap each query's attention to a
fixed window of the most recent $w$ keys, so cost stays linear in sequence length
$n$ instead of quadratic. To actually generate text of *unbounded* length —
chatting for hours, never restarting — we go one step further: as each new token is
produced we **slide the window** and **evict** (delete from the cache) the key/value
of the token that just fell off the back. The cache then holds a constant $w$ most
recent tokens forever. This is the natural, memory-bounded way to stream.

It does not work. The empirical observation behind this concept: the instant the
window slides far enough to evict **position 1** (the very first token), the model's
**perplexity** — its average surprise at the next token, a standard quality measure
where lower is better — explodes, often by orders of magnitude. The text degenerates
into nonsense. Crucially, the failure tracks *which* tokens are evicted, not *how
many* tokens are in the window: keeping the same window size but never evicting the
first few tokens restores stable quality. That asymmetry is the clue.

### Why it happens — the [[softmax]] sum-to-1 constraint

The mechanism lives entirely in [[softmax]]. Recall that for a query with raw scores
(logits) $z_1,\dots,z_k$ against its $k$ visible keys, the attention weights are

$$a_i = \mathrm{softmax}(z)_i = \frac{e^{z_i}}{\sum_{j=1}^{k} e^{z_j}}, \qquad \sum_{i=1}^{k} a_i = 1.$$

The output is then the weighted average $\sum_i a_i v_i$ of the value vectors $v_i$.
The weights $a_i$ are guaranteed positive and **forced to sum to exactly 1** — that
normalization is the whole point of softmax, what makes the output a proper average.

Now consider what happens at a layer/head whose job, for this particular query, is
essentially *"there is nothing relevant here, pass the input through unchanged."*
A query that finds no good match produces scores $z_i$ that are all low and roughly
equal. Softmax does **not** have an option to output "all weights near zero" — the
sum is pinned at 1. The model cannot say "attend to nothing." It must place a full
unit of probability mass on *something*, and that mass then drags some value vectors
into the average whether or not they are relevant. This is the trap: **the leftover
mass has to go somewhere.**

During training the model discovers a clean escape. The first few token positions are
present in **every** training example (a sequence always has a position 1), and every
query — at every later position — can always see them (they are the earliest keys, so
they are inside any causal window that has not yet evicted them). So the model learns
to assign those positions a large, *content-independent* score: a bias that says
"when in doubt, dump the excess mass here." Because the same few positions act as the
universal dumping ground, the value vectors stored there get trained to contribute
almost nothing to the output — they are a learned **no-op sink**. The first tokens
become an attention sink: a constant drain that absorbs whatever probability mass the
real keys do not deserve, leaving the weights on the genuinely relevant recent keys
undistorted.

### Why eviction is catastrophic — and the fix

Now slide the window past position 1 and **evict** the sink tokens. The query still
runs softmax, the sum is still pinned at 1, and the model still produces a big score
for the dumping ground — but the dumping ground is **gone**. The excess mass that
used to park on the sink is now forced, by the normalization, onto whichever keys
*remain*: the recent tokens in the window. Those recent tokens were never meant to
absorb it; their value vectors are real content. Pouring a large, spurious weight
onto them corrupts the weighted average, the corrupted representation feeds the next
layer, and the error compounds — perplexity explodes. The problem is not that the
window is too small; it is that the **invariant the model was trained to rely on (a
sink is always reachable) was broken.**

The fix, from StreamingLLM (Xiao et al., 2023), follows directly: **always keep the
first few tokens** — typically just **4** — pinned in the cache, *alongside* the
sliding window of recent tokens. The cache becomes "4 sink tokens + the most recent
$w-4$ tokens." This is a constant-size addition that costs essentially nothing, yet
it restores the sink, so the excess mass goes back to parking harmlessly, and the
model streams stably to effectively unbounded length. The sink tokens' actual
*content* barely matters — even keeping placeholder tokens works — because their job
is to be a mass drain, not to carry meaning.

### Worked instance

Take a single query at a late position whose raw scores against its visible keys are
all low and similar — exactly the "nothing here is a great match" situation. Suppose
besides the (optional) sink there are three recent keys $r_1, r_2, r_3$ with logits

$$z(r_1) = 1.0, \quad z(r_2) = 0.5, \quad z(r_3) = 0.8.$$

The model *wants* $r_1$ to lead slightly, then $r_3$, then $r_2$ — but it has no
strong opinion, and these scores carry a unit of probability mass that mostly should
not land on any of them.

**With the sink present.** The sink token at position 1 carries the large learned
bias score $z(\text{sink}) = 4.0$. Exponentiate all four logits (using
$e^{1.0}=2.72,\ e^{0.5}=1.65,\ e^{0.8}=2.23,\ e^{4.0}=54.60$):

$$\text{sum} = 54.60 + 2.72 + 1.65 + 2.23 = 61.20.$$

The [[softmax]] weights are

$$a_{\text{sink}} = \tfrac{54.60}{61.20} = 0.892, \quad
a_{r_1} = \tfrac{2.72}{61.20} = 0.044, \quad
a_{r_2} = \tfrac{1.65}{61.20} = 0.027, \quad
a_{r_3} = \tfrac{2.23}{61.20} = 0.036.$$

About **89%** of the mass parks on the sink (a no-op, contributing nothing to the
output), and the recent keys split the remaining ~11% in the intended order
($r_1 > r_3 > r_2$). The output $\sum_i a_i v_i$ is then dominated by the *inert*
sink value, i.e. very close to a pass-through — exactly the gentle, near-no-op
behavior the model intended.

**Without the sink (evicted).** Same query, same recent logits, but the sink is gone.
Softmax must renormalize over only the three survivors:

$$\text{sum} = 2.72 + 1.65 + 2.23 = 6.60,$$

$$a_{r_1} = \tfrac{2.72}{6.60} = 0.412, \quad
a_{r_2} = \tfrac{1.65}{6.60} = 0.250, \quad
a_{r_3} = \tfrac{2.23}{6.60} = 0.338.$$

The full unit of mass that *used* to sit on the sink has been forced onto the three
recent keys. The weight on $r_1$ jumped from $0.044$ to $0.412$ — nearly a
**$10\times$** increase — and $r_2$, which the model rated *least* relevant, now
carries a hefty $0.250$. The output is no longer a near-pass-through; it is a strong,
confident average of value vectors the model never wanted to commit to. That
distortion is the perplexity spike, multiplied across every layer and head and every
generated token. Pinning the four initial tokens in the cache is what prevents it.

## Prerequisites

- [[sliding-window-attention]]
- [[softmax]]

## Sources

- Xiao, Tian, Chen, Han, Lewis. *Efficient Streaming Language Models with Attention Sinks* (StreamingLLM), 2023. arXiv:2309.17453.
