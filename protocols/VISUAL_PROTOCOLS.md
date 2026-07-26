# Visual protocols — subsidiary (figure mechanics only)

> **Primary guidance is in `EXPLAIN.md`.** A node is taught by its **prose**, grounded in prerequisite
> nodes (the closed-world law) and the four explanation principles — all in `EXPLAIN.md`, which is
> **authoritative**. A **figure is optional and subsidiary**: draw one only when something is
> *irreducibly visual*. This file covers only how to draw that figure. Where a block contract below
> restates an explanation principle (worked instance, teach the why, concept spine, coordinated
> levels), `EXPLAIN.md` governs — here they apply to the figure case.

**Every rule here is universal.** State and apply each as a *general principle*. Any example is only an
*illustration* — it must never *narrow* the rule, and it must never name a specific concept you happen to
be drawing. A rule that genuinely fires only in a specific situation is allowed **only if it explicitly
annotates the condition** under which it applies (e.g. "when the figure has a memory-hierarchy axis: …");
an *unannotated* case-specific rule is overfitting and is banned. Otherwise generalize — record the
**principle**, not the incident.

**Organization.** A figure is a **composition of building blocks**, not an instance of a concept
category. §0 decides whether to draw at all. §1 is the catalog: for each fact the figure must express,
the block that renders it, with its contract and known failure modes. §2 gives the composition laws that
bind the assembled blocks into one figure. Legacy tags — `(rule n)` for the old global rules, `(AP-n)`
for the old anti-patterns, `(conv n)` for the old mechanism conventions — mark where each numbered rule
now lives, so committed specs citing those numbers still resolve.

**Craft stance (AP-1, AP-7).** Draw from your own understanding of the mechanism. A source figure is an
optional craft reference: if you use one, **render it and study every frame** — never reason from its
code or a single frame — and never copy it 1:1. That includes its *numeric shortcuts* (under-derived
numbers, silent rounding, implicit results — the figure still owes the full derive-on-canvas treatment)
and its *structural undercounting* (a drawing that lumps regions its own prose distinguishes).

## §0 — Draw at all?

Draw when the meaning is irreducibly visual: most strongly **SHAPE/structure**, **FLOW/routing**, or
**CHANGE over steps** — but also any relationship, comparison, or process a visual scaffold makes click.
Guardrail: what a single sentence, equation, or table FULLY conveys stays text (a bare number, a one-line
rule, a clean derivation).

