# Figure spec — `state-space-model` (Step 0)

> Derived FROM `nodes/state-space-model.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and
> `protocols/EXPLAIN.md`. Iteration 11, blind-drawer pass.

**Genre**: math/quantity (equation protocol — type-colored cells, operator/readout accents) —
BUT the defining structure is a genuine **temporal recurrence** (a state carried and mutated
across ≥2 timesteps), so the mechanism-genre's state-carrying-loop rules (HOW-1, WHEN-1,
"≥2 iterations with visible carry") govern the loop's animation in full, layered on top of the
math genre's cell/color conventions. Overlay: the convolution form is a second, independently
complete computation of the identical answer — not a competing spatial axis — so it is drawn as
a **comparison** sub-panel (subordinate ink) that appears once the recurrence reaches its
answer, proving the "one magic-step justification" (rule 6) that recurrence ≡ convolution.

## Figure trigger (EXPLAIN.md)

Drawing is warranted: the node's central claim — "linearity buys two *equal* computational
forms" — is irreducibly visual; a reader cannot verify by eye, from prose alone, that the same
three numbers fall out of two structurally different processes.

- **SHAPE/structure**: the fixed-size state register $h$ that persists across steps while
  $A,B,C,D$ stay constant — a *persistent structure with an invariant* (WHAT-4), not a growing
  buffer.
- **FLOW/routing**: the recurrence's data path per step — old state × $A$, new input × $B$,
  summed into the new state, then read out through $C$ (+ $D$) to $y_t$ — and, in the
  comparison panel, the column-aligned convolution sum $y_t=\sum_j k_{t-j}x_j$.
- **CHANGE over steps**: the state-carrying loop itself — $h_0\to h_1\to h_2\to h_3$, each step
  a genuine mutation of the same fixed-size register. This is the "sequential fold" branch:
  the source explicitly asserts the order ("runs left to right, one step at a time... step $t$
  must wait for step $t-1$"), so this is a true recurrence, not an atomic/parallel combine.

Caption-only facts (also listed in §f): the $O(n)$ vs. attention's $O(n^2)$ contrast (WHY-1,
one-sided magnitude motivator, no dedicated panel — the figure doesn't draw attention at all,
so a drawn contrast panel would earn more ink than the node itself spends on it); the fixed-size
invariant statement (quoted, not re-derived); the recurrence⇄convolution relationship being an
*identity*, not a trade-off (WHY-3 n/a, stated below, not silently dropped).

## (a) Entity inventory

**Math-variant defaults applied:** WHO-1 = n/a — no actors/substrate/protocol in a quantity
concept (single-engine recurrence, not a multi-party exchange). WHERE-1 = n/a — no memory/IO
hierarchy; the concept is not bandwidth-bound. HOW-2 = n/a — no message alphabet.

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors/participants | n/a — no actors/substrate/protocol in a quantity concept |
| WHAT-1 | data items with identity | $x_1{=}1, x_2{=}0, x_3{=}2$ — the input sequence; each keeps its own identity/color as it is consumed at its own step, never fused with another input |
| WHAT-2 | computed/derived results | $h_1,h_2,h_3$ (operator-adjacent: direct output of the combine) and $y_1,y_2,y_3$ (non-adjacent: a *readout* of an already-computed $h_t$ through $C$) — see §d for why these get different accent treatment |
| WHAT-3 | running state | $h_t$ itself — the accumulator the recurrence carries and mutates every step; drawn as a labeled cell on the spine, never bare text |
| WHAT-4 | persistent structure + invariant | the state register $h$ — outlives any single step; invariant (quoted verbatim, spliced from two adjacent clauses): "the state has a *fixed size regardless of sequence length*" / "$h$ never grows: whether you are at step $3$ or step $3{,}000$, $h$ is the same size." **Cross-reference**: WHAT-3 and WHAT-4 point at the same drawn element ($h$-track cells) — this is the streaming-accumulator-is-the-persistent-structure default. |
| WHERE-1 | substrate/resource tiers | n/a — no memory hierarchy; not an IO-/bandwidth-bound concept |
| WHERE-2 | layout/addressing rule | n/a — no addressing scheme beyond time-step order, which is WHEN, not WHERE |
| WHEN-1 | ordered phases | per step $t$: (1) old state $h_{t-1}$ enters combine, scaled by $A$; (2) new input $x_t$ enters combine, scaled by $B$; (3) combine sums the two → new state $h_t$ (WHAT-2, adjacent); (4) $h_t$ is read out through $C$ (+ $D\,x_t$, here $D{=}0$) → $y_t$ (WHAT-2, non-adjacent). Repeats for $t=1,2,3$. Nothing is ever freed/evicted — the state is overwritten in place, not accumulated as a growing list, so there is no "freed" column (mechanism only mutates, never evicts a separate structure). |
| WHEN-2 | concurrency lanes | n/a — one sequential chain, not concurrent lanes |
| WHEN-3 | before→after snapshot | n/a — this is a genuine multi-step iteration (WHEN-1 already covers it frame by frame), not a single global transition |
| HOW-1 | algorithm / control structure | **sequential fold** — the source asserts the order explicitly ("autoregressive... runs left to right, one step at a time"); a state-carrying loop, so the figure animates **all 3** iterations ($t=1,2,3$) with $h$ visibly evolving between them, never pre-baking early steps as a static "done" |
| HOW-2 | protocol/message alphabet | n/a — no named message kinds |
| WHY-1 | quantities/complexity | $O(n)$ total, $O(1)$ state per step, vs. attention's $O(n^2)$ all-pairs cost — one-sided magnitude motivator; caption-only (see trigger section for why no panel) |
| WHY-2 | failure/edge/degenerate branch | $x_2{=}0$: the state must still propagate $x_1$'s (decayed) echo even though the new input is zero. This sits inside the sanctioned worked instance's own step range (t=2), so it is drawn on that iteration, not as a separate panel. |
| WHY-3 | trade-off comparison | n/a — recurrence and convolution are two *exactly equal* forms of the same linear model (an algebraic identity from linearity), not a tunable knob with genuine two-sided tension; an identity is never a trade-off |
| ANCHOR-1 | worked numeric instance | $A{=}0.5, B{=}2, C{=}3, D{=}0$, $x=[1,0,2]$, $h_0{=}0$ → $h=[2,1,4.5]$, $y=[6,3,13.5]$ — the node's own instance; it hits all three exercised branches (multi-step $A$-decay, zero-input propagation, mixed decayed-tail + fresh-input) |
| ANCHOR-2 | composition refs | [[neural-network]] — the node explicitly says $A,B,C,D$ *may* be supplied by neural-network weight matrices, but "the concept here is the recurrence structure, not the maps." Role in this figure: **not drawn** as machinery (drawing NN internals would misrepresent the concept's own spine); referenced only in a caption line. |

Drawing table:

| element | type | drawn as | level/role |
|---|---|---|---|
| $A,B,C,D$ | matrix (given), 1×1 shown | amber cell + faint dashed "ghost" outline signaling general $d\times d$ shape | persistent parameter panel, always visible |
| $x_1,x_2,x_3$ | vector (given), $d{=}1$ shown | teal cell + ghost outline (general $d$-vector) | input row, one per station, opacity = pending→active→past |
| $h_0,h_1,h_2,h_3$ | vector (running state / persistent structure), derived-adjacent | coral cell + ghost outline | spine, opacity = state (now bright, past dim, future hidden) |
| combine (×3) | operator | coral box, edges labeled ×A / ×B | spine, between consecutive $h$ cells, flashes bright only during its active step |
| $y_1,y_2,y_3$ | vector (readout, derived non-adjacent) | gold cell | branch below each combine, opacity = state |
| state-token | traveling marker | small coral circle riding the persistent horizontal track | rides h→combine→h each step |
| input-drop (×3) | traveling marker | small teal circle | rides the persistent dashed vertical track from $x_t$ into its combine |
| readout-token (×3) | traveling marker | small gold circle | rides the persistent dashed vertical track from combine down to $y_t$ |
| convolution panel | comparison (subordinate) | static 3×3 lower-triangular grid, columns = $x_j$ (shared, column-aligned), rows = $t$, kernel cells $k_k{=}CA^kB$ gold | appears (fades to full ink) only once the recurrence has reached $y_3$; faint/pending before that |

Layout is by the compute DAG (old-state and new-input are co-inputs to the same combine, so
they sit at the same level feeding it), not reading order.

## (b) Dynamics

Every step: $h_{t-1}$ travels right along the persistent horizontal track into the combine box
(scaled ×A **inside** the combine, never in transit); simultaneously $x_t$ travels down the
persistent dashed vertical track into the same combine (scaled ×B, also inside the combine).
The combine sums the two **inside itself** and the result continues right along the track as
the new $h_t$ — the traveling state-token literally is the value, riding the same track its
whole journey, never teleporting. A second, independent transfer branches off $h_t$: the
readout-token rides a second persistent dashed vertical track down through ×C (computed inside
the combine/readout box, not in transit) to land on $y_t$. The state-token's cx values across
the master clock (`150;150;300;450;600;750;900;1050;150`) trace one continuous path: dwell at
$h_0$ → slide to combine1 → land at $h_1$ → dwell → slide to combine2 → land at $h_2$ → ...
→ land at $h_3$ → dwell through the comparison reveal → loop back to $h_0$.

In the comparison panel, $x_j$ is drawn once per column and **shared** by every row that uses
it (column-aligned per the co-indexed-sequence rule) — never redrawn per row — so the reader
reads pairing $k_{t-j}\!\cdot\!x_j$ straight down the column.

## (c) Ordered phases → animation frames

One master clock, `keyTimes="0;0.125;0.25;0.375;0.5;0.625;0.75;0.875;1"`, `dur="16s"`,
`repeatCount="indefinite"`, shared verbatim by every animated element (fully aligned, not just
same-`dur`).

- **F(idx0, t=0)** — STEP 0/4. Init: $h_0=0$ shown bright (it is "now"); $x_1,x_2,x_3$ all
  shown pending (faint); parameters always visible.
- **F(idx1–idx2, t=1)** — STEP 1/4. $x_1{=}1$ activates, slides into combine1; state-token
  slides $h_0\to$combine1 (mid-step) $\to h_1$; combine1 flashes; $h_1{=}2$ appears bright;
  readout-token rides combine1$\to y_1$; $y_1{=}6$ appears bright. $h_0$ dims to past.
- **F(idx3–idx4, t=2, WHY-2 branch)** — STEP 2/4. $x_2{=}0$ activates (the degenerate input);
  $h_1$ (now past, dim) feeds forward regardless; combine2 flashes; $h_2{=}1$ appears — the
  echo of $x_1$ survives a zero input, exactly the case the node calls out. $y_2{=}3$ appears.
  $h_1$ dims to past.
- **F(idx5–idx6, t=3)** — STEP 3/4. $x_3{=}2$ (fresh, large) mixes with the twice-decayed
  tail; combine3 flashes; $h_3{=}4.5$ appears; $y_3{=}13.5$ appears (stays bright through the
  next phase — it is the visible final answer). $h_2$ dims to past.
- **F(idx7, t=3, reveal)** — STEP 4/4. Comparison panel brightens from faint to full ink:
  kernel $k_0{=}6, k_1{=}3, k_2{=}1.5$ (each a non-adjacent, multi-hop derivation through
  repeated ×A then ×C — gold), column-aligned products, row sums reproduce $y=[6,3,13.5]$
  identically to the recurrence spine.
- **idx8 = idx0** — loop back to STEP 0/4 (every animated attribute's idx8 value equals its
  idx0 value, verified below, for a seamless repeat).

Control structure stated explicitly: this is a **sequential fold** (loop head = "next $t$",
body = the four WHEN-1 sub-phases), not a parallel/atomic combine and not concurrent lanes —
≥2 iterations ($t{=}1,2,3$, i.e. 3) animate with the state visibly evolving between them.

## (d) Color

**Identity dimension = type** (scalar | vector | matrix), applied only to *given* elements per
the math protocol's type-color/operator-color split:

- Given matrices $A,B,C,D$: amber fill `#FBF0DB` / stroke `#C79A3E` (house matrix color).
- Given vectors $x_t$: teal `#3F9B86`.
- Derived, **adjacent** to the operator that made it ($h_t$, direct combine output): coral
  `#D85A30` (operator accent) — per the math protocol's "individual derived cells take the
  operator color instead" rule.
