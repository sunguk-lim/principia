# Figure spec — `flash-attention` (Step 0)

> Derived FROM `nodes/flash-attention.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and
> `protocols/EXPLAIN.md`.
>
> **Number methodology — the reference's honest-dataset method (refFA
> `flashattention_component.jsx` lines 83–111), NOT a hand-picked single row.** Define a real,
> small, integer Q/K/V dataset ON CANVAS and COMPUTE every block's S_ij = Q_i·K_jᵀ and the full
> running (m, ℓ, O, α, β) by real arithmetic (the drawer runs a tiny trace script, exactly like
> the reference's `trace()`), so EVERY block in the Tr×Tc grid carries consistent real numbers —
> no block left number-less, no number fabricated. This is the whole point of the reference's
> comment "Real example data so the trace is consistent & honest." The node's own single-query
> illustration (S=[1,3,2,5]) cannot exercise the outer loop, so it is generalized to a real
> multi-tile dataset; on-canvas Q/K/V are the source of truth and every number derives from them.
>
> **Concrete dataset for this figure** (d=2, N=4, Br=2→Tr=2, Bc=2→Tc=2, SCALE=1 for clean integers):
> Q = [[2,0],[1,1] | [0,2],[1,0]], K = [[1,0],[0,1] | [1,1],[2,0]], V = [[1,0],[0,1],[1,1],[2,2]]
> (the `|` marks the tile boundary). Then S = Q·Kᵀ has blocks
> S_00=[[2,0],[1,1]], S_01=[[2,4],[2,2]], S_10=[[0,2],[1,0]], S_11=[[2,0],[1,2]] — a 2×2 grid of
> 2×2 blocks. The outer loop runs TWICE (i=0 then i=1), and both rows hit a real max-grows rebase
> on their j=1 block (row0: 2→4, row1: 1→2; i=1 row: 2 on j=1), so α is genuinely exercised. The
> drawer MUST compute the (m,ℓ,O) trace with a script and render the actual resulting numbers —
> verify, do not hand-copy.

> **[USER-grounded, governs this whole spec] Never unfold this nested loop along the time axis.**
> A real reader rejected an earlier version of this figure: *"you are not showing the tiling and
> second-order iterations. You shouldn't have unfolded along the time-axis."* That earlier version
> set Br=1, traced a single query row, and linearized its inner loop into 15 time panels — which
> collapsed FlashAttention's 2-D iteration space to 1-D and deleted the outer loop entirely. This
> spec MUST instead draw, as co-equal first-class objects on one master clock (protocol
> anti-pattern 17):
> (i) the **iteration space** — the S = Q·Kᵀ block-tile grid, Tr row-tiles × Tc col-tiles, with
>     exactly ONE block "computing now" and every other block in an explicit state
>     (done-and-folded-into-O · not-yet-computed);
> (ii) the **loop structure** — the actual nested pseudocode with the currently-executing line
>     highlighted (a line pointer);
> (iii) **both loop counters live** — `i = ?/Tr, j = ?/Tc`.
> The cursor sweeps THROUGH the grid and the OUTER loop advances at least once (complete output
> tile O₁ → reset carry → begin Q₂), so the second-order iteration is actually exercised, never
> left "faint/pending" forever.

> **Genre:** a **two-region synchronized mechanism** (grid/tiling + resource-hierarchy), one master
> clock. LEFT region (the primary reading object, where the eye starts) = the **iteration space**:
> the S-tile grid + the nested-loop pseudocode with a line pointer + the (i,j) counters. RIGHT
> region = the **memory hierarchy substrate** (HBM ⨯ SRAM ⨯ registers), showing what is resident and
> what crosses the link each clock. The two are coupled: the block that is "computing now" in the
> grid is exactly the tile resident in SRAM/registers on the right — that coupling IS FlashAttention
> (IO-aware tiling), so both substrates are drawn, neither buried inside the other.
>
> **Tie-breaker reasoning (revised):** the earlier spec made the memory hierarchy the sole spine and
> demoted tiling to a detail drawn *inside* it. That is what hid the tiling and nesting. FlashAttention
> is *both* facts at once — (1) the tiled, doubly-nested sweep that keeps only one Br×Bc block live,
> and (2) the IO-awareness that this is what keeps the N×N matrix off HBM. Neither is subordinate;
> the concept is precisely their coupling. So the figure is two synchronized regions, and the
> iteration space is given reading primacy (left/first) because that is the axis the reader was
> shown to need.

## Figure trigger (EXPLAIN.md)

Drawing is warranted: this is a HARD, irreducibly visual mechanism — a tiled, doubly-nested
streaming algorithm with running state, whose entire point is a **structural** fact (a 2-D
iteration space swept one block at a time) coupled to a **resource** fact (where bytes live and
travel) plus a **temporal** fact (state evolving under a rebase rule).

- **SHAPE/structure** — the S = Q·Kᵀ **block-tile grid** (the iteration space), and Q/K/V/O each
  partitioned into tiles that are *slices* of the true matrix, never abstract boxes; the HBM
  (huge, slow, off-chip) vs SRAM (tiny, fast, on-chip) containment on the right.
- **FLOW/routing** — the K,V tile streaming from HBM into SRAM, folded, discarded; the finished
  O-tile written back; the single link both directions share (the bottleneck).
- **CHANGE over steps** — the cursor sweeping the grid under the nested loop, and the running carry
  (m,ℓ,O) evolving tile-by-tile with the one-multiply rebase when a new tile's max exceeds the
  carried max. This is the mechanism's whole reason to exist, so it is not caption-only.

Guardrail check: the formulas themselves ($O=\mathrm{softmax}(S)V$, the O(n²)/O(n) cost) are
one-liners and stay caption-only (see §f). The nested-loop pseudocode is NOT caption-only — it is a
first-class panel (the loop structure the reader must see), per anti-pattern 17.

## (a) Entity inventory

**Mechanism-genre defaults applied:** WHO-1 → n/a (single-engine mechanism). WHY-3 → n/a (node
presents FlashAttention as a strict win — same output, less traffic — never a tunable trade-off).

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | n/a — single streaming kernel |
| WHAT-1 | data items with identity | Q, K, V, O — each keeps one color the whole figure; Q/K/V given, O derived-but-identity-bearing |
| WHAT-2 | computed / derived results | per-block scores S_ij (= Q_i·K_jᵀ), local weights P̃ = e^(S−m); derived-color (orange), never a source's color |
| WHAT-3 | running state | carry (m, ℓ, O) — 3 labeled cells in SRAM, mutated block-by-block along the inner loop, **RESET when the outer loop advances to the next Q row-tile**; MUST animate the full inner sweep AND one outer advance |
| WHAT-4 | persistent structure + invariant | the carry register IS the persistent structure (WHAT-3/4 merge); invariant quoted verbatim: "O/ℓ equals the true softmax over the keys processed so far" (holds after every inner block, for any valid running max m) |
| WHAT-5 | **iteration space** (the tiling) | the **S = Q·Kᵀ block grid**, Tr row-tiles (queries ↑) × Tc col-tiles (keys →); exactly ONE block is "computing now" (gold, in registers); others are done-folded / not-yet-computed. THIS is the tiling made visible — the object the earlier spec omitted. |
| WHERE-1 | substrate / resource tiers | HBM (slow, huge, off-chip) ⨯ SRAM (fast, tiny, on-chip) ⨯ registers — RIGHT region; qualitatively to scale (node gives no capacity numbers; stated in caption) |
| WHERE-2 | layout / addressing rule | row-tile index i → Q rows of block i (Br rows each); col-tile index j → K/V rows [Bc·j, Bc·(j+1)); the (i,j) pair addresses block S_ij in the grid |
| WHEN-1 | ordered phases | see §(c) — frames grouped by (outer i, inner j, phase) coordinates, NOT by a flat time index |
| WHEN-2 | concurrency lanes | n/a — single sequential doubly-nested loop |
| HOW-1 | algorithm over the structure | **doubly-nested loop**, drawn as pseudocode with a live line pointer: outer `for i=1..Tr` over Q row-tiles, inner `for j=1..Tc` over K/V col-tiles; inner body = load K_j,V_j → S_ij=Q_i·K_jᵀ → online-softmax fold into carry (rebase α when max grows); after inner loop, normalize + write O_i, then outer advances (carry resets). Order = **sequential fold** (rebase depends on encounter order). |
| HOW-2 | protocol / message alphabet | n/a |
| WHY-1 | quantities / complexity | O(n²) HBM traffic (naive, materializes full S) vs O(n) (FlashAttention, one block resident) — caption-only (§f); the grid's "one block live at a time" is the visual proof |
| WHY-2 | failure / edge / degenerate branch | "first block of a row, nothing to rebase yet" (m: −∞→3) — covered for free by the traced row's own first inner block; no separate panel |
| WHY-3 | trade-off comparison | n/a — strict win |
| ANCHOR-1 | worked numeric instance | the real on-canvas Q/K/V dataset above (d=2, 2×2 block grid), computed honestly for EVERY block by a trace script (like refFA). Both outer iterations (i=0, i=1) are fully numeric; each row's j=1 block triggers a real α rebase (max grows). No block is number-less; the outer loop is exercised with real data, not "shown as structure". |
| ANCHOR-2 | composition refs | [[transformer-attention]] ($O=\mathrm{softmax}(S)V$, baseline re-derived at O(n) traffic); [[softmax]] ($w_j=e^{S_j}/\ell$, max-subtraction invariance licensing any reference m); [[online-softmax]] (the streaming (m,ℓ,O) carry + one-multiply rebase, here applied to attention with 2-D tiling + HBM/SRAM IO motivation) |

Drawing table:

| element | type | drawn as | level / role |
|---|---|---|---|
| **S-tile grid** | WHAT-5 (iteration space) | Tr×Tc grid of blocks S_ij, rows = query-tiles (↑, labeled Q₁..Q_Tr), cols = key-tiles (→, labeled K₁..K_Tc); each block small but ≥ legibility floor; block STATE by fill: done-&-folded (muted teal + "→O_i"), computing-now (gold ring + "S_ij" + its scalar values on the traced block), not-yet-computed (faint dashed outline). Caption above: "Only one Br×Bc block exists at a time — the two loops sweep it across S." | LEFT region, primary object |
| **nested-loop pseudocode** | HOW-1 | a monospace code panel, ~14 lines, the two `for` headers indented to show nesting; the line executing THIS clock gets a highlight bar (the line pointer) | LEFT region, below/beside the grid |
| **(i,j) counter chip** | WHEN-1 / HOW-1 | a header chip reading `i = 2/Tr · j = 1/Tc · phase: compute S_ij` updated every clock | LEFT region, top |
| Q (full) | WHAT-1 | column of Tr row-tiles at true shape; the current i-tile bright, others neutral; lives in HBM (right region) with a copy Q_i in SRAM | HBM/SRAM |
| K (full), V (full) | WHAT-1 | Tc col-tiles at true shape, **columns = keys** (co-indexed with S columns — column-alignment rule); current j-tile bright | HBM, streamed |
| O (full) | WHAT-2/identity | column of Tr row-tiles; O_i filled when its row's inner loop finishes and writes back; others pending | HBM, result |
| HBM / SRAM / registers containers | WHERE-1 | right region: large HBM box (slow,huge,off-chip), small SRAM box (fast,tiny,on-chip), tiny register area inside; width∝capacity, vertical=proximity-to-compute; link drawn as the shared corridor (the bottleneck) | RIGHT region spine |
| Q_i / K_j / V_j resident copies | WHAT-1 (same color as source) | small grids in SRAM; K_j/V_j slide in from HBM; the OLD tile is evicted (opacity→0) the instant the new one slides — SRAM holds ONE block | SRAM |
| S_ij, P̃ cells | WHAT-2 | scalar cells, derived-orange, in the SRAM/register compute area; values toggle on | registers |
| α cell | WHAT-2 (the magic step) | 1 scalar cell, gets the ACCENT ring exactly when it fires/applies | registers |
| carry register (m, ℓ, O) | WHAT-3/4 | 3 labeled cells in a bordered box; persists across the INNER loop; **visibly resets to (−∞,0,0) when the outer loop advances** | SRAM, persistent-per-row |
| O_i result packet | WHAT-2→WHAT-1 | small grid; on inner-loop completion, normalize then slide SRAM→HBM into O row-i, land with accent ring | travels SRAM→HBM |

## (b) Dynamics

- **The cursor sweeps the grid.** Each inner-loop step, the "computing now" gold ring moves to the
  next block S_ij along the current row (j advances). Completed blocks in that row flip to
  done-&-folded ("→O_i"). When the row's inner loop ends, O_i is written and the gold cursor jumps
  to the FIRST block of the next row (i advances, j resets to 1) — the visible second-order step.
- **The line pointer tracks the pseudocode.** Every clock, the highlighted code line matches the
  phase in the (i,j) chip: `load K_j,V_j` → `S_ij = Q_i·K_jᵀ` → `m_new=max(...)` → `α=exp(...)` →
  `O_i = α·O_i + P̃·V_j` → (inner end) `O_i = O_i/ℓ_i` → `write O_i` → (outer step) back to `load Q_i`.
- **The carry resets on outer advance.** When i advances, the (m,ℓ,O) cells visibly blank back to
  (−∞,0,0) — the reader sees each output row is an independent fold, which is why only one block's
  worth of state is ever live.
- K/V block: appears at its HBM col-tile bracket (the slice it is carved from — anti-pattern 15),
  slides through the link corridor into its SRAM slot; old block evicted on arrival of the new one.
- Compute (S_ij, P̃, rebase α, ℓ/O update) happens ONLY inside the register/SRAM compute area —
  never on a value in transit (global rule 2).
- Every transfer rides a persistent visible path and lands squarely on its destination; a moving
  token passes BEHIND opaque labels, never over their text (anti-pattern 13 transit clause).

## (c) Ordered phases → animation frames

Control structure: **doubly-nested loop**. Frames are indexed by their `(i, j, phase)` coordinate
(shown in the counter chip), NOT a flat time counter — this is the anti-pattern-17 requirement made
concrete. One master clock (`repeatCount="indefinite"`, identical `keyTimes` on every animate
element). BOTH outer iterations are fully numeric (the honest dataset covers the whole grid); the
phase list below walks the full nested sweep i=0→1, j=0→1, with the actual computed numbers on canvas.

- **Setup** `(i=1, j=0)`: partition Q into Tr row-tiles, K/V into Tc col-tiles; the full S grid drawn
  with every block "not-yet-computed"; init carry m=−∞, ℓ=0, O=0; line pointer on `for i` / `Load Q_1`.
- **Row 1 (Q-tile 0), inner block j=1** (the WHY-2 degenerate case, for free): load K₁,V₁ → compute
  block S_00=[[2,0],[1,1]] (gold cursor on block (1,1)) → first max, nothing to rebase → weights +
  fold into carry; block (1,1) flips to done-&-folded.
- **Row 1, inner block j=2** (the magic step, rule 6): evict K₁V₁, load K₂,V₂ → compute block
  S_01=[[2,4],[2,2]] (cursor on block (1,2)) → new max grows (2→4) → α=e^{2−4}=0.135 [ACCENT] →
  rebase old carry by α → merge block 2; block (1,2) flips to done-&-folded. Row 1 inner loop complete.
- **Row 1 finalize + write-back**: normalize O_1 = O/ℓ (in registers, computed value on canvas) →
  O_1 packet slides SRAM→HBM into O row-1, lands with accent ring; line pointer on `write O_i`.
- **Outer advance to Row 2** `(i=2, j=1)`: line pointer jumps back to `for i` / `Load Q_2`; carry
  visibly RESETS to (−∞,0,0); gold cursor jumps to block (2,1)=S_10=[[0,2],[1,0]]; row-1 blocks stay
  done. The second-order iteration, with real data.
- **Row 2 inner sweep + write-back** `(i=2, j=1→2)`: compute S_10 then S_11=[[2,0],[1,2]] (rebase on
  j=2), fold, normalize O_2, write to HBM row-2. Grid now fully done. Loop back to Setup.

The finer-grained ink goes to the load-bearing rebase steps (rule 10); row 2 is drawn at the same
fidelity as row 1 (real numbers throughout), so the nesting is undeniable and honest.

## (d) Color

- **Identity dimension = data role**: Q (indigo `#3B5BDB`), K (teal `#12897B`), V (magenta
  `#9C36B5`), O (green `#2F9E44`) — held across the whole figure, including traveling copies.
