---
id: tree-search-decoding
title: Tree-Search Decoding
summary: "Tree-search decoding is a concrete way to spend test-time-compute: instead of producing one reasoning chain left-to-right and committing to each next step as it comes, you treat…"
type: concept
tags: [ml/llm/reasoning]
prereqs: [test-time-compute]
sources:
  - "Yao et al. 2023, Tree of Thoughts: Deliberate Problem Solving with Large Language Models (arXiv:2305.10601)"
  - "Cobbe et al. 2021, Training Verifiers to Solve Math Word Problems (arXiv:2110.14168) — best-of-N verifier reranking"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Tree-Search Decoding

## Summary

**Tree-search decoding** is a concrete way to *spend* [[test-time-compute]]: instead
of producing one reasoning chain left-to-right and committing to each next step as it
comes, you treat generation as a **search over a tree of partial continuations**. At a
choice point you **branch** into several candidate next-steps, **score** each candidate
(with a verifier, a reward model, a self-evaluation prompt, or — at the end — agreement
of final answers), **keep** the promising branches and **prune** the rest, and repeat.
The number of branches you explore *is* the amount of inference compute you pay; a
*scorer* is what converts that compute into accuracy, by selecting good paths that a
greedy left-to-right decode would have thrown away. The family spans a spectrum by how
much of the tree you keep: **best-of-N** (N independent full chains, score them, pick
the best — a depth-1 tree), **beam search** (keep the top-$b$ partial sequences by
cumulative score as you grow them step by step), and **full tree search / Tree-of-Thoughts**
(branch and backtrack over reasoning steps, with an explore-vs-exploit policy for hard
math and planning). Branching width sets the budget; pruning keeps it affordable.

## Grounded explanation

**The starting point and the problem it leaves open.** From [[test-time-compute]] we
have the core idea: a model with frozen weights can be made more accurate by doing
*more work per query at inference*, and the natural way to do that work is to generate
reasoning tokens — each token its own forward pass, the written text serving as memory
the later passes attend to. But that node mostly described generating tokens *in a
straight line*: one long chain, decided one token at a time. Decoding one token at a
time means that at every step the model picks *one* next token (greedily, the
highest-probability one) and never reconsiders. That is a **single root-to-leaf walk**:
commit, commit, commit, never look back. The trouble is that a step which looks best
*locally* — highest probability right here — can lead into a dead end, while a
locally-worse step opens onto the *globally* best solution. A straight-line decode has
no way to recover from such an early wrong turn: the good path was discarded the instant
it was not the top choice. Tree-search decoding is the concept that fixes exactly this,
and it is a distinct way to spend the test-time budget.

**The central object: generation as a tree, not a line.** Picture every partial
output as a **node** in a tree. The **root** is the empty continuation (just the
problem). From any node, the possible *next steps* — next tokens, or next whole
reasoning steps — are its **children**; a path from the root down to a finished answer
is a complete generation. A straight-line greedy decode walks *one* path of this tree,
always taking the single most-probable child. Tree-search decoding instead **keeps
several paths alive at once** and decides among them using a score, not just local
probability. Three verbs define the mechanism:

- **Branch (expand).** At a node, generate *several* candidate children instead of one —
  e.g. sample $k$ different next steps. This is where compute is spent: each child is
  more forward passes.
- **Score.** Attach a number to a node (or to a finished path) saying how promising it
  is. The scorer can be a separate **verifier** model trained to predict "does this
  reasoning lead to a correct answer?", a **reward model**, the model **judging its own**
  partial work via a prompt ("rate this step's plausibility 0–1"), or, for completed
  chains, **agreement among final answers** (the majority-vote idea from
  [[test-time-compute]], now used to rank rather than just tally).
- **Prune (select).** Discard low-scoring nodes; keep only the top few. This is the
  budget control: without pruning the tree grows exponentially and compute explodes.

**Why it works — the key insight.** Two ingredients must both be present, and the
concept is precisely their combination. (1) *Exploring more candidates raises the
chance the right path is somewhere in what you looked at.* If the correct solution
requires a first step the model only assigns, say, 30% probability, a greedy decode
that takes the 70% step never even visits it; branching into the top few steps does.
(2) *A scorer lets you actually pick that path out of the pile.* Exploration alone is
useless if you can't tell good from bad at the end — you would just have many chains and
no way to choose. The scorer is the load-bearing, "magic-looking" part, so it deserves
its justification: the model's *local* next-token probability is a poor judge of whether
a partial path will ultimately succeed (that is the whole reason greedy fails), but a
*verifier* — which gets to look at more of the reasoning, or even the final answer — is
a far better judge of eventual correctness. Tree search routes compute toward the
branches the verifier rates highly, so the extra forward passes are not spent uniformly;
they are spent where a *better* judgment says success is likely. That is how raw
inference compute (more nodes expanded) is converted into accuracy (a correct path
selected). The invariant the search maintains is: *at all times the kept set contains
the most promising partial solutions found so far,* so the answer you finally read off
is the best the scorer could find within the compute you paid — never just the first
greedy guess.

