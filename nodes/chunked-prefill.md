---
id: chunked-prefill
title: Chunked Prefill
summary: LLM inference has two phases.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache, transformer-attention]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Chunked Prefill

## Summary

LLM inference has two phases. **Prefill** reads the whole prompt in one shot to
fill the [[kv-cache]]; its cost grows with prompt length, so a long prompt is a
single large compute burst. **Decode** then emits one token per step, each step
cheap. The problem: when many requests share a server, one long prompt's prefill
burst hogs a step and **stalls the decode** of everyone else — a latency hiccup.
**Chunked prefill** cuts the prefill into fixed-size token **chunks** processed
across successive steps, and **interleaves** those chunks with other requests'
decode tokens in the same batch. Each step now carries a bounded, even amount of
work, so per-step latency stays smooth. It is exactly correct because attention
is **causal**: a chunk's tokens attend (via [[transformer-attention]]) to every
earlier token already in the [[kv-cache]], so processing the prompt in pieces
gives bit-identical keys, values, and outputs to processing it all at once.

## Grounded explanation

**Two phases, two cost profiles.** Generating from an LLM splits into:

- **Prefill** — the prompt of $P$ tokens is fed in *together*. Every token's
  query, key, and value are computed, all $P$ keys/values are written to the
  [[kv-cache]], and each token attends over the tokens at or before it. This does
  $\approx P$ tokens' worth of attention and projection work in **one** step. It
  is **compute-bound**: lots of arithmetic, and the cost rises with $P$.
- **Decode** — having filled the cache, the model emits one token per step. Per
  the [[kv-cache]], each step computes just the *one* new token's $q,k,v$,
  appends that $k,v$, and runs $o_t=\mathrm{softmax}(\tfrac{q_t K_{1:t}^{\top}}{\sqrt{d_k}})V_{1:t}$
  — one query against the whole cache. The arithmetic is tiny; the step is
  dominated by *reading* the cache from memory, so it is **memory-bound** and
  cheap in compute.

**The problem chunked prefill solves.** A server batches many in-flight requests
into each step to keep the hardware busy. Most are in decode (one token each,
cheap). If a fresh request arrives with a 4000-token prompt, its prefill wants to
do 4000 tokens of work in a single step. Slotting that into a batch makes that
one step **far longer** than a normal decode step, so every other request's next
token is delayed — a visible latency spike (a stutter in streamed output). The
prefill is *one big compute spike sitting on top of everyone's decode*.

**The idea.** Don't do the whole prefill at once. Choose a chunk size $C$ (a
token budget per step) and split the $P$-token prompt into $\lceil P/C\rceil$
chunks. Process **one chunk per step**, and fill the rest of that step's token
budget with other requests' decode tokens. Every step then carries about $C$
tokens of work total — bounded and roughly constant — instead of alternating
between cheap decode steps and one giant prefill step.

**Why it's exactly correct (the key insight).** Splitting the prompt must not
change the answer, and it doesn't — because [[transformer-attention]] is
**causal**: token $i$ only attends to tokens $1..i$, never to later ones. So what
a token needs from its context is *entirely to its left*. The [[kv-cache]] holds
exactly that left context as $K,V$ columns. When we process chunk $k$, two things
hold:

1. Every token *before* chunk $k$ has already had its $k,v$ written to the cache
   by an earlier chunk's step. So a token in chunk $k$ can attend over all of its
   real left context: the cached columns **plus** the earlier tokens within
   chunk $k$ itself.
2. Tokens *after* chunk $k$ are never attended to by chunk $k$'s tokens anyway
   (causality), so it is irrelevant that they haven't been processed yet.

Therefore each token's query sees the **same** set of keys/values whether the
prompt was processed whole or in chunks. The $q,k,v$ projections are per-token
and context-independent, and the attention sum is over the same columns — so the
keys, values, and outputs written are **bit-identical**. Chunking is a *scheduling*
change, not a *math* change. (Tokens within one chunk still attend to each other
in that chunk's step, exactly as in a full prefill — the chunk boundary is not an
attention boundary, only a step boundary.)

**Worked instance.** Prompt of $P=9$ tokens $t_1..t_9$, chunk size $C=3$, so
3 chunks: $A=\{t_1,t_2,t_3\}$, $B=\{t_4,t_5,t_6\}$, $D=\{t_7,t_8,t_9\}$. Write
$\text{cache}=m$ to mean the [[kv-cache]] holds columns for tokens $t_1..t_m$.

- **Step P1 — chunk $A$.** Cache starts empty ($m=0$). Compute $q,k,v$ for
  $t_1,t_2,t_3$; append their 3 $k,v$ columns. Inside the step, $t_1$ attends to
  $\{t_1\}$, $t_2$ to $\{t_1,t_2\}$, $t_3$ to $\{t_1,t_2,t_3\}$ (causal mask).
  Cache now $m=3$.
- **Step P2 — chunk $B$.** Cache holds $t_1..t_3$. Compute $q,k,v$ for
  $t_4,t_5,t_6$; append 3 columns. $t_4$ attends to the **3 cached** columns plus
  itself $=\{t_1..t_4\}$; $t_6$ attends to $\{t_1..t_6\}$. Cache now $m=6$.
- **Step P3 — chunk $D$.** Cache holds $t_1..t_6$. $t_7$ attends to
  $\{t_1..t_7\}$, …, $t_9$ to $\{t_1..t_9\}$. Cache now $m=9$ — identical to what
  a single 9-token prefill would have produced. Decode of $t_{10}$ proceeds
  normally from here.

Check the invariant on $t_5$: its real left context is $t_1..t_5$. In the chunked
run it sees $t_1..t_3$ from the cache (written in P1) and $t_4,t_5$ from its own
step — exactly $t_1..t_5$. Nothing missing, nothing extra.

**The schedule, quantified.** Measure a step's load in *tokens processed* (a fair
proxy here: prefill work scales with tokens, and one decode token costs $\approx 1$
token-unit). Suppose request **X** has a 9-token prompt to prefill, while
requests **Y** and **Z** are each decoding (1 token/step).

*Unchunked* — X's prefill is one spike:

| Step | X | Y | Z | Step load |
|------|----|----|----|-----------|
| 1 | prefill all 9 | decode 1 | decode 1 | **11** |
| 2 | decode 1 | decode 1 | decode 1 | 3 |
| 3 | decode 1 | decode 1 | decode 1 | 3 |

Step 1 is $\approx 3.7\times$ a normal step — Y and Z stutter while X prefills.

*Chunked* ($C=3$, with a per-step token budget of, say, 5; the 3-token chunk
leaves room for 2 decode tokens):

| Step | X | Y | Z | Step load |
|------|------------|----------|----------|-----------|
| 1 | prefill $A$ (3) | decode 1 | decode 1 | **5** |
| 2 | prefill $B$ (3) | decode 1 | decode 1 | **5** |
| 3 | prefill $D$ (3) | decode 1 | decode 1 | **5** |

Same total work (9 prefill + 6 decode = 15 token-units both ways), but the peak
step load drops from **11 to 5**, and every step is identical — Y and Z see a
steady, bounded latency instead of one 11-unit stall. That is the smoothing:
chunked prefill trades a tall spike for a longer flat plateau, capping per-step
latency at the chunk budget while leaving the final result untouched.

## Prerequisites

- [[kv-cache]]
- [[transformer-attention]]

## Sources

_none_
