---
name: draw-brain-figure
description: >
  MANDATORY entry point for drawing or editing ANY figure (a node's companion
  nodes/<id>.svg) in the learning brain. Self-contained inline procedure — draw ONE
  candidate in the main loop, reviewing your renders as you draw. Invoke whenever
  creating or changing a node figure.
---

# Draw a brain figure — inline procedure

This skill is **self-contained**: it holds both *when* to draw and *how*. There is no fan-out, no
best-of-N bidding, no orchestration workflow, and no formal verification gate — you draw ONE candidate
in this loop, looking at your own renders as you go. The **rules** (what a good figure *is*) are
canonical in `brain/protocols/VISUAL_PROTOCOLS.md` — organized as §0 draw-at-all → §1 the building-block
catalog → §2 composition laws; do not duplicate them here — read that file each run.

> **Draw from understanding — but SEE the source.** Compose from your own grasp of the concept + the
> protocols. If a source artifact exists, **render it and study every frame** before drawing. Reading
> its *code*, or capturing a *single* frame of an animated/stepped source, is a lossy proxy — it loses
> the figure's thesis, composition, and motion, and is the root cause of repeated mis-draws.

> **Historical note.** This procedure was progressively simplified: first a best-of-N parallel
> `Workflow()` (N candidate drawers + independent protocol/cold-mechanism reviewer agents) was replaced
> by a zero-agent inline draw; then the formal binary self-gate was dropped as well. What remains is the
> one craft habit all of that apparatus existed to enforce: **render every frame at reading size while
> drawing, and fix what you see** — it is part of drawing, not a gate.

## Paths (per node `<id>`)

- rules: `brain/protocols/VISUAL_PROTOCOLS.md`
- node prose (the SOURCE): `brain/nodes/<id>.md`
- result figure: `brain/nodes/<id>.svg`
- persistent anchor spec: `brain/specs/<id>.spec.md`
- scratch (gitignored): `brain/.draw-cache/<id>/`
- Chrome: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

## Procedure

Run this autonomously — do not pause to ask the user to approve or continue.

### 1. Anchor spec (persistent — reuse, don't re-ground)

- If `brain/specs/<id>.spec.md` **exists**, reuse it verbatim as the source of truth for what the figure
  must teach. Do NOT re-derive it.
- If it is **missing**, author it ONCE from the node prose `brain/nodes/<id>.md` (never invent content),
  then freeze it to that path. Apply §0 of the protocol (the figure trigger + guardrail). The spec
  records: (a) components/actors with type + level; (b) the dataflow/routing or shape-evolution; (c) the
  ordered phases that become animation frames, **plus the full control structure** (every loop/level,
  not just the inner body); (d) the ONE identity colour dimension + the ONE reserved accent; (e) a
  non-degenerate worked instance carried to the visible answer; (f) what stays caption/text.

### 2. Read the rules and draw ONE candidate

- Read `brain/protocols/VISUAL_PROTOCOLS.md` in full: §0, the §1 building-block catalog (pick the block
  that renders each fact the spec requires — data atoms at true shape, containers by residence,
  connectors with ridden arrows, motion primitives on one master clock, status blocks, encoding
  channels, composite panels), and the §2 composition laws.
- Target a **self-contained SMIL/CSS-animated SVG — no JS, no external assets**. If spec (c) defines
  animation frames / a master clock, the deliverable MUST actually animate on **one master clock** with
  a complete static `t=0` fallback — a static multi-panel storyboard is a substitute ONLY when the spec
  defines no animation (§2 law 7's invariant-genre exception).
- Write the SVG to the result path (or a scratch copy first); write any generator/temp files under
  `brain/.draw-cache/<id>/` with unique names.

### 3. Render, look, fix — as part of drawing

- Render one PNG per timestep (t in {0..4}, or one per phase) with headless Chrome:
  ```
  "<CHROME>" --headless=new --disable-gpu --force-device-scale-factor=2 \
    --screenshot=<out.png> --window-size=<W>,<H> "file://<svg-or-per-step-svg>"
  ```
  NOTE: `--virtual-time-budget` does NOT advance SMIL clocks. Either materialize a temp per-step SVG per
  timestep, or use an HTML harness that inlines the SVG and calls `pauseAnimations()` +
  `setCurrentTime(t)` (launch Chrome with `--allow-file-access-from-files`).
- Downscale a copy of EVERY frame to ≤1400px wide with `uv run --with pillow python` (PIL) and look at
  THAT — the size a human actually views; never judge on a zoomed crop.
- Fix what you see and re-render until the frames read clean against the spec and the §2 laws —
  unreadable labels, unidentifiable blocks, snapping motion, occlusion, causality slips, missing phases.
  This is drawing, not a gate: no formal passes, no PASS/FAIL ritual — just don't ship what you haven't
  looked at.

### 4. Promote, embed, report

- The finished SVG is `brain/nodes/<id>.svg`. Confirm it is non-empty.
- Confirm `brain/nodes/<id>.md` embeds it via `![alt](<id>.svg)`; if the alt text is stale, update ONLY
  the alt text.
- Clean scratch (`brain/.draw-cache/<id>/` temp files); keeping the final per-timestep renders is
  optional.
- Report: spec reused vs. authored, and any rule files changed.

## Invariants

- **Persistent initial condition.** The anchor spec is fixed and reused; never re-ground it on each run.
- **Rule changes go to `protocols/VISUAL_PROTOCOLS.md`, kept universal.** If drawing exposes a missing
  rule, add it there (universal, or annotate the exact condition if genuinely case-specific — an
  unannotated narrowing is overfitting and banned). Never special-case a fix inside this skill.
- **Edit scope.** Touch only `nodes/<id>.svg`, scratch under `.draw-cache/<id>/`, the anchor spec (only
  if missing), and a rule file when a failure forces it.
- **Autonomy.** No approval prompts mid-run; report rule changes when done.

**Definition of done:** the figure is drawn, every frame was looked at at reading size,
`nodes/<id>.svg` is promoted and embedded, and any rule changes are reported.
