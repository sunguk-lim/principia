# Figure spec — `page-cache` (Step 0)

> Derived FROM `nodes/page-cache.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and `protocols/EXPLAIN.md`.

**Genre:** dataflow (mechanism) — a memory-hierarchy **substrate** (RAM page-cache tier vs. disk
tier) folded into the spine's own containment (not a separate panel; see rule 8 default-fold and
the WHERE-1 discussion below). A **comparison** sub-genre appears only for the ACT IV fork
(writeback vs. crash), as a subordinate contrast panel branching off the shared spine state.

Tie-break rationale: the defining shape of "page cache" is *not* a to-scale resource hierarchy —
there is no fixed capacity to size against ("whatever RAM is otherwise free"), so rule 9's
IO-bound test fails (changing the 5 ms/5 µs numbers would not reshape the spine, only its pacing).
The defining shape is the **dataflow + branch structure**: program ⇄ VFS ⇄ page cache ⇄ disk, with
the hit/miss and dirty/clean state machine riding on top. That dataflow owns the spine; the
memory-tier axis is folded into it as containment (cache pages drawn *inside* the RAM tier lane,
disk blocks *inside* the disk tier lane) rather than a second competing panel.

## Figure trigger (EXPLAIN.md)

Drawing is warranted: the hit/miss/dirty state machine and its two branches are irreducibly
visual (a reader must see *which path bytes take* and *where they physically sit*, not just read
a sentence about it).

- **SHAPE/structure** — three residency tiers (process buffer / page-cache RAM / disk) and which
  one currently holds the authoritative copy of a given page.
- **FLOW/routing** — the read path (program → VFS → cache → [disk] → cache → buffer) and the
  write path (program → VFS → cache page, marked dirty) and the two divergent futures of a dirty
  page (→ disk via writeback, or → lost on crash).
- **CHANGE over steps** — cache residency evolving from empty → populated (miss) → reused (hit) →
  mutated (dirty) → resolved (clean) or destroyed (lost). This is the loop-bearing state the
  mechanism carries; it is the reason a figure earns its keep here.

Caption-only facts (guardrail): the ~1000× RAM/disk latency ratio and the concrete 5 ms / 5 µs
numbers (WHY-1); "the cache uses whatever RAM is free and is reclaimed on demand" (stated once,
not drawn — no eviction occurs in the worked instance, see WHEN-1); the `fsync`/`O_DIRECT`
mentions (source itself calls these "plain prose, not a prerequisite node" — one caption line
each, no dedicated frame, since `fsync` is fully conveyed as "branch A, but immediate" and adds no
new drawn state).

## (a) Entity inventory

**Genre defaults applied:** this is *not* single-agent — the background writeback thread has
independent timing from the calling program, so WHO-1 is populated rather than defaulted n/a.
WHY-3 is populated as caption-only (see below), not a drawn panel, because the drawn ACT III (gain:
instant return) + ACT IV-B (cost: data loss) already make the trade-off's two sides visible without
a dedicated panel — per the guardrail's "contrast is caption-only when the figure's own drawn
states already show it."

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors | **Program** (the calling process — issues `read`/`write`/`fsync` syscalls); **Writeback thread** (background kernel actor, independent timing, wakes periodically — appears only in ACT IV branch A) |
| WHAT-1 | data items with identity | The file's 256 pages of `report.dat`; **page 0** is the single traced identity (present in every ACT); pages 1–255 stay neutral/untracked (drawn as a strip, not individually followed) |
| WHAT-2 | computed/derived results | n/a — the page cache is a passive transport/storage tier (protocol rule 2: caches move bytes **unchanged**); no transformation of file data occurs anywhere in this mechanism |
| WHAT-3 | running state | n/a — no accumulator. The miss-fill of 256 pages is a single atomic bulk transfer (source asserts no per-page order → "many co-inputs travel together", not a manufactured stepwise loop); the hit/miss pairing itself is **producer/consumer via persistent shared state** (ACT I populates the cache, ACT II later reads it) — this is HOW-1's explicit 4th shape, which is *why* WHAT-3 is n/a rather than a fold |
| WHAT-4 | persistent structure + invariant | **The page cache** (the region of cache-page cells). Invariant, spliced verbatim from source: "a region of RAM, organised in 4 KB pages exactly like the rest of memory, in which the kernel keeps copies of file data it has recently moved between disk and a program" — plus the dirty-bit sub-invariant "dirty [meaning] modified in RAM but not yet written back to disk." Cross-referenced with WHAT-3 per the template's own rule (running state IS the persistent structure here: cache residency is exactly the state ACT I writes and ACT II reads) |
| WHERE-1 | substrate/resource tiers | Three tiers, containment = residence: **process buffer** (user space RAM) / **page cache** (kernel RAM) / **disk** (block device). Not drawn to scale (rule 9 test fails — no capacity number; see genre note above); tiers are fixed-position lanes, and the *disk* lane's activity (touched vs. idle) is the bottleneck signal, marked by whether the transfer arrow into it is drawn live or dimmed |
| WHERE-2 | layout/addressing rule | file offset → page index (`offset ÷ 4096`) → cache slot **if resident**, else → disk block address (via the inode's own block map — a prerequisite-node detail, not re-derived here, one caption line) — directly the template's own "page→frame" example |
| WHEN-1 | ordered phases | See §(c) below. `freed` column: n/a throughout — this instance only ever grows the cache (fills, dirties, flushes); no eviction is exercised, so per the template's own omit-rather-than-invent instruction, no freed step is drawn. (Reclaim-on-demand is stated once in the WHAT-4 caption, not drawn.) |
| WHEN-2 | concurrency lanes | Two lanes only where they overlap in time: **Program lane** and **Writeback-thread lane**, both only in ACT IV branch A (the thread's wake-and-flush runs asynchronously to the program, which has already returned from `write` in ACT III) |
| WHEN-3 | before→after snapshot | ACT III→IV: page 0 at "dirty, disk stale" is the single shared **before** state that the ACT IV comparison panel forks from, into two **after** states (A: clean/flushed, B: lost) |
| HOW-1 | algorithm + control structure | Two control shapes present, both licensed by the template's HOW-1 options: (1) **producer/consumer via persistent shared state** for the miss→hit pair (ACT I populates the cache; ACT II — a later, unrelated call — reads it: order is real, nothing folds, nothing runs concurrently); (2) a **branch** (not a loop) at the dirty-page fork: ACT IV splits into two mutually exclusive futures from one shared state |
| HOW-2 | protocol/message alphabet | `read`, `write`, `fsync` (named syscalls — the alphabet of program→VFS requests); no wire protocol beyond these |
| WHY-1 | quantities | Disk ≈ 5 ms/block, RAM ≈ 5 µs/copy (≈1000× gap); 1 MB file = 256 pages @ 4 KB. Caption text only (rule 9 test: these numbers drive pacing/dwell, not on-canvas size — see genre note) |
| WHY-2 | failure/edge branch | **Crash before writeback**: the dirty page 0 exists only in volatile RAM; power loss destroys it; disk keeps stale bytes forever. Drawn (not omitted) because the worked instance's own Step 4 explicitly walks through this exact case — the omission clause only licenses skipping a same-logic sibling the instance never reaches, which does not apply here |
| WHY-3 | trade-off comparison | Deferred-write gain (fast return + batching, ACT III) vs. cost (crash data-loss window, ACT IV-B) — genuine two-sided tension as the "how long before flush / whether fsync is called" knob moves. Caption-only: both sides are already visible in the drawn ACTs (guardrail), so no separate panel earns its ink |
| ANCHOR-1 | worked numeric instance | `report.dat`, 1,048,576 B = 256 pages × 4,096 B; disk ≈5 ms/block, RAM ≈5 µs/copy; write of 512 B at offset 0 (→ page 0). Exercises miss (ACT I), hit (ACT II), dirty write (ACT III), and both ACT IV futures — every branch is hit by this single instance, no invented numbers needed |
| ANCHOR-2 | composition refs | **page** — defines the 4 KB cell unit every cache/disk cell is drawn at; **vfs** — the routing waypoint between Program and the cache lookup; **inode** — resolved once at `open()` to hand back fd=3 (caption-only, not re-expanded); **system-call** — the `read`/`write`/`fsync` entry arrows from Program |

### Drawing table

| element | type | drawn as | level/role |
|---|---|---|---|
| Program | WHO-1 | rounded box, top lane, user-space region | issues syscalls; holds the process buffer |
| Process buffer | WHERE-1 | small cell strip inside the Program's user-space region | destination of read copies / source of write bytes |
| VFS routing waypoint | HOW-1 locus | small labeled pill on the request arrow ("VFS → ext4"), not a residency box | execution locus only, no WHERE-1 semantics (per WHERE-1's own bracket clarification) |
| Page cache (region) | WHAT-4/WHAT-3 (cross-ref) | a bounded lane containing the 256-cell strip, kernel-RAM tier | persistent structure; residency state carried across ACTs |
| Page cells (0..255) | WHAT-1 | small cells in a strip, page 0 outlined/labeled distinctly, "…" elision for 2..254, cell 255 shown explicitly (true-shape strip, not one solid block) | traced identity = page 0; rest stay house-neutral |
| Disk (region) | WHERE-1 | bounded lane below the cache lane, mirrored 256-cell strip, column-aligned with the cache strip (page *i* under cache page *i*) so divergence (dirty vs. stale) is directly legible | passive tier; transfer arrow to/from it only drawn live during miss/writeback, dimmed during hit |
| Writeback thread | WHO-1 | small rounded box docked beside the cache lane, faint/idle until ACT IV-A wakes it | independent timing actor |
| Dirty-bit flag | WHAT-3/4 element | small tag on page 0's cell, "clean"/"dirty"/"lost" states, accent-ring at the instant it flips | control/bookkeeping scalar — stays house-neutral except the transient accent pulse per rule (d) |
| Fault/crash marker | WHY-2 | small icon on the ACT IV-B sub-lane's timeline, before the writeback dwell would complete | one-shot terminal event marker |

Layout is by the compute/data DAG / residency (containment = residence): Program (top) → VFS
waypoint → Page cache (middle) → Disk (bottom), not left-to-right reading order; time is expressed
by discrete animated steps within that fixed spatial layout, plus a bottom two-column split for
ACT IV.

## (b) Dynamics

Every transfer rides a persistent drawn track between two fixed lane positions:
- Disk → cache (ACT I, miss fill): travels the disk↔cache track, dwells longest (the costly step).
- Cache → buffer (ACT I F5 and ACT II F9): travels the cache↔buffer track; ACT II's dwell is short
  (RAM speed) and the disk↔cache track stays dim/untouched the whole ACT — the drawn contrast
  between "track lit" (ACT I) and "track dark" (ACT II) *is* the hit/miss payoff, requiring no
  extra badge.
- Buffer → cache page 0 (ACT III write): travels buffer↔cache track; the dirty flag flips at
  arrival (accent pulse), `write` returns before any cache→disk track lights up.
- Cache → disk (ACT IV-A only): the same disk↔cache track as ACT I, now traveled in the opposite
  direction, carrying page 0's new bytes; disk cell 0 updates to match, dirty flag → clean.
- (ACT IV-B): no track is traveled — the crash marker fires *on* the dirty cache cell itself
  (opacity fades toward 0, labeled "LOST"), and the disk↔cache track is explicitly never lit,
  making "never reached disk" the visible fact rather than an inferred one.

No value is transformed in transit (protocol rule 2): every packet on every track carries page
bytes unchanged; the only per-step "compute" is the dirty-bit flip, which happens in place on the
cache cell, not on a link.

## (c) Ordered phases → animation frames

Control structure: ACT I/II are a **producer/consumer pair sharing the persistent cache
structure** (not a loop — 2 iterations of "the same read call," state carried between them, which
satisfies the ≥2-iteration state-carrying requirement without inventing an artificial loop). ACT
III is a single write. ACT IV is a **branch** — two mutually exclusive continuations of the same
prior state, shown as a two-column comparison sub-panel (WHY-2).

- **ACT I — first read, cache miss** (F1–F6)
  - F1: Program → `read(fd=3, buf, 1MB)` (arrow: Program → VFS waypoint)
  - F2: VFS waypoint → cache lookup; pages 0–255 all **absent** (cells shown empty/dashed)
  - F3: kernel allocates 256 empty cache-page slots (cells switch from "n/a" to "empty, pending")
  - F4: disk → cache transfer (longest dwell; disk cells 0–255 shown holding original bytes,
    copied unchanged into the now-filled cache cells)
  - F5: cache → buffer copy (fast dwell); all 256 cache cells settle to "resident, clean"
  - F6: `read` returns 1 MB to Program
- **ACT II — second read, cache hit** (F7–F10) — cache state carried over from ACT I unchanged
  - F7: Program → `read(fd=3, buf2, 1MB)` (same file/offset)
  - F8: VFS waypoint → cache lookup; pages 0–255 all **present** (cells already "resident, clean"
    from ACT I — reused slot, not re-created, per the reused-slot rule)
  - F9: cache → buffer copy only; disk↔cache track stays dark the whole ACT (no F4-equivalent)
  - F10: `read` returns 1 MB, fast
- **ACT III — write, page 0 goes dirty** (F11–F14)
  - F11: Program → `write(fd=3, newbytes[512], offset=0)`
  - F12: VFS waypoint → locate page 0 (already resident from ACT I/II)
  - F13: buffer → cache page 0: 512 bytes copied in; dirty flag flips (accent pulse); disk cell 0
    explicitly still shows the **old** bytes (visible divergence)
  - F14: `write` returns immediately — Program lane goes idle; this is the shared **before** state
    the ACT IV fork branches from
- **ACT IV — the fork** (F15A / F15B, side-by-side comparison sub-panel, shared master clock)
  - **F15A (writeback, normal case):** after a dwell representing "a few seconds," Writeback
    thread wakes, reads dirty cache page 0, travels the cache→disk track, disk cell 0 updates to
    the new bytes, dirty flag → clean. Cache and disk now agree.
  - **F15B (crash, degenerate case):** a fault marker fires *before* the writeback dwell
    completes; dirty cache page 0 fades to 0 opacity, labeled "LOST"; disk cell 0 is left at its
    **old** bytes, permanently (this sub-lane freezes rather than looping — a one-shot terminal
    event, per protocol's own named exception).

`STEP n/m` header + one-line caption per frame (per (f)); ACT IV emits two `STEP` chips, one per
sub-panel header, since it's the static-storyboard-within-an-animation case.

## (d) Color

- **Identity dimension = data** (per-item identity): page 0 (the traced page) keeps one stable hue
  across every tier it visits (buffer/cache/disk); pages 1–255 stay house-neutral. Chosen over
  *device* because the *same bytes* cross tier boundaries — a device-keyed palette would repaint
  page 0 at every tier crossing and break traceability (rule 5).
  Page 0 hue: **teal `#3F9B86`**.
