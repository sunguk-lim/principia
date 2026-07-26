---
id: shared-memory
title: Shared Memory
summary: Shared memory is one of the gpu-memory-spaces — specifically the fast, on-chip region whose scope is exactly one block of the cuda-thread-hierarchy.
type: concept
tags: [gpu]
prereqs: [gpu-memory-spaces, cuda-thread-hierarchy, barrier]
sources:
  - "linux-internals-complete.html — 'Shared memory — the per-block scratchpad'"
  - "linux-internals-complete.html — 'Synchronization — making threads wait for each other'"
  - "linux-internals-complete.html — 'Memory access patterns — coalescing and bank conflicts'"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Shared Memory

## Summary

**Shared memory** is one of the [[gpu-memory-spaces]] — specifically the fast, on-chip
region whose *scope* is exactly one **block** of the [[cuda-thread-hierarchy]]. Recall the
two facts those prerequisites established: shared memory lives on the fast on-chip rung
(roughly as quick as a thread's private registers, and far faster than the large, slow
off-chip main memory the GPU calls *global memory* — HBM, on the order of an order of
magnitude slower per access), and *every thread in the same block* can read and write it,
while threads in other blocks cannot see it at all. This node explains what a programmer
actually *does* with that space. It has two uses. First, it is a **programmer-managed
scratchpad**: the block loads a chunk of data from slow global memory into shared memory
*once*, and then its threads reuse that chunk many times on-chip instead of re-reading
global memory. Second, it is a **communication channel**: one thread writes a value, and
another thread in the same block reads it, without any trip out to global memory. Both uses
need a new mechanism the prerequisites only hinted at — a **[[barrier]]**, written
`__syncthreads()`, that makes the whole block wait at one line so that a thread never reads
a shared value before the thread responsible for writing it has actually done so. The
*why* of shared memory is the single most important GPU optimization: it is the explicit
tool for converting expensive, repeated reads of slow global memory into **one** global
read plus **many** fast on-chip reuses.

## Grounded explanation

### What it is: the block-scoped fast space, now used on purpose

From [[gpu-memory-spaces]] we already have the inventory: a value lives in *registers*
(private to one thread, fastest, tiny), in *shared memory* (on-chip, fast, visible to a
whole block), or in *global memory* (the large, slow, off-chip main memory — HBM — that the
whole grid and the host can see). That node also gave the structural law: each space's scope
matches a level of the [[cuda-thread-hierarchy]] — registers ↔ thread, shared ↔ block,
global ↔ grid. So "shared memory" is not new hardware here; it is the *block-scoped* space,
examined for how a program puts it to work.

The defining facts that make it useful are three, and each follows from the prerequisites:

- **It is fast.** It sits on the on-chip rung, so reading it costs on the order of a few
  cycles — comparable to a register, and far cheaper than the several-hundred-cycle latency
  of a global-memory (HBM) read. The source measures it at roughly 30× faster than HBM.
- **It is shared across the block.** This is the part registers cannot do. A register slot
  belongs to one thread and no other thread can ever see it. A shared-memory location, by
  contrast, is reachable by *every* thread in the block — that is precisely what
  "block scope" means. So shared memory is the only fast space through which the threads of
  a block can hand data to one another.
- **It is small and temporary.** It is a modest on-chip region (a block may use up to a few
  hundred kilobytes, far less than the gigabytes of global memory), and, as
  [[gpu-memory-spaces]] noted about the fast spaces, it **evaporates** when the block
  finishes. Nothing written to shared memory survives the block; only global memory persists.

A program declares a shared array inside its per-thread function (the *kernel*, from
[[cuda-thread-hierarchy]]) and that one array is *the same physical storage* for all threads
of the block — when thread 3 writes element 7 and thread 50 later reads element 7, they touch
the identical location. That single shared object is the whole concept's central tool, and it
supports the two uses below.

### Use 1 — the scratchpad: load once from global, reuse many times on-chip

Here is the use that matters for speed, and it is the direct continuation of the lesson
[[gpu-memory-spaces]] ended on. That node showed that *moving bytes off the slow rung is what
you pay for*, and that a program wins by loading a chunk into a fast space once and reusing
it. Shared memory is the handle on that lever, and now we can say *how* the block pulls it.

The pattern is always the same three phases:

1. **Cooperative load.** The threads of the block split the work of copying a chunk of data
   from global memory into a shared array — the natural split is one element per thread, so a
   chunk of *N* elements arrives in **one** pass of *N* global reads, each element read by
   exactly one thread.
