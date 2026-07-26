# Figure spec — `simt` (Step 0)

> Derived FROM `nodes/simt.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

## Genre & spine

Genre: **timeline** (concurrency lanes / execution-trace grid), drawn as a static
**cycle × lane trace grid** — rows = ordered cycles (WHEN-1), columns = the warp's 32
lanes (WHO-1), cells = executing/masked state. This is the literal spine: the figure
does not animate a playhead sweeping over a frozen diagram; the grid **itself is time**
— every cycle is a drawn row, visible simultaneously, so divergence (mask split) and
reconvergence (mask re-merge) read directly off the vertical axis without playback.

Tie-break reasoning: WHO-1 (the 32 lanes of one warp) is the actor set and the *only*
independently-asserted spatial multiplicity in the mechanism (no memory hierarchy, no
second device axis, no addressing scheme) — so per the "no second spatial axis" bullet,
the lane count directly supplies one axis of the spine (one column per lane). The
remaining question is whether cycles (WHEN-1) become the *animation* axis (the
mechanism default) or a *second drawn spatial axis* (rows). I chose the latter:
 See "Animate vs. static" below for the full
justification.

## Figure trigger (EXPLAIN.md)

Drawing is warranted. Load-bearing ideas that are irreducibly visual:
- **SHAPE/structure** — the warp as a persistent 32-lane container that outlives any one
  cycle; a single instruction issued per cycle across all resident (non-masked) lanes.
- **FLOW/routing** — none (no data crosses between actors; SIMT's whole point is that
  nothing needs to move — one instruction reaches all lanes in place). n/a for
  arrow-based dataflow; the "routing" that matters is *mask routing* (which lanes are
  live this cycle), captured by cell opacity/state, not travel.
- **CHANGE over steps** — the mask pattern flipping cycle to cycle: full → half(A) →
  half(B) → full again. This *is* divergence-then-reconvergence, and it is exactly the
  fact a sentence cannot make visible as well as a grid can (a reader must see "16
  lanes went dark while 16 lit up, then it reversed, then all 16+16 relit together").

Guardrails checked:
- The ~2× cost of the branch is caption-only (WHY-1) since it is directly countable
  from the grid (2 rows spent on the branch vs. the 1 row an aligned instruction
  costs) — per §(f)'s omission check, no separate cost panel is drawn.
- SIMD is caption-only (source explicitly says SIMD "is not a prerequisite concept
  here and gets no node"); it does not appear in the drawn grid at all.
- The 32-way worst-case divergence (all lanes disagree) is a same-logic sibling of the
  16/16 split already covered in the node's prerequisite ([[warp]]) prose and not
  produced by this figure's own worked instance — omitted per the instance-conditional
  guardrail (see WHY-2 below).

## (a) Entity inventory

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors/participants | The 32 **lanes** of one **warp** (thread ⊂ warp, no further nesting — block/SM are out of `simt`'s own scope, they belong to `warp`'s prereq chain). Lane index `i = 0..31`. No cross-warp actors — SIMT's defining claim is that the lockstep group is exactly one warp, so a second warp is deliberately *not* drawn (drawing one would need masking to independent lockstep, contradicting "two warps are completely independent"). |
| WHAT-1 | data items with identity | Per-lane inputs `a[i]`, `b[i]` — one fixed input pair per lane, not decomposed further (each lane's contribution is a non-decomposable scalar pair per the WHAT-1 aggregate-cell allowance). |
| WHAT-2 | computed/derived results | Per-lane, per-cycle result `c[i]` (ADD or SUB fold of that lane's own `a[i]`,`b[i]`) — takes the *result* reading inside each active cell; masked cells show no new result (they hold whatever they last computed, undrawn/blank this cycle). |
| WHAT-3 | running state | n/a — no accumulator; each lane's result is an independent atomic combine of its own two inputs, never folded across lanes or across cycles. (Per decision rule: never invent an accumulator just to satisfy a loop-shape reflex — there is no asserted input order across lanes to fold.) |
| WHAT-4 | persistent structure + invariant | The **warp** itself — the one container that persists across all 4 drawn cycles while cell contents inside it change. Invariant, quoted from `simt.md` (itself quoting/restating [[warp]]): **"the 32 threads always retire instructions together as one warp"** — lockstep is preserved "by letting some of the lockstepped instructions be no-ops for the masked-off threads." Drawn as one bounding box around the whole 32-lane × 4-cycle grid, present unchanged in all four rows. |
| WHERE-1 | substrate/resource tiers | n/a — no memory/bandwidth hierarchy in this concept's scope; SIMT is an instruction-issue/execution model, not a data-movement one. |
| WHERE-2 | layout/addressing | n/a — no addressing scheme beyond a lane's own index identity (covered by WHO-1). |
| WHEN-1 | ordered phases | Four cycles, in order: **(1)** shared ADD, no branch yet, all 32 lanes on. **(2)** branch predicate `i<16` evaluated; pass A — lanes 0–15 on executing the ADD arm, lanes 16–31 masked off. **(3)** pass B — masks flip; lanes 16–31 on executing the SUB arm, lanes 0–15 masked off. **(4)** reconvergence — next shared instruction, all 32 lanes on again. (No backward/freed phase — SIMT issues instructions forward only; nothing is evicted here, so no "freed" column — per WHEN-1's own-only-what's-asserted rule.) |
| WHEN-2 | concurrency lanes / timeline | **This is the spine.** One column per lane (32), one row per cycle (4); cell state (bright = executing, dim+dashed = masked) is the entire payload. |
| WHEN-3 | before→after snapshots | n/a — this is not a single global state transition; it is the WHEN-1/WHEN-2 multi-cycle trace above, which subsumes it (row 1 vs. row 4 already *is* the "before/after" of the divergence episode, read as two rows of the same grid rather than a separate snapshot pair). |
| HOW-1 | algorithm over the structure | Composite: cycles 1 and 4 are plain, non-branching shared instruction issue (every lane executes the one issued instruction — no fold, no branch). Cycles 2–3 are **HOW-1 shape 5 (conditional branch)**: predicate `i<16` routes lanes down two mutually exclusive arms; the worked instance exercises each side once, in sequence (pass A, then pass B), which is exactly what shape 5 licenses ("let the worked instance exercise each side once in sequence") since real hardware cannot issue a simultaneous fork. |
| HOW-2 | protocol/message alphabet | n/a — no inter-actor messages; a single hardware unit issuing instructions to its own fixed lanes is not a message protocol. |
| WHY-1 | quantities/complexity | The divergence cost: the branch spends **2 cycles** (rows 2+3) versus the **1 cycle** an already-agreeing warp would spend — caption-only, and per the omission check, not given its own panel because it is directly countable by counting drawn rows. |
| WHY-2 | failure/edge/degenerate branch | n/a for this figure — the worst case (all 32 lanes mutually disagreeing, up to 32 serial passes) is a same-logic sibling of the drawn 16/16 split, already stated in the prerequisite [[warp]] node's prose, and this figure's own worked instance (one 16/16 branch) never produces that sibling case on canvas — omitted per the instance-conditional guardrail, with a one-line caption cross-reference so it is not silent. |
| WHY-3 | trade-off comparison | n/a — per the mechanism-genre default: SIMT's masking behavior is a fixed hardware guarantee ("the hardware copes by masking"), not a tunable knob with a genuine two-sided tension the programmer trades off within this figure's scope. (SIMD-vs-SIMT is a *different*, one-sided contrast — the source frames SIMT as strictly winning "the best of both" — so it is WHY-1-flavored caption text, not a WHY-3 trade-off panel, and SIMD gets no drawn ink per the figure trigger above.) |
| ANCHOR-1 | worked numeric instance | `a[i] = 10·(i+1)`, `b[i] = i+1` (source's own values: `a=[10,20,30,…]`, `b=[1,2,3,…]`), carried through all 4 cycles. Cycle 1 & cycle 2 (lanes 0–15): `c[i]=a[i]+b[i]` — lane 0 → 11, lane 1 → 22, lane 2 → 33, lane 15 → 176. Cycle 3 (lanes 16–31): `c[i]=a[i]-b[i]` — lane 16 → 153, lane 17 → 162, lane 31 → 288. Cycle 4: mask returns to all-on (structural fact only — no new arithmetic invented; labelled generically as "next shared instr" rather than assigning it fabricated semantics). |
| ANCHOR-2 | composition refs | [[warp]] — supplies the 32-lane lockstep group, the lane/mask vocabulary, and the retire-together invariant quoted in WHAT-4; this figure is the cycle-by-cycle *trace* of exactly the mechanism `warp.md` already described in prose. |

### Drawing table

| element | type | drawn as | level / role |
|---|---|---|---|
| Warp (WHO-1/WHAT-4) | persistent structure | one amber-stroked bounding box enclosing the full 32×4 grid | outermost container, present unchanged across all rows |
| Lane *i*, path A (WHO-1, i=0–15) | actor | a column of 4 cells, teal hue | spine column, position-identity = "path A" |
| Lane *i*, path B (WHO-1, i=16–31) | actor | a column of 4 cells, coral hue | spine column, position-identity = "path B" |
| Cell (lane i, cycle t) (WHAT-2) | computed result / mask state | small square: bright+solid border = executing this cycle (shows `c[i]` for representative lanes), dim+dashed border = masked this cycle | grid body, one per (lane, cycle) |
| Branch-fork marker (HOW-1 shape 5) | control event | gold-outlined fork glyph between row 1 and row 2, labelled `i < 16 ?` | accent, marks the divergence transition |
| Reconverge marker | control event | gold-outlined merge glyph between row 3 and row 4 | accent, marks the reconvergence transition |
| Row headers (WHEN-1) | phase labels | `STEP n/4` chip + op-code + one-line caption, left margin | one per row |
| Lane-index axis | scaffold | tick labels 0, 4, 8, …, 15|16, …, 28, 31 above the grid | scaffold, legend-exempt from entity table per protocol note |

Layout is by the actor/time grid described above (columns = lanes in index order,
rows = cycle order top-to-bottom) — not narrative reading order, but this happens to
coincide with reading order here since lane index and time order are both the
mechanism's own natural axes.

## Animate vs. static — decision and justification

**Decision: static.** The whole figure is one non-animated SVG; there is no SMIL/CSS
motion.

Justification: per VISUAL_PROTOCOLS rule 5, a mechanism figure animates *by default*,
but the annotated exception is for genres "whose defining fact is a structural
invariant rather than a process" where the SHAPE bullet is legible in one static
frame. A cycle-by-cycle trace grid is the case that exception was written for, one
level more literally than the listed examples (address/stack, layered stack,
comparison): here **time is not merely invariant-like, it is already a drawn spatial
axis** (the rows). Animating on top of that would mean encoding the same ordering
information twice — once as row position, once as playback position — which is exactly
what anti-pattern 8 warns against ("never let animated elements run on independent
clocks"): a sweeping "now" marker over the grid's own row axis would either (a) merely
re-narrate the row order the reader can already see, adding no information, or (b)
desynchronize from it if authored loosely, which is a worse failure than not animating.
The protocol's own "Prefer a static storyboard... unless you have real playback
verification" (anti-pattern 10) also favors this: a trace grid *is* the storyboard —
every phase is simultaneously present and independently verifiable per row, with no
frame-0-only blind spot possible, because there is no frame 0 that hides other frames.

## (b) Dynamics

No cross-actor travel — nothing here is a dataflow genre, so the "must be seen to
travel" rule for inter-actor packets does not apply (SIMT's whole point is that no data
moves: one instruction reaches all lanes without any of them exchanging values). The
only "motion" this figure represents is a lane's own state persisting down its fixed
column across cycles — each lane's column is itself the "persistent drawn path" its
state rides on, read top-to-bottom, satisfying the traceability rule (rule 5) without
needing arrows: a reader can follow lane 20, say, straight down its column and see
bright → masked → executing(SUB) → bright, with no ambiguity about identity, since hue
(path A/B) never changes and only opacity/border style changes.

## (c) Ordered phases → static storyboard panels

Four rows = four `STEP n/4` panels, one master grid, no separate ACT split needed
(each row already is a self-contained ACT, per the "grid itself is time" decision above).

- **STEP 1/4 — shared ADD, pre-branch.** All 32 lanes bright (path-A teal / path-B
  coral, both at full opacity). Every lane executes `c[i]=a[i]+b[i]` on its own data.
  Zero lanes masked. Caption: "one instruction, 32 results, 0 lanes idle."
- **STEP 2/4 — branch pass A.** Predicate `i<16` evaluated (gold fork glyph above this
  row). Lanes 0–15 (path A) stay bright, executing the ADD arm again (`c[i]=a[i]+b[i]`,
  same formula, source's own construction). Lanes 16–31 (path B) go dim+dashed — fed
  the instruction, discard the result. Caption: "16 lanes work, 16 lanes masked off."
- **STEP 3/4 — branch pass B, masks flipped.** Lanes 16–31 (path B) now bright,
  executing the SUB arm `c[i]=a[i]-b[i]`. Lanes 0–15 (path A) now dim+dashed — masked,
  holding their step-2 result. Caption: "masks flip; the other 16 lanes work now."
- **STEP 4/4 — reconverged.** Gold merge glyph above this row. All 32 lanes bright
  again on the next shared instruction — no branch, no masking. Caption: "both arms
  done; the warp is back at full width — 'the 32 threads always retire together.'"

## (d) Color — ONE identity dimension + ONE accent

- **Identity dimension = position** — which half of the warp a lane belongs to under
  the branch predicate (path A = lanes 0–15, path B = lanes 16–31). This is fixed by
  lane index and never changes across the whole figure (unlike a "current-assignment"
  dimension, which would revert to neutral between bindings — here the assignment is
  permanent for the life of the figure, since the predicate is a pure function of lane
  index).
  - Path A: teal `#3F9B86`.
  - Path B: coral `#D85A30`. (Reused here as a *data/position*-identity hue, per the
    protocol's own note that hues are genre-scoped, not global — this SVG is the
    mechanism/dataflow genre, where coral is not reserved for "operator" as it is in
    the math genre.)