**Compute is nodes expanded; width is the dial.** Every node you expand is forward
passes, so **nodes expanded = test-time compute**, in the same currency
[[test-time-compute]] measures (generated tokens / passes). The concept gives you a knob:
**branching factor** (how many children per node) times **how many you keep after
pruning** (the *beam width* $b$, or the $N$ of best-of-N) times **depth** (how many steps
deep you search). Crank these up and you explore more of the tree and tend to find
better answers; crank them down and you save compute. Pruning is what keeps the bill
linear instead of exponential: a beam of width $b$ over depth $d$ with $k$ candidates
per step expands about $b \times k \times d$ nodes, not $k^d$.

**The spectrum — three points on one idea.** The family differs only in *how much of
the tree is kept alive*:

| Method | Tree shape | What is kept | Scorer used |
|---|---|---|---|
| **Best-of-N** | depth-1: $N$ full chains from the root | all $N$ to the end, then pick 1 | score *finished* chains (verifier / agreement) |
| **Beam search** | grow step by step | top-$b$ *partial* sequences by cumulative score | score each partial as it grows |
| **Tree-of-Thoughts / full search** | branch *and* backtrack over reasoning steps | a frontier, with revisiting of abandoned nodes | self-evaluation per step + explore/exploit policy |

Best-of-N never branches *mid-chain* (it's the shallowest, simplest case: throw many
darts, keep the best). Beam search prunes continuously as it grows, so it can let a
locally-worse first step survive *because its cumulative score stays competitive*. Full
tree search adds **backtracking** and an explore-vs-exploit rule (try the
currently-best-looking branch, but also occasionally probe under-explored ones, so the
search doesn't commit too early on a misleading early score) — the heaviest spend,
reserved for hard reasoning and planning.

**Worked instance, part A — best-of-N, $N=4$.** Take a problem and sample $N=4$
*independent, complete* reasoning chains (a depth-1 tree: four leaves hanging off the
root). A trained **verifier** scores each finished chain in $[0,1]$ = "probability this
chain's answer is correct":

| Chain | Verifier score |
|---|---|
| 1 | 0.2 |
| 2 | **0.9** |
| 3 | 0.3 |
| 4 | 0.5 |

We *select* the argmax — chain 2, score 0.9 — and return its answer. Note this is
strictly stronger than majority vote: even if chains 1, 3, 4 happened to agree on a
*wrong* answer (a 3–1 majority), the verifier's 0.9 on chain 2 overrides the popular-but-wrong
bloc. Compute spent: 4 chains expanded; if each chain is ~30 tokens, that is ~120 tokens
— four times a single decode, the price of the search.

**Worked instance, part B — beam search width $b=2$ over 2 steps, where greedy
loses.** This shows the thing best-of-N can't: rescuing a path by a *locally-worse*
first step. Each "step" is a reasoning move; the score on a node is a running
("cumulative") self-evaluation in $[0,1]$, higher = more promising. From the root,
expand candidate first steps. Suppose their step-scores are:

```
root
 ├─ step A   (local score 0.7)
 └─ step B   (local score 0.4)
```

A **greedy** decode keeps only the single best, **A (0.7)**, and discards B. A **beam of
width $b=2$** keeps the top *two* partials — **both A and B survive** the first prune.
Now expand each surviving node's best continuation and accumulate (sum the step-scores
along the path):

```
A → A2   path score 0.7 + 0.2 = 0.9
B → B2   path score 0.4 + 0.8 = 1.2
```

The cumulative winner is **B → B2 at 1.2**, beating **A → A2 at 0.9**. The globally-best
sequence began with the *locally-worse* step B (0.4 < 0.7) — exactly the path greedy
threw away at step 1. Because the beam *kept* B alive past the first prune, the search
finds it; greedy never could. Compute spent: with $b=2$, $k=2$ candidates per step,
depth $d=2$, about $b \times k \times d = 2 \times 2 \times 2 = 8$ nodes expanded —
versus 2 for a greedy walk. That 4× more expansion is the test-time compute, and it is
what bought the better answer.

**Tie-back.** Both parts are one lesson and it is the lesson of [[test-time-compute]]
seen through a tree: pay more inference compute (more nodes expanded), and use a *scorer*
to turn that payment into accuracy by keeping good paths a greedy decode would prune.
Best-of-N is the depth-1 corner of this idea; beam search keeps a width-$b$ frontier of
partials; Tree-of-Thoughts searches and backtracks over whole reasoning steps. Branching
buys candidates, the scorer picks the winner, and pruning keeps the budget finite.

## Prerequisites

- [[test-time-compute]]

## Sources

- Yao, S. et al. (2023). *Tree of Thoughts: Deliberate Problem Solving with Large
  Language Models.* arXiv:2305.10601.
- Cobbe, K. et al. (2021). *Training Verifiers to Solve Math Word Problems.*
  arXiv:2110.14168 (best-of-N verifier reranking).
