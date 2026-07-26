---
id: simt
title: SIMT
summary: SIMT stands for Single Instruction, Multiple Threads, and it is the name for the GPU's execution model — the one the warp node described mechanically but never had to name.
type: concept
tags: [gpu]
prereqs: [warp]
sources:
  - "linux-internals-complete.html — Phase 7: Where SIMT lives — the rules at each level; SIMT is at the warp level, not the SM level; SIMD vs SIMT — both lockstep, differently managed"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# SIMT

## Summary

**SIMT** stands for **Single Instruction, Multiple Threads**, and it is the name for the
GPU's execution model — the one the [[warp]] node described mechanically but never had to
name. The model is exactly this: the hardware issues **one** instruction to a whole [[warp]]
of 32 threads, and all 32 execute that same instruction on the same cycle, each working on
its **own** data in its **own** registers. The defining claim, and the thing this node exists
to nail down, is that *SIMT operates per-warp* — the lockstep group is the [[warp]], not
anything larger. Two different warps are completely independent; they can be at different
instructions, on different branches, doing different jobs in the same cycle. The other half of
SIMT is how you *write* code for it: you write ordinary single-thread code — "here is what
**one** thread does" — and the hardware does the bundling into lockstep [[warp]]s for you. This
is the whole payoff. You get to think one-thread-at-a-time, which is simple, while the hardware
quietly reclaims the efficiency of running 32 of them off a single instruction fetch. And
because each thread keeps its own registers and its own position in the program, threads in a
[[warp]] *can* take different branches; the hardware copes by masking, which a stricter form of
this idea cannot do.