- Derived intermediates (S_ij, P̃, α) get their OWN color, orange `#E8590C` — never a source's color.
- Carry control scalars (m, ℓ) drawn in neutral house amber (`#FBF0DB`/`#C79A3E`), accented only at
  the instant they drive a transition.
- **S-grid block states**: done-&-folded = muted teal fill; computing-now = gold ring (the accent);
  not-yet-computed = faint dashed outline (≈0.32 opacity). These three states must be visually
  unmistakable at fit-to-screen size and keyed in the legend (glyph-semantics rule).
- **ACCENT** = gold `#E8A02E`, used ONLY as a stroke/pulse **ring** (never a fill), on the one key
  element per clock: the "computing now" grid block, α when computed/applied, m when it changes, and
  the O_i packet landing.

## (e) Worked instance carried to the visible answer

The reference's honest-dataset method: real on-canvas Q/K/V (d=2, N=4, Br=Bc=2, Tr=Tc=2, SCALE=1),
EVERY block computed by real arithmetic — the drawer runs a trace script (like refFA `trace()`,
lines 90–111) and renders the ACTUAL numbers it returns. Do not hand-copy; compute and verify.

Dataset (drawn on canvas as the true-shape Q/K/V matrices):
- Q = [[2,0],[1,1] | [0,2],[1,0]], K = [[1,0],[0,1] | [1,1],[2,0]], V = [[1,0],[0,1],[1,1],[2,2]].
- S = Q·Kᵀ blocks: S_00=[[2,0],[1,1]], S_01=[[2,4],[2,2]], S_10=[[0,2],[1,0]], S_11=[[2,0],[1,2]].

