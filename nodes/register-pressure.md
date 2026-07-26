---
id: register-pressure
title: Register Pressure
summary: Register pressure is the number of registers each thread uses — where a register is the fastest storage the hardware has, a tiny on-chip slot that holds one of a thread's live…
type: concept
tags: [gpu]
prereqs: [occupancy, warp]
sources:
  - "linux-internals-complete.html — Register pressure — connecting back to occupancy (register pressure = registers used per thread; the register file ÷ registers-per-thread sets how many warps fit, so register pressure is the dominant occupancy limiter; the per-thread register cap of 255 on Hopper; spilling overflow to HBM-backed \"local memory\" at ~400 cycles, ~400× slower than a register read)"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Register Pressure

## Summary

**Register pressure** is the number of **registers** each thread uses — where a register
is the fastest storage the hardware has, a tiny on-chip slot that holds one of a thread's
live working values and is read or written in a single cycle. Every thread that is resident
on the chip needs its own private set of these slots, and they all come out of one fixed pool
called the **register file**. Because that pool is a fixed size, register pressure sets, by
plain division, how many threads — and therefore how many warps (the bundles of 32 threads
the hardware schedules) — can be resident at once: the file's total capacity divided by
registers-per-thread gives the thread ceiling. So register pressure is the tension between
how much fast storage each thread claims and how many threads can coexist. This is exactly
the lever that controls [[occupancy]]: a register-hungry kernel fits *fewer* [[warp]]s, lowering
[[occupancy]], which (per that node) weakens the chip's one trick for hiding slow-memory
waits — switching to another ready [[warp]]. There is also a hard cliff: if a thread's live
values exceed the per-thread register limit, the compiler **spills** the overflow to slow
off-chip memory, paying a large latency penalty on every spilled access. So a kernel author
trades thread-local speed (more registers held close) against [[occupancy]] (fewer warps),
and that trade-off is one of the primary knobs for tuning a kernel.

## Grounded explanation

### Where this sits: the prerequisite left one number unexplained

The [[occupancy]] node established the whole chain of *why* a chip wants many resident warps.
A [[warp]] is a bundle of 32 threads the hardware schedules together; **resident** means
loaded onto the chip with its working state in place, ready to run; **occupancy** is the
fraction of the chip's warp-slot capacity that is actually resident. That node's load-bearing
result was that resident warps are the *supply* the latency-hiding trick draws from: when one
warp stalls for hundreds of cycles waiting on slow main memory, the scheduler switches for
free to another resident warp, so the arithmetic units stay busy only if enough other warps
are on hand. It also stated the punchline that this node now unpacks: the dominant thing that
drains [[occupancy]] is **register pressure**, because for compute-heavy kernels the register
file is the resource that runs out first.

That node treated "registers used per thread" as a given number it divided into the file. This
node explains where that number comes from, why it is the binding constraint so often, and the
second failure mode — spilling — that the [[occupancy]] node only named in passing.

### What a register is, and why each thread needs its own

A **register** is the smallest, fastest piece of storage the processor has: a named slot,
each holding one value (a 32-bit number), that an instruction can read and write in a single
clock cycle — the speed at which arithmetic itself runs. Every other place a value can live —
on-chip scratchpad, caches, off-chip main memory — is slower, from tens of cycles to many
hundreds. When a thread computes, the values it is actively working with (loop counters,
accumulating sums, intermediate products) must sit in registers to be operated on at full
speed. The set of values a thread needs alive *at the same instant* is its **working set**,
and the count of registers that working set requires is what register pressure measures.

Crucially, the chip keeps every resident thread's registers physically present *all the
time*. This is the substrate behind the free warp-switch the [[occupancy]] node relied on:
the scheduler can flip from a stalled warp to a ready one at zero cost precisely because
nothing is saved or restored — each thread's values never leave their own slots. The price of
that zero-cost switch is that the slots must all coexist in hardware simultaneously. They live
in the **register file**: a single fixed block of fast on-chip storage, of a size set when the
chip was manufactured, that must hold the registers of *every* resident thread at once.

### The why: a fixed file divided by per-thread demand caps the warp count

Here is the load-bearing mechanism, and it is just division. Call the register file's total
capacity $F$ (a fixed hardware constant) and call register pressure $R$ (the registers each
thread uses, set by the kernel). Because every resident thread needs its own $R$ slots and
all of them must fit inside the one file of size $F$, the largest number of threads that can
be resident is $F \div R$. Divide that by 32 — the threads in a warp — and you have the
largest number of *warps* that fit, which is the numerator of [[occupancy]].

The non-obvious consequence is the *inverse* relationship: $R$ sits in the denominator, so
making each thread richer in registers makes the resident warp count *smaller*. A kernel does
not lower its own [[occupancy]] by lacking parallel work to do; it lowers [[occupancy]] by
each thread being too register-hungry, so the shared file is drained by only a few warps. And
because the [[occupancy]] node showed that few resident warps means the scheduler runs out of
ready warps to switch to during a memory stall — leaving the arithmetic units idle — high
register pressure translates, through this one division, straight into wasted throughput. That
is the whole reason register pressure is the chip's primary [[occupancy]] limiter rather than
one factor among many: it is the resource compute-heavy kernels exhaust first, and it moves
[[occupancy]] by simple, unavoidable arithmetic.