2. **Barrier.** The block waits until *all* of those loads have completed (this is where
   `__syncthreads()` comes in — next section).
3. **Reuse.** Every thread now reads from the shared array, as many times as the computation
   demands, paying only the cheap on-chip cost each time — never touching global memory for
   that data again.

The payoff is exactly the trade [[gpu-memory-spaces]] quantified: the *same* total number of
data reads happens, but the expensive ones (global/HBM) collapse to a single load pass, while
the bulk of the reads are served by the fast on-chip rung. We did not reduce the arithmetic;
we only changed *which space serves the reused data*.

### Use 2 — communication: one thread writes, another in the block reads

The second use exploits the *sharing* directly rather than the speed. Because all threads of
the block see the same shared locations, a block can compute something **collectively**: each
thread writes its own partial result into a distinct shared slot, and then threads read each
other's slots to combine them. (A typical case is summing a block's values: each thread
deposits its number, then the threads fold the deposited numbers together into one total — a
*reduction*.) This is impossible across the whole grid, because, as [[cuda-thread-hierarchy]]
stressed, blocks are mutually independent with no shared meeting place; it is possible
*inside* a block precisely because a block is co-located on one processing unit, which is the
very reason block scope exists.

### Why synchronization is mandatory: the race, and the `__syncthreads()` barrier

