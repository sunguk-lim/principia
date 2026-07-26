---
id: occupancy
title: Occupancy
summary: Occupancy is the ratio of warps actually resident on a streaming-multiprocessor (loaded and ready, in that node's sense) to the maximum number that SM is built to hold.
type: concept
tags: [gpu]
prereqs: [streaming-multiprocessor, warp, shared-memory]
sources:
  - "linux-internals-complete.html — Phase 7: Occupancy — how many blocks fit on an SM (the MIN-across-fixed-resources rule; H100 caps of 64 warps / 2048 threads / 65,536 registers / 228 KB shared memory per SM); Why the design works — the synthesis (over-subscription hides latency); Register pressure — connecting back to occupancy (registers-per-thread as the dominant occupancy limiter; spilling)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Occupancy

## Summary

**Occupancy** is the ratio of [[warp]]s actually **resident** on a
[[streaming-multiprocessor]] (loaded and ready, in that node's sense) to the maximum
number that SM is built to hold. An SM has *fixed* resources — a register file (fast
on-chip storage holding every resident thread's working values), a block of on-chip
scratchpad memory, and a hard cap on how many resident warp slots it has at all. Each
piece of resident work consumes some of each resource, so **whichever resource runs out
first** sets how many warps fit, and occupancy is that number divided by the cap. It
matters because of the [[streaming-multiprocessor]]'s one trick: it hides slow-memory
stalls by switching for free to a *different* ready [[warp]] whenever the current one
stalls. The more resident warps, the more likely *some* warp is ready while others wait,
so the lanes stay busy. Low occupancy means few warps, so when they all stall at once the
SM has nothing to run and its lanes go idle — wasted throughput. The dominant cause of low
occupancy is **register pressure**: if each thread demands many registers, the fixed
register file is exhausted by fewer warps. The crucial nuance is that you do **not** need
100% — you need just *enough* resident warps to keep a ready one on hand through the
longest memory wait; past that point more occupancy buys nothing and can even hurt, since
squeezing in more warps leaves less register and scratchpad space per thread.

## Grounded explanation

### Where this sits: putting a number on "how over-subscribed is the SM?"

The prerequisite [[streaming-multiprocessor]] node established the GPU's whole strategy: an
SM deliberately keeps far more work **resident** (loaded onto the SM with its state in
place, ready to run) than it has **lanes** (arithmetic positions, each doing one add or
multiply per cycle) to execute at once. When a group of resident work stalls on a
hundreds-of-cycles memory load, the SM's scheduler switches *for free* to a different ready
group, burying the wait under other work. The [[warp]] node then named that group: the
scheduler's actual unit is the **warp** — a fixed bundle of 32 threads run in lockstep — so
the SM holds *many resident warps* and picks one ready warp to issue each cycle.

That immediately raises a quantitative question the two prerequisite nodes left open: *how
many* warps are actually resident? The latency-hiding trick only works if the SM has a
ready warp to switch to. Hold too few warps and the trick starves. **Occupancy is the name
for that count, expressed as a fraction.** Precisely:

> occupancy = (warps resident on the SM) ÷ (the maximum warps the SM can hold)

It is a ratio between 0 and 1 (often quoted as a percentage). The denominator is a fixed
hardware constant of the SM — on an H100, an SM can hold at most **64 resident warps**. The
numerator is whatever a given workload actually achieves, which is usually *less*, and the
rest of this node is about what pulls it down and why that hurts.

One term to fix before going on, used throughout: a **block** is the bundle of threads the
programmer launches together; the SM slices each resident block into [[warp]]s of 32. So
"how many blocks fit on the SM" and "how many warps fit" are the same question scaled by
32, and the SM holds whole blocks at a time.

### The why: occupancy is what feeds the latency-hiding trick

Here is the load-bearing reason occupancy matters at all — it is a direct consequence of
the [[streaming-multiprocessor]] mechanism, not a separate fact to memorize.

Recall the scheduler's game each cycle: scan resident warps, find one whose next
instruction is ready, issue it; if it stalls on memory, mark it and switch to another ready
warp next cycle. This works *only if there is another ready warp to find.* A memory load
takes on the order of hundreds of cycles to return. During those hundreds of cycles, the
warp that issued it is stalled and useless. To keep the lanes busy the SM needs *other*
warps that are not stalled — enough of them that, at every cycle, at least one has its next
instruction ready.

Now picture the two extremes:

- **Low occupancy — few resident warps.** Suppose only a handful of warps are resident. They
  all start, all soon hit memory loads, and all stall at roughly the same time. For the
  hundreds of cycles until data returns, the scheduler scans its few warps and finds *none*
  ready. The lanes have nothing to issue and sit **idle**. The SM's expensive width is
  wasted exactly when it should be working — the latency was *not* hidden because there was
  nothing to hide it behind.

- **Higher occupancy — many resident warps.** Now suppose dozens of warps are resident.
  When one stalls on a load, dozens of others are at different points in their own
  instruction streams; the odds that *all* of them are stalled in the same cycle are
  vanishingly small. The scheduler almost always finds a ready warp, so the lanes keep
  issuing. The hundreds-of-cycles wait of any one warp is completely buried under the
  arithmetic of the others. The latency is hidden — which is the entire point of the
  machine.

So occupancy is, concretely, *the supply of warps the latency-hiding trick draws from.* Raise
it and the trick has more to work with; starve it and the trick fails and lanes idle. This is
why "more resident warps = better latency hiding" — the [[streaming-multiprocessor]]'s free
warp-switch is only as good as the number of ready warps available to switch to.

### What sets the number: whichever fixed resource runs out first

The SM cannot hold unlimited warps because each resident warp *consumes* fixed resources, and
the SM has only so much of each. Three limits matter, and they are independent ceilings:

- **A hard cap on resident slots.** The SM has a fixed maximum number of resident warps (and
  blocks) it can track at all, regardless of how cheap each one is — 64 warps per SM on an
  H100. Even infinitely small warps cannot exceed this.
- **The register file.** Every resident thread needs its own permanent slice of the register
  file (the storage that makes the free warp-switch possible, per
  [[streaming-multiprocessor]]: nothing is saved or restored because each thread's values
  never move). The file is fixed — 65,536 32-bit registers per SM on an H100 — so the more
  registers *each thread* demands, the fewer threads, hence fewer warps, fit.
- **The on-chip scratchpad memory ([[shared-memory]]).** Each resident block reserves a chunk
  of the SM's fast on-chip scratchpad — the block-scoped fast space that [[shared-memory]]
  describes — (228 KB per SM on an H100). The more each block reserves, the fewer blocks fit.

The decisive rule — the one non-obvious step — is that these limits are **not** added or
averaged. They are applied independently, and the number of warps that actually fit is the
**minimum** across all of them. Each limit, taken alone, says "at most this many blocks";
the *most restrictive* one wins, because once any single resource is exhausted no further
block can be admitted no matter how much of the *other* resources remains free. A block
needing a lot of scratchpad but few registers is capped by scratchpad while its register
budget sits unused; a block needing many registers but little scratchpad is capped by
registers while scratchpad sits unused. **The binding constraint is whichever runs out
first, and that single constraint sets occupancy.** In practice, for compute-heavy kernels,
the resource that runs out first is overwhelmingly the register file — so register usage per
thread is the dominant lever on occupancy.

### Register pressure: the dominant cause of low occupancy

**Register pressure** means "registers used per thread" — how many of the SM's registers each
individual thread needs to hold its live working values. The compiler sets this number based
on how many intermediate values the kernel keeps alive at its busiest point: a kernel juggling
many partial results at once needs many registers per thread; a lean kernel needs few.

Because the register file is fixed and shared across all resident threads, register pressure
translates *directly* into occupancy through simple division. The file holds a fixed total;
divide by registers-per-thread to get the maximum threads that fit; divide by 32 to get warps.
Push registers-per-thread up and the warp count falls; pull it down and more warps fit. This is
the chief reason a kernel ends up with low occupancy: not too little parallel work, but each
thread being too *register-hungry*, so the file is drained by only a few warps.

There is also a cliff to avoid. The SM allows at most a fixed number of registers per thread
(255 on an H100-class GPU). If a kernel's live values exceed even that, the compiler **spills**
the overflow to far-away main memory instead of registers. A spilled value's load is roughly
*hundreds of times slower* than a register read — so the cure (cramming more state into each
thread) becomes far worse than the disease. The practical lever, then, is to keep each thread's
register demand modest: enough warps fit to hide latency, and no thread spills.

### The nuance: enough is enough — 100% is not the goal

The most-misunderstood point, and the one the source is emphatic about: **you do not need full
occupancy.** The trick needs *enough* ready warps to cover the longest memory wait — and once
you have that many, additional warps add nothing. If a stall lasts, say, a few hundred cycles
and the warps you already hold can keep the lanes fed across that entire window, then the lanes
are *already* saturated. A warp that is never needed because some other warp was always ready
contributes zero extra throughput.

Worse, chasing the last bit of occupancy can *backfire.* Fitting more warps means giving each
thread *fewer* registers and each block *less* scratchpad — the very resources threads compute
with. If the compiler is forced to spill to make room for warps that were not needed anyway, a
push for higher occupancy makes the kernel *slower*. So the target is not "maximize occupancy"
but "reach the occupancy that hides the latency, then stop" — typically well short of 100%.
Occupancy is a *means* to keep a ready warp on hand, not an end in itself.

### Worked instance: an SM that holds 64 warps, at 25% vs 75% occupancy

Take a single SM whose hard cap is **64 resident warps** (the H100 number). This example is
non-degenerate: it runs the *register-pressure* path explicitly (the binding limit is the
register file, not the slot cap or scratchpad), and it triggers both the low-occupancy failure
*and* the recovery, so the mechanism is visible rather than assumed.

**The register-hungry version — 16 warps, 25% occupancy.** Suppose the SM's register file holds
65,536 registers and the kernel's threads are register-heavy — the compiler reports each thread
needs many registers (say the budget works out so that only 16 warps' worth of threads fit
before the file is exhausted). Run the MIN-across-resources rule: the slot cap would allow 64,
scratchpad would allow plenty, but the register file allows only **16 warps**. The minimum wins,
so 16 warps are resident — occupancy = 16 ÷ 64 = **25%**. Now watch the latency-hiding trick try
to work with only 16 warps. They issue their loads from slow memory and stall. Sixteen is few
enough that, during the hundreds-of-cycles wait, the scheduler can run out of ready warps: it
scans all 16, finds them all stalled, and the lanes go idle. The SM is hiding *some* latency but
not all of it — every time the 16 warps bunch up on memory, throughput stalls. The expensive
lanes are starved, not by lack of work in the world, but because each thread hogged so many
registers that too few warps could be resident.

**The leaned-out version — 48 warps, 75% occupancy.** Now restructure the kernel so each thread
keeps fewer values live — fewer registers per thread. The same fixed 65,536-register file now
admits, say, 48 warps before it is full. Re-run the MIN: slot cap 64, scratchpad plenty,
register file now 48 → the minimum is **48 warps** resident, occupancy = 48 ÷ 64 = **75%**. With
48 warps on hand, when one batch stalls on memory there are dozens of others at different points
in their streams; the scheduler essentially *always* finds a ready warp, so across the entire
hundreds-of-cycles memory window the lanes keep issuing. The latency is now fully buried — the
lanes are saturated. Same SM, same hardware, same memory latency; the only change was cutting
register pressure so more warps fit, and that is what lifted occupancy from 25% to 75% and turned
idle lanes into busy ones.

**And the nuance, on the same machine.** Note we did *not* need all 64 warps. If 48 already keep
the lanes saturated through the longest stall, then forcing the file to fit 64 — by squeezing each
thread's registers even tighter, possibly to the point of spilling to slow memory — would add
warps that are never the one chosen and might *slow* each thread down. The win was reaching *enough*
occupancy (here ~75%), not maxing it. **The lever to remember:** tune registers-per-thread and block
size so that just enough warps stay resident to hide the latency — no fewer (lanes starve) and no
more than the resources comfortably allow (threads get starved instead).

## Prerequisites

- [[streaming-multiprocessor]]
- [[warp]]
- [[shared-memory]]

## Sources

- linux-internals-complete.html — *Occupancy — how many blocks fit on an SM* (occupancy as the
  fraction of the SM's warp cap that is resident; the rule that the actual count is the **minimum**
  across independent fixed-resource limits; the H100 caps used here — 64 warps / 2048 threads / 32
  blocks per SM, 65,536 registers, 228 KB shared memory — and "more resident warps = better latency
  hiding"); *Why the design works — the synthesis* (the whole architecture hides memory latency
  through over-subscription: provide far more warps than can run at once and the scheduler always
  finds a ready one); *Register pressure — connecting back to occupancy* (register pressure =
  registers used per thread; the fixed register file ÷ registers-per-thread sets how many warps fit,
  making register pressure the dominant occupancy limiter; the per-thread register cap and the
  ~hundreds-of-times-slower cost of spilling to main memory).
