# Figure spec — `address-space-layout` (Step 0)

> Derived FROM `nodes/address-space-layout.md`; governed by `protocols/VISUAL_PROTOCOLS.md` and
> `protocols/EXPLAIN.md`.
> Genre: **address/stack**, carrying a **growth-dynamics overlay animated as change over
> steps** (heap edge and stack pointer advancing; a degenerate branch where the stack plunges
> into the gap and faults).

## Figure trigger (EXPLAIN.md)

Drawing is warranted. The concept's defining fact — a fixed **order of regions along one
address axis**, each with a distinct **permission**, with two regions (heap, stack) that
**grow toward each other** across a shared gap — is irreducibly spatial: no sentence
conveys "low-to-high order + which two regions move toward each other + how much slack
exists between them" as legibly as a drawn column.

- **SHAPE/structure** — the six-region column, low address at the bottom to high address
  at the top, in fixed order (null → text → data(+BSS) → heap → gap(+mmap) → stack), each
  region's permission (R/W/X) attached to its box.
- **FLOW/routing** — `malloc`/`brk` requests traveling from the running program to the
  heap edge; function-call requests traveling from the program to the stack top; each
  lands and moves the corresponding boundary.
- **CHANGE over steps** — the heap edge climbing (two `malloc` calls), the stack pointer
  descending (two function calls, then unbounded recursion), and the collision: the stack
  pointer crossing into the gap and faulting.

