---
id: roofline-model
title: Roofline Model
summary: The roofline model is a single picture that predicts the fastest a computation could possibly run on a given chip, and — more usefully — which limit is holding it back.
type: concept
tags: [ml/llm/inference]
prereqs: [memory-hierarchy]
sources:
  - "Williams, Waterman & Patterson, 'Roofline: An Insightful Visual Performance Model' (CACM 2009)"
  - "etc/llm_parallelism_strategies.jsx — ChunkedPrefill and MemoryMovement panels (memory-bound vs compute-bound, weight-load amortization)"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Roofline Model

## Summary

The roofline model is a single picture that predicts the *fastest a computation
could possibly run* on a given chip, and — more usefully — *which limit is holding it
back*. From [[memory-hierarchy]] we already have the two numbers that matter: a
computation's **arithmetic intensity** (operations performed per byte dragged up from
the slow main memory) and the machine's **balance point** (how many operations the
hardware can do in the time it takes to fetch one byte). The roofline model takes the
hardware's two hard ceilings — its peak operation rate and its peak memory bandwidth —
and draws them as one rising-then-flat "roof." You then drop your computation onto that
roof at the spot fixed by its arithmetic intensity. If it lands on the *rising* part,
it is memory-bound: bandwidth is the wall, and only faster or fewer bytes will help. If
it lands under the *flat* part, it is compute-bound: the cores are the wall, and only
more or faster cores will help. The model's whole value is that it tells you, before you
optimize anything, *which* lever can possibly move you — and which cannot.

## Grounded explanation

### What the concept *is*: turning two ceilings into one performance envelope

From [[memory-hierarchy]] we already have the moving parts. A computation has an
**arithmetic intensity** — its floating-point operations performed divided by the bytes
it must read from and write to the slow main memory (call those operations *FLOPs*, for
floating-point operations, and call the rate of doing them *FLOP/s*, FLOPs per second).
And the machine has a **balance point** — the ratio of its peak FLOP/s to its peak
memory bandwidth in bytes per second, which works out to a number of FLOPs the cores can
finish in the time one byte arrives. [[memory-hierarchy]] uses these to *classify* a
computation as memory-bound (intensity below the balance point) or compute-bound
(intensity above it).

The roofline model is the step *beyond* that yes/no classification: it predicts the
actual ceiling on achievable speed, for *every* intensity at once, as a single curve.
The insight is that two independent hardware limits act on the computation
simultaneously, and the slower of the two always wins:

- The **compute ceiling** is flat: no matter how data-rich your computation is, the
  cores cannot exceed their peak FLOP/s. Call this peak rate $P$ (in FLOP/s). On a plot
  of achievable FLOP/s, this is a horizontal line at height $P$.
- The **bandwidth ceiling** is sloped: if your computation moves a lot of bytes per
  FLOP (low intensity), then bandwidth caps how fast the FLOPs can be fed. If the
  machine streams $B$ bytes per second, and the computation does $I$ FLOPs per byte (its
  arithmetic intensity), then bytes arrive at rate $B$ and each carries $I$ FLOPs of
  work — so the achievable rate is $B \times I$ FLOP/s. On the plot this is a straight
  line rising with $I$: double the intensity, double the attainable rate.

The achievable performance is whichever ceiling is lower:

$$\text{attainable FLOP/s}(I) = \min\big(\,P,\ \ B \times I\,\big).$$

Plot that with arithmetic intensity $I$ on the horizontal axis and attainable FLOP/s on
the vertical axis: for small $I$ the term $B \times I$ is the smaller one, so the curve
*rises* along the sloped bandwidth line; for large $I$ the flat compute line $P$ is
smaller, so the curve *flattens* at height $P$. The result is a line that climbs and then
levels off — the shape that names the model, the "roofline." It is the **envelope** of
everything the hardware can possibly attain. No real computation can sit above it.

### Why it works: the ridge point is the machine balance, and intensity fixes your fate

