---
id: context-switch
title: Context Switch
summary: "A context switch is the maneuver by which one CPU runs more processes than it has cores: the kernel pauses whichever process is currently executing, saves everything that process…"
type: concept
tags: [os/process]
prereqs: [process, interrupt]
sources:
  - linux-internals-complete.html ("Context switching — swapping one process for another", "When does a context switch happen?")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Context Switch

## Summary

A **context switch** is the maneuver by which one CPU runs more [[process]]es than it
has cores: the kernel pauses whichever process is currently executing, *saves* everything
that process needs in order to resume later, then *loads* a different process's saved state
and lets it run instead. The "context" is exactly that resumable state — the contents of
the CPU's registers (its small, fast internal scratch slots), including the **program
counter** (which records the next instruction to execute) and the **stack pointer** (which
records the top of the process's working memory). Because the kernel snapshots and later
restores this state faithfully, the paused process, when resumed, cannot tell it was ever
stopped: it continues from the exact instruction it was on, with the exact values it had.
That illusion — many processes each believing it has the CPU to itself, while really they
take turns microseconds at a time — is what the context switch buys, and it is not free:
saving and restoring state, and switching to the new process's private memory map, costs
real time, and the new process then runs slowly for a while until the CPU's caches refill.

## Grounded explanation

### The problem a context switch solves

A CPU core executes one instruction stream at a time — physically, at any single instant it
is running the instructions of exactly one [[process]]. Yet a running system has dozens or
hundreds of processes that all want to make progress. Recall from [[process]] that a process
is a *running instance of a program* with its own private memory and its own live state, and
that the kernel tracks each one in a record in its process table; recall too that a process
can be **runnable** (wants the CPU now) or **sleeping** (waiting for some event). The kernel
needs a way to give many runnable processes the *appearance* of running at once on a CPU that
can truly run only one. The context switch is that mechanism: run process A for a brief slice,
set it aside, run process B for a slice, and so on, rotating fast enough that to a human each
process looks continuously alive.

For this rotation to be honest, setting a process aside and bringing it back must be perfectly
reversible. That requirement is the whole design problem, and "context" is its answer.

### What the "context" is — and why exactly this state

To pick up an interrupted [[process]] *as if nothing happened*, you must restore everything
the CPU was relying on at the moment you stopped it. That state lives in two places.

First, the CPU's **registers**: a small fixed set of named storage slots inside the processor
itself — far smaller and far faster than memory — holding the values the program is working
with right now. Two registers matter by name. The **program counter** (PC) holds the address
of the next instruction the CPU will fetch; it *is* the answer to "where in the code was this
process?" The **stack pointer** holds the address of the top of the process's stack, the
scratch region (introduced in [[process]]) that records pending function calls and local
values; it *is* the answer to "how deep into its work was it?" Lose the program counter and
you would not know where to resume; lose the stack pointer or any general register and the
arithmetic the process was mid-way through would be corrupted. So the context is precisely the
set of values that, if any one were wrong on resume, would make the process behave differently
than if it had never been paused. That is the invariant a context switch must preserve:
*resume state = pause state, exactly.*

Second, each process has its own private view of memory — its **address space**, from
[[process]]. The CPU finds the right memory for the running process by consulting a small
hardware register that points at *that process's* memory map. Switching processes therefore
also means re-pointing this register at the incoming process's map, so that the same numeric
address now refers to the new process's private memory and not the old one's.

### The mechanism, step by step

When the kernel decides to switch from process A to process B, it performs, in order:

1. **Save A's registers** — every general register, plus the program counter and stack
   pointer — into A's record in the kernel's process table (the per-process slot from
   [[process]]). This is the "snapshot": A's complete context, set safely aside.
2. **Switch the memory map** — re-point the CPU's memory-map register from A's address space
   to B's. From this instant the CPU "sees" B's private memory.
3. **Load B's registers** from B's record — the mirror image of step 1. B's program counter
   and stack pointer come back exactly as they were when B was last paused.
4. **Resume** — the CPU, now holding B's program counter, fetches B's next instruction. B
   runs on, oblivious; from B's point of view, it simply executed its next instruction.

The kernel itself does the saving and loading, so during the switch the CPU is briefly running
*kernel* code rather than either process. A and B never touch each other's saved contexts —
the kernel is the trusted party that owns the process table and moves state in and out of it.

### What triggers a switch

A context switch is not something a process schedules for itself by name; it is provoked. Two
triggers dominate.

- **The timer interrupt (time-slicing).** The hardware is configured to fire an [[interrupt]]
  at a fixed cadence — say every few milliseconds. An [[interrupt]] forcibly diverts the CPU
  into the kernel. On each such tick the kernel gets a chance to ask "should someone else run now?" If a
  running [[process]] has used enough of its turn, the kernel switches it out for another
  runnable one. This is what stops a single compute-bound process from hogging the CPU forever:
  even if it never cooperates, the timer wrests control back. (The policy deciding *who* runs
  next is a separate matter, handled by the kernel's scheduler — its own topic; here we care
  only that once that choice is made, a context switch carries it out.)
- **Blocking on an event.** When a process asks the kernel for something that is not ready yet
  — data from a slow disk, bytes from the network — it cannot proceed, so it transitions to the
  **sleeping** state from [[process]] and *voluntarily* gives up the CPU. Rather than waste the
  core spinning, the kernel context-switches to some runnable process. Later, when the awaited
  event arrives, the sleeper is marked runnable again and will be switched back in on some
  future turn.

So a switch happens either because a process *gave up* the CPU (it blocked) or because the
kernel *took* it (the timer fired) — the involuntary case being why time-sharing is robust
against uncooperative programs.

### The why it isn't free — direct and indirect cost

The illusion costs real time, in two distinct ways, and understanding both is the point.

The **direct cost** is the visible work of the maneuver: copying a register set out to memory
and another set back in (steps 1 and 3), and re-pointing the memory-map register (step 2). This
is bounded, on the order of a microsecond.

The **indirect cost** is subtler and often larger. A CPU keeps recently used data and recently
used address-translations in small on-chip **caches** — fast memories that let it avoid going
all the way out to main memory. While process A was running, those caches filled with *A's*
data and *A's* address mappings. The moment you switch to B, B's data is not there: B's first
many memory accesses miss the cache and must crawl out to slow main memory, so B runs at a
fraction of full speed until the caches refill with B's footprint. Crucially, re-pointing the
memory-map register in step 2 means the cache of address-translations is now largely stale and
must be rebuilt for B's address space — a sizeable share of the indirect cost. None of this
shows up as an explicit step; it is paid silently as slowness right after every switch.

This is why switching *too often* backfires. If the kernel rotates among processes so
frequently that each gets only a sliver of CPU before being evicted, the system can spend more
time saving, restoring, and re-warming caches than doing the processes' actual work — a
self-defeating regime called **thrashing**, where the machine is busy but accomplishes little.
The existence of an indirect cost is the reason a sensible turn length is not "as short as
possible": a turn must be long enough to amortize the switch that precedes it.

### Worked instance: A is computing, the timer fires

Make it concrete with two processes and one CPU core. Process **A** is in the middle of a long
calculation — summing a large array — and at this instant its program counter points at the
instruction `add the next element to the running total`, its stack pointer is at some depth,
and one of its registers holds the partial sum, say `4096`. Process **B** has been sleeping,
waiting on the network; its data just arrived, so the kernel has marked B runnable.

1. **A runs.** The CPU executes A's instructions; the partial sum climbs: `4096`, `4097`, …
2. **Timer interrupt.** A few milliseconds in, the hardware timer fires and diverts the CPU
   into the kernel. A has had a full turn, and B is runnable, so the kernel decides to switch.
   Suppose A's partial sum register reads `5000` at this exact moment, and its program counter
   points at the very next `add` it had not yet executed.
3. **Save A.** The kernel writes A's registers — partial sum `5000`, that program counter, the
   stack pointer — into A's slot in the process table. A is now a faithful snapshot; the value
   `5000` is preserved, not lost.
4. **Switch map, load B.** The kernel re-points the memory-map register to B's address space,
   then loads B's saved registers — including B's own program counter, which points at the
   instruction *after* the network call B had blocked on.
5. **B runs.** The CPU resumes at B's program counter. B processes the bytes that just arrived.
   From B's perspective, its blocking call simply *returned* — it has no notion that, between
   making the call and getting the answer, an unrelated process A ran for milliseconds on the
   same core. For its first instructions B is slow (its data is not yet in the caches; A's was),
   then it speeds up as the caches refill — the indirect cost, observed.
6. **Back to A.** On a later timer tick (or when B blocks again), the kernel switches back: it
   saves B, restores A's snapshot — partial sum `5000`, that same program counter — and A
   resumes by executing exactly the `add` it was about to do, continuing `5001`, `5002`, …
   with no gap and no corruption. To A, no time and no other process ever intervened.

The non-degenerate details to notice: the saved partial sum `5000` is a *general* register
whose loss would silently wreck the answer (not just the program counter); the trigger here was
involuntary (the timer), so A never cooperated yet was still set aside cleanly; and B's
post-switch slowness is the indirect cost made visible. Had the kernel instead switched away
from A and back hundreds of times per millisecond, A's sum would still come out right — but the
machine would spend its effort on saves, restores, and cache re-warming rather than on adding
numbers. That is the line between time-sharing and thrashing.

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — section "Context switching — swapping one process for
  another" (the save/restore steps, the memory-map switch and its cache cost, the ~1–5 μs
  figure) and "When does a context switch happen?" (the timer-interrupt and blocking triggers).
