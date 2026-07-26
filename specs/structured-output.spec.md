# Figure spec — `structured-output` (Step 0)

> Derived FROM `nodes/structured-output.md`; governed by `protocols/VISUAL_PROTOCOLS.md`
> and `protocols/EXPLAIN.md`.
>
> **Genre: state machine** (main spine — the constraint engine's grammar automaton),
> carrying a **dataflow overlay** on the one rich transition (mask → renormalize → sample).
> Tie-breaker (per template): the concept's defining shape is "where in the required
> structure are we, and which tokens does that position permit" — that is a state machine;
> the mask/softmax arithmetic is real but subsidiary detail attached to *one* transition
> (the enabling computation, not what the concept *is*), so it becomes a subordinate detail
> panel that appears only where it's needed.

## Figure trigger (EXPLAIN.md)

Drawing is warranted. Load-bearing ideas that are irreducibly visual:

- **SHAPE/structure** — the grammar is a finite sequence of positions (state 0..3), each
  with its own legal-token subset; that state→legal-set mapping, and how it advances, is
  a structural fact best shown as an automaton, not prose.
- **FLOW/routing** — the sampled token must be *seen to travel* from "chosen" to
  "appended to the output"; and the same decision point has two divergent futures
  (masked vs. unmasked) that a reader needs to see fork and die.
- **CHANGE over steps** — the mask-then-renormalize transformation of a probability
  distribution (four numbers before, four numbers after) is a "before → after" fact far
  more legible as two aligned bar rows than as prose fractions.

Guardrail facts kept to caption/table only (not lettered onto the spine): the softmax
formula itself (the prerequisite node's job), the general claim "$e^{-\infty}=0$"
(stated once in the invariant line), and the multi-legal-token generalization (same-logic
sibling, already stated in the node prose; the worked instance never visits a multi-survivor
mask on canvas, so caption-only is licensed by the instance-conditional rule — kept as one
footer sentence for self-containedness).

## (a) Entity inventory

**Mechanism-genre defaults applied:** WHO-1 → n/a (single-agent mechanism: one model, one
constraint engine, no multi-party exchange). WHY-3 → n/a (mask-then-renormalize is a fixed,
non-tunable guarantee — no genuine two-sided tension asserted anywhere in the source).

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors/participants | n/a — single-agent serial pipeline (one model, one constraint engine), per the mechanism-genre default |
| WHAT-1 | data items with identity | the 4 vocabulary tokens: `{"x":` (opener), `7` (digit), `}` (closer), `cat` — each keeps one fixed identity color everywhere it appears (vocab strip, logit cells, bars, output spine) |
| WHAT-2 | computed/derived results | the probability distribution at each stage (unconstrained softmax output; renormalized softmax output) — derived from logits, takes no source's color, drawn as bars; the assembled output string is *not* WHAT-2 — it is WHAT-1 items moved/appended, not fused, so it keeps each token's own color |
| WHAT-3 | running state | the constraint engine's **current legal set** — drawn not as a separate register but as a gold ring overlay on the persistent vocabulary strip (WHAT-1), evolving step to step: {opener} → {digit} → {closer} → ∅ (accept). Reuse of the WHAT-1 strip is deliberate: the vocabulary is small and static, so a dedicated second register would duplicate four cells for no traceability gain. |
| WHAT-4 | persistent structure + invariant | the grammar automaton (4 states, 3 labeled transitions) — invariant quoted verbatim from the node: "masking removes the illegal tokens and redistributes their probability mass across the legal ones in proportion to what they already had" |
| WHERE-1 | substrate/resource tiers | n/a — no memory/bandwidth hierarchy in this concept |
| WHERE-2 | layout/addressing rule | n/a — no addressing scheme beyond automaton-state identity (already WHAT-4) |
| WHEN-1 | ordered phases | see §(c) — 7 STEPs grouped into 3 ACTs (opener collapse / digit decision+catch / closer collapse) |
| WHEN-2 | concurrency lanes | n/a — one sequential process, no concurrent actors |
| WHEN-3 | before→after snapshots | n/a as a *global* transition (the mechanism is a 3-iteration loop, not one shot) — the same "before → after" idea appears *locally*, once per rich transition, as the unconstrained-vs-renormalized bar rows; folded into HOW-1/§(c) |
| HOW-1 | algorithm over the structure | **sequential fold, order asserted by the source**: the grammar position is a recurrence (state_{t+1} depends on state_t and the sampled token) — inherently ordered, so a state-carrying loop, not an atomic combine. 3 iterations shown (S0→S1→S2→S3), satisfying "≥2 iterations with state evolving." Iterations 1 and 3 are algebraically trivial (legal-set size 1 ⇒ probability 1 regardless of the underlying logit) and are shown as quick collapse phases without invented numbers, per the template's numberless-phase rule (the source supplies no numbers for them); iteration 2 (the digit decision) carries the node's full worked arithmetic. |
| HOW-2 | protocol/message alphabet | n/a — no exchanged messages between actors (single-agent); the ordered *step* names (mask, renormalize, sample, advance) are the algorithm's own stages, already covered by HOW-1/§(c) |
| WHY-1 | quantities/complexity | caption-only: one mask pass over the vocabulary's logits per generation step (no big-O drawn; not the concept's point) |
| WHY-2 | failure/edge/degenerate branch | **the catch, drawn**: the counterfactual "without masking" branch — the illegal favorite `}` (p=0.644) would be sampled, producing invalid `{"x":}`. Drawn as a dashed ghost branch off the real decision point, appearing for exactly one STEP, then discarded (never taken). The other edge case the node mentions (≥2 legal tokens) is same-logic, never visited by this worked instance, and already stated in the node prose — caption-only per the instance-conditional omission rule. |
| WHY-3 | trade-off comparison | n/a — fixed, non-tunable guarantee, per the mechanism-genre default; no genuine tension asserted in the source |
| ANCHOR-1 | worked numeric instance | the node's own example: 4-token vocab, step "await digit", logits (2.0, 1.0, 3.0, 0.0) → unconstrained P (0.237, 0.087, 0.644, 0.032) → masked logits (−∞, 1.0, −∞, −∞) → renormalized P (0, 1.000, 0, 0) → sampled `7` → final output `{"x":7}` |
| ANCHOR-2 | composition refs | **[[softmax]]** — performs the exponentiate-and-normalize step at *both* the unconstrained and the post-mask stage; its output type is a **[[probability-distribution]]** (every entry positive, summing to 1) — both prerequisite nodes are named on the figure's compute-step arrow/label rather than redrawn |

Drawing table:

| element | type | drawn as | level/role |
|---|---|---|---|
| vocabulary strip (4 cells) | WHAT-1 | persistent labeled cells, one fixed hue each | top row, always visible |
| legal-set ring overlay | WHAT-3 | gold ring on the currently-legal vocab cell(s) | overlay on vocab strip, evolves per STEP |
| grammar automaton (S0..S3 + 3 edges) | WHAT-4 | circles + labeled arrows | main spine, center |
| raw logit cells (row 1) | WHAT-1 (numeric instance) | 4 labeled cells, token-colored | detail panel, top sub-row |
| unconstrained probability bars (row 2) | WHAT-2 | 4 bars, height ∝ probability | detail panel, below row 1 |
| masked logit cells (row 3) | WHAT-2 (post-mask) | same 4 cells; 3 dimmed "−∞", 1 unchanged + gold ring | detail panel, below row 2 |
| renormalized probability bars (row 4) | WHAT-2 | 4 bars, height ∝ probability (one at full height) | detail panel, below row 3 |
| ghost/counterfactual branch | WHY-2 | dashed red path + box, appears one STEP only | beside the digit decision, off to the side |
| traveling token copies (×3) | dynamics | small colored cell gliding along a persistent drawn path | from vocab strip down to output spine |
| output spine (3 slots) | WHAT-1 (moved, not fused) | boxes appended left→right, each token's own color | bottom, growing |
| legend + invariant caption | caption | static text/swatches | footer |

Layout is by the compute/data DAG (automaton states are the sequential spine; the
digit-decision's logit/probability rows sit directly under the transition they explain;
the output spine sits at the bottom because it is the accumulating *result*, fed by every
transition above it) — not by an arbitrary reading order.

## (b) Dynamics

- The sampled token **rides its own persistent drawn path**: each of the 3 travels
  (opener/digit/closer) is a small colored cell that glides in a straight line from its
  vocab-strip cell down to its output-spine slot, at the exact moment its grammar
  transition fires — it never fades in/out in place.
- The mask→renormalize transformation happens **only inside the detail panel** (the
  compute tier): the raw logit row and masked logit row are the same 4 columns, so the
  "before" and "after" states of the same token sit in the same column, one above the
  other — the transformation is legible as a vertical before/after pair (column-aligned,
  identical element order), never as an in-transit mutation.
- The ghost token's hypothetical path is dashed and travels only far enough to reach its
  own (dead-end) box — explicitly marked discarded (✗), never merging into the real
  output spine.
- The automaton's "current" highlight and the firing edge's gold accent move together,
  one state/edge pair per STEP — never two unrelated elements accented at once.

## (c) Ordered phases → animation frames

One master clock, `repeatCount="indefinite"`, split into **7 discrete STEPs** (shared
keyTimes on every animate element). Grouped into 3 ACTs matching the automaton's 3
transitions (control structure: the loop head is "at state S_i, compute the legal set,
mask, renormalize, sample, advance to S_{i+1}"; it visibly loops S0→S1→S2→S3, 3 full
iterations, then holds and resets):

- **ACT 1 — trivial opener collapse** (STEP 1-2). STEP 1: setup, S0 current, legal
  set={opener}. STEP 2: legal-set size is 1, so masking has no work to do regardless of
  the underlying logit — opener is sampled trivially, travels to the output spine,
  state advances to S1.
- **ACT 2 — the rich digit decision** (STEP 3-5), the node's actual worked instance.
  STEP 3: raw logits (2.0, 1.0, 3.0, 0.0) emitted at S1; unconstrained softmax shows `}`
  as the favorite (0.644) — illegal here. STEP 4 (WHY-2, the catch): counterfactual
  ghost branch — without masking, `}` would be sampled, producing invalid `{"x":}`.
  STEP 5: mask the 3 illegal logits to −∞, softmax renormalizes over the sole survivor →
  digit collapses to p=1.000 → sampled → travels to the output spine → state advances to
  S2.
- **ACT 3 — trivial closer collapse + result** (STEP 6-7). STEP 6: legal set={closer},
  again trivial, closer sampled, travels, state advances to S3 (accept). STEP 7: output
  spine reads `{"x":7}` complete, accept state lit, held, then the whole clock loops back
  to STEP 1 (a fresh generation).

Every phase and every transfer (who moves what, to where) from this list must be present
in the SVG and verified frame-by-frame.

## (d) Color

- **Identity dimension = token identity** (data), held across the whole figure: opener
  `#3B6FA8`, digit `#2E9E83`, closer `#7A5CB0`, cat `#B5502B` — same hue in the vocab
  strip, logit cells, probability bars, traveling copies, and output spine.
- Idle/neutral chrome (automaton circles, cell outlines, panel dividers): `#FBF0DB` fill,
  `#C79A3E` stroke.
- Opacity = state: automaton circles are full-opacity only while "current," dimmed
  otherwise (no separate hue change for current/past/future — opacity alone carries
  that channel, keeping gold free for the one accent).
- **ACCENT (gold `#E8A02E`, one only)** = the currently-legal / just-sampled token this
  STEP — manifested as a ring on the vocab-strip cell, a ring on the masked-logit
  survivor cell, a ring on the renormalized-bar survivor, and (once per firing) a
  thickened gold overlay on the automaton edge that is transitioning. All of these are
  the *same* causal event (one token becoming legal, then sampled, then advancing the
  state), so painting gold in multiple connected places is one accent telling one story,
  not several.
- Ghost/counterfactual branch uses a dedicated **red** (`#B23A3A`), never gold — it is
  explicitly the path *not* taken, so it must never be confused with the accent.

## (e) Worked instance carried to the visible answer

Vocabulary: `{"x":`, `7`, `}`, `cat`. At the digit decision (state S1): raw logits
`z = (2.0, 1.0, 3.0, 0.0)` → unconstrained softmax `P = (0.237, 0.087, 0.644, 0.032)`
(every number derived on-canvas: $e^{2.0}=7.389$ etc., sum $31.193$, shown as the bar
heights/labels) → mask the 3 illegal logits to −∞ → renormalized softmax
`P = (0, 1.000, 0, 0)` → sample `7` → append. Combined with the two trivial collapses
(opener, closer — both forced with probability 1 by construction of a singleton legal
set, no invented numbers), the spine reads the complete, valid answer **`{"x":7}`**,
held on screen at STEP 7 before the loop resets.

## (f) Stays as caption / text

- Header: title (static) + `STEP n/7` indicator + one-line caption per STEP (7 lines,
  opacity-toggled, one visible at a time) — whole-figure header content.
- Footer (static, always visible): the invariant quoted verbatim; one line noting the
  same-logic multi-legal-token generalization (caption-only per the instance-conditional
  guardrail; kept as a footer sentence so the figure reads self-contained without the
  node prose); a legend mapping the 4 token colors + the gold accent + the red
  ghost-branch + the opacity code.
- Anchoring: the numeric logit/probability values are inline in their own cells/bars
  (not a separate list); the "current favorite (illegal!)" and "without masking: ..."
  labels are inline next to the specific bar/box they describe; only the invariant and
  legend — facts about the figure as a whole — live in the separate footer block.