Outer i=0 (Q-tile 0, query rows 0,1):
- j=0 (K-tile 0): block S_00. Per-row: row0 max 2 → P=[1, e^{−2}=0.135], ℓ=1.135, O=1·[1,0]+0.135·[0,1]
  =[1, 0.135]; row1 max 1 → P=[1,1], ℓ=2, O=1·[1,0]+1·[0,1]=[1,1]. (First block: nothing to rebase.)
- j=1 (K-tile 1): block S_01. row0 max grows 2→4 → α=e^{2−4}=0.135 [ACCENT]; row1 max grows 1→2 →
  α=e^{1−2}=0.368. Rebase the carried (ℓ,O) by α, then merge this block's weighted V. (Real rebase.)
- Finalize: O_1 = O/ℓ per row, written to HBM O rows 0,1.

Outer i=1 (Q-tile 1, query rows 2,3): carry RESETS; same inner sweep over S_10, S_11 (rebase on j=1),
normalize, write O_2 to HBM rows 2,3. Grid fully computed.

Every number on canvas derives from the on-canvas Q/K/V by the drawn arithmetic — the strongest form
of "derivable on-canvas". Q/K/V drawn at true shape (2-vectors as 2-cell strips), no invented
components. The exact ℓ/O decimals are whatever the trace script computes; the spec fixes the dataset
and the mechanism, the drawer fixes the digits by computing them.