For a mechanism, write its **complete step-list FIRST** (conv step-0): every phase, state, and
data-movement — forward *and* backward, every collective, every transfer (who moves what, to where, then
what is freed) — from your understanding of how it works. The figure must show **all** of it (n/a is
valid for a backward half the node's own prose never asserts — do not invent one). A partial mechanism
reads as wrong and is the single biggest cause of rework.

## §1 — Building blocks

Express each fact with its block; blocks compose freely under the §2 laws.

### B1 · Data atoms — a value, at its true shape

| value | block |
|---|---|
| scalar | single **cell**, labeled with a concrete example value ($d = 4096$, $r = 8$) — abstract letters blur; the value says *which* |
| vector | **strip** of cells |
| matrix | **grid** of cells |
| tile / shard / intermediate | **sub-grid** at its own true shape, shown as the highlighted slice carved from its parent — provenance (which rows/cols of which matrix) visible, never an abstract labeled box (AP-15) |
| running state (accumulator, running max/sum, counter) | **register** of labeled cells the reader watches update — never bare text; text-only state reads as annotation, not the data the loop maintains (rule 1) |

Contract:
- **No solid-block shortcuts** (rule 1, AP-5) — this covers *every* element: shards, partials,
  replicated inputs, not just the headline ones. A scalar stand-in for a vector/matrix operand still owes
  its true shape and/or a real-dimension label ("each = a $d$-vector"); so does anything *derived* from
  it (a weighted sum of value *vectors* is a *vector*).
- **Worked-instance values** (rule 4): concrete data, never placeholders; carried to the visible result
  in the spine (no blank output slot); **every shown number derivable on-canvas** from other on-canvas
  numbers; drawn shapes dimensionally consistent (show all *k* rows, or mark the one traced slice).
- **Stable identity** (rule 5): each logical element keeps one colour *and* label end to end, so a reader
  can follow a single element through every step; identity changes only mark transitions.

### B2 · Containers — where something lives

| residence fact | block |
|---|---|
| actor / device / engine | labeled **rounded box** |
| tier / scope / address space | **region**; containment = residence |
| nesting, trees, rings | **nested regions** (concentric when the concept's vocabulary names rings/shells; inner = more contained/privileged — an ordinal rank, no magnitude implied) |
| linear resource along one axis | **axis strip** |
| privilege / abstraction layers | **layer bands** |

Contract (rule 2): draw each element *inside* the region that physically holds it — never a box implying
a tier it doesn't occupy. **Computation has residence too**: a transform is performed only in a compute
tier; transport/storage tiers (caches, buses, memory) move bytes **unchanged** — never animate a value
mutating in transit or inside a cache. Depth-of-unpacking is an ink channel (rule 10): unpack to full
depth only the sibling(s) the worked instance traces; untraced co-equal siblings stay collapsed,
label-only.

### B3 · Connectors — relationships and routes

| relationship | block |
|---|---|
| static relation | **directional labeled edge** — the label a specific verb/protocol read in the arrow's direction ("scatters rows to", "reduces into", "reads page from"), never a vague word ("uses", "calls", "sends") (conv 3) |
| several static relations that would cross | a shared labeled **tinted region** — membership carries the relation; prefer containment over crossing (conv 1) |
| a movement's route | **persistent drawn arrow**, source box → destination box, visible arrowhead (AP-11) |
| pointer retargeting (no payload moves) | **edge state change** — the old target's edge dims to "superseded," the new brightens; never a traveling marker (conv 1) |
| correspondence across panels | **pairing glyph/line** (e.g. "≈") between matched levels (comparison) |
| optional / deferred / zoom link | **dashed** edge; a zoom-link's "same object at two scales" is a standing structural fact — mark the source tile with its own identity hue at higher emphasis, never spend the step accent on it (conv 4) |

Contract:
- **The flow *pattern* carries meaning** (conv 1) — converge (reduce), disperse (broadcast/scatter),
  all-to-all, rotate (ring), pointer-chain. Distinct message kinds need distinct line styles only when
  genuinely confusable (same path, direction, and time window); phase + payload colour is otherwise a
  sufficient alphabet.
- **[USER-grounded] HARD — every movement is an arrow the element rides** (AP-11): the moving element's
  animated position interpolates **along that exact drawn line** — starting on the source, landing on the
  destination, ON the line at any mid-transit instant, never floating beside it or teleporting past it.
  No element changes position except by riding a drawn arrow in the arrow's direction. Author routes to
  avoid cutting across unrelated elements' boxes mid-transit.
- **Cyclic/ring topology** (AP-11): arrange the actors along the ring's own adjacency (a square or
  circle) — never a linear row with modular wraparound, whose wrap edge becomes a long cross-cutting jump.

### B4 · Motion primitives — change over time, on ONE master clock

| change | block |
|---|---|
| payload moves | **traveling packet** riding its drawn arrow (B3), visible across the whole journey — never a fade-in/out blip (AP-11). It rides over the static labeled track, flips to the accent colour at the key transition, and carries a background-coloured halo stroke |
| value computed | **state flip** in place: pending/faint → live, exactly at its own compute phase (AP-12) |
| the one key event | **accent ring/pulse** on the single element changing now (conv 4) |
| loop advance | **cursor** over the iteration grid + **line pointer** in the pseudocode panel (B7) |
| carry reset / eviction | **visible blanking** back to the initial state |

Contract:
- **One master clock** (AP-8): every animation shares aligned `keyTimes` (or one `dur`); independent
  clocks drift and read as sloppy.
- **Continuous transit, discrete dwells** ([USER-grounded], conv 5): `calcMode="discrete"` is reserved
  for opacity/state flips — never position/transform, which snaps/warps. Every move is a watchable
  interpolated transit over a visible fraction of a second, then a dwell. Never teleport. **Pacing
  carries meaning**: a longer dwell flags the costly/critical step; a loop packing many phases lengthens
  its cycle rather than racing into flicker.
- **A packet carries its origin's value** (conv 2, rule 2): transforms (normalize, reduce, cast) are
  compute steps rendered inside the compute tier, *then* the packet carries the result unchanged — a
  value never silently changes identity between boxes.
- **Causality** (AP-12): a display slot shows a value only at/after the phase that computes it. A reused
  slot gates to pending even when its upcoming value equals the previous one; a step never shows a later
  step's result.
- **No dead-space blanking** (conv 5): content persists across step transitions — only the element that
  actually changes animates; never fade the live scene to empty scaffold and refill.
- **Transit occlusion** (AP-13): a moving token never paints OVER another element's text — route around
  it, or paint the token earlier so it passes behind (reads as "through the station").
- **Animate the substance, not a cursor** (conv 5): as steps advance the depicted state changes — values
  update, cells fill, the accumulator grows. A highlight sweeping an otherwise-frozen diagram animates a
  bookmark, not the mechanism.
- **State-carrying loops walk ≥2 iterations** (conv 5), with the carry visibly evolving *between* them —
  at EVERY nesting level of a multi-scale loop; the second walked iteration uses genuinely different
  data, so growth is witnessed, not asserted. Make the loop visibly loop (the pointer returns to the
  loop head). At each step the **delta** is explicit: what changes, what stays.
- **Decide the combine's order before animating** (conv 5): associative/commutative over an unordered
  set → one atomic many-to-one combine (no manufactured accumulator states). Inherently sequential
  (recurrence, chained/ring pass, streaming fold, prefix scan) → the serialized state-carrying loop.
  Concurrent independent instances → ≥2 instances advancing together (a barrier/join is a control-flow
  gate drawn as running state + persistent structure, not a new shape). Producer/consumer via persistent
  shared state → draw the durable structure as its own entity: a write into it, later a read out — two
  one-way transfers sharing one drawn structure.
- **Loop vs freeze, per branch** (conv 5): loop by default (`repeatCount="indefinite"`) after a short
  final hold — a figure is opened at an arbitrary time. Freeze only a genuinely one-shot terminal event
  (crash, irreversible change); a looping spine may contain a one-shot branch that stays terminal within
  each cycle.

### B5 · Status & narration blocks

| need | block |
|---|---|
| "what is happening right now" | **STEP n/m chip** + live loop counters (`i = 2/Tr · j = 1/Tc`) + the accent ring on the active element — mandatory, prominent, clock-synced for any auto-playing loop; any single frozen frame must be self-explanatory (AP-18, [USER-grounded]) |
| what this step does | **caption band**: one anchor slot; the current caption alone visible, every non-current caption at `opacity=0` (never merely dimmed) — check the LAST frame, where stale captions accumulate (AP-18) |
| glyph meaning | **legend**: every distinct shape+colour+border combination is directly labeled or legended; minimize gratuitous variety — if two kinds need no distinction, draw them the same (conv 3, glyph semantics, [USER-grounded]) |
| invariants, costs, trade-offs | **caption box** anchored to its own element/panel; never letter prose, derivations, or intuitions onto the figure body — that text belongs in the node (AP-4) |

Contract (conv 3): the figure plus its captions reads on its own, without the node prose. Entities and
edges carry their **real names** (op, struct, device). When one iteration decomposes into ≥2 named atomic
sub-phases, each sub-phase earns its own STEP tick and one-line caption — identifiable from any single
static capture. In a static storyboard, the STEP chip anchors to each panel's header. A scaffold element
(e.g. a swept playhead) still needs an inline label or legend line when confusable with another line.
**One sibling series, one naming scheme** (AP-16, [USER-grounded]): `ACT I · II · III` continues as
`ACT IV-A`, never bare `IV-A` — carried to every member, including forked/suffixed ones.

### B6 · Encoding channels — modifiers on any block

Bind real magnitudes to channels the eye reads directly (rule 9): **length/area ∝ amount · thickness ∝
rate · position ∝ ordered axis · opacity ∝ certainty/state**. Proportions legible from the drawing
itself, not only labels; pick a clear scale (linear, or log across orders of magnitude); label the key
magnitudes. Opacity as state (conv 4): bright = active/now, dim = done/past, faint = future/scaffold.

- **Identity = hue + one redundant channel** (rule 11): whatever colour encodes (data / device / type)
  must also ride shape, texture/hatch, position, or an explicit label, so the figure survives greyscale
  and colour-vision deficiency (~8% of male readers) — never hue alone, especially red/green. The
  accent's *active* state likewise also reads through a stroke, ring, or motion.
- **Extreme dynamic range** (rule 9): never a *partial* scale (some elements sized, others not). Commit
  to genuine to-scale (log if needed), or drop size-encoding for uniform order-preserving spacing plus a
  "not to scale — spans N orders" caption.
- **Honest numbers** (rule 9): "never invent" targets *fabrications* — a citable constant of the named
  real system (a GPU's published bandwidth) may size a to-scale gradient; attribute it in-figure so
  "external fact" is distinguishable from "derived here". Never back-solve an invented decomposition from
  a target total (72 = 9×8, tidy and structurally wrong) — check it against the system's real topology.
- **Fixed-size-by-design units** (rule 9) — pages, blocks, a fixed per-step budget: no inter-unit
  gradient exists; encode at **occupancy** granularity (filled slots, explicit free slots or overflow
  count) with the capacity line drawn — an unbounded bar loses "this literally doesn't fit."

### B7 · Composite panels — assembled from the blocks above

- **Iteration space** (AP-17, [USER-grounded]): for a nested-loop/tiled mechanism, **never unfold along
  the time axis** — a time-unroll of one swept path collapses the 2-D iteration space to 1-D and deletes
  the outer loop. Draw, as co-equal first-class objects on one clock: (i) the **tile grid** with exactly
  ONE block live and every other block in an explicit state (done-and-folded · not-yet-computed); (ii)
  the **nested pseudocode** with a highlighted line pointer; (iii) **both loop counters live**. The
  cursor sweeps THROUGH the grid and the outer loop advances at least once with real data — never left
  "faint/pending" forever.
- **Resource gradient** (rule 9, AP-3): draw memory/bandwidth hierarchies **to scale** — size ∝
  capacity · position ∝ proximity · link thickness ∝ bandwidth — and **mark the bottleneck**; never
  abstract boxes. **IO-bound test**: the hierarchy is the spine exactly when the figure's own on-canvas
  magnitudes are *derived from* a bandwidth/capacity number (changing it would reshape the drawing);
  when bandwidth is only a qualitative condition, it stays caption-only and the mechanism's own
  structure is the spine.
- **Curve/plot** (rule 9): regime name labels sit inside/atop their own shaded regions, never a strip
  the reader aligns by eye; an uncrossable boundary (ceiling/floor/feasibility) gets shading on the
  correct side of the curve; when a log-log slope carries meaning, pixels-per-decade match across axes
  or the mismatch is flagged as deliberate distortion.
- **State machine**: labeled nodes + labeled transition edges — transitions carry their trigger.
- **Timeline**: events per actor against an explicit time axis; synchronization points drawn.
- **Comparison pair**: two (or more) co-equal peer designs side by side; **pairing glyphs** between
  matched levels; each side's causal-implication caption anchored under its OWN panel, never a shared
  bottom block. "Static structural floorplan" vs. "worked-instance-driven animation" is an orthogonal
  choice gated by the trigger's CHANGE answer — both may coexist in one figure on one clock.
- **Before/after pair** (conv 2): stacked rows or side-by-side panels, both valid, provided the two keep
  an identical element order so one column traces across the pair.
- **Equation/shape figure** (math): type-coloured cells — scalar blue `#2F6FB5`, vector teal `#3F9B86`,
  matrix amber `#FBF0DB`/`#C79A3E`, on the light background — colouring **inputs/given** and
  whole-object classification; **individual derived cells take the operator colour** coral `#D85A30`
  (the given-vs-computed contrast). **Gold** is the one extra accent, reserved for the single most
  load-bearing *non-adjacent* readout (a value read out of an already-computed structure); competing
  readouts keep their data-identity colours. Box proportions and cell counts show the **relative
  dimension sizes** (a rank-$r$ sliver beside a $d$-sized matrix) so the ordering is *seen*.

**Palettes are genre-scoped, not global**: the same hue can mean different things per panel type — coral
is an *operator* colour in math figures but a *data-identity* colour in mechanism figures. Only the
contracts above are universal.

## §2 — Composition laws (whole figure)

1. **Layout by the compute/data DAG, not reading order** (rule 2): operands feeding the *same* operation
   share a level (co-inputs); sequence only for genuine dependency — `Z = GeLU(X·A)·B` puts `X`,`A` on
   one level (→`Y`), then `Y`,`B` (→`Z`); `X→A→Y→B→Z` is a false cascade. **Co-indexed sequences
   combined element-by-element are column-aligned** — one shared column per index, the pairing read down
   the column, never left to the reader to match across side-by-side strips. Where alignment re-orients
   a 1-D slice against its parent, B1 protects **cell-count/dimensionality, not pixel orientation**:
   re-lay along the pairing axis, keep the parent's highlighted slice visible as provenance, label the
   re-orientation.
2. **Spine = the concept's defining structure** (rule 7) — never let an enabling sub-part take it over.
   **Coordinated views fold into ONE svg** (rule 8): structure ↔ algorithm ↔ substrate on one worked
   example, one master clock — side-by-side panels allowed, separate figures not. Default to folding the
   subordinate axis into the spine's own containment; split into a second co-equal panel only when
   nesting would visually contradict an invariant the figure states elsewhere.
3. **Teach the why** (rule 6): the figure is not a mere display — carry the **one magic-step
   justification** visually (the identity, not a bare number); the broader why belongs in the node prose.
4. **The thesis gets the most ink** (rule 10): size and centre by importance to the concept; a flat,
   evenly-weighted figure hides what matters. An overlay may legitimately shrink to caption-only when
   the spine's own states already make its payoff legible; it earns more ink (still subordinate) when it
   carries a fact shape+contrast cannot state.
5. **One identity dimension + one accent** (conv 4): colour holds ONE consistent identity dimension
   (data, *or* device, *or* type) figure-wide — never switch mid-figure. Reserve ONE accent (gold/amber)
   for the single most important element per step; an accent change marks a state transition (a value
   becoming computed or shared).
6. **One step = one atomic stage** (conv 2, AP-6): if the operation has *N* phases (load · compute ·
   normalize · merge · accumulate · write), the figure walks *N* steps — never a "do-everything" step.
   Show the transformation, not just the end state: `inputs → combine (labeled box) → result`,
   arithmetic spelled out (`3 + 5 + 2 + 7 = 17`).
7. **A process animates; an invariant may stand still** (conv 5): a mechanism unfolds in motion by
   default — traverse ALL phases, never hard-code one frame. *Annotated exception:* when the genre is an
   invariant one (address/stack, layered stack, comparison, timeline-as-grid — time already spatial) and
   the SHAPE fact is fully legible in one static frame, a **static storyboard of ACT panels** is an
   equally valid default; reserve looping motion for when watching an element travel is itself the
   load-bearing fact.
8. **Legibility floor — the fit-to-screen test** (conv 3, AP-14, [USER-grounded]): with the WHOLE figure
   fitted to a laptop window (~1200–1400px), no label under **1.2% of canvas width** (≈14px @ 1200px),
   no numeric under 1%. If content doesn't fit, enlarge the element, split the figure's acts, or cut
   content — never shrink the font. Judge at that size, never a zoomed crop, with the reader's three
   questions: can I read every label? tell what each block is? follow every movement without jumps?
9. **No rest occlusion** (AP-13, [USER-grounded]): no element overlaps another element's text or body at
   any dwell state — a hard fail even if every value underneath is technically present.
10. **Mechanics** (rule 3): the node `.md` stays pure Markdown (no raw HTML/SVG); the figure is a
    companion `nodes/<id>.svg` embedded via `![alt](<id>.svg)`, on a light background `<rect>` so it
    reads in any theme. **Self-contained SMIL/CSS animation only — no JS, no external assets** —
    Markdown viewers embed via `<img>`, which runs SMIL but strips scripts. SMIL `values`/`keyTimes`
    lists are `;`-separated — a comma-separated list is silently inert. Likewise, `keyTimes` must
    start at 0 (and, for `calcMode="linear"`, end at 1) or the browser silently drops the whole
    animate — pad the timeline with duplicated first/last values to span the full clock; a frozen
    element that "should be moving" is the symptom, caught only by rendering mid-transit frames. **Author base attributes to
    equal the t=0 state**: every element hidden at t=0 gets an explicit `opacity="0"`, every moving
    packet a base transform — so the **static first frame** (the GitHub fallback, which strips SMIL) is
    complete and reads on its own. While drawing, render the frames at fit-to-screen size and fix what
    you see — every frame, never frame 0 alone.