- Derived, **non-adjacent** (a readout tracing back through an already-computed structure):
  gold `#E8A02E` — $y_t$ (via $C$) and the convolution kernel weights $k_k=CA^kB$ (a multi-hop
  chain through $A$ then $C$, not a single adjacent op).
- Idle/neutral house amber reserved for the always-on parameter panel background only.
- Opacity = state throughout: bright = active/now, mid (0.65–0.8) = settled/past-but-legible,
  faint (0.15–0.3) = future/pending, 0 = not yet existing.

$h_0$ (the given initial condition, not itself computed) is colored the same coral as
$h_1,h_2,h_3$ rather than switching families, because WHAT-3/WHAT-4 name the *entire register*
as one persistent structure — a hue-per-step split would fragment a single entity's identity
mid-figure, which rule 5 (traceability) forbids.

## (e) Worked instance carried to the visible answer

$A{=}0.5, B{=}2, C{=}3, D{=}0$; $x=[1,0,2]$; $h_0{=}0$.
Recurrence: $h_1{=}0.5(0){+}2(1){=}2 \Rightarrow y_1{=}3(2){=}6$;
$h_2{=}0.5(2){+}2(0){=}1 \Rightarrow y_2{=}3(1){=}3$;
$h_3{=}0.5(1){+}2(2){=}4.5 \Rightarrow y_3{=}3(4.5){=}13.5$.
Convolution: $k_0{=}CB{=}6, k_1{=}CAB{=}3, k_2{=}CA^2B{=}1.5$;
$y_1{=}k_0x_1{=}6$; $y_2{=}k_0x_2{+}k_1x_1{=}0{+}3{=}3$; $y_3{=}k_0x_3{+}k_1x_2{+}k_2x_1{=}12{+}0{+}1.5{=}13.5$.
Both views land on the identical visible answer $y=[6,3,13.5]$, drawn on-canvas in both panels;
every number derives from another on-canvas number (nothing off-canvas).