## (g) Animation choreography constraints (HARD — two prior rebuilds passed structure but failed here)

The structure (grid + nested pseudocode + line pointer + counters + memory coupling) is correct in
prior candidates; the mechanism gate blocked them on TIMING. A fresh build MUST obey both:

1. **The line pointer LEADS; state values FOLLOW — never the reverse (causality; anti-pattern 12).**
   A state cell may display a value ONLY at/after the clock moment the line pointer reaches the code
   line that produces it. Concretely, within one inner block's window the order is strict: pointer on
   `S = Q_i·K_jᵀ` → the S_ij register fills; pointer on `m' = max(...)` → m updates; pointer on
   `α = e^(m−m')` → α fills AND gets its ACCENT ring; pointer on `ℓ = α·ℓ + …` → ℓ updates; pointer on
   `O = α·O + …` → O updates. The carry must NOT show a block's fully-folded (m,ℓ,O) while the pointer
   is still on `S = …` or `max`. Each of these is its own frame/keyTime — do not collapse them.
2. **No dead-space blanking between steps (global rule 5 'no dead space').** Content must PERSIST
   across step transitions; only the element that actually changes animates (moves/updates/rings).
   Never blank the live content — S-grid values, resident tiles, compute cells, carry cells, the gold
   cursor, the code highlight bar, the step chip — to empty scaffold between steps. A transition is a
   continuous hand-off (old value dwells, new element animates in), never a fade-to-empty-then-refill.
