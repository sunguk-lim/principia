---
id: moe-routing
title: MoE Routing
summary: Routing is the decision mechanism inside a mixture-of-experts layer that chooses which experts each token is sent to.
type: concept
tags: [ml/llm/architecture]
prereqs: [mixture-of-experts, softmax]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# MoE Routing

## Summary

**Routing** is the decision mechanism inside a [[mixture-of-experts]] layer that
chooses **which** experts each token is sent to. A small learned matrix — the
**router** (or **gate**) — scores every expert for the token, a softmax turns those
scores into weights, and **top-K selection** sends the token to only its few
highest-scoring experts, whose outputs are then combined weighted by those gate
scores. The central difficulty is **load imbalance**: left to itself the router
piles most tokens onto a handful of "hot" experts and starves the rest. Three fixes
counter this — an **auxiliary load-balancing loss** that penalizes uneven usage, a
**capacity factor** that caps how many tokens an expert will accept, and **token
dropping** when an expert overflows. Balanced routing is what lets the sparse layer
actually use all its parameters and stay efficient on parallel hardware.

## Grounded explanation

A [[mixture-of-experts]] layer holds many independent feed-forward sub-networks
(the **experts**) but runs only a few of them per token. **Routing** is the part
that decides *which* few. It is the layer's steering wheel: everything the
[[mixture-of-experts]] promises — large capacity at small per-token compute —
depends on this choice being made well.

**The router (gate).** Each token enters the layer as a **hidden vector** $h$: the
list of numbers the model currently holds for that token. The router is a single
small learned matrix, written $W_{\text{gate}}$, with one row per expert. Multiplying
it by the token gives one raw **score** per expert, $W_{\text{gate}} \cdot h$ — how
well each expert "fits" this token, as judged by weights the model learned during
training. These raw scores are unbounded and need not be positive, so a **[[softmax]]**
(a function that exponentiates each score and divides by the total, yielding positive
numbers that sum to 1) converts them into **gate weights**: a clean set of
preferences, each between 0 and 1, adding up to 1 across all experts.

**Top-K selection.** The layer does not run every expert. It keeps only the $K$
experts with the largest gate weights — almost always $K=1$ or $K=2$ — and ignores
the rest. The token is then processed only by those $K$ experts, and their outputs
are blended in proportion to the kept gate weights (renormalized so the kept weights
again sum to 1). This is the step that makes the layer **sparse**: total work per
token scales with $K$ (a small fixed number), not with the full expert count, which
is exactly the efficiency the [[mixture-of-experts]] exists to deliver.

**Worked instance (top-2).** Take $K=2$ and a token whose [[softmax]] gate weights over
three experts come out as $E_1 = 0.5$, $E_2 = 0.3$, $E_3 = 0.2$. Top-2 keeps the two
largest, $E_1$ and $E_2$, and drops $E_3$. The kept weights $0.5$ and $0.3$ sum to
$0.8$, so they are **renormalized** by dividing by $0.8$: $E_1$ becomes
$0.5 / 0.8 = 0.625$ and $E_2$ becomes $0.3 / 0.8 = 0.375$ (these now sum to 1). The
layer's output for this token is $0.625$ times $E_1$'s output plus $0.375$ times
$E_2$'s output. Expert 3 never runs for this token.

**The load-imbalance problem.** Routing has a damaging failure mode. Because the gate
weights also serve as the training signal, an expert that wins a few tokens early gets
trained on them, gets better at them, and so scores higher and wins *more* tokens — a
feedback loop. Left unchecked the router **collapses** onto a small set of favorite
("hot") experts that receive most of the traffic, while the remaining experts stay
"cold," barely trained, and effectively wasted. That defeats the whole purpose of a
[[mixture-of-experts]]: its many parameters sit idle while a few experts do all the
work, and on parallel hardware the GPUs holding cold experts stall while the GPU
holding the hot expert is overwhelmed.

**Fix 1 — auxiliary load-balancing loss.** During training the model optimizes a main
objective (predicting the next token). Routing adds a second, *auxiliary* penalty term
to that objective: a number that grows when expert usage is uneven and shrinks when it
is even. Minimizing it nudges the router to spread tokens out, counteracting the
collapse — the model is rewarded for keeping every expert busy, not just for predicting
well.

**Fix 2 — capacity factor.** A hard cap, used especially at inference (when the loss is
no longer being optimized). Each expert is allotted a fixed maximum number of tokens
per batch — roughly the average fair share multiplied by the **capacity factor** (e.g.
$1.25$ gives a 25% cushion above the even split). Beyond that cap an expert simply
refuses more tokens, so no single expert can monopolize the batch.

**Fix 3 — token dropping.** When an expert hits its cap, the overflowing tokens have to
go somewhere. The simplest answer is to **drop** them: that expert does not process them
this layer, and they pass through unchanged (or get rerouted to a less-loaded expert).
A dropped token loses the benefit of that layer's experts, which is a small accuracy
cost — accepted in exchange for keeping the load even and the hardware efficient.

**Worked instance (imbalance).** Suppose a batch of tokens. With **no** auxiliary loss,
the router has collapsed: 80% of tokens score expert $E_1$ highest, so $E_1$ is wildly
over its capacity. With a capacity factor of $1.25$, $E_1$ can accept only a quarter
again above its fair share, so the excess — a large fraction of that 80% — is **dropped**
or rerouted, and those tokens go unserved by $E_1$. Now add the **auxiliary
load-balancing loss**: it penalizes that 80% concentration during training, the router
learns to spread the same tokens roughly evenly across all experts, each expert lands
near its fair share, almost nothing exceeds the capacity cap, and almost nothing is
dropped. Same tokens, same experts — only the routing changed, and that is the difference
between a wasted layer and a working one.

The **why**, in one line: routing is the mechanism that turns a pile of experts into a
usable [[mixture-of-experts]] — and the balancing machinery (loss, capacity, dropping)
is what keeps that mechanism from quietly sabotaging itself.

## Prerequisites

- [[mixture-of-experts]]
- [[softmax]]

## Sources

_none_
