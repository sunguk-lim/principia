---
id: prefix-caching
title: Prefix Caching
summary: A kv-cache reuses keys and values within one sequence as it grows.
type: concept
tags: [ml/llm/inference]
prereqs: [kv-cache]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Prefix Caching

## Summary

A [[kv-cache]] reuses keys and values **within one sequence** as it grows. **Prefix
caching** reuses them **across sequences**: when many requests begin with the
*identical* token sequence — a shared system prompt, a few-shot preamble, or the
frozen history of a chat — that shared **prefix** produces the *same* `K`/`V`
every time. So you compute the prefix's `K`/`V` **once**, store it, and hand a
copy to every later request that starts the same way. Each such request skips the
expensive **prefill** (the bulk pass that processes the prompt before any token is
generated) over the shared part and only prefills the **suffix** where it differs.
The licensing fact is causality: a token's key and value depend on the tokens **at
or before it** — never on what comes after — so two prompts that agree on their
first $p$ tokens have bit-identical `K`/`V` for those $p$ tokens regardless of how
they continue.

## Grounded explanation

**The concept.** Prefix caching is a cache *keyed by token-sequence prefix* that
sits in front of generation and is shared across requests. Its central object is a
stored block of `K`/`V` columns for a specific prefix, tagged by the exact tokens
that produced it; its contribution is letting a new request **adopt** that block as
the start of its own [[kv-cache]] instead of recomputing it.

**Where the cost is, and why this helps.** Serving a prompt has two phases. In
**prefill** the model ingests the whole prompt at once and computes a `K`/`V` column
for *every* prompt token — this is the heavy phase, growing with prompt length. Then
**decoding** emits tokens one at a time, each appending one column (this is exactly
what the [[kv-cache]] optimizes within a single sequence). If a 2000-token system
prompt is glued in front of every user request, plain [[kv-cache]] still pays the
full 2000-token prefill *anew* for each request, because a fresh sequence starts
with an empty cache. That repeated prefill is the waste prefix caching removes.

**The invariant that licenses reuse.** In [[kv-cache]] we relied on a token's `K`/`V`
being *frozen* once computed, because attention is **causal**: token $t$ attends only
to tokens $1..t$, so $k_t$ and $v_t$ are functions of the tokens at positions $1..t$
**and nothing later**. Push that one step further. Take two *different* requests,
A and B, whose first $p$ tokens are literally the same token IDs in the same order.
For any position $j \le p$, the inputs that determine $k_j$ and $v_j$ — the tokens at
$1..j$ — are identical between A and B. The model weights are the same. Therefore

> $k_j^{A} = k_j^{B}$ and $v_j^{A} = v_j^{B}$ for every $j \le p$.

These are **equal values, not merely similar** — the same arithmetic on the same
inputs. Whatever A and B do *after* position $p$ cannot reach back to change a
causal token's key or value. So the first $p$ columns of A's `K`/`V` cache and the
first $p$ columns of B's are bit-identical. Computing them twice is provably
redundant; computing them once and copying is provably correct. (The equality holds
per layer and per head, so the stored block is the prefix's columns across **all**
layers — the same shape the [[kv-cache]] would have built.)

**The mechanism.** Maintain a store mapping a prefix (its exact token sequence) to
the `K`/`V` columns it produces. On a new request: find the **longest stored prefix**
that matches the request's leading tokens; load those columns straight into the
request's [[kv-cache]] as columns $1..p$; then run prefill **only** on the suffix —
the tokens from $p+1$ onward — which appends columns $p+1, p+2, \dots$ in the usual
way. Decoding then proceeds exactly as a normal [[kv-cache]] would, oblivious to
where its early columns came from. The first request that ever sees a given prefix
pays full price and *populates* the store; everyone after it pays only for their
suffix.

**Worked instance (non-degenerate: both requests have a real, differing suffix).**
Shared system prompt = 4 tokens: `["You", "are", "a", "helper"]`. Two requests:

- **A** = system prompt + `["What", "is", "2+2", "?"]` → 8 tokens total.
- **B** = system prompt + `["Translate", "hi"]` → 6 tokens total.

Process **A first**. Its cache is empty, so prefill runs over all 8 tokens and
produces 8 `K`/`V` columns. We store the first $p=4$ columns under the key
`["You","are","a","helper"]`.

Now process **B**. Its leading tokens `["You","are","a","helper"]` match the stored
key exactly, so columns $1..4$ of B's cache are loaded from the store. By the
invariant, those four columns equal what B's own prefill *would* have produced —
column $j$ of B's K-cache equals column $j$ of A's K-cache for $j=1..4$, value by
value. Prefill for B then runs over only its 2 suffix tokens `["Translate","hi"]`,
appending columns 5 and 6. B never recomputes a single column of the system prompt.

**Quantify the saving.** Counting prefill as the number of token-columns whose
`K`/`V` must be computed:

| | columns computed for A | columns computed for B | total |
|---|---|---|---|
| No prefix cache | 8 | 6 | **14** |
| With prefix cache | 8 | 2 | **10** |

B's prefill drops from 6 columns to 2 — the 4 shared columns are reused, not
recomputed. The saving is exactly the shared-prefix length, and it scales with how
*long* the shared prefix is and how *many* requests share it: a 4-token preamble
saves little, but a 2000-token system prompt reused across 1000 requests saves
$2000 \times 999 \approx 2{,}000{,}000$ columns of prefill — the difference between
recomputing the preamble a thousand times and computing it once.

**Distinguish from plain [[kv-cache]].** Same equality, different scope. The
[[kv-cache]] reuses a token's `K`/`V` *across decode steps within one sequence*;
prefix caching reuses them *across separate sequences that share a leading prefix*.
[[kv-cache]] never crosses a request boundary (each request starts empty); prefix
caching is precisely the bridge that lets the frozen columns survive that boundary.

**In practice.** Serving systems implement this as **automatic prefix caching**
(e.g. vLLM): the engine hashes prefixes of incoming prompts, transparently detects
the longest match against already-cached `K`/`V` blocks, reuses them, and prefills
only the divergent tail — with no change to the request, since the invariant
guarantees the answer is identical to a full recompute.

## Prerequisites

- [[kv-cache]]

## Sources

_none_
