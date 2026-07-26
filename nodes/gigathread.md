---
id: gigathread
title: GigaThread Engine
summary: The GigaThread engine is the GPU's single global hardware scheduler — a small fixed circuit on the chip, not a program — whose one job is to hand out the work of a launched job to…
type: concept
tags: [gpu]
prereqs: [streaming-multiprocessor, warp]
sources:
  - "linux-internals-complete.html — Phase 7: The bridge — GigaThread maps program to chip; Host interface → GigaThread → SMs; Level 1/Level 2 — blocks mapped to SMs by GigaThread (3907-block worked example on a 132-SM H100)"
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# GigaThread Engine

## Summary

The **GigaThread engine** is the GPU's single global hardware scheduler — a small
fixed circuit on the chip, not a program — whose one job is to hand out the work of a
launched job to the chip's [[streaming-multiprocessor]]s (SMs). A GPU job is a
**kernel** (one computation applied across a large pile of data), and launching it
produces a **grid**: a flat collection of many independent **blocks**, where each block
is one bundle of threads responsible for its own slice of the data. The
[[streaming-multiprocessor]] node already named a "small global distributor" that hands
blocks to SMs and refills an SM when one finishes — *the GigaThread engine is that
distributor*, and this node opens it up. It assigns each block to some SM that has free
capacity (enough registers, scratchpad memory, and warp/thread slots to host it),
packing several blocks onto each SM up to that SM's resource limit. The crucial behavior
is its refill rule: the instant a block *finishes* on an SM and frees that SM's
resources, GigaThread immediately drops a waiting block from the grid onto the freed SM,
so no SM ever sits idle while blocks remain undispatched. Because blocks are
**independent** — no ordering and no communication between them — this distribution
needs no synchronization, and the *same* grid scales transparently: on a small GPU (few
SMs) the blocks run in more sequential **waves**, on a big GPU (many SMs) more blocks run
at once in fewer waves. You write the kernel once; GigaThread spreads it to fit whatever
hardware it lands on.

## Grounded explanation

### What GigaThread is, and the gap it bridges

The prerequisite [[streaming-multiprocessor]] node built the chip from one side: a GPU is
an array of many SMs (about 132 on an NVIDIA H100), each SM a self-contained engine that
hides memory latency by keeping far more threads resident than it has lanes and switching
between them for free. That node also said a GPU job — a **kernel**, meaning one
computation applied across a huge pile of data — is partitioned by the programmer into
many independent pieces called **blocks** (each block one bundle of threads owning a slice
of the data), and that "a small global distributor on the chip" hands those blocks to the
SMs and refills an SM with a fresh block whenever one finishes. It deliberately left that
distributor unnamed and unopened. **This node is that distributor: the GigaThread engine.**

So there are two things that have to be married. On the software side is the **grid** — the
name for the entire collection of blocks produced by one kernel launch, the complete pile
of work to be done. On the hardware side is the physical **SM array** — the fixed number of
SMs etched into the chip. The grid says *what* work exists; the SM array says *where* work
can physically run. GigaThread is the bridge between them: it is the piece of silicon that
turns the abstract command "run these N blocks" into the concrete reality "keep every SM
loaded with blocks until all N are done." Like the SM's own [[warp]] scheduler from the
prerequisite node, GigaThread is *fixed hardware* — a small circuit, not software running on
the cores — so its decisions cost essentially nothing and happen continuously as the chip
runs.

### What GigaThread does, step by step

GigaThread's behavior is a simple, continuously-running loop over the grid's blocks. To
state it precisely, one term first: an SM has finite **capacity** — a fixed budget of the
three resources the prerequisite node described (the register file that must hold every
resident thread's working values, the on-chip scratchpad memory, and the slots for resident
threads). A block consumes some of each when it lands. How many blocks an SM can host *at
once* is called its **occupancy**, and it is just "however many blocks fit before one of
those three budgets runs out." A lightweight block (few registers, little scratchpad) packs
many to an SM; a heavy one packs few.

With that, the loop is:

1. **Pick a waiting block** from the grid (the blocks not yet placed on any SM).
2. **Find an SM with free capacity** — one whose register/scratchpad/slot budget still has
   room for another block. GigaThread fills SMs *greedily*: it dispatches to whichever SM
   has room, spreading blocks across the array.
3. **Dispatch the block to that SM.** The SM allocates the block its slice of registers and
   scratchpad and admits its threads as resident. From this moment the block lives on that
   one SM for its entire life — *it never migrates* to another SM.
4. **On completion, refill.** When a block finishes, it releases its resources back to its
   SM. GigaThread sees the freed capacity and immediately dispatches a waiting block onto it.

Steps 1–3 fill the chip; step 4 keeps it full. The loop runs until the grid is exhausted.

### The why: independence is what makes the whole scheme work

The single non-obvious property — the one that justifies why GigaThread can be so simple and
why the scheme scales — is that **blocks are independent**. There is no defined order in
which blocks must run, no block waits on another, and blocks never communicate or share
state. (Within a block its threads can cooperate, but that is internal to the block and
handled by the SM, not by GigaThread.)

