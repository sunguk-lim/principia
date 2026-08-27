# Figure spec — `<node-id>` (Step 0)

> TEMPLATE — copy to `specs/<id>.spec.md` and fill every section. A section that does not
> apply is written `n/a — <reason>`, never deleted: the absence must be a decision, not an
> oversight. Derived FROM `nodes/<id>.md`; governed by `protocols/VISUAL_PROTOCOLS.md`
> (mechanism/dataflow protocol) and `protocols/EXPLAIN.md`.

## Visual teaching contract

Complete this section before choosing a genre, inventorying entities, or drawing SVG.

**Audience:** `<who is unfamiliar with this concept, and what prerequisites may the figure rely on?>`

**Single job:** `<the one understanding this figure must deliver; not “teach the whole node”>`

**Visual thesis — one sentence:**

> Because `<problem>`, `<concept>` changes `<before>` into `<after>` by `<decisive action>`, so
> `<payoff>`.

**Traced object:** `<one concrete value/request/token/region from the worked instance>`

**Subject visual vocabulary:** `<real shapes, materials, instruments, spatial relations, operations,
and characteristic motion available from this concept>`

**Signature moment:** `<the one concept-specific event receiving dominant scale, contrast, or motion>`

**Anti-template test:** `<what makes this composition unable to explain an unrelated concept by merely
changing its labels?>`

Plan every visual channel before rendering. Write `neutral — no semantic job` rather than inventing
meaning for an unused channel:

| channel | fact encoded | planned treatment |
|---|---|---|
| **Form** | `<entity/type/shape>` | `<treatment>` |
| **Space** | `<containment/order/relationship>` | `<treatment>` |
| **Scale** | `<magnitude/importance>` | `<treatment>` |
| **Colour** | `<one identity dimension>` | `<treatment>` |
| **Rhythm** | `<sequence/recurrence/dwell importance>` | `<treatment>` |

State how one visual model becomes progressively more precise. These are disclosure levels, not
necessarily separate panels:

| level | what the reader sees | words/notation introduced | what remains unchanged |
|---|---|---|---|
| **Intuition — what and why** | `<dominant picture showing problem + payoff>` | `<few short labels>` | `<traced object, identity, layout>` |
| **Mechanism — how** | `<decisive transformation on the same object>` | `<essential technical names>` | `<same visual model and mapping>` |
| **Precision — limits/exactness** | `<exact shapes, values, equation, boundary, or substrate>` | `<minimum qualifying detail>` | `<same thesis and traced result>` |

**Comprehension test — intended answers from the figure alone:**

1. What problem exists? — `<answer>`
2. What changes? — `<answer>`
3. What causes the change? — `<answer>`
4. Why is the result useful? — `<answer>`

**First-view constraints:** State how the intuitive view remains legible when the whole figure is fit
to a mobile screen and a laptop window. List any detail deliberately deferred to the mechanism,
precision, caption, or node prose.

**Plan critique:** `<which initially plausible but generic choice was rejected or revised, and why?>`

**Rendered critique:** Record findings from the static fallback, every dwell, and representative
mid-transit frames at mobile and laptop fit-to-screen sizes. Name the element removed during the
mandatory subtraction pass; restore it only if a specific comprehension answer becomes weaker.

**Reduced-motion result:** `<how the static fallback/storyboard preserves the thesis and exact result>`

## Genre & spine