- Idle/neutral house color `#FBF0DB` fill / `#C79A3E` stroke is used only for the
  non-data scaffold: the persistent warp bounding box and the lane-index axis ticks —
  never for a masked *data* cell (a masked lane still has a data identity, it is just
  temporarily inactive, so it keeps its path hue at low opacity rather than being
  repainted neutral).
- Opacity = state: bright/opaque = executing this cycle; dim (~0.22 opacity) + dashed
  cell border = masked this cycle. There is no "future" state to encode (nothing is
  faint-for-not-yet-drawn) because every row already co-exists on canvas — the grid has
  no frame-0-only content.
- **ACCENT (gold `#E8A02E`, one only)** = the fork glyph (row 1→2, divergence) and the
  merge glyph (row 3→4, reconvergence) — the two moments the mask configuration changes
  state. Nothing else takes gold.

## (e) Worked instance carried to the visible answer

See ANCHOR-1 above. Every number derives from the source's own `a[i]=10(i+1)`,
`b[i]=i+1`: lane 0 → 11 (cycles 1–2), lane 1 → 22, lane 2 → 33, lane 15 → 176 (cycle 1
and again cycle 2, since the branch's true-arm repeats the identical ADD — this is the
source's own construction, not a coincidence I introduced); lane 16 → 153 (cycle 3),
lane 17 → 162, lane 31 → 288. Middle lanes (3–14, 18–30) keep their grid cell (true
32-wide shape preserved) but are labelled only by index, not by a re-derived numeric
value, to keep the figure legible — their formula and colored/masked state are
identical to their nearest labelled neighbor, so no information is lost by eliding the
arithmetic repetition (same-logic elision, analogous to the WHY-2 guardrail).

## (f) Stays as caption / text

- The retire-together invariant (quoted verbatim, WHAT-4).
- WHY-1 cost line: "branch costs 2 cycles vs. 1 for an agreeing warp — count the rows."
- One-line cross-reference for the omitted 32-way worst case (WHY-2): "a warp where
  all 32 lanes disagree serializes up to 32 passes, one lane wide each — see [[warp]]."
- One-line SIMD contrast (WHY-1-flavored, not drawn): "SIMD would need this masking
  written by hand; here the hardware does it — no vector register appears above."
- Legend: path A / path B hue, bright = executing, dim+dashed = masked, gold = mask
  transition (fork/merge).
- `STEP n/4` chip + one-line caption per row (per the static-storyboard,
  once-per-panel convention — here "panel" = "row"; ).
- Omission check applied: lane count (32), cycle count (4), and the fact that path A/B
  split is exactly 16/16 are all directly countable from the drawing and are not
  separately captioned as numbers (only named in row captions where they anchor a
  specific transition, e.g. "16 lanes masked off").
