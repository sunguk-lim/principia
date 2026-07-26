---
id: fair-scheduler
title: Fair Scheduler (CFS/EEVDF)
summary: The fair scheduler is the specific policy that Linux's scheduler uses to answer the recurring question "which runnable task runs next?" — and the structure that makes the answer…
type: concept
tags: [os/process]
prereqs: [scheduler, binary-search-tree]
sources:
  - linux-internals-complete.html ("EEVDF scheduler" under-the-hood; glossary CFS/EEVDF; "Why Linux can't guarantee this")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Fair Scheduler (CFS/EEVDF)

## Summary

The **fair scheduler** is the specific *policy* that Linux's [[scheduler]] uses to answer the
recurring question "which runnable task runs next?" — and the structure that makes the answer
fast. Its one governing idea is to give every task an equal share of the CPU over time, bent only
by priority. To do that it stores, for each task, a single number called **virtual runtime**
(*vruntime*): the amount of CPU time the task has consumed, but *weighted* so that a
higher-priority task's number climbs more slowly per real second it runs. The selection rule is
then a one-liner: run the runnable task with the **smallest** vruntime — the one that has had the
least weighted CPU so far. Because every task's vruntime keeps climbing only while it actually
runs, repeatedly picking the smallest drives all of them up together, so each of *N* equal tasks
tends toward 1/*N* of the CPU, while a high-priority task — whose number rises slower — is picked
more often and gets a larger cut. The first widely used version, **CFS** (Completely Fair
Scheduler, 2007–2023), kept the runnable tasks sorted in a balanced binary tree keyed by vruntime
so "pick the smallest" was cheap. Its successor **EEVDF** (Earliest Eligible Virtual Deadline
First, 2023) keeps the weighted-fairness core but adds a second test so a task that needs to run
*soon* is also served promptly, not merely *eventually*.

## Grounded explanation

### What this node adds on top of [[scheduler]]

The [[scheduler]] node established the *shape* of the problem: of all **runnable** tasks (those
ready to use the CPU right now, as opposed to **blocked** ones waiting on disk or network), the
kernel must repeatedly pick one and grant it a bounded turn (a **time slice**), and Linux's
default does so *fairly* — steering each next slice toward whoever is most behind its fair share.
That node deliberately stayed at the level of "track accumulated CPU time, pick the most-behind."

This node is about the concrete machinery that *is* Linux's fair scheduler: the exact quantity it
tracks (vruntime, and how priority weights it), the exact selection rule, the **data structure**
that makes selecting cheap even with thousands of runnable tasks, and the one refinement (EEVDF)
that the bare rule needs to also bound *how long* a task waits. The defining contribution is not
"scheduling is fair" — that is the [[scheduler]] — but *this particular invariant and structure*
that deliver fairness mechanically.

### Virtual runtime: one number per task

A task's **virtual runtime** (*vruntime*) is the heart of the policy. Start with the plain version:
ignoring priority, a task's vruntime is just the total real CPU time it has been given so far,
measured in nanoseconds and accumulating only while the task is actually running on a core. A task
that has run for 30 ms total has a larger vruntime than one that has run for 10 ms; a **blocked**
task's vruntime is frozen, because it is consuming no CPU.

The whole point of the number is to be *comparable across tasks*: a small vruntime means "this
task has had little CPU lately," a large one means "this task has already had a lot." That is
exactly the "most behind / least behind" notion the [[scheduler]] described, now made into a
single stored integer per task instead of an abstract idea.

### Priority via weighting: how `nice` bends the share

Pure "least CPU time so far" would give every task an *identical* share. Real systems want some
tasks to get more. Linux expresses priority with a value called **nice**, an integer (on Linux,
from −20 to +19) where a *higher* nice value means the task is "nicer" — it voluntarily claims a
*smaller* share — and a *lower* (even negative) nice value means higher priority and a larger
share. The name is the trap: nice = −5 is *high* priority, not low.

Nice does not change the selection rule; it changes how fast vruntime *climbs*. Each task has a
**weight** derived from its nice value — higher priority means higher weight. When a task runs for
some real time Δ*t*, its vruntime advances not by Δ*t* but by Δ*t* scaled *inversely* by its
weight:

> vruntime increment = (real time run) × (a fixed reference weight ÷ this task's weight)

So a high-weight (high-priority, low-nice) task's vruntime climbs *more slowly* per real second
than a normal task's. The consequence is the whole trick: because the scheduler always picks the
*smallest* vruntime, and a high-priority task's vruntime lags behind, that task keeps looking
"most behind" and so gets picked more often — it earns a larger fraction of the CPU. A
low-priority (high-nice) task's vruntime races ahead per real second, so it quickly stops being
the smallest and is picked less. One mechanism — reweighting how vruntime advances — turns the
single fairness rule into a tunable priority knob, with no separate "give priority tasks extra
turns" logic.

### The selection rule and why it produces fairness

The rule, stated fully: **at every decision point, run the runnable task with the smallest
vruntime.** A decision point is when the current slice ends (a timer interrupt returns control to
the kernel) or when the running task **blocks** or otherwise yields the CPU early — the same
triggers the [[scheduler]] node described.

Why does repeatedly running the smallest produce *equal shares*? Because running a task is the
only thing that *raises* its vruntime. Pick the smallest, let it run a slice, and its vruntime
rises until it is no longer the smallest; now some other task is smallest and gets picked. The
rule is self-correcting: any task that falls behind (small vruntime) is immediately favored, and
any task that gets ahead (large vruntime) is passed over until the others catch up. Left running,
all the runnable tasks' vruntimes stay clustered together and climb in near-lockstep — and "all
tasks have had nearly equal weighted CPU time" *is* the definition of weighted fairness. The
fairness is not commanded ("give each 1/*N*"); it *emerges* from the local rule of always serving
the most-behind.

A subtlety the [[scheduler]] node already noted, now grounded: a task that was **blocked** for a
while had its vruntime *frozen*, so when it wakes it is far smaller than everyone else's and would
monopolize the CPU to "catch up." So on wakeup the kernel does not restore that stale tiny
vruntime; it sets the woken task's vruntime to roughly the current minimum among runnable tasks.
The task still rejoins as one of the smallest (so it is served *promptly* — the responsiveness the
[[scheduler]] node wanted) but it does not get to claw back all the CPU it missed while asleep.

### The data structure: a red-black tree keyed by vruntime

"Run the smallest vruntime" is easy with three tasks and a disaster with three thousand if you
rescan the whole runnable set every few milliseconds. The fair scheduler avoids the rescan by
keeping the runnable tasks in a **red-black tree** keyed by vruntime.

A red-black tree is a *self-balancing [[binary-search-tree]]*: a binary tree (each node has up to
two children) ordered so that everything in a node's left subtree sorts *before* it and everything
in the right sorts *after* — here, "sorts before" means "smaller vruntime." The BST property
(every key in a node's left branch is smaller, every key in the right branch is larger) is exactly
what guarantees that the **smallest vruntime is always the leftmost node** — follow left children
until you can't. "Self-balancing" means the tree enforces colour rules (each node is tagged red or
black, with constraints on how they may stack) that keep it from degenerating into a long lopsided
chain — the degenerate worst-case a plain BST can fall into — and this guarantees its height stays
proportional to log *n* for *n* nodes. So the scheduler's "pick the smallest" costs a single walk
down one side, and in practice the kernel even *caches* a pointer to that leftmost node so the
pick is effectively instant. Inserting a newly runnable task at its correct sorted position, and
removing one that blocks, each touch only a path from root to leaf and a few rotations to
rebalance — **O(log n)** work, the same guarantee a balanced BST buys for any ordered data. That
logarithmic cost (rather than linear in the number of tasks) is what lets the fair scheduler stay
cheap on a busy server, and it is the reason the policy is built around a tree rather than a plain
list.

### CFS versus EEVDF: adding a latency bound

**CFS — Completely Fair Scheduler** (Linux's default 2007–2023) is exactly the policy above:
vruntime in a red-black tree, always run the leftmost (smallest-vruntime) task. It is *fair* in
the long run, but "you will get your share *eventually*" is not the same as "you will run *soon*."
A task that just woke and only needs a tiny slice to handle, say, a keystroke could still sit
behind others under pure lowest-vruntime ordering, hurting latency.

**EEVDF — Earliest Eligible Virtual Deadline First** (Linux's default since 2023) keeps the
weighted-vruntime fairness core but splits selection into two tests. First, **eligibility**: from
each task's vruntime the kernel derives a **lag** — how far behind its fair share the task
currently is. A task whose lag is non-negative (it is at or behind its fair share) is *eligible*;
a task that has already run ahead of its share is temporarily *ineligible* and skipped, so no task
can race ahead of fair. Second, among the *eligible* tasks, EEVDF does not just take the smallest
vruntime; it gives each task a **virtual deadline** computed from the slice length that task
*requested* (a task asking for a short slice gets a nearer deadline) and runs the eligible task
with the **earliest** virtual deadline. The effect: fairness is still enforced (only eligible,
not-ahead tasks can run), but among those, the one that needs to run soonest goes first — so
latency-sensitive tasks are served promptly *by construction*, not by a bolted-on heuristic. The
runnable tasks still live in a red-black tree (now augmented to also track eligibility and virtual
deadlines), so selection stays O(log n).

### Worked instance: three tasks, then a priority bump

Take one CPU core and three runnable, CPU-bound tasks **A**, **B**, **C** — each a tight compute
loop that always wants the CPU and never blocks. Equal nice (so equal weight), and start all three
at vruntime 0. Let each slice be 10 ms. To keep the arithmetic plain, use the equal-weight case
where vruntime advances 1-for-1 with real time (the reference weight equals each task's weight, so
the scaling factor is exactly 1).

1. **Equal-weight phase.** All three are tied at vruntime 0, i.e. all are the leftmost-equivalent.
   Break the tie in order: run **A** for 10 ms → A's vruntime = 10; B and C still 0. The tree now
   has B and C (both 0) as the smallest; run **B** 10 ms → 10; then **C** 10 ms → 10. Now A = B =
   C = 10. The pattern repeats: A → 20, B → 20, C → 20, and so on. Each is picked exactly as often
   as the others, so each gets **~1/3 of the core** — fairness emerging from "always run the
   smallest vruntime," with no explicit one-third anywhere.

2. **Give A higher priority.** Now set **A**'s nice to −5 (higher priority → higher weight). The
   rule does not change, but A's vruntime now advances *slower* than real time. Suppose A's weight
   makes its vruntime climb at half speed: when A runs a 10 ms slice, its vruntime rises by only 5
   (= 10 ms × reference-weight ÷ A's-larger-weight), whereas B and C still rise by the full 10 per
   slice. Trace it from the tied state A = B = C = 0:
   - Run A 10 ms → A = 5 (half speed); B = C = 0.
   - Smallest are B, C at 0. Run B → 10. Run C → 10. Now A = 5, B = 10, C = 10.
   - Smallest is A at 5 again — A is picked **again** before B or C come round. Run A → 10. Now
     A = 10, B = 10, C = 10.
   - And so on: in the time B and C each take one slice, A takes *two*, because its vruntime keeps
     sinking back to the bottom of the tree fastest.

   So A ends up running roughly twice as often as B or C — it earns a **larger share** of the
   core, while B and C split the rest evenly. Nothing in the selection rule said "favor A"; A's
   higher weight simply made its vruntime climb slower, so A keeps re-appearing as the smallest.
   This is the non-degenerate case worth seeing: with the half-speed weight, the scaling factor is
   *not* 1, so the example actually exercises the priority mechanism rather than collapsing to the
   plain equal-share round-robin of step 1.

If one of these tasks blocked (asked for disk data not yet present), it would leave the tree and
yield the core early, exactly as the [[scheduler]] node traced; on waking, its vruntime would be
reset up to the current minimum so it rejoins near the bottom and is served promptly without
hogging the CPU to catch up.

## Prerequisites

- [[scheduler]]
- [[binary-search-tree]]

## Sources

- `linux-internals-complete.html` — the "EEVDF scheduler" *Under the hood* panel (vruntime =
  CPU time weighted by priority; lag derived from vruntime; eligibility test; earliest virtual
  deadline from the requested slice; CFS's predecessor rule of "lowest vruntime"; the augmented
  red-black tree with O(log n) insert/remove and the cached next pick; the scheduler runs every
  few ms or when a task blocks), the glossary entries for **CFS** (Completely Fair Scheduler,
  Linux's default 2007–2023) and **EEVDF** (Earliest Eligible Virtual Deadline First, default
  since kernel 6.6 in 2023, picking the earliest virtual deadline weighted by nice value), and
  the "Why Linux can't guarantee this" panel (EEVDF gives a fair share, reconsidering each tick —
  the fair-not-strict-priority character of the policy).