Trace through the consequences, because every desirable property falls out of this one fact:

- **No synchronization is needed.** Since block 7 neither depends on nor talks to block 3,
  GigaThread can place them on any SMs, in any order, at any time, with zero coordination.
  It never has to ask "is it safe to run this block yet?" — the answer is always yes. That is
  why the distributor can be a tiny fixed circuit rather than a complex software scheduler.

- **Greedy refill is always correct.** Because order does not matter, the instant an SM frees
  up, *any* remaining block is a valid choice to run next. So GigaThread can refill on pure
  availability — first free SM gets the next block — and never leave an SM idle while work
  remains. This is the "SMs never idle" guarantee, and it is sound *only* because blocks are
  interchangeable in ordering.

- **The same grid scales across any GPU — write once, scale with the hardware.** This is the
  payoff. A **wave** is one round of blocks running concurrently across the SM array — as many
  blocks as the chip can hold resident at one time. If a grid has more blocks than fit in one
  wave, the leftovers wait and stream onto SMs as earlier blocks finish, forming later waves.
  A small GPU has few SMs, so each wave holds few blocks and the grid takes *more* waves; a big
  GPU has many SMs, holds more blocks per wave, and finishes in *fewer* waves. The programmer
  changes nothing — the identical grid simply runs in however many waves the hardware dictates.
  GigaThread absorbs the difference. This works for exactly the same reason the greedy refill
  is correct: independent blocks impose no ordering, so splitting them across more or fewer
  waves never changes the result, only the running time.

In one line: GigaThread converts "launch N blocks" into "keep all SMs saturated," and it can
do so with a trivial circuit precisely because independent blocks demand nothing more.

### Worked instance: 3907 blocks on a 132-SM GPU, and the same grid on a small one

Take the concrete kernel from the [[streaming-multiprocessor]] node — element-wise addition
`c = a + b` over one million elements, partitioned into blocks of 256 threads, giving
`1,000,000 ÷ 256 ≈ 3,907` independent blocks. That whole set of 3,907 blocks is the grid. It
is a non-degenerate instance: many blocks (not one), and a real distribution decision rather
than a trivial fit.

**On a 132-SM H100.** The add kernel is featherweight — each thread does a single add and uses
very few registers — so each SM's occupancy is high; here an SM can host up to its hardware
maximum of **32 blocks** at once before any resource budget is hit. GigaThread fills greedily
across the array. One wave can therefore hold up to `132 × 32 = 4,224` resident blocks. The
grid has only 3,907 blocks — *fewer than one wave* — so **every block fits at once**: GigaThread
sprays all 3,907 across the 132 SMs (roughly `3,907 ÷ 132 ≈ 30` blocks per SM) and the entire
grid runs concurrently in a single wave. There is nothing left to refill; the grid completes in
about the time of one block. Note the worked numbers expose the *non-degenerate* branch: 3,907
is a genuine many-block grid, it just happens to fit in one wave because occupancy is high.

**The refill branch.** To see step 4 actually fire, enlarge the grid to, say, 50,000 blocks (a
bigger array). Now `50,000 > 4,224`, so the first wave fills all 132 SMs to their 32-block
capacity — `4,224` blocks resident — and the remaining `~45,800` blocks wait. As each resident
block finishes its 256 adds and frees its SM's resources, GigaThread immediately drops a waiting
block onto that freed slot. Blocks thus stream onto the SMs in successive waves until all 50,000
are done, with the SMs never idling between waves.

**The same 3907-block grid on a small GPU.** Now run the *unchanged* 3,907-block grid on a tiny
16-SM GPU. With the same 32-block occupancy, one wave holds only `16 × 32 = 512` blocks. So the
3,907 blocks no longer fit at once: GigaThread loads the first 512, and as those finish it streams
the rest on, taking about `3,907 ÷ 512 ≈ 8` waves instead of one. The programmer wrote exactly the
same kernel and launched exactly the same grid; GigaThread simply ran it in more waves to match the
smaller chip. Same code, scaled to the hardware — the property the whole design exists to deliver.

Throughout, GigaThread only *places and refills* blocks. Once a block is resident on an SM, hiding
that SM's memory latency by switching among the block's resident warps is the SM's own job, exactly
as the [[streaming-multiprocessor]] node described — GigaThread's contribution ends at keeping every
SM full of blocks to switch among.

## Prerequisites

- [[streaming-multiprocessor]]

## Sources

- linux-internals-complete.html — *The bridge — GigaThread maps program to chip* (GigaThread as the
  matchmaker: grid → GPU, block → one SM where it stays, many blocks per SM; greedy/round-robin
  distribution and immediate refill of freed slots), *Host interface → GigaThread → SMs* (the grid is
  handed to GigaThread, which dispatches blocks across SMs), and *Level 1 / Level 2 — blocks mapped to
  SMs by GigaThread* (the 3907-block grid on a 132-SM H100 fitting in one wave at 32 blocks/SM; a larger
  grid waiting and refilling in waves; blocks independent and non-migrating).