## (f) Stays as caption / text

- `STEP n/m` + one-line-ish caption per frame (folded together, see below), whole-figure header
  content, anchored per current phase.
- Legend: teal = vector (given); amber = matrix (given); coral = state $h_t$ (derived,
  adjacent); gold = readout $y_t$ / kernel weight (derived, non-adjacent).
- Shape-honesty note (once, not per-cell): "$x_t,h_t,y_t$ are vectors — $d{=}1$ shown (ghost
  outline marks the general $d$-dim shape); $A,B,C,D$ are matrices — $1\times1$ shown (general
  $d\times d$)."
- Invariant (quoted): "the state has a fixed size regardless of sequence length — $h_t$ is the
  same size at every $t$."
- WHY-1 (one-sided magnitude, caption-only): "$O(n)$ total, $O(1)$ state per step — vs.
  attention's $O(n^2)$ all-pairs cost (not drawn)."
- WHY-3, explicitly n/a (not silently dropped): "recurrence ⇄ convolution is an exact identity
  from linearity, not a tunable trade-off."
- ANCHOR-2 note: "$A,B,C,D$ are learned parameters — e.g. supplied by neural-network weight
  matrices (not drawn: the recurrence structure, not the maps, is this concept)."
- $D{=}0$ note inline at the one drawn ×D edge: "$\times D$ (here $0$; applies at every $t$,
  shown once)."