Both uses contain a hidden hazard, and resolving it is the heart of this node. The
prerequisite [[cuda-thread-hierarchy]] told us that the hardware does not run a block's
threads all at the same instant: it slices the block into groups of 32 that run as lockstep
units (the chip's *warp*), and **different such groups run at different times**, scheduled
independently. So at any given moment, some of the block's threads may have finished their
work and others may not have started.

Now combine that with shared memory. In the scratchpad pattern, thread A loads element 7 of
the tile while thread B intends to *read* element 7. If B's group runs before A's group has
done its write, B reads whatever garbage was sitting in that shared slot — a value not yet
written. This is a **race**: the result depends on the unpredictable relative timing of the
threads, so the program is simply wrong, sometimes. The same hazard appears in the
communication use: a thread reading a neighbor's partial result before the neighbor has
deposited it.

The fix is a **barrier**: a line in the kernel, written `__syncthreads()`, with one rule —
**no thread in the block proceeds past it until every thread in the block has reached it.**
Placed *after* the writes and *before* the reads, it guarantees that by the time any thread
is allowed to read shared memory, all the writes it might depend on have already happened. The
barrier is what converts "the threads run at unknown relative times" into "the threads run in
two well-ordered phases: everyone writes, then everyone reads." It is the missing coordination
the prerequisites pointed at but did not provide.

(One caution the source flags: the barrier must sit where *all* threads of the block actually
reach it. If it is hidden inside a branch that only some threads take, the rest never arrive,
the arrived threads wait forever, and the kernel hangs or corrupts data. Put `__syncthreads()`
on a line every thread executes.)

### Bank conflicts: laying data out so the fast space stays fast

One more property governs how fast shared reads really are. The hardware splits shared memory
into 32 equal slices called **banks**, and each bank can serve only one request per cycle, but
all 32 banks work in parallel. The locations are striped across the banks in order: element 0
is in bank 0, element 1 in bank 1, …, element 31 in bank 31, and element 32 wraps back to bank
0. So if the 32 lockstep threads of a group each read a *consecutive* element, they hit 32
*different* banks and all 32 reads complete in a single cycle. But if their access pattern
makes several threads land on the *same* bank — for instance, reading with a stride of 32, so
every thread targets bank 0 — those accesses cannot be served together; the bank handles them
one after another, serializing what should have been parallel. That is a **bank conflict**, and
it throws away much of shared memory's speed. The practical lesson is to lay shared arrays out
so a group of threads touches spread-out banks; a classic trick for a two-dimensional tile is
to pad each row by one extra element, which shifts every row's bank alignment and breaks an
otherwise conflicting pattern. (Bank conflicts concern reads *within* shared memory; they are
distinct from *coalescing*, which is the analogous "spread your accesses out" rule for reads
from global memory — both reward consecutive, regular access patterns, but on different
spaces.)

### Worked instance: a tiled matrix multiply

Take a concrete, non-degenerate case: one block computing a 16×16 block of a matrix product
`C = A × B`. Each output element `C[row][col]` is a dot product of a row of `A` with a column
of `B`. Lay the block out as **256 threads arranged 16×16**, so thread `(ty, tx)` owns output
`C[ty][tx]`. For this worked instance the relevant slice of the multiply is a single 16-wide
strip: a 16×16 tile of `A` and a 16×16 tile of `B`, both starting in global memory (HBM).

**The naive cost, with no shared memory.** Each of the 256 threads must read 16 elements of
its `A` row and 16 elements of its `B` column from global memory — 32 global reads per thread:

```
naive global reads = 256 threads × 32 elements = 8,192 reads from HBM.
```

But notice the waste: the 16 threads sharing a row of `C` all read the *same* 16 `A` elements,
and the 16 threads sharing a column all read the *same* 16 `B` elements. Each tile element is
re-read from slow HBM 16 times over. Counting another way: the two 16×16 tiles hold
`2 × 16 × 16 = 512` distinct elements, yet the naive scheme reads `8,192`, i.e. each element
fetched `8,192 ÷ 512 = 16` times. Sixteen-fold redundant traffic on the slowest rung.

**The tiled version, using shared memory.** Declare two shared arrays, `tile_A[16][16]` and
`tile_B[16][16]`. Run the three phases:

1. **Cooperative load.** Each of the 256 threads loads *one* element of `A` into
   `tile_A[ty][tx]` and *one* element of `B` into `tile_B[ty][tx]`. That is the whole of both
   tiles brought in by a single pass:

   ```
   tiled global reads = 256 threads × 2 elements = 512 reads from HBM (each element loaded once).
   ```

2. **Barrier.** The block calls `__syncthreads()`. This is the load-bearing step. Without it,
   thread `(0, 0)`'s lockstep group might race ahead to phase 3 and start reading
   `tile_A[0][5]` or `tile_B[10][0]` while the threads responsible for *writing* those slots
   are in a group that has not run yet — reading values not yet loaded, and producing a wrong
   product. The barrier forces every one of the 256 threads to finish its load before any
   thread begins the dot product.

3. **Reuse on-chip.** Now each thread computes its dot product by reading the tiles from fast
   shared memory:

   ```
   sum = 0
   for k = 0 … 15:
       sum += tile_A[ty][k] * tile_B[k][tx]
   ```

   That is 16 reads of `tile_A` and 16 of `tile_B` per thread — `256 × 32 = 8,192` *shared*
   reads. The reuse count is **identical** to the naive scheme's read count; what changed is
   the rung serving it.

Compare only the slow-rung traffic, the term that dominates the cost:

```
HBM reads, naive : 8,192
HBM reads, tiled :   512
reduction        : 8,192 ÷ 512 = 16× fewer trips to slow global memory.
```

The 8,192 expensive HBM reads collapse to 512 expensive loads plus 8,192 *cheap* on-chip
shared reads. Since the on-chip rung is roughly an order of magnitude faster per access, the
block's time drops by a comparable factor — and we changed no arithmetic and bought no new
hardware. We only moved the reused data from the grid-scoped slow space into the block-scoped
fast one, ordered the two phases with one barrier, and (if we cared to shave the last cycles)
would lay the tiles out to avoid bank conflicts among each group of 16 reading threads. That is
the entire payoff of shared memory, and it is why it is called *the* core technique behind every
fast matrix-multiply kernel.

## Prerequisites

- [[gpu-memory-spaces]]
- [[cuda-thread-hierarchy]]
- [[barrier]]

## Sources

- *linux-internals-complete.html* — "Shared memory — the per-block scratchpad": shared memory is ~30× faster than HBM, lets a block's threads exchange data without going through global memory, the `__shared__` tile declaration, and the 16×16 tiled-matmul example where loading each element once (256 reads) and reusing it 16 times cuts HBM traffic 16×.
- *linux-internals-complete.html* — "Synchronization — making threads wait for each other": threads in different warps run independently, so a write-then-read across warps needs coordination; `__syncthreads()` is a per-block barrier (no thread proceeds until all reach it), used after writing shared memory and before reading what another thread wrote; the trap that a barrier inside divergent control flow hangs or corrupts.
- *linux-internals-complete.html* — "Memory access patterns — coalescing and bank conflicts": shared memory is split into 32 banks striped across consecutive elements, one request per bank per cycle; same-bank accesses by a warp serialize (bank conflict), with the pad-the-row fix; coalescing as the analogous contiguous-access rule for global memory.