This also explains why it is a *tunable knob* and not a fixed property. The compiler decides
$R$ by looking at how many values the kernel keeps alive at its busiest point. An author can
push $R$ down — for example by recomputing a value when it is next needed instead of holding
it live in a register across a long stretch, trading a little extra arithmetic for a freed
slot — or accept a higher $R$ to keep more state close and avoid recomputation. Lower $R$ buys
more warps and better latency hiding; higher $R$ buys faster work *within* each thread. Tuning
a kernel is largely choosing where on that trade-off to sit.

### The cliff: spilling to slow memory

There is a second, sharper failure mode hiding inside register pressure. The hardware not only
has a finite file; it also imposes a fixed **per-thread** cap on registers — the most slots any
single thread is allowed to claim (255 on a Hopper-class chip). If a kernel's working set needs
*more* live values than that cap allows, the values cannot all stay in registers. The compiler
then **spills**: it picks some live values and stores them in off-chip main memory instead,
loading each one back into a register only for the moment an instruction needs it.

The trap is the name this spilled storage carries — **"local memory"** — which sounds fast and
nearby but is the opposite. Local memory is physically the chip's slow off-chip main memory; a
register read costs one cycle, while a load from local memory costs on the order of hundreds of
cycles — roughly four hundred times slower. So a spilled value turns what would have been a
free, single-cycle register access into a long memory wait, *on every use of that value*. The
cure for "too many live values" (cram them all into the thread) becomes far worse than the
disease once it overflows into spilling: instead of a thread that merely lowers [[occupancy]],
you get a thread that is itself slow on every spilled access. The practical guidance the source
draws from this is to keep register pressure modest enough that two things hold at once — enough
warps fit to feed the latency-hiding trick, and no thread spills.

### Worked instance: one SM, three levels of register pressure

Take a single processing unit — the unit that holds resident warps and runs the warp-switching
trick — with a register file of $F = 65{,}536$ registers (call it 64K) and a hard cap of 1024
resident threads, i.e. $1024 \div 32 = 32$ warp slots. This example is non-degenerate: it walks
three distinct $R$ values that each land in a *different* regime — capped by threads, exactly
balanced, and capped by registers — and then pushes into the spill cliff, so every branch of the
mechanism fires rather than being assumed.

**$R = 32$ registers per thread.** The file allows $65{,}536 \div 32 = 2048$ thread-slots, but
the unit's hard thread cap is only 1024. The register file is *not* the binding limit here — the
thread cap is — so 1024 threads (all 32 warp slots) are resident: full [[occupancy]], with the
register file half empty. Register pressure is low enough that it does not even enter the
calculation; latency hiding has the maximum number of warps to draw from.

**$R = 64$ registers per thread.** Now the file allows $65{,}536 \div 64 = 1024$ thread-slots —
exactly the thread cap. Both limits coincide at 1024 threads, so [[occupancy]] is still full, but
the register file is now *completely* full. This is the knife's edge: there is no headroom left.
The kernel is faster per thread (each thread holds twice the working set close, fewer
recomputations) yet has spent its entire register budget to do so.

**$R = 128$ registers per thread.** The file now allows only $65{,}536 \div 128 = 512$
thread-slots — well below the 1024 cap. The register file is the binding limit, so just 512
threads, $512 \div 32 = 16$ warps, are resident: [[occupancy]] = $16 \div 32 = 50\%$. Watch the
[[occupancy]] node's mechanism bite: with only 16 warps, when a batch of them issues loads from
slow memory and stalls for hundreds of cycles, it is far more likely that the scheduler scans all
16 and finds none ready, so the arithmetic units go idle. Doubling each thread's register appetite
from 64 to 128 halved the warp supply and opened gaps the latency-hiding trick can no longer cover.

**Past the cliff.** Push the kernel's working set beyond the 255-register per-thread cap and the
compiler can no longer satisfy it from registers at all: it spills the overflow to local (off-chip)
memory. Now the threads that are resident are *also* slow, because some of their values cost a
hundreds-of-cycles memory load on every use rather than a one-cycle register read. The kernel has
hit the worst of both worlds — few resident warps *and* slow threads.

The lever to remember spans all four cases: register pressure $R$ is the denominator that sets how
many warps fit, so the author tunes $R$ (how much state each thread keeps live) to land where just
enough warps stay resident to hide the memory latency — high enough $R$ to keep each thread fast,
low enough to keep [[occupancy]] adequate, and never so high that the thread spills.

## Prerequisites

- [[occupancy]]
- [[warp]]

## Sources

- linux-internals-complete.html — *Register pressure — connecting back to occupancy* (register
  pressure defined as "registers used per thread"; the register file ÷ registers-per-thread sets
  how many warps fit per scheduling unit, so higher pressure lowers occupancy and leaves the
  scheduler fewer warps to hide latency with; the per-thread register cap of 255 on Hopper; the
  compiler **spills** overflow to HBM-backed "local memory", where a spilled load is ~400 cycles
  and roughly 400× slower than a register read). The worked instance uses SM-level numbers
  (65,536-register file, 1024-thread / 32-warp cap) consistent with the [[occupancy]] node, where
  the source's own derivation is stated at the sub-core level (16K registers, 16 warps).