- Idle/neutral (untracked pages, empty cache cells, idle actors): `#FBF0DB` fill / `#C79A3E`
  stroke (house amber).
- Dirty-bit flag and the residency counter are control/bookkeeping scalars: house-neutral at rest,
  touched only by a transient gold accent ring at the instant they flip (never a permanent hue).
- Opacity = state: bright = active/now; dim = done/past (e.g., ACT I's cache fill once ACT II
  starts); faint = future (ACT IV-B's fault marker before it fires — explicit `opacity="0"` base,
  not merely absent from markup).
- **ACCENT (one only) = gold `#E8A02E`**: the dirty-flag flip (ACT III), the writeback completion
  flip (ACT IV-A), and the crash-fade trigger instant (ACT IV-B) — each is the single key event of
  its step.

## (e) Worked instance carried to the visible answer

`report.dat`, 1,048,576 B = 256 × 4,096 B pages. Disk ≈5 ms/block, RAM ≈5 µs/copy. ACT I fills all
256 cache cells from disk (miss); ACT II re-reads the same 256 cells from cache only (hit); ACT III
dirties page 0 with a 512 B write at offset 0; ACT IV forks page 0's fate into "flushed to disk"
(A) or "lost to a crash" (B). Every number shown (256, 4096, 512, offset 0) is either given by the
source or derived from it on-canvas; no placeholders.

## (f) Stays as caption / text

- Latency facts: "disk ≈5 ms/block vs. RAM ≈5 µs/copy — ≈1000×" (WHY-1)
- "1 MB = 256 × 4 KB pages" (WHY-1, inline near the page-cell strip's count label)
- WHAT-4 invariant, quoted verbatim (see table above), as the page-cache lane's header subtitle
- WHERE-2 addressing rule, one line, inline near the cache lane
- "The cache uses whatever RAM is free; reclaimed on demand — not exercised in this run" (WHAT-4,
  one caption line, no drawn eviction)
- `fsync`/`O_DIRECT` mention, one caption line each, anchored to ACT IV-A's header ("fsync forces
  this flush immediately, blocking until done")
- WHY-3 trade-off summary line, anchored to the ACT III/IV boundary: "instant return + batching
  (ACT III) vs. a crash-durability window (ACT IV-B)"
- Legend: page-0 teal = traced identity; amber = idle/untracked; gold = key event this step
- `STEP n/m` + one-line per-frame caption, whole-figure header (per-panel header in ACT IV)