3. **[USER-grounded] Every movement rides a drawn source→destination arrow (protocol anti-pattern 11).**
   Each transfer in this figure — K_j,V_j loading HBM→SRAM, and the finished O_i packet going SRAM→HBM —
   MUST have an explicit drawn **arrow from its source box to its destination box** with a visible
   arrowhead giving direction, and the moving element's animated position MUST interpolate **along that
   exact arrow line** (start on source, travel on the line, land on destination). No tile or packet may
   change position except by riding its arrow in the arrow's direction. The HBM↔SRAM link is that route
   drawn once; the K/V tile rides UP it into SRAM, the O_i packet rides DOWN it to HBM's O-row — each on
   the drawn line, never floating beside it or teleporting. Verify at a mid-transit timestamp that the
   moving element sits ON its arrow. A real reader rejected the prior build for movements that did not
   follow a drawn arrow path.

Verification: the cold-mechanism reviewer must step the frames in order and confirm that at every
frame, every visible state value is one the pointer's current-or-past lines have already produced, that
no frame shows only bare scaffold, and that at mid-transit every moving element sits ON a drawn
source→destination arrow. Any violation = FAIL.

## (f) Stays as caption / text

- Legend (top): color meaning for Q/K/V/O/derived/carry-scalars; the three S-grid block states; what
  the gold accent means.
- Bottom caption box: the invariant quoted verbatim; the O(n²)-vs-O(n) cost fact (with "the grid
  showing one live block at a time is the visual proof"); the one-line "same output, only WHERE the
  bytes live and HOW MANY cross the link change" summary.
- The `(i,j,phase)` counter chip is the whole-figure header (top bar), one coordinate at a time.
- Addressing rule + "not to scale" note: one caption box anchored in the HBM/right region.
- Inline, anchored to their own element: tile-size labels (Br, Bc, Tr, Tc) on the grid axes and Q/K/V
  headers; the α-identity justification ("one multiply rebases the WHOLE carry — α is independent of
  S") next to the α cell itself.
