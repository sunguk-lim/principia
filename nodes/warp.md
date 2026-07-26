---
id: warp
title: Warp
summary: "A warp is a fixed group of 32 threads that a streaming-multiprocessor runs in lockstep: each cycle the SM's scheduler issues one instruction, and all 32 threads execute that same…"
type: concept
tags: [gpu]
prereqs: [streaming-multiprocessor]
sources:
  - "linux-internals-complete.html — Phase 7: Where SIMT lives — the rules at each level; Different threads in a warp doing different jobs — expensive; The optimization rule — branch on warp boundaries, not thread boundaries; Warps — fixed at 32 on NVIDIA"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Warp

## Summary

A **warp** is a fixed group of **32 threads** that a [[streaming-multiprocessor]] runs in
**lockstep**: each cycle the SM's scheduler issues **one** instruction, and all 32 threads
execute that same instruction on the same cycle, each on its own data. The 32 positions a
warp occupies are called its **lanes**. The crucial fact is that the warp — not the
individual thread — is the SM's *actual unit of scheduling*: when the prerequisite
[[streaming-multiprocessor]] node said the scheduler picks "a group whose next instruction
is ready" and switches between resident groups for free to hide memory latency, *that group
is a warp*. So the SM's whole latency-hiding trick runs at warp granularity. This buys
efficiency — 32 threads advance on the strength of a single instruction fetch and decode —
but it comes with one sharp cost called **divergence**: if the 32 threads in a warp want to
take *different* branches of an `if/else`, the warp cannot run both at once. It runs the
first path with the threads that did not choose it switched **off** (idle), then runs the
second path with the masks flipped — two serial passes, with lanes wasted in each. Hence the
optimization rule that governs fast GPU code: arrange branches so that **whole warps go the
same way**, never so a branch splits threads *inside* a single warp.

## Grounded explanation

### Where this sits: the warp is the SM's real scheduling unit

The prerequisite [[streaming-multiprocessor]] node deliberately left one thing unnamed. It
described how the SM hides memory latency: it keeps far more **threads** resident (loaded
and ready) than it has **lanes** (arithmetic positions, each doing one add or multiply per
cycle) to run them, and each cycle its scheduler "scans the resident threads for a *group*
whose next instruction is ready," issues that group, and — if the group stalls on a slow
memory load — switches to a *different* ready group for free (because every resident
thread's working values already sit in their own permanent slice of the register file, so
nothing is saved or restored). That node ended by flagging that "the fixed-size groups the
scheduler issues, and the rule that those grouped threads all run the same instruction in
lockstep," were a separate topic. **This node is that topic.** That fixed-size group is the
warp.

So the warp is not a software convenience; it is the unit at which the SM's hardware
actually operates. The scheduler does not point at one thread per cycle — it points at one
*warp* per cycle. A thread, in the [[streaming-multiprocessor]] sense, is one independent
stream of work with its own values; a warp staples 32 of those threads together and marches
them as one. Two terms to fix before going on, each defined now so nothing is used before it
is introduced:

- **Lockstep** means the grouped threads do not move independently: on any given cycle they
  are all executing the *very same* instruction, at the very same point in the program. They
  cannot be at different instructions at the same moment. (This is the constraint the
  hardware is built around; the industry name for "many threads, one shared instruction
  stream, each on its own data" is *SIMT*, but the name is not needed to understand it.)
- A **lane** is one of the 32 thread-positions inside a warp — the same arithmetic position
  from [[streaming-multiprocessor]], now viewed as "slot *k* of this warp," for *k* from 0
  to 31. When we say a lane is **masked off**, we mean the hardware feeds it the instruction
  but tells it to discard the result and change nothing — the lane is present but idle for
  that cycle.

Why exactly 32? It is simply a hardware constant. On every NVIDIA GPU since 2006 the warp
size is fixed at 32 — you do not choose it; the SM forms warps automatically by chopping its
resident threads into groups of 32. (Programmers declare how many threads they want in a
bundle the SM calls a *block*; the SM then slices each block into warps of 32. Blocks are a
separate topic; here it is enough that warps are 32 wide and the programmer does not pick
that number.)

### The why: one instruction drives 32 threads — the upside and the catch

The reason the warp exists is amortization. Fetching an instruction from memory, decoding it
into control signals, and steering the scheduler all cost real work. If the SM did that once
per thread, the overhead would swamp the cheap arithmetic. By doing it **once per 32 threads**
— one fetch, one decode, one scheduling decision, then 32 lanes all firing the same operation
on their own data — the SM spreads that fixed overhead across 32 useful results. This is the
throughput bet from the [[streaming-multiprocessor]] node made concrete at the instruction
level: spend transistors on *width* (32 lanes sharing one control path), not on per-thread
control machinery.

But the bet has a sharp edge, and it is the central thing this node must teach. The 32 lanes
share **one** instruction per cycle. That is fine as long as all 32 threads *want* the same
instruction. The moment the program reaches a branch — an `if/else` — where some of the 32
threads would go one way and the rest the other, the warp is stuck: it has one instruction
slot and two different next-instructions demanded of it. It physically cannot issue both in
the same cycle.

The hardware's resolution is the one non-obvious step, so here is the full mechanism, which
is called **divergence**. The warp does *not* split into two independently-running halves
(it has no machinery to be at two instructions at once). Instead it serializes the two paths
and uses **masking** to fake the split:

1. It runs the first path's instructions with the lanes whose threads chose that path turned
   **on**, and every other lane **masked off** — present, fed the instruction, but discarding
   its result so it changes nothing.
2. Then it runs the second path's instructions with the **masks flipped** — the lanes that
   were idle now active, and the ones that already finished their path now masked off.

The justifying invariant — the identity that makes this legal — is that *the 32 threads
always retire instructions together as one warp.* The hardware never lets them drift apart;
it preserves lockstep by the trick of letting some of the "lockstepped" instructions be
*no-ops* for the masked lanes. So SIMT is, precisely, "lockstep, but with per-lane masks."
The cost is direct: during the first path the masked lanes did nothing useful, and during the
second path the other lanes did nothing useful. The warp paid for *both* paths in series
even though each thread only needed *one* of them. A branch that perfectly splits a warp in
half therefore takes about **twice** as long as a non-divergent warp, and the worst case — all
32 threads wanting different things — runs the body up to **32 times**, one lane active at a
time.

### The consequence: branch on warp boundaries, not inside a warp

This is where the rule that governs fast GPU code comes from, and it follows directly from
the mechanism above. Divergence is only a cost *within* a single warp — it only fires when the
32 threads of *one* warp disagree. If two *different* warps take different paths, there is no
cost at all: the SM was already running them as separate scheduling units, picking one ready
warp per cycle regardless of which path each is on. Warp A can be issuing a load this cycle
while warp B issues an add the next; the scheduler does not care that they are running
different code, because each warp is internally in agreement.

So the rule is: **structure branches so the condition is the same for all 32 threads in a
warp.** A branch whose answer is constant across a warp — for instance, branching on *which
warp this is* — is essentially free, because every lane in the warp takes the same side and
no masking is needed; the warp goes one way as a single unit. A branch whose answer varies
*within* a warp — for instance, on a per-thread index or on per-thread data — risks
divergence and the serialization penalty. Expert kernels often look like they are contorting
their logic; they are not avoiding branches in general, they are avoiding *intra-warp*
branches, pushing every split onto a warp boundary so whole warps, never half-warps, diverge.

### Worked instance: 32 threads adding, then the same 32 forced to disagree

Take one warp — 32 threads, lanes 0 through 31 — and run two cases on it. The first is the
*aligned* case; the second deliberately triggers divergence so the masking mechanism is
visible rather than hidden.

**Case 1 — no divergence (full efficiency).** Every thread does the identical job: lane *k*
loads element *k* of two arrays and adds them, `c[k] = a[k] + b[k]`. All 32 threads want the
exact same instruction — an add — at the exact same moment. The scheduler issues that one
add; all 32 lanes fire on their own *k*; 32 results are produced. One instruction, 32 useful
results, **zero lanes masked off**. This is the warp operating at its design point: the
fixed cost of one fetch/decode amortized perfectly across 32 lanes. (This is exactly the
element-wise `c = a + b` workload the [[streaming-multiprocessor]] node ran across the whole
chip; now we see what happens inside *one* of its warps.)

**Case 2 — divergence inside the warp (≈2× slower).** Now the same 32 threads hit a branch
that splits them by lane:

> `if (lane < 16) doA();  else  doB();`

Lanes 0–15 want `doA()`; lanes 16–31 want `doB()`. The warp has one instruction slot, so it
cannot run both. It serializes:

- **First pass:** issue `doA()`'s instructions with lanes 0–15 **on** and lanes 16–31
  **masked off**. The 16 high lanes are powered, clocked, and fed the instruction — but
  discard their results. They are idle. Half the warp's width is wasted this pass.
- **Second pass:** flip the masks. Issue `doB()`'s instructions with lanes 16–31 **on** and
  lanes 0–15 **masked off**. Now the 16 low lanes are idle.

Add it up: the warp executed `doA()` *and* `doB()` back-to-back, each pass leaving ~16 of its
32 lanes idle. Where Case 1 finished its work in one pass at full width, this branch took two
passes at half width — about **2× the time** for the branched region, with roughly half the
lanes wasted in each pass. The penalty is real and it came purely from the 32 threads
disagreeing.

**The fix, by the rule.** Suppose instead the split falls on a *warp* boundary — warp 0's 32
threads all take `doA()`, warp 1's 32 threads all take `doB()`. Now *within* warp 0 all 32
threads agree (all want `doA()`), so it runs one pass at full width with no masking; likewise
warp 1 runs `doB()` at full width. The two warps run different code, but the SM was already
scheduling them as independent units, so there is **no divergence and no penalty**. Same total
work, same `doA()`/`doB()` split — but by aligning the branch to the 32-thread boundary
instead of cutting through the middle of a warp, the 2× cost vanishes. That is the entire
content of "branch on warp boundaries, not thread boundaries."

## Prerequisites

- [[streaming-multiprocessor]]

## Sources

- linux-internals-complete.html — *Where SIMT lives — the rules at each level* (a warp of 32
  threads is the SIMT/lockstep unit; the SM hosts many warps, each at a different point, and
  the scheduler picks one ready warp per cycle); *Different threads in a warp doing different
  jobs — expensive* (warp divergence; serialization with per-lane masking; ~2× for a half/half
  split, up to 32× worst case; "lockstep but with masks"); *The optimization rule — branch on
  warp boundaries, not thread boundaries*; and *Warps — fixed at 32 on NVIDIA* (warp size is a
  hardware constant of 32, formed automatically by chopping a block's threads into groups of 32).