Pick the concept's defining shape; it IS the layout:
dataflow · grid/tiling · hierarchy/nesting (including a **concentric/radial** realization
when the concept's own vocabulary is spatial-radial — ring/shell/orbit, inner = more
contained/privileged/central; prefer radial over "layered stack" whenever the concept's own
terms name a radial structure, not a linear one) · address/stack · layered stack ·
state machine · timeline · comparison · curve/plot (a continuous quantity plotted against
another, with regime regions and/or a crossover/peak point — scale and shading conventions
per VISUAL_PROTOCOLS rule 9) — plus any overlays (e.g. "hierarchy carrying a
flow overlay animated as change over steps").

Tie-breakers when two axes both look spine-worthy (first check: a supporting
cost/timing/magnitude fact that never competes for spatial layout — it only motivates or
quantifies the spine — is not a tie-break case at all; route it to WHY-1's small-inset
allowance directly. Second check: run VISUAL_PROTOCOLS rule 9's IS-IO-bound test — if the
figure's own on-canvas magnitudes derive from a bandwidth/capacity number, the resource
hierarchy that number lives in IS the spine, decided before any two-axis analysis):

- **The defining shape IS two (or more) co-equal peer designs** answering the same underlying
  problem (genre = comparison): skip tie-breaking entirely — there is no primary axis and no
  subordinate challenger to arbitrate; the peers co-own the spine as the comparison's sides.
- **No second spatial axis exists at all:** when the mechanism's actor/participant set (WHO-1)
  is the figure's only spatial multiplicity — no independently-asserted competing axis — that
  actor count directly supplies the spine's own subdivision (one row/column/lane per actor).
  Nothing to tie-break: skip the two-axis analysis entirely.
- **Two competing spatial axes:** the one answering "what makes this concept *itself*, as
  opposed to how it's computed" owns the spine; the other becomes a subordinate panel that
  appears only where it's needed. Subordinate treatment includes **nesting inside the spine's
  own containment** (when the losing axis bears residency, global rule 2 dictates it); use a
  separate panel only when nesting would misrepresent something the figure asserts
  (see VISUAL_PROTOCOLS rule 8).
- **The "losing axis" is just the spine's own state changing across steps** (not a distinct
  spatial shape competing for layout): not a tie-breaker case at all — skip straight to
  animating the spine per the mechanism default.
- **A second, independently-complete COMPUTATION reaching the identical result** (recurrence
  vs. convolution, iterative vs. closed-form): default it to a comparison-genre subordinate
  panel that earns its ink by proving the magic-step justification; it needs no spine of its own.
- **Time itself becomes a second DRAWN spatial axis** (rows OR columns = cycles/steps in a
  trace grid — the *timeline* genre; the ordered-stage axis may occupy whichever grid axis
  the case/instance axis does not) rather than the animation axis: not a competing axis to arbitrate;
  the grid is the spine and the figure is a static storyboard by construction (rule 5's
  invariant-genre exception applies — a time-axis grid is already every frame at once).
- **Same mechanism, same spine, different value of a free parameter** (batch size, replica
  count) with genuinely different outcomes — not an identical result reached two ways, and not
  a competing spatial axis: draw both parameter settings as lanes sharing one spine's
  tiers/containment, reserving a separate co-equal panel only when nesting would misrepresent
  an invariant (rule 8).
- A **composite HOW-1** (multiple constituent control shapes governing different portions of
  one mechanism) does not by itself license a second spine or panel: check each constituent
  shape independently against the bullets above — if none asserts its own competing *spatial*
  axis (they are just different modes of state-change on the same actor set), keep one spine
  and animate all constituent shapes as state changes within it.

## Figure trigger (EXPLAIN.md)

State whether drawing is warranted and why. Name the load-bearing ideas whose understanding
materially benefits from visual expression, each tagged with its visual kind:
- **SHAPE/structure** — <what spatial arrangement carries meaning?>
- **FLOW/routing** — <what path/movement carries meaning?>
- **CHANGE over steps** — <what unfolding process carries meaning?> (for a static
  identity / closed-form concept, `n/a — no temporal process` is a first-class answer,
  not a deficiency to argue around)

Guardrails — what does NOT earn drawn ink:

- Anything fully conveyed by one sentence/equation/table stays as caption text (list those
  facts here and again in §(f)). Exception: if a phase would land a simultaneous highlight
  across every already-drawn instance of a persistent structure across the whole spine —
  proving a stated invariant holds everywhere at once, not merely restating a fact in one more
  place — that capstone moment may earn its own STEP even when the underlying fact is a single
  sentence; judge against the diagrammatic payoff of watching it land, not sentence length.