![Static 4-row cycle grid of one warp's 32 lanes under SIMT: STEP 1/4 a shared ADD executes on all 32 lanes (inputs a[i]=10·(i+1), b[i]=i+1, results 11…198 drawn per lane); a gold mask-set band marks the i<16 divergence; STEP 2/4 branch pass A runs lanes 0–15 while 16–31 sit masked/dashed; STEP 3/4 masks flip and lanes 16–31 run the SUB arm (153, 162, …) while 0–15 hold; a gold masks-cleared band reconverges; STEP 4/4 all 32 lanes bright again. A control-structure sidebar shows the one instruction stream forking through the branch diamond and reconverging; captions state the retire-together invariant and the 2-cycle divergence cost.|960](simt.svg)

## Grounded explanation

### What SIMT is, and the term it names

The [[warp]] node already built the machine. It explained that a [[warp]] is 32 threads run in
**lockstep** — each cycle the hardware issues one instruction and all 32 threads execute that
same instruction at the same point in the program, each on its own data — and it even noted, in
passing, that "the industry name for this is *SIMT*, but the name is not needed to understand
it." This node is that name made into the concept. **SIMT — Single Instruction, Multiple
Threads — is the execution model whose unit is the lockstep [[warp]].** "Single Instruction"
is the one instruction the hardware issues per cycle; "Multiple Threads" is the 32 threads of
the [[warp]] that all run it at once. So SIMT is not a new mechanism on top of the [[warp]]; it
*is* the [[warp]]'s behavior, named and stated as a general model so we can reason about it and
contrast it with other ways of doing parallel work.

Before going further, one term needs defining because the contrast below leans on it. A
**thread**, here, is one independent stream of work: it executes instructions one after
another, has its own set of register values, and has its own **program counter** — the marker
that records which instruction it is currently at. The phrase "each thread has its own program
counter" will do real work shortly, so hold onto it: it means each thread independently tracks
where *it* is in the code.

### The defining insight: SIMT is at the warp level, not above it

The single most important thing to get right about SIMT — the source states it as a heading,
"SIMT is at the warp level, not the SM level" — is the *scope* of the lockstep. It is tempting
to imagine that a whole chip, or a whole large cluster of lanes, marches in lockstep on one
instruction. That is false, and the falseness is the point. The lockstep group is exactly **one
[[warp]]** — 32 threads — and no larger. A [[warp]] is a SIMT group; the larger structure that
*hosts* many warps is **not** a SIMT group. It is a host for many concurrent SIMT groups, each
of which is independently somewhere different in the program.

Why does this matter so much? Because it is the same fact that made the [[warp]] node's
hardware fast, now stated as a property of the model. Recall from [[warp]] that the scheduler
keeps many warps resident and, each cycle, picks *one* [[warp]] whose next instruction is
ready and issues it; when a [[warp]] stalls waiting on slow memory, the scheduler switches to a
*different* ready [[warp]] for free. That trick only works *because* warps are independent — at
different points in the program, on different instructions. If everything moved in one giant
lockstep, there would be no "other ready [[warp]]" to switch to when one stalled, and the
latency-hiding would collapse. So "SIMT is per-[[warp]]" is not pedantry; it is the precise
reason the hardware can hide latency. Lockstep is tight *inside* a [[warp]] and absent
*between* warps, and that combination is what buys both efficiency and flexibility.

This gives a clean rule for "what must agree and what may differ," which is worth stating
plainly. Within a single [[warp]], the **instruction** issued each cycle must be the same for
all 32 threads — that is what lockstep means; only the **data** each thread operates on may
differ. Across different warps, *nothing* must agree: two warps can be on different
instructions, different branches, different jobs entirely. And a single thread, considered
alone, is under no constraint at all — its program counter, its registers, its locals are
entirely its own. SIMT is the model that holds all three of these levels together at once.

### The contrast that defines SIMT: writing scalar code, not vector code

SIMT is best understood against the older model it improved on, which lives on CPUs and is
called **SIMD** — *Single Instruction, Multiple Data*. (SIMD is not a prerequisite concept here
and gets no node; it is described in plain prose only, as a foil.) SIMD and SIMT are cousins:
both run **one instruction across many lanes in the same cycle**. The difference — the thing
that makes SIMT its own concept — is *who manages the parallelism and what the programmer
writes.*

In classic SIMD, the parallelism is explicit in the instruction set and in the programmer's
hands. A single thread issues one **vector instruction** that operates on one wide **vector
register** — a register holding a fixed number of values side by side, say 16 floating-point
numbers packed together. The programmer must know that width, lay the data out to fill the
vector, and manage by hand any masks needed when not all positions should participate. The
mental unit is "one instruction operating on a packed vector of 16."

In SIMT, the programmer writes none of that. You write **ordinary scalar per-thread code** —
code phrased entirely as "this is what *one* thread does," with no vector register, no declared
width, no packed lanes in sight. The hardware then automatically groups threads into lockstep
[[warp]]s of 32 and issues one instruction across all 32 at runtime. The width (32) is the
[[warp]] size, fixed in hardware, never written by the programmer. So the two models reach the
same place — one instruction, many lanes, same cycle — from opposite directions: SIMD makes the
programmer build the vector explicitly; SIMT lets the programmer pretend there is just one
thread and assembles the vector behind the scenes.

### The why: divergence is what scalar-per-thread buys you

The contrast is not just stylistic. It produces a real capability gap, and it is the deepest
reason SIMT is worth naming as its own model. Because each SIMT thread has **its own program
counter and its own registers** — the very property defined above — the 32 threads of a [[warp]]
*are allowed to want different next instructions*. They can hit an `if/else` where some go one
way and the rest the other. This is **divergence**, and the [[warp]] node already showed how the
hardware survives it: it cannot issue two instructions at once, so it **serializes** the two
paths and uses **masking** — running the first path with the threads that chose it switched on
and the others switched off (fed the instruction but discarding the result), then flipping the
masks for the second path. The justifying invariant, from [[warp]], is that the 32 threads
always retire instructions together as one [[warp]]; lockstep is preserved by letting some of
the lockstepped instructions be no-ops for the masked-off threads. As that node put it: SIMT is
"lockstep, but with per-lane masks."

Here is the punchline that makes SIMT a distinct, better model and not just a rebranding of
SIMD. *Pure SIMD has no per-lane program counter*, so it has no clean notion of a lane "being
somewhere else in the program"; a SIMD vector instruction simply applies to the packed register
as a whole. Branching that genuinely sends different lanes down different code paths is exactly
what SIMD is bad at. SIMT, by giving every thread its own program counter, makes per-thread
branching a first-class thing the hardware *handles for you* — at a cost (the serialization),
but it handles it. So SIMT delivers the best of both: the **programming simplicity** of writing
independent scalar threads that may branch however they like, fused with the **execution
efficiency** of running 32 of them off a single instruction fetch. That fusion — think
one-thread-at-a-time, run 32-in-lockstep — is the entire reason the model exists and the entire
reason it earns a name.

### Worked instance: one scalar line becomes 32 results, then a branch splits the warp

Take the most ordinary kernel line a programmer could write, and watch SIMT turn it into
parallel execution. The programmer writes, *for a single thread*:

> `c[i] = a[i] + b[i];`

There is no vector register here, no width, no lanes — it reads as if exactly one thread will
load element `i` of arrays `a` and `b`, add them, and store the result into `c[i]`. The
variable `i` is the thread's own index — its identity, different for each thread. This is
scalar per-thread code, the SIMT way of writing it. The programmer is *not* thinking about 32
of anything.

Now watch what the hardware does at runtime. It bundles 32 of these threads into one [[warp]]
and hands them indices `i = 0, 1, 2, …, 31`. The single line above compiles to (among others)
one **ADD** instruction. On one cycle, the hardware issues that **one** ADD to the whole
[[warp]]. All 32 threads execute it on the same cycle — but thread 0 adds `a[0] + b[0]`, thread
1 adds `a[1] + b[1]`, thread 17 adds `a[17] + b[17]`, and so on through thread 31. **One
instruction issued, 32 results produced, zero lanes idle.** Concretely, if `a = [10, 20, 30,
…]` and `b = [1, 2, 3, …]`, then in that single ADD cycle `c[0]` becomes `11`, `c[1]` becomes
`22`, `c[2]` becomes `33`, … each thread computing its own sum from its own `i`. That is SIMT
operating at its design point: scalar code in, lockstep parallel execution out, the width
supplied for free by the [[warp]].

Now force the threads to disagree, so the per-thread (not per-vector) nature of SIMT shows
itself — this is the non-degenerate part the aligned add alone would hide. Add a branch keyed
on the thread's own index:

> `if (i < 16)  c[i] = a[i] + b[i];  else  c[i] = a[i] - b[i];`

Threads 0–15 want the ADD; threads 16–31 want the SUBTRACT. In SIMD this would be the
programmer's problem to mask by hand; in SIMT the hardware handles it via divergence. It issues
the ADD with threads 0–15 switched **on** and threads 16–31 **masked off** — those 16 are fed
the ADD but discard it, idle for that pass. Then it flips the masks and issues the SUBTRACT
with threads 16–31 on and 0–15 off. Two serial passes, half the [[warp]] idle in each, so the
branched region costs about twice an undivided one — the cost from [[warp]]. The reason this is
even *possible*, rather than illegal, is the SIMT property at the center of this node: each
thread has its own program counter, so the hardware can legitimately treat threads 0–15 and
16–31 as being at different instructions and run them in turn. That is precisely the capability
pure SIMD lacks — and it is why SIMT, not SIMD, is the model the GPU is built around.

## Prerequisites

- [[warp]]

## Sources

- linux-internals-complete.html — *Where SIMT lives — the rules at each level* and its lead
  *SIMT is at the warp level, not the SM level* (a warp of 32 threads is the SIMT unit; all 32
  run the same instruction simultaneously on different data; the SM is a host for many
  concurrent SIMT groups, not a SIMT group itself, and that independence is why latency hiding
  works; the per-level table of what must be the same — the current instruction within a warp —
  versus what can differ — the data, and a thread's PC/registers/locals).
- linux-internals-complete.html — *SIMD vs SIMT — both lockstep, differently managed* (both run
  one instruction across many lanes per cycle; in SIMD one thread issues a wide vector
  instruction over a fixed-width register and manages masks/layout by hand; in SIMT you write
  scalar per-thread code and the hardware bundles 32 threads into a warp, issuing one
  instruction across all 32 and handling divergence for you; divergence serialized with masking).
