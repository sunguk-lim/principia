---
id: state-space-model
title: State Space Model
summary: "A state space model (SSM) is a sequence model that carries a fixed-size hidden state forward in time by a learnable linear recurrence: at each step the state is a weighted blend…"
type: concept
tags: [ml/llm/architecture]
prereqs: [neural-network]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# State Space Model

## Summary

A **state space model (SSM)** is a sequence model that carries a fixed-size
**hidden state** forward in time by a *learnable linear recurrence*: at each step the
state is a weighted blend of the previous state plus the new input, and the output reads
out from the state. Because the recurrence is **linear**, the same model has two exactly
equivalent forms — a cheap step-by-step recurrence for generating one token at a time, and
a single fixed convolution kernel that processes the whole sequence in parallel for
training. Its defining virtue is that the state has a *fixed size regardless of sequence
length*, so cost and memory per step stay constant as the sequence grows.

![Animated 4-step figure (STEP 0/4→4/4 on one master clock) of the SSM recurrence h_t = A·h_{t-1} + B·x_t, y_t = C·h_t + D·x_t: a fixed params sidebar (A=0.5, B=2, C=3, D=0), inputs x=[1,0,2] traced step by step with full on-canvas arithmetic (h₁=2→y₁=6; the degenerate x₂=0 step showing the state carrying x₁'s echo, y₂=3; h₃=4.5→y₃=13.5), a red state value travelling the persistent register with the active combine node gold-ringed and a prominent STEP n/4 + per-step caption at each step, and a closing convolution panel proving the same y=[6,3,13.5] emerges from the equivalent convolution form.|960](state-space-model.svg)

## Grounded explanation

### What it is, and why it is not just a neural network

A [[neural-network]] maps one input to one output: feed it $x$, it returns $f(x)$. It has
no built-in notion of *sequence* or *carried memory* — show it the tenth word of a sentence
and it has forgotten the first nine. A state space model adds exactly that missing piece: a
**state** $h$ that persists from one step to the next and summarizes everything seen so far
in a single fixed-size vector. The model *itself* is this recurrence; the linear maps inside
it could be supplied by neural-network weight matrices, but the concept here is the
**recurrence structure**, not the maps.

**Symbol table** (🟦 scalar · 🟩 vector · 🟧 matrix):

| Symbol | Type | Meaning |
| --- | --- | --- |
| $t$ | 🟦 | time step (position in the sequence), $t = 1, 2, \dots, n$ |
| $n$ | 🟦 | sequence length |
| $x_t$ | 🟩 | input at step $t$ (🟦 in the worked example below) |
| $h_t$ | 🟩 | hidden **state** after step $t$ (🟦 in the example) |
| $y_t$ | 🟩 | output at step $t$ (🟦 in the example) |
| $A$ | 🟧 | **state-transition** map: how much of the old state carries forward |
| $B$ | 🟧 | **input** map: how the new input enters the state |
| $C$ | 🟧 | **output** map: how the state is read out |
| $D$ | 🟧 | optional direct input-to-output map (a skip connection) |

The whole model is two equations, applied at every step:

$$h_t = A\,h_{t-1} + B\,x_t \qquad\qquad y_t = C\,h_t + D\,x_t$$

Read literally: the new state $h_t$ is the **old state scaled by $A$** (memory that decays
or persists) **plus the new input injected through $B$**; the output $y_t$ is the state
**read out through $C$** (plus, optionally, the raw input through $D$). The matrices
$A, B, C, D$ are *fixed across all time steps* and are the learned parameters. The state
$h$ never grows: whether you are at step $3$ or step $3{,}000$, $h$ is the same size. This
is the entire point — the model compresses an unbounded past into a bounded summary.

### The WHY: linearity buys two equivalent forms

The recurrence above is **autoregressive** — to get $h_t$ you need $h_{t-1}$, so it runs
left to right, one step at a time, with $O(1)$ work and memory per step. That is ideal for
*inference* (generating the next token), but it cannot be parallelized: step $t$ must wait
for step $t-1$.

Here is the non-obvious, magic-looking step. Because the recurrence is **linear** (no
nonlinearity sits between steps), we can unroll it in closed form. Starting from $h_0 = 0$:

$$h_t = \sum_{j=1}^{t} A^{\,t-j} B\, x_j, \qquad
  y_t = C h_t = \sum_{j=1}^{t} \big(C A^{\,t-j} B\big)\, x_j.$$

Each unrolled term is just the geometric chain of the recurrence: an input $x_j$ entered the
state through $B$ at step $j$, was multiplied by $A$ once per step for the $t-j$ steps since,
and was finally read out by $C$. **The justifying identity is the equation above**: the
output is a weighted sum of all past inputs, and the weight on the input that arrived
$k = t-j$ steps ago is

$$k_k = C A^{\,k} B.$$

These weights $(k_0, k_1, k_2, \dots) = (CB,\ CAB,\ CA^2B,\ \dots)$ depend only on the lag
$k$, not on absolute time. So the entire output sequence is a **convolution** of the input
with one fixed kernel — the same kernel for every position. That means we can compute *all*
$y_t$ in parallel during training (convolution over the whole sequence at once), then switch
to the cheap step-by-step recurrence at inference. **Recurrence and convolution are two
faces of the same model**, and linearity is exactly what makes them equal.

Contrast this with attention, which compares every position to every other and costs
$O(n^2)$. The SSM's recurrence is $O(n)$ total with $O(1)$ state — the past is summarized,
never re-scanned.

### A worked instance — the same $y$ two ways

Take a 1-D state (everything scalar) with $A = 0.5$, $B = 2$, $C = 3$, $D = 0$, input
$x = [\,1,\ 0,\ 2\,]$, and $h_0 = 0$. The branches to exercise: the $A$-decay of old state
must actually carry across at least two steps, a *zero* input must still propagate prior
state, and a later large input must mix with the decayed tail — this instance hits all
three.

**View 1 — recurrence**, step by step:

- $h_1 = A h_0 + B x_1 = 0.5(0) + 2(1) = 2,\quad\; y_1 = C h_1 = 3(2) = 6$
- $h_2 = A h_1 + B x_2 = 0.5(2) + 2(0) = 1,\quad\; y_2 = C h_2 = 3(1) = 3$
- $h_3 = A h_2 + B x_3 = 0.5(1) + 2(2) = 4.5,\; y_3 = C h_3 = 3(4.5) = 13.5$

Note $y_2 = 3$ even though $x_2 = 0$: the state still remembers $x_1$, decayed once by $A$.
And $y_3 = 13.5$ mixes the fresh $x_3 = 2$ with the twice-decayed echo of $x_1$. Output
$y = [\,6,\ 3,\ 13.5\,]$.

**View 2 — convolution** with the fixed kernel $k_k = C A^k B$:

$$k_0 = CB = 3 \cdot 2 = 6,\quad k_1 = CAB = 3(0.5)(2) = 3,\quad k_2 = CA^2B = 3(0.25)(2) = 1.5.$$

Now $y_t = \sum_{j=1}^{t} k_{t-j}\, x_j$:

- $y_1 = k_0 x_1 = 6(1) = 6$
- $y_2 = k_0 x_2 + k_1 x_1 = 6(0) + 3(1) = 3$
- $y_3 = k_0 x_3 + k_1 x_2 + k_2 x_1 = 6(2) + 3(0) + 1.5(1) = 13.5$

Identical: $y = [\,6,\ 3,\ 13.5\,]$. The kernel $1.5$ on $x_1$ in $y_3$ is precisely
$C A^2 B$ — the input from two steps back, decayed by $A$ twice — the same echo we saw in
the recurrence. One model, two equal computations: the recurrence for cheap generation, the
convolution for parallel training.

This linear-recurrence-plus-convolution structure is the foundation of modern long-sequence
architectures such as Mamba (handled by another node), which keep this core and make the
$A, B, C$ maps depend on the input.

## Prerequisites

- [[neural-network]]

## Sources

_none_