The single most informative spot on the roof is the corner where the rising line meets
the flat line — the **ridge point**. Set the two ceilings equal to find it: $B \times I
= P$ gives $I = P / B$. But $P / B$ — peak FLOP/s over peak bytes/s — is *exactly* the
machine's balance point from [[memory-hierarchy]]. So the corner of the roofline sits at
the balance point. This is why the roofline and the balance point are the same idea seen
two ways: the balance point is a single number ("memory-bound below it, compute-bound
above it"); the roofline is that number drawn as the kink in a curve, with the *cost* of
being on the wrong side made visible as vertical distance below the flat ceiling.

That visibility is the payoff. Drop your computation onto the roof at its own intensity:

- If its intensity is **left of the ridge** (below the balance point), it lands on the
  sloped part. It is memory-bound — the same conclusion [[memory-hierarchy]] reaches —
  and the roof tells you the ceiling it is pinned under is $B \times I$, far below peak
  compute. Crucially it also tells you the *only* two ways up: raise $B$ (a chip with
  more bandwidth) or raise $I$ (move fewer bytes per FLOP, sliding rightward along the
  slope toward the ridge). Buying more cores — raising $P$ — lifts the flat ceiling you
  are nowhere near, so it does nothing.
- If its intensity is **right of the ridge** (above the balance point), it lands under
  the flat part. It is compute-bound; its ceiling is $P$. Now the levers reverse: more
  bandwidth is wasted (you are not on the sloped line), and only more or faster cores —
  a higher $P$ — raises the ceiling.

So the model's contribution is not "is this fast?" but "*which knob is even connected?*"
— and it answers that from a single glance at which side of the ridge the point falls.

### Worked instance: two kernels on one roof

Take a chip with peak compute $P = 100 \times 10^{12}$ FLOP/s (100 TFLOP/s) and peak
main-memory bandwidth $B = 3 \times 10^{12}$ bytes/s, the representative values from
[[memory-hierarchy]]. Its ridge point — its balance — is

$$\tfrac{P}{B} = \frac{100 \times 10^{12}}{3 \times 10^{12}} \approx 33 \text{ FLOP per byte}.$$

So the roof rises along the line $3 \times 10^{12} \times I$ until $I = 33$, then runs
flat at $100 \times 10^{12}$. Now place two genuinely different computations on it; the
two cases sit on opposite sides of the ridge, so the instance triggers both branches.

**Kernel A — an element-wise add** (one of the streaming operations from
[[memory-hierarchy]]): for each output number it reads two inputs and writes one — three
4-byte numbers, 12 bytes — to perform a single `+`. Its arithmetic intensity is

$$I_A = \frac{1 \text{ FLOP}}{12 \text{ bytes}} \approx 0.083 \text{ FLOP per byte}.$$

That is far left of the ridge at 33. So on the roof it lands on the sloped line, and its
ceiling is $B \times I_A = 3 \times 10^{12} \times 0.083 \approx 2.5 \times 10^{11}$
FLOP/s — about $0.25$ TFLOP/s, a *quarter of one percent* of the 100 TFLOP/s peak
directly above it. The vertical gap to the flat ceiling is the wasted compute the roof
makes visible. Deeply memory-bound; only bandwidth or higher intensity helps.

**Kernel B — a large matrix multiply.** Multiplying two $n \times n$ matrices does
$\approx 2n^3$ FLOPs but moves only $\approx 3n^2$ numbers ($4 \times 3 n^2$ bytes) — so
every number loaded gets *reused* across a whole row or column of the multiply rather
than touched once. (This reuse is precisely the amortization the source's weight-matmul
panel describes: one loaded weight tile feeds many tokens, so the byte load is paid off
over many FLOPs.) For $n = 4096$ the intensity is

$$I_B = \frac{2 n^3}{4 \times 3 n^2} = \frac{2n}{12} = \frac{n}{6} = \frac{4096}{6} \approx 683 \text{ FLOP per byte}.$$

That is far *right* of the ridge at 33. So matrix-B lands under the flat part of the
roof: its ceiling is the full $P = 100$ TFLOP/s. Compute-bound — more bandwidth would
sit idle, and only faster cores lift it.

Read off the contrast the roof now displays. The two kernels differ in attainable speed
by a factor of $100 \times 10^{12} \div 2.5 \times 10^{11} = 400\times$, *purely because*
one reuses its loaded bytes and the other does not — same chip, same roof, opposite
sides of one ridge. That 400× gap, and the single picture that exposes it, is what the
roofline model exists to make obvious.

### Why it matters: it names the lever before you pull it

The reason this model is reached for constantly in large-model systems is that it
converts a vague worry ("this is slow") into a directed action. Sweeping operations like
adds, normalizations, and activation functions are low-intensity and pin to the sloped
line — fusing them (so a chunk is loaded once and many of these cheap operations run on
it before it is written back) raises intensity and slides the point rightward toward the
ridge, which is the only move that helps a memory-bound kernel. Big matrix multiplies
are high-intensity and pin under the flat line, where the only lever is faster cores.
The roofline model is the map that says, for any given kernel, which of those two worlds
it lives in — so effort goes to the knob that is actually connected to its ceiling, and
not to the one that is already maxed out.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- Williams, Waterman & Patterson, "Roofline: An Insightful Visual Performance Model," *CACM* 2009 — the original model: the $\min(\text{peak compute},\ \text{bandwidth} \times \text{intensity})$ envelope, the ridge point, and reading off which bound applies.
- `etc/llm_parallelism_strategies.jsx`, ChunkedPrefill and MemoryMovement panels — the memory-bound vs. compute-bound regimes and weight-load amortization (one weight tile reused across many tokens) that the matrix-multiply worked instance draws on.
