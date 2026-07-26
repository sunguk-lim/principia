---
id: mamba
title: Mamba
summary: "Mamba is a selective state-space-model: it keeps the SSM's linear recurrence and its fixed-size state, but makes the input map $B$, the output map $C$, and the per-step \"step…"
type: concept
tags: [ml/llm/architecture]
prereqs: [state-space-model]
sources:
  - "Gu & Dao, Mamba: Linear-Time Sequence Modeling with Selective State Spaces (2023), arXiv:2312.00752"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Mamba

## Summary

**Mamba** is a **selective** [[state-space-model]]: it keeps the SSM's linear recurrence
and its fixed-size state, but makes the input map $B$, the output map $C$, and the
per-step "step size" $\Delta$ **functions of the current input** $x_t$ instead of fixed
numbers. A plain SSM uses the *same* $A, B, C$ at every position, so it processes a token
the same way no matter what the token is — it is **content-blind**. Mamba lets each token
choose how strongly it writes to the state: a token can use a large step to *seize* the
state (remember itself) or a near-zero step to *slide past* it (forget itself). This
recovers the content-based "decide what matters" power that made attention strong, while
keeping the SSM's $O(n)$ cost and $O(1)$ state. The price is that input-dependent parameters
break the time-invariance, so the fixed-kernel convolution form no longer exists; Mamba
instead runs the recurrence with a hardware-aware **parallel scan**.

## Grounded explanation

### What Mamba adds to a plain SSM

Recall the [[state-space-model]] recurrence, applied at every step $t$ with state $h$,
input $x_t$, and the maps $A$ (state-transition), $B$ (input), $C$ (output):

$$h_t = A\,h_{t-1} + B\,x_t, \qquad y_t = C\,h_t.$$

In a plain SSM the matrices $A, B, C$ are **fixed across all time steps** — learned once,
then reused identically at position $1$ and position $3{,}000$. That fixedness is what let
the SSM unroll into a single **convolution kernel** $k_k = C A^k B$ that is the same for
every position (the "two equivalent forms" of the prerequisite). Being the same everywhere
has a hidden cost, and that cost is the whole motivation for Mamba.

Two more pieces of standard SSM notation that Mamba leans on:

- **Step size $\Delta$** (🟦 scalar, also called the *discretization step* or "delta"):
  before the recurrence runs, the continuous-time maps are converted to the discrete
  per-step maps used above. The conversion makes the effective state-transition
  $\bar{A} = e^{\Delta A}$ and the effective input map $\bar{B} \approx \Delta B$. The intuition
  you need is simple: **$\Delta$ is a volume knob on how much the current input is allowed to
  enter and refresh the state.** A large $\Delta$ means "this step matters a lot — write it
  in hard and reset the old state's grip"; a small $\Delta \to 0$ means "barely change the
  state — let it coast." (I use $\bar{A}, \bar{B}$ for the discretized maps to keep them
  distinct from the raw $A, B$.)

In a plain SSM, $\Delta$ is also **fixed** — one learned constant for the whole sequence.

**Mamba's one structural change:** make $B$, $C$, and $\Delta$ **depend on the current
input** $x_t$. Write them as $B_t = B(x_t)$, $C_t = C(x_t)$, $\Delta_t = \Delta(x_t)$, each
produced by a small linear map from $x_t$. ($A$ stays input-independent.) The recurrence
becomes

$$h_t = \bar{A}_t\,h_{t-1} + \bar{B}_t\,x_t, \qquad y_t = C_t\,h_t,$$

where $\bar{A}_t = e^{\Delta_t A}$ and $\bar{B}_t \approx \Delta_t B_t$ now **change from step
to step because the input changes.** That input-dependence is the entire concept; everything
else is the SSM you already know. This property is called **selectivity** — the model can
*select*, per token, what to keep and what to drop.

### The WHY: content-blindness, and how selectivity fixes it

Here is the key insight, and why fixed-everywhere is a real limitation.

Because a plain SSM applies the identical kernel $k_k = C A^k B$ at every position, its
behavior depends only on **where** an input sits relative to now (the lag $k$), never on
**what** the input is. The state decays at one universal rate. So consider a sequence with a
few important tokens buried in a long run of filler ("um", padding, repeated words). A fixed
SSM has no mechanism to treat the important token differently from the filler: each token is
multiplied into the state through the *same* $B$ and decayed by the *same* $A$. It must
either keep everything (and let the important token's signal get diluted by hundreds of
filler tokens) or decay fast (and forget the important token along with the filler). It
cannot say "remember *this* word, ignore *those*." That is what content-blind means, and it
is the direct consequence of time-invariance — the very property that gave us the convolution
form.

Attention does not have this problem: it compares the actual content of every pair of
positions, so it can route information based on what tokens *are*. But it pays $O(n^2)$ for
that, re-scanning the whole past at every step. Mamba's goal is to get the content-based
"decide what matters" behavior **without** paying $O(n^2)$.

Selectivity buys exactly that. Make $\Delta_t$ depend on $x_t$, and each token controls its
own write strength:

- **A "keep" token** sets $\Delta_t$ **large**, so $\bar{B}_t \approx \Delta_t B_t$ is large
  (the token is written hard into the state) and $\bar{A}_t = e^{\Delta_t A}$ pushes the old
  state strongly through $A$ — the state is **refreshed around this token**.
- **A filler token** sets $\Delta_t \approx 0$, so $\bar{B}_t \approx 0$ (it barely enters the
  state) and $\bar{A}_t = e^{0} = 1$ (the state is carried forward **unchanged**) — the token
  **slides past** and the state simply remembers what it already held.