Per-frame captions (each is whole-figure header content, **exactly one visible at a time**):

> **HARD caption-swap constraint (a prior animated build FAILED here — anti-pattern 13/18):** the
> STEP captions share one anchor slot; each is its own text element gated to its phase. Every
> non-current caption MUST be `opacity=0` (fully hidden), not merely dimmed or drawn-under. When
> caption *k* appears, caption *k−1* must already be gone — no two caption strings may occupy the
> slot at once. VERIFY at the LAST frame specifically (STEP 4/4), where stale captions accumulate:
> the only text in the caption band must be STEP 4/4's own single line, cleanly legible.

1. STEP 0/4 — init: $h_0=0$ (fixed-size state, given).
2. STEP 1/4 — $t{=}1$: $x_1{=}1$ enters. $h_1{=}A h_0{+}Bx_1{=}0.5(0){+}2(1){=}2$. $y_1{=}Ch_1{=}6$.
3. STEP 2/4 — $t{=}2$: $x_2{=}0$ (degenerate input). $h_2{=}0.5(2){+}2(0){=}1$ — the state still
   carries $x_1$'s echo. $y_2{=}3(1){=}3$.
4. STEP 3/4 — $t{=}3$: $x_3{=}2$ mixes with the decayed tail. $h_3{=}0.5(1){+}2(2){=}4.5$.
   $y_3{=}3(4.5){=}13.5$.
5. STEP 4/4 — convolution check: fixed kernel $k_0{=}6,k_1{=}3,k_2{=}1.5$ reproduces the same
   $y{=}[6,3,13.5]$ — recurrence and convolution are one linear model, two forms.

