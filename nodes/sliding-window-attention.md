---
id: sliding-window-attention
title: Sliding-Window Attention
summary: In ordinary transformer-attention every query attends to all $n$ keys, so the work scales like $n^2$.
type: concept
tags: [ml/llm/architecture]
prereqs: [transformer-attention, softmax]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Sliding-Window Attention

## Summary

In ordinary [[transformer-attention]] every query attends to all $n$ keys, so the
work scales like $n^2$. **Sliding-window attention** restricts each query to a
fixed local window — only the most recent $w$ keys — dropping the cost to $n\cdot w$.
A single layer then sees only $w$ tokens back, but **stacking $L$ such layers**
widens the effective reach to roughly $L\cdot w$ tokens, because information hops
one window further up at every layer. So locality per layer still buys long-range
reach across depth.

## Grounded explanation

### What the concept is

Recall from [[transformer-attention]] that for a sequence of $n$ tokens we form a
query, a key, and a value vector per token, and the output for each query is a
weighted average of value vectors, the weights coming from how well that query
matches each key. The **attention pattern** is just the set of keys each query is
allowed to look at. In standard attention that set is *all* keys: query $i$ scores
itself against every key $1,\dots,n$, so the score matrix is $n\times n$ and the
cost grows with $n^2$.

Sliding-window attention changes **only one thing**: the allowed set. Define the
**window size** $w$ (a small fixed integer, say 3 or 4096 in practice). Query at
position $i$ may attend only to keys in the band

$$\{\, i-w+1,\ i-w+2,\ \dots,\ i \,\},$$

i.e. itself and the $w-1$ keys immediately before it (we use the *causal* version —
look back, never forward — which is the common one for language models). Every key
outside that band is masked out: its score is discarded before the softmax, so it
contributes zero weight. The query–key matching, the scaling, the [[softmax]] over the
*surviving* scores, and the weighted average of the corresponding values are all
exactly as in [[transformer-attention]]; the window only narrows *which* keys enter
the average.

Two symbols, fixed for the rest of this note:

- $n$ — number of tokens in the sequence.
- $w$ — window size: how many keys (including the query's own position) each query may attend to.

### Why it works — the cost argument

In full attention, query $i$ computes $n$ scores (one per key), so all queries
together do on the order of $n\cdot n = n^2$ score computations. The $n\times n$
matrix is the bottleneck: doubling the sequence quadruples the work and the memory.

With a window, query $i$ computes at most $w$ scores instead of $n$. Across all $n$
queries that is at most $n\cdot w$ work. When $w$ is a fixed constant (it does not
grow with $n$), the cost is **linear** in $n$ rather than quadratic. That is the
whole point: for a sequence of $32{,}000$ tokens with window $w = 4096$, full
attention touches $32{,}000^2 \approx 10^9$ score entries per head, while the window
touches about $32{,}000 \times 4096 \approx 1.3\times10^8$ — roughly an $8\times$
reduction here, and the gap widens without bound as $n$ grows past $w$.

### The trade-off and its resolution

The obvious objection: if query at position $i$ can see only $w-1$ tokens back, how
can the model ever use information from far earlier in the sequence — a word
hundreds of tokens ago that determines the meaning here?

The resolution is **depth**. A transformer is a stack of $L$ attention layers, each
feeding its outputs as the inputs to the next. Track how far information can travel:

- After **layer 1**, the representation at position $i$ has absorbed positions
  $i-w+1,\dots,i$ — a span of $w$.
- That layer-1 output at, say, position $i-w+1$ has *itself* already absorbed
  positions $(i-w+1)-w+1,\dots$ down to $i-2w+2$. So when **layer 2** reads its
  window ending at $i$, it indirectly pulls in everything those neighbors saw:
  position $i$ now reflects roughly the span $i-2w+2,\dots,i$, about $2w$ wide.
- Each additional layer extends the reach by one more window. After $L$ layers the
  **effective receptive field** of a position is about $L\cdot w$ tokens —
  information has propagated window-by-window up the stack, like ripples joining.

So locality per layer is not a ceiling on what the model can connect; it is a budget
per hop. Stacking trades a single wide-but-expensive layer for many narrow-but-cheap
layers whose reaches compose. This is exactly the design used in real long-context
models — **Longformer** introduced windowed attention (combined with a few global
tokens) to scale to long documents, and **Mistral 7B** uses a sliding window of
$w = 4096$ across $32$ layers, giving a theoretical reach of about $4096\times32
\approx 131{,}000$ tokens.

### Worked instance

Take $n = 8$ tokens (positions $1,\dots,8$) and window $w = 3$. Each causal query
attends to itself plus the 2 keys before it.

| Query position $i$ | Allowed keys $\{i-2,\,i-1,\,i\}$ | Count |
|--------------------|----------------------------------|-------|
| 1 | $\{1\}$ (nothing earlier exists) | 1 |
| 2 | $\{1, 2\}$ | 2 |
| 5 | $\{3, 4, 5\}$ | 3 |
| 7 | $\{5, 6, 7\}$ | 3 |

So **query at position 5** scores against keys 3, 4, 5 only — three dot products,
three softmax weights summing to 1, and its output is the weighted average of value
vectors $v_3, v_4, v_5$. Keys 1 and 2 are masked; they get weight 0. Under full
attention this same query would have scored against all 8 keys.

**Per-query cost.** With the window, query 5 does 3 score computations; full
attention does 8. Across the whole sequence the window does $1+2+3+3+3+3+3+3 = 21$
score computations (early positions do fewer because there are fewer earlier tokens),
versus the $1+2+\dots+8 = 36$ of causal full attention. The saving is modest at
$n=8$ because $n$ is barely larger than $w$; it becomes dramatic only when $n \gg w$,
which is the regime the method targets.

**Reach across stacked layers — trace position 7.** In a single layer, position 7
sees keys 5, 6, 7 — it has *no direct path* to position 1.

- **Layer 1:** position 7's output mixes in 5, 6, 7. Separately, position 5's
  layer-1 output mixed in 3, 4, 5.
- **Layer 2:** position 7 again attends to positions 5, 6, 7 — but those are now
  *layer-1 outputs*. Position 5's layer-1 output already carries traces of 3 and 4.
  So after layer 2, position 7 indirectly reflects positions 3 through 7 — a span of
  5, wider than the window of 3.
- **Layer 3:** position 7 attends to 5, 6, 7 (layer-2 outputs). Position 5's layer-2
  output, by the same reasoning one step deeper, already reaches back to position 1.
  So after **3 layers** the information at position 1 has finally reached position 7.

That matches the estimate: reach $\approx L\cdot w$. Here $L=3$, $w=3$ gives about
$3\times3 = 9 \ge 8 = n$, so 3 windowed layers suffice to connect the two ends of an
8-token sequence that a single windowed layer could never bridge.

## Prerequisites

- [[transformer-attention]]

## Sources

_none_