So a small $\Delta_t$ is a *gate that says "forget me, preserve the past"* and a large
$\Delta_t$ is a *gate that says "remember me."* Input-dependent $B_t, C_t$ add the same
content-control to how the input is written in and read out. This is the content-based
reasoning of attention, recovered inside a recurrence that is still $O(n)$ total time with an
$O(1)$-size state.

### The cost: no more convolution, so use a parallel scan

There is no free lunch, and the lost property is precise. The convolution form existed only
because the kernel $k_k = C A^k B$ was the **same at every position** — that sameness
(time-invariance) is exactly what input-dependent $B_t, C_t, \Delta_t$ destroy. Once
$\bar{A}_t, \bar{B}_t, C_t$ vary with the token, there is no single fixed kernel, and the
parallel-convolution training shortcut from the prerequisite is gone.

But the recurrence $h_t = \bar{A}_t h_{t-1} + \bar{B}_t x_t$ is *still linear* in the state,
and a chain of linear updates can be evaluated by a **parallel scan**: an associative
combine that computes all the partial $h_t$ in $O(\log n)$ parallel depth (and $O(n)$ total
work) rather than $n$ strictly sequential steps. Mamba implements this as a **hardware-aware**
scan — it keeps the state in the GPU's fast on-chip memory and avoids writing the large
per-step $\bar{A}_t, \bar{B}_t$ out to slow memory — so even though the convolution is gone,
training stays fast and the overall cost stays linear in $n$. So Mamba trades the convolution
trick for a scan, and in exchange gets selectivity. That trade is the design.

### A worked instance — fixed SSM vs. selective Mamba

Reuse the scalar SSM of the prerequisite: state, input, output all scalar, with
$A = -1$ (chosen so the continuous-time map decays; recall $\bar{A} = e^{\Delta A}$),
$B = 1$, $C = 1$, $h_0 = 0$. Feed a 4-token sequence

$$x = [\,5,\ 0.1,\ 0.1,\ 0.1\,],$$

i.e. **one important token ($x_1 = 5$, "keep this") followed by three filler tokens**
($\approx 0.1$). The question both models must answer: *does the state still remember the 5
after the filler?*

**Fixed SSM** — one constant step for all tokens, say $\Delta = 1$. Then for every step
$\bar{A} = e^{\Delta A} = e^{-1} \approx 0.37$ and $\bar{B} \approx \Delta B = 1$:

- $h_1 = 0.37(0) + 1(5) = 5.00$
- $h_2 = 0.37(5.00) + 1(0.1) = 1.95$
- $h_3 = 0.37(1.95) + 1(0.1) = 0.82$
- $h_4 = 0.37(0.82) + 1(0.1) = 0.40$

The state holds $5.00$ right after the keep token, but because **every** token (filler
included) decays it by the same $0.37$, the memory of the $5$ erodes to $0.40$ after just
three filler steps — and the tiny filler inputs leak in too. The model had no way to say "the
filler should not have disturbed the state." That is content-blindness in numbers.

**Selective Mamba** — let $\Delta_t$ depend on $x_t$: large when the token is important,
near zero when it is filler. Concretely set $\Delta_t = 2$ for the keep token and
$\Delta_t = 0.01$ for filler. Then $\bar{A}_t = e^{\Delta_t A}$ and $\bar{B}_t \approx \Delta_t B$
become **per-token**:

- token 1 ($x_1 = 5$, $\Delta_1 = 2$): $\bar{A}_1 = e^{-2} \approx 0.14$, $\bar{B}_1 = 2$
  $\Rightarrow h_1 = 0.14(0) + 2(5) = 10.0$
- token 2 ($x_2 = 0.1$, $\Delta_2 = 0.01$): $\bar{A}_2 = e^{-0.01} \approx 0.99$,
  $\bar{B}_2 = 0.01$ $\Rightarrow h_2 = 0.99(10.0) + 0.01(0.1) \approx 9.90$
- token 3 (filler, $\Delta_3 = 0.01$): $h_3 = 0.99(9.90) + 0.01(0.1) \approx 9.80$
- token 4 (filler, $\Delta_4 = 0.01$): $h_4 = 0.99(9.80) + 0.01(0.1) \approx 9.70$

Now contrast the trajectories:

| step | input $x_t$ | fixed-SSM state $h_t$ | Mamba state $h_t$ |
| --- | --- | --- | --- |
| 1 | 5 (keep) | 5.00 | 10.0 |
| 2 | 0.1 (filler) | 1.95 | 9.90 |
| 3 | 0.1 (filler) | 0.82 | 9.80 |
| 4 | 0.1 (filler) | 0.40 | 9.70 |

Same model family, same $A, B, C$, same inputs — the **only** difference is that Mamba let
$\Delta_t$ read the token. Because each filler token chose $\Delta_t \approx 0$, its
$\bar{A}_t \approx 1$ carried the state forward almost untouched and its $\bar{B}_t \approx 0$
let almost nothing new in: the state **preserves the memory of the 5** (drifting only from
$9.90$ to $9.70$ across three filler steps) instead of decaying it to $0.40$. The keep token,
by choosing a large $\Delta_1$, wrote itself in hard. That is selection: the content of each
token decided whether it refreshed the state or slid past it — and it cost the same $O(1)$
per-step recurrence as the plain SSM.

## Prerequisites

- [[state-space-model]]

## Sources

- Gu & Dao, *Mamba: Linear-Time Sequence Modeling with Selective State Spaces* (2023), arXiv:2312.00752