Caption-only facts (also listed in §(f)): exact byte/address values (WHY-1); the
null-pointer-dereference fault (a one-sentence structural fact already shown by the
null page's hatch + "always faults" tag, so no dedicated animated branch); the
security fact "no region is both writable and executable" (already visible by
scanning the R/W/X badge on every region — no region shows W+X together — so it stays
caption, per the guardrail that a contrast already visible in the drawn states does not
get its own panel); ASLR (a placement detail, not a structural change — caption only).

**Axis convention (rule 9, extreme dynamic range):** addresses span ~47 bits, far too wide
for true or even suggestive scaling. Per rule 9, no partial scale: every region band gets a
**uniform, order-preserving height** (the gap included), and one caption line states the
truth — "schematic: uniform band heights, not to scale — the address axis spans ~47 bits
(~128 TB); the gap dwarfs every named region." Band height carries NO magnitude meaning;
position/order carries all of it.

## (a) Entity inventory

| # | entity kind | in this node |
|---|---|---|
| WHO-1 | actors / participants | **Program (CPU)** — issues `malloc`/`brk`, makes function calls, dereferences pointers. **Kernel** — installs per-region page-table permissions; on a bad access, looks up the faulting address, finds no mapping, raises the fault. No nesting (single process, single thread — this node does not discuss threads). |
| WHAT-1 | data items with identity | **Heap blocks** (block 1, block 2 — each a distinct `malloc`'d chunk, never fused, own color/opacity by age). **Stack frames** (frame `main`, frame `f(depth 1)`, frame `f(depth 2)` — each a distinct call, own identity). |
| WHAT-2 | computed / derived results | n/a — the mechanism relocates region boundaries; it does not fold/combine values into a new derived result. |
| WHAT-3 | running state | **Heap-break pointer** (the `brk` edge — a single address that only increases) and **stack pointer** (the top-of-stack address — a single address that only decreases). Both drawn as a labeled marker cell showing the current hex address, updated at each step, not bare text. |
| WHAT-4 | persistent structure + its invariant | **The address space itself** — the whole six-region column, which outlives any one `malloc` or call. Invariant (quoted from the node): "the layout's job is to keep the two from silently overwriting each other" — heap and stack may each grow arbitrarily far, but must never occupy the same address. |
| WHERE-1 | substrate / resource tiers | n/a — not a multi-tier memory hierarchy (no cache/RAM/disk gradient); the entire mechanism lives inside one virtual address space, which *is* the figure's spine already (WHERE-2), not a separate resource tier. |
| WHERE-2 | layout / addressing rule | **Address → region rule**: which region a given virtual address falls in is decided purely by which fixed range it lies in (an address ruler alongside the column maps boundary addresses to region edges). This is the node's core subject and is the spine. |
| WHEN-1 | ordered phases | See §(c): (0) static load of null/text/data; (1) heap grows via two `malloc` calls; (2) shared library mapped via `mmap`; (3) stack grows via two function calls; (4) degenerate branch — unbounded recursion drives the stack pointer down through the gap until it collides with unmapped space → fault. |
| WHEN-2 | concurrency lanes | n/a — single program, single thread of execution; no second actor's independent timeline (this node does not cover multi-threaded stacks). |
| WHEN-3 | before → after snapshot | n/a — superseded by WHEN-1's multi-step phase list; several incremental transitions, not one global one. |
| HOW-1 | algorithm over the structure | Two independent monotonic loops (heap edge only rises, stack pointer only falls), each a *state-carrying* loop over "extend boundary by request size." **Order decision: sequential fold** — the node's own worked instance narrates a specific temporal story (load → malloc → malloc → mmap → call → call → runaway), and each loop step is causally dependent on the previous edge position; both loops animate ≥2 iterations with the edge/pointer visibly evolving between them. |
| HOW-2 | protocol / message alphabet | `brk(+Δ)` (extend heap), `mmap(...)` (map shared library / large allocation), implicit `call f()` (push frame), page-fault → `SIGSEGV` (kernel's response to an unmapped touch). |
| WHY-1 | quantities / complexity | The worked-instance hex addresses (`0x400000`, `0x601000`, `0x602000`, `0x7f...`, `0x7fff...`); address-space size (~128 TB on a 64-bit machine). Caption text only (§(f)). |
| WHY-2 | failure / edge / degenerate branch | **Primary, animated**: unbounded recursion → stack pointer descends past its reserved band into the gap → kernel finds no mapping → `SIGSEGV` (stack overflow) — the branch that directly exercises the figure's central SHAPE fact (heap/stack converging across the gap), drawn as an in-place animated continuation of the same mechanism (the pointer literally continues its established downward motion), not a separate contrast panel. **Secondary, caption-only**: null-pointer dereference (address 0 always faults) — already conveyed by the null page's static hatch + label. **Secondary, caption-only**: the symmetric heap-runaway case (endless `malloc` climbing through the gap from below) — same collision logic, mirrored direction. Instance-conditional check: the worked instance never walks these two siblings on canvas, so caption-only is licensed. |
| WHY-3 | trade-off comparison | n/a as a drawn panel — the security payoff of per-region permissions ("no region grants both W and X, so injected bytes can never execute") is directly readable off the R/W/X badges already on every region box; caption line only, per the guardrail. |
| ANCHOR-1 | worked numeric instance | Null `0x0`; text `0x400000` (R+X); data `0x601000` (R+W, init + BSS); heap starts `0x602000`, two `malloc`s move the edge to `0x603000` then `0x603800`; `mmap` region around `0x7f...` (R+X code, R+W data); stack starts near `0x7ffffffff000`, two calls move the pointer down by `0x40` each step, then runaway recursion drives it through the gap boundary to a fault. |
| ANCHOR-2 | composition refs | **[[virtual-memory]]** — supplies the private, contiguous address range this figure furnishes; each process's copy of this layout is private because each has its own virtual-memory map (caption note, not redrawn). **[[page-table]]** — supplies the per-region permission enforcement (R/W/X) and is *why* an out-of-range touch faults instead of silently succeeding; represented as the Kernel actor's lookup at the fault moment. |

Drawing table:

| element | type | drawn as | level / role |
|---|---|---|---|
| Program (CPU) | actor | rounded box, top-left | issues malloc/call requests (WHO-1) |
| Kernel | actor | small rounded box near fault glyph | permission check / fault raiser (WHO-1) |
| Null page | region | thin hatched band, bottom of column | address 0, unmapped (WHAT-4 member) |
| Text segment | region | colored band (blue) | R+X, code (WHAT-4 member) |
| Data segment | region | colored band (teal-green), split init/BSS | R+W, globals+statics (WHAT-4 member) |
| Heap region | region + growing fill | colored band (orange), fill grows upward in 2 steps | R+W, WHAT-3 heap-break marker rides its top edge |
| Heap block 1, 2 | data item | small labeled cells inside heap fill | WHAT-1, own color/opacity by age |
| Gap | region | hatched band, uniform height (see axis convention) | unmapped slack between heap and stack |
| mmap region | region | colored box (purple) inside gap, appears at ACT 2 | R+X code / R+W data, shared libc |
| Stack region | region + growing frames | colored band (coral), frames pushed downward in 2 steps + runaway | R+W, WHAT-3 stack-pointer marker rides its bottom edge |
| Stack frame (main, depth1, depth2) | data item | 3-compartment cell (locals / ret-addr / saved-regs) | WHAT-1, own color/opacity by age |
| Address ruler | annotation | tick marks + hex labels beside column | WHERE-2 addressing rule |
| Permission badges | annotation | R/W/X tags on each region | the security fact, caption-reinforcing |
| Fault glyph | event marker | burst icon + "SIGSEGV" label at collision point | WHY-2 primary branch |

Layout is by residence along the address axis (bottom = low address), not reading order —
position IS the ordering relation for the address/stack genre.

## (b) Dynamics — routing / shape-evolution

- A `malloc(Δ)` request is drawn as a small gold-accented packet traveling from the
  Program box down to the current heap edge along a persistent drawn line; on arrival, the
  edge marker moves up by Δ and a new heap-block cell appears at the vacated space, taking
  the heap's orange hue at full opacity (bright/now); the previous block dims (opacity
  1 → 0.5, done/past).
- An `mmap(...)` request travels the same way from Program to the middle of the gap; on
  arrival the mmap box fades in (opacity 0 → 1) — a one-time event, no further evolution.
- A `call f()` request travels from Program down to the current stack top; on arrival the
  pointer marker moves down by Δ and a new frame cell appears, full opacity; the previous
  frame dims to 0.5.
- The runaway branch compresses many identical iterations into a "⋮ more recursive calls
  ⋮" tick, then a single fast plunge of the pointer marker down through the stack band's
  lower boundary into the gap's hatch; on contact, the Kernel box appears, a gold-to-red
  flash rings the crossing point, and the "SIGSEGV — stack overflow" label appears and
  holds (longest dwell in the sequence — the costliest, most important moment).
- Every transfer rides a persistent drawn line from source to landing point (no fades in
  place); the heap edge and stack pointer are the only elements that reposition, and they
  do so in discrete jumps timed to each step, never a continuous glide.

## (c) Ordered phases → animation frames, with control structure

Control structure: two independent monotonic loops (heap-edge-only-rises,
stack-pointer-only-falls), each a state-carrying accumulator over "current edge address."
Both loops show ≥2 iterations with the state visibly evolving between them, per the
sequential-fold order decision in HOW-1. One master clock, `repeatCount="indefinite"`,
shared keyTimes across every animate element.

- **ACT 0 — static load.** Kernel maps null (unmapped), text (R+X), data (R+W, init+BSS)
  at the bottom of the column. Heap/gap/stack bands shown as empty reserved outlines.
  Base/first-frame state — everything else below starts at opacity 0 here.
- **ACT 1 — heap growth loop, iteration 1 then 2.**
  - F1: `malloc` packet travels Program → heap edge; edge moves `0x602000 → 0x603000`;
    block 1 appears, bright.
  - F2: second `malloc` packet, same path; edge moves `0x603000 → 0x603800`; block 2
    appears, bright; block 1 dims to done.
- **ACT 2 — one-time mmap event.** `mmap` packet travels Program → gap middle; mmap box
  fades in, labeled "shared libc — R+X code / R+W data."
- **ACT 3 — stack growth loop, iteration 1 then 2.**
  - F1: `call f()` packet travels Program → stack top; pointer moves down `0x40`; frame
    `depth 1` appears, bright (locals / ret-addr / saved-regs compartments shown).
  - F2: second `call f()` (recursive); pointer moves down another `0x40`; frame `depth 2`
    appears, bright; frame `depth 1` dims; frame `main` already dim (oldest).
- **ACT 4 — degenerate branch (WHY-2), the collision.**
  - F1: "⋮ more recursive calls, no base case ⋮" tick appears; pointer marker begins its
    fast plunge.
  - F2: pointer crosses the stack band's lower boundary into the gap's hatch; Kernel box
    appears; gold→red fault ring flashes at the crossing point; "SIGSEGV — stack overflow"
    label appears. Longest dwell — the costliest step.
- **Reset + hold:** ACT 1–4 additions fade back to their t=0 (absent) state, brief hold at
  the clean base state, then repeat.

The figure loops indefinitely rather than freezing on the crash, per the protocols'
per-branch loop rule: the crash is one *possible* outcome of unbounded recursion, not the
mechanism's necessary terminus — the spine loops while the fault branch reads as terminal
within each cycle (its state never reverse-animates inside the cycle; the next cycle
restarts the whole instance).

## (d) Color — ONE identity dimension + ONE accent

- **Identity dimension = region type.** Each of the six regions (and its contents) holds
  one stable hue for the whole figure: null = gray `#B0B0B0` (hatched, "absence"), text =
  blue `#2F6FB5`, data = teal-green `#3F9B86`, heap (+blocks) = orange `#D8722E`, mmap =
  purple `#7B5EA7`, stack (+frames) = coral `#D85A30`.
- Idle/neutral (reserved-but-unfilled band outlines, the gap's hatch, the ruler): `#FBF0DB`
  fill, `#C79A3E` stroke (house amber), per protocol default.
- Opacity = state: bright/full = active/now (the block or frame just added), dim (~0.5) =
  done/past (an earlier block/frame), and the reserved-band outlines before their region
  is populated read as faint/future.
- **ACCENT (one only) = gold `#E8A02E`** — used for exactly one thing per step: the
  currently-moving edge/pointer marker and the traveling request packet. At the collision
  (ACT 4 F2) the accent transitions gold → red `#C0392B` to mark the fault — the one state
  transition that changes the accent's own color, exactly as the rule permits ("a change
  to the accent marks a state transition").

## (e) Worked instance carried to the visible answer

Every number shown is drawn from the node's own worked-instance table, and each is derived
from the one before it on-canvas:

- Heap: edge starts at `0x602000` (label on-canvas from ACT 0) → `+ 0x1000` (labeled on the
  traveling `malloc` packet) → `0x603000` (new edge label, ACT 1 F1) → `+ 0x800` → `0x603800`
  (ACT 1 F2). The visible result: two heap blocks sized proportionally to their request
  (block 1 wider than block 2, `0x1000` vs `0x800`), stacked at the heap's floor.
- Stack: pointer starts at `0x7ffffffff000` (frame `main`, ACT 0) → `- 0x40` → new pointer
  address (ACT 3 F1, frame `depth 1`) → `- 0x40` → next address (ACT 3 F2, frame `depth 2`)
  → unbounded further `- 0x40` steps (compressed as the "⋮" tick, ACT 4 F1) → pointer
  value crosses the stack band's low boundary, landing inside the gap (ACT 4 F2) — the
  visible answer is the fault, not a numeric address (the whole point is that the next
  address is unmapped, so there is nothing meaningful to compute further).

Note: within-region proportions (block 1 vs block 2 widths) ARE drawn to scale — the
extreme-range convention applies only to the inter-region axis, where scale is disclaimed
by the axis caption.

## (f) Stays as caption / text (not lettered onto the spine)

- The axis convention line: "schematic: uniform band heights, not to scale — the address
  axis spans ~47 bits (~128 TB); the gap dwarfs every named region."
- WHY-1 quantities: "128 TB max address-space size on a 64-bit machine"; the full worked
  hex-address table (also reproduced as ruler labels — a redundant plain-text confirmation).
- The invariant, quoted: "the layout's job is to keep the two from silently overwriting
  each other."
- Security line: "code is R+X, never W; data/heap/stack are R+W, never X — no region
  grants both, so injected bytes can never be executed" (readable directly off the R/W/X
  badges; stated once in prose per the guardrail).
- Caption-only edge cases: "a null pointer (value 0) always faults immediately — the null
  page is deliberately left unmapped"; "the symmetric failure is a heap that never frees,
  climbing through the gap from below — same collision, opposite direction."
- ASLR note: "the kernel randomizes each region's exact starting address every run; the
  *order* and *permissions* drawn here never change — only where they start."
- `STEP n/m` indicator (5 steps: ACT 0–4) and one-line caption per ACT — whole-figure
  header content.
- Legend: color = region type; opacity = active (bright) vs. past (dim) vs. reserved
  (faint outline); gold = the moving edge/request; gold→red = fault; the playhead/sweep
  scaffold (if any) labeled explicitly.