- A contrast is caption-only even when it is *also* a SHAPE fact, if this figure's own drawn
  states already make it visible — add a dedicated panel only when the main figure alone does
  NOT show the contrast. Caption-only means at minimum ONE caption sentence naming the
  tension — never total silence — whenever already-drawn panels jointly reveal a genuine
  trade-off the worked instance itself produces, even if the node prose never names it.
- The figure does NOT owe on-canvas space to every enumerable edge case: if the node prose
  already states a same-logic edge case adequately, the figure may omit it entirely. This
  omission is **instance-conditional, not case-conditional**: it applies only when the chosen
  worked instance never actually produces the sibling case on canvas. If the instance's own
  step range passes through it (e.g. a loop iteration where the case genuinely occurs), draw
  it on that iteration.
- Before inventing a new accent/visual device for a provenance-style fact ("which part of X
  feeds output Y"), try one caption sentence first — a drawn device is warranted only when the
  mapping has enough internal structure (multiple sources, asymmetric cardinality) that prose
  would lose it.

## (a) Entity inventory — name everything BEFORE drawing

Fill the checklist first (or `n/a`), then expand into the table. This is the mechanism's
cast list; the single biggest cause of rework is an entity discovered mid-draw.
Per-row decision rules follow the table.

**Genre variant — math/quantity:** WHO-1, WHERE-1, HOW-2 default to `n/a — no
actors/substrate/protocol in a quantity concept` (one line each, no re-derived justification);
WHY-2 reads as *domain restriction / degenerate input*, not fault path; WHY-3 defaults to n/a
unless the concept is a literal design choice with a tension knob — an identity or derivation
is never a trade-off.

**Mechanism-genre defaults:** WHO-1 defaults to n/a for a single-agent mechanism (one engine,
no multi-party exchange — no re-derived justification needed); WHY-3 defaults to n/a when the
mechanism is a fixed guarantee rather than a tunable knob with genuine two-sided tension. A
phase for which the source supplies no numbers may collapse without invented placeholders —
the derive-on-canvas rule owes numbers only where the source itself has them. "No invented
placeholders" bans invented magnitudes/measurements, not a minimal invented structural
cardinality (an index count, a fork position) needed to satisfy ANCHOR-1's own
branch-exercise mandate when the source is qualitative: default to full collapse when the ACT
can be dropped without violating other rules; otherwise a minimal symbolic instance (generic
indices, no claimed real-world count) is permitted only if flagged in-figure as
structural/illustrative, never presented as a measured value.

**Genre variant — comparison/classification:** HOW-1 defaults to n/a when the spine is a
static classification — each case/row fixed to its bucket by an out-of-band decision the
figure itself never executes — rather than a depicted algorithm; name the closest control
shape only when an actual procedure runs on the drawn structure.

**Dual-genre concepts** (a math identity whose defining shape is itself an iterative
mechanism): the two variants apply **simultaneously** — math's actor/substrate/protocol n/a
defaults (WHO-1/WHERE-1/HOW-2) together with mechanism's animation/loop requirements (HOW-1,
WHEN-1, ≥2 iterations). They govern different rows of the same table, not competing readings
of the whole figure. The mirror case also exists: a mechanism whose defining shape is a single
non-iterative atomic combine but whose teaching payoff is a quantity/ratio fact (an intensity
scaling with a parameter) — this does NOT switch to the equation/math genre (no symbol-table
spine exists); classify as mechanism/dataflow and carry the quantity through the mechanism's
own to-scale proportions (rule 9), not the equation genre's cell/operator convention.

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | **actors / participants** (incl. nesting: thread⊂block, replica sets) | |
| WHAT-1 | **data items with identity** (moved/copied, never fused — each keeps its color; a WHO-1 actor whose per-step contribution is a fixed, non-decomposable cardinality may be drawn as one aggregate cell/bar-segment rather than an expanded per-token row — the derive-on-canvas rule owes detail only where the source has it) | |
| WHAT-2 | **computed / derived results** (folded from inputs — takes the *result* color, never a source's; for a 1:1 transform of one already-identified element — not a fold — keep the source's identity color and mark the transform instant with the single accent instead: the result-color treatment is for genuine multi-input folds only; exception: when the identity dimension is position/slot-membership and the result does not itself occupy a slot, do not inherit the source's position color — default to neutral house color with an accent ring at the creation instant) | |
| WHAT-3 | **running state** (accumulator, counter, running max — drawn as labeled cells, never bare text) | |
| WHAT-4 | **persistent structure + its invariant** (the object that outlives any one operation, and the one rule the mechanism preserves) | |
| WHERE-1 | **substrate / resource tiers** (memory levels, disk, links; a scheduler's fixed per-step compute/token budget or quota is a WHERE-1 capacity resource too — not only memory tiers) | |
| WHERE-2 | **layout / addressing rule** (logical coordinate → physical location: page→frame, key→shard, word→bank; n/a when no addressing scheme exists apart from actor identity; a plot axis's own value→pixel scale is governed by rule 9, not WHERE-2 — stays n/a for a curve/plot unless a genuine discrete addressing scheme also exists) | |
| WHEN-1 | **ordered phases** (the complete forward-and-backward step-list — every transfer) | |
| WHEN-2 | **concurrency lanes / timeline** (one lane per actor, when timing/ordering — not data — is the point) | |
| WHEN-3 | **before → after snapshots** (when the mechanism is a single global state transition) | |
| HOW-1 | **algorithm over the structure** (the read/mutate procedure + its control structure — state the order decision explicitly; see the five shapes below) | |
| HOW-2 | **protocol / message alphabet** (named message kinds whose sequence is the mechanism) | |
| WHY-1 | **quantities / complexity** (formulas, byte counts, O(·) — usually caption text, §(f)) | |
| WHY-2 | **failure / edge / degenerate branch** (the "catch": fault path, dropped packet, worst-case chain) | |
| WHY-3 | **trade-off comparison** (A-vs-B panel that justifies the design; when the spine itself IS the comparison genre, WHY-3 is satisfied entirely by the spine's own worked-instance panels — no separate inset, per rule 10's zero-ink escape hatch) | |
| ANCHOR-1 | **worked numeric instance** (concrete values, chosen to exercise every branch, carried to the visible answer) | |
| ANCHOR-2 | **composition refs** ("X = Y + Z" — name each prerequisite node AND its role in this figure) | |

### Decision rules per row

**WHAT-3 (running state):** n/a is valid when the combine is a single atomic op with no
asserted input order — never invent an accumulator just to satisfy the loop rule.

**WHO-1 (actors):** for a comparison genre with a peer multi-actor set on each side, use one
row listing both sides' sets, naming each side's own nesting depth explicitly — never force
symmetric nesting onto a side whose real structure has none; the asymmetry is often itself
part of the payload. When an actor's internal sub-components differ in real relative magnitude
(silicon/capacity/budget share) and that differential allocation is part of the concept's
causal argument, size each sub-component box **proportionally to its real share** (rule 9's
citable-constant allowance applies) — a generic uniformly-sized internals box forfeits the
floorplan's SHAPE payload even when a worked-instance mechanism is drawn elsewhere in the same
figure; the two are not substitutes.

**Coverage proofs (ring/rotate and similar pairing mechanisms):** when the central correctness
claim is "every pair over a symmetric index set is covered exactly once, without materializing
the full cross-product," check whether a **coverage grid** (one axis per side of the pair,
cells filling as rounds complete) is load-bearing SHAPE ink — a per-actor fill-bar proves
count-so-far, not pairing-completeness (no gaps, no double-counts); only the grid proves the
latter.

**WHAT-4 (invariant):** quote the invariant verbatim; if the source states it across multiple
adjacent bullets, splice the clauses together verbatim (connector/ellipsis fine) rather than
paraphrasing, and paraphrase only portions with no source wording at all. When the running
state IS the persistent structure (a streaming accumulator carrying its own invariant), fill
WHAT-3 and WHAT-4 by pointing at the same drawn element with a cross-reference — the default
whenever the running state IS the persistent structure, regardless of genre, including a
math-genre figure whose own spine is a fold/recurrence.

**WHERE-1 (substrate):** if the concept is IO-/bandwidth-bound, the bottleneck is the SPINE,
drawn to scale (see the IS-IO-bound test in VISUAL_PROTOCOLS rule 9). n/a when the only sense
of "location" is which actor currently holds a value — fold that into WHO-1. A bracket marking
which algorithm step is currently executing, with no capacity/proximity/bandwidth semantics,
is a HOW-1 execution locus, not a WHERE-1 entity. When a WHERE-1-eligible capacity resource's
slots are representationally identical to an axis already drawn elsewhere (same cells, same
cardinality, no separate occupancy/overflow semantics), WHERE-1 collapses to n/a with a
cross-reference to that axis — a capacity resource earns its own entity only when it has
geometry or fill-state distinct from what's already on canvas (a queue with slack, a buffer
with eviction). A physically singular substrate accessed by both sides of a comparison is
drawn ONCE — shared beneath/between the panels, per global rule 2's residence principle;
duplicating it misrepresents one resource as two. Encode each side's differential access via
per-side link thickness/position (rule 9), not by redrawing the substrate.

**WHEN-1 (phases):** every transfer names who moves what, to where, and what is freed — but
each of who/what/where/freed applies only where the source actually asserts it: a mechanism
that only grows, never evicts, legitimately has no freed column; omit rather than invent.

**HOW-1 (the order decision — pick the control shape, or the COMPOSITION of shapes, that
governs the mechanism):** a single pass may genuinely chain shapes (most commonly shape 3 →
shape 2: concurrent independent per-actor chains feeding one atomic combine — the map/reduce
pattern). Name each constituent shape and the portion of the mechanism it governs; the shape
governing the **combine** is what decides WHAT-3.

0. **Lockstep broadcast** — one instruction/control signal reaching every actor in the same
   step, each computing independently on its own data: no fold, no branch, no per-actor
   timing. The baseline beneath shape 5's branch and shape 2's combine — name it rather than
   forcing it into an ill-fitting shape.
1. **Sequential fold** — the source asserts an order among the inputs. A state-carrying loop
   must show ≥2 iterations with the state visibly evolving between them.
2. **Atomic/parallel combine** — an associative/commutative combine over a symmetric,
   unordered input set: all inputs travel together, one result emerges, no manufactured
   accumulator (WHAT-3 n/a).
3. **Concurrent independent instances** — many separately-ordered chains overlapping in time
   with no VALUE folded across them, though they may share a pure CONTROL-flow rendezvous
   (a barrier/join: an arrival counter reaching N releases all at once — draw that
   gate/counter as WHAT-3/WHAT-4, not a new shape). "≥2 iterations" is satisfied by ≥2
   concurrently-advancing instances.
4. **Producer/consumer via persistent shared state** — one instance populates a durable
   structure (WHAT-4), a later one reads it: two one-way transfers sharing one drawn
   structure — not a fold, not concurrent lanes.
5. **Conditional branch** — one input routed down mutually exclusive paths by a runtime
   predicate (routine control flow, distinct from WHY-2's failure connotation): draw a
   simultaneous fork with the untaken path dimmed, or let the worked instance exercise each
   side once in sequence, or — when the illegal path is actively attempted, blocked mid-flight,
   and forcibly rerouted through the same channel the legal path uses (faults/exceptions
   reusing the normal entry gate) — draw the attempt, the visible block, and the forced
   redirect through the shared gate as one continuous traced journey.
6. **One-shot structured fan-out** — a single computational pass over an internally-ordered
   input (e.g. a causal/triangular structure) yields MULTIPLE simultaneous, order-dependent
   outputs. Not a fold (no sequential dependency in the pass's own execution) and not shape
   2's many-to-one combine (no single combined result — each output stays distinct and
   separately consumed). Draw all outputs appearing together at the one computation step,
   each tagged with the ordering its structure encodes.

**WHY-1 (quantities):** a one-sided contrast against a naive/legacy baseline — not a
two-sided trade-off, see WHY-3 — lives here as a magnitude motivator, and earns a small inset
only when the main figure's own drawn states don't already show that side of the contrast.
For any partition/shard/distribute mechanism, the **un-partitioned computation is a standing
candidate baseline**; run the own-states test **stage-by-stage, not only at the final output**.
A sharded intermediate that is a slice of a whole (or a partial of a true value) which never
exists on any single actor cannot show its whole inside the sharded figure — the whole's one
honest residence is a **subordinate unsharded baseline lane** running the same worked instance
at matching stages, so slice-vs-whole and partial-vs-true read as direct per-stage contrasts.
This baseline-lane trigger applies to slice-of-a-whole partitioning (tensor/data sharding)
only: a mechanism that distributes whole, indivisible units (experts, replicas,
shard-as-atom placement) across actors never produces a partial fragment of one true value,
so n/a requires no further justification there. It also never fires for a single actor's own
workload sliced across time/steps — that case is governed by the
same-mechanism-different-parameter tie-breaker instead.

**WHY-2 (edge cases):** usually a contrast panel. When several edge cases share one underlying
logic, show only the one anchored to a drawn element — same-logic siblings already covered by
the node prose may be omitted from the figure (subject to the instance-conditional guardrail
above). A routine either/or path is not a WHY-2 case — that's HOW-1 shape 5.

**WHY-3 (trade-off):** verify the panel shows a genuine tension — as the underlying knob
moves, name what improves AND what worsens. A panel where only one output gets better is a
magnitude illustration (WHY-1), not a trade-off, even if it looks like a comparison.

**ANCHOR-1 (worked instance):** it must also make the genre's defining shape unmistakable —
e.g. for hierarchy/nesting prefer ≥3 siblings and/or one level of nesting, since a single
shared parent with 2 children reads as a pair, not a tree. When the sanctioned instance
exercises only one of two structurally-asserted tiled axes, draw the silent axis structurally
(a faint/pending second tile or slot, no invented numbers) rather than fabricating values to
complete it. For a state-carrying loop the minimum instance size is set by HOW-1's
≥2-iterations rule in VISUAL_PROTOCOLS — cross-reference it, don't re-derive it per instance.
When the mechanism partitions a dimension into shards, size the instance so every shard — and
every per-shard derived intermediate the math allows — keeps **≥2 cells along the partitioned
axis**. Shard-count = dimension-size is the degenerate instance: a 1-cell shard renders as a
bare scalar, erasing the "strip carved from a whole" shape that makes the partition visible.
This ≥2-cell test targets partition/shard sizing only — it does NOT apply to a
workload/scenario parameter that is genuinely 1 in the real mechanism (e.g. a per-step batch
of 1): a parameter value is not a shard, and padding it to 2 would misrepresent the mechanism.

Then the drawing table (every WHO/WHAT/WHERE row above appears here):

| element | type | drawn as | level / role |
|---|---|---|---|
| | | | |

Layout is by the compute/data DAG (co-inputs share a level; containment matches residence),
**not** reading order.

## (b) Dynamics — routing / shape-evolution (mechanism) · provenance / derivation flow (math)

The coordinated motions, and which drawn element each one rides on. Every transfer must be
*seen to travel* along a persistent drawn path; transforms happen only inside the compute
tier that performs them, never in transit.

## (c) Ordered phases → animation frames (mechanism) · static storyboard panels in DAG order (math), with control structure

The Step-0 list from WHEN-1, expanded frame by frame (`F1…Fn`), grouped into ACTs. State
the control structure explicitly (the loop head, what repeats). One step = one atomic
stage; a loop that carries state animates ≥2 iterations with the state visibly evolving
between them. Include the failure/degenerate branch (WHY-2) as its own ACT or panel.

## (d) Color — ONE identity dimension + ONE accent

- **Identity dimension** = <data (each logical data item keeps one hue) | device (each
  physical execution unit keeps one hue) | type (scalar/vector/matrix class keeps one hue) |
  position (fixed index-derived membership — e.g. lane index or predicate-outcome group —
  held even while the element is dimmed/masked) | ownership/reference (which party
  currently holds or references a shared resource — distinct from "device" when the holder is a
  logical actor like a request/sequence, not hardware) | static origin/home (an identity fixed
  to an element's point of origin while it is held elsewhere — distinct from ownership's
  current-possession meaning; required whenever the mechanism's invariant says "returns to X,"
  not merely "ends up somewhere") | current-assignment (neutral/idle by default; an element
  takes a hue only while actively bound to a destination/role and reverts to neutral when the
  binding ends — for mechanisms with no persistent per-element identity outside the assignment
  window) — pick exactly one and state its meaning; hold it across the whole figure>
- For a math/quantity figure routed into mechanism-style animation, prefer **data**
  (per-named-variable identity) over **type** — type collapses to a single hue whenever the
  recurrence's moving parts all share one shape, and cannot discriminate the load-bearing entities.
- Idle/neutral: `#FBF0DB` fill, `#C79A3E` stroke (house amber).
- Control/bookkeeping scalars with no data identity of their own (a running max, a count) rest
  in the neutral house color — never a dedicated hue; the accent touches them only as a
  transient ring/pulse at the instant they update. A permanent hue on a control scalar quietly
  creates a second always-on accent and erodes the one-accent rule.
- Opacity = state: bright = active/now, dim = done/past or discarded, faint = future.
- **ACCENT (one only)** = gold `#E8A02E` for the single key event per step; a change *to*
  the accent marks a state transition. Nothing else ever takes it.

## (e) Worked instance carried to the visible answer

The concrete run (ANCHOR-1): input values → every intermediate → the visible result in the
spine. Every number on-canvas derives from other on-canvas numbers; drawn shapes stay
dimensionally honest (a scalar stand-in for a vector is still drawn/labeled at true shape).
For concurrency/timeline genres with N independent actors, choose per-actor timings so
arrival/completion order does NOT coincide with the actors' display/index order — a matching
order silently implies a causal/identity relationship the concept explicitly denies.

## (f) Stays as caption / text (not lettered onto the spine)

One-line rules, cost facts (WHY-1), the invariant statement, trade-off summary lines.
Plus: `STEP n/m` indicator, one-line caption per frame, small legend for the color code.

- **Anchoring:** a fact that belongs to a single drawn region/element goes **inline in that
  element's own label/subtitle**, not in a separate bottom caption list the reader must
  cross-reference. Reserve the separate caption block for facts about the figure as a whole
  (invariants, trade-off summaries, legends).
- The `STEP n/m` indicator and its per-step one-liner are always whole-figure header content —
  they summarize the current frame as a whole, never one region of it. Exception: in a static
  storyboard (all ACT panels visible at once, no single current frame), emit `STEP n/m` once
  per panel, anchored to that panel's own header — the panel is the equivalent of "the current
  frame." A "panel" may be a row/band within one continuous grid (a time-axis trace) — the
  per-panel rule applies to grid rows or columns identically — and when the stage axis is
  columnar with self-labeling headers (named stages, S1/S2/S3), a numeric STEP chip is
  redundant and may be omitted. In a two-scale zoom/detail-link layout
  where only one panel animates, STEP-scoping is decided independently per panel: the static
  panel (zero phases) omits the chip; the animating panel keeps its own STEP n/m. A setup/initialization state preceding the first real step is not counted in the
  denominator — label it distinctly ("SETUP") rather than incrementing m. Symmetrically, a
  trailing hold/loop-reset state after the last real step is uncounted too — give it its own
  label ("one cycle complete"), never a vacuous STEP m+1/m. When the whole
  figure has zero ordered phases (WHEN-1 n/a for the entire figure), omit the STEP chip
  entirely — never emit a vacuous "STEP 1/1" implying a sequence where none exists.
- **Omission check:** before anchoring a fact anywhere, check it is not already directly
  legible from the drawing itself (e.g. a count recoverable by counting cells) — if it is,
  omit it from both locations; captions exist only for facts the drawing cannot state on its
  own, and an anchoring/geometry conflict is often a sign the fact was redundant, not that it
  needs a home.
