---
id: scheduler
title: Scheduler
summary: "A scheduler is the part of the kernel that answers one question, over and over, thousands of times a second: of all the tasks that are ready to run right now, which one should…"
type: concept
tags: [os/process]
prereqs: [context-switch, interrupt]
sources:
  - linux-internals-complete.html ("The scheduler's job", "Scheduler & context switching")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Scheduler

## Summary

A **scheduler** is the part of the kernel that answers one question, over and over,
thousands of times a second: *of all the tasks that are ready to run right now, which one
should this CPU run next, and for how long?* It does not itself swap tasks — that is the
job of a [[context-switch]], the maneuver that saves the outgoing task's state and loads
the incoming one's. The scheduler is the *decider*; the context switch is the *hands* that
carry the decision out. The decision matters because a CPU core can run only one task at an
instant, yet a system holds many tasks wanting to run, and only some of them are even
candidates: a task waiting on a slow disk or the network is **blocked** and must not be
chosen, while a task that wants the CPU now is **runnable** and competes for it. From the
runnable set the scheduler picks one and grants it a bounded turn — a **time slice** (or
*quantum*) — after which a timer [[interrupt]] hands control back so the scheduler can choose
again. In choosing, it juggles goals that pull against each other: **fairness** (no task
starves), **responsiveness** (interactive tasks react quickly), and **throughput** (don't
burn cycles switching when you could be computing). Linux's default scheduler is a *fair,
time-sharing* one: it tracks how much CPU each task has received and steers the next slice
toward whoever is most behind its fair share, so over time every task gets a roughly even
cut, biased by priority.

## Grounded explanation

### What the scheduler is — and what it is not

Recall from [[context-switch]] that one CPU core executes a single instruction stream at a
time, yet a running system has many tasks that all want to make progress, and the kernel
sustains the illusion of simultaneity by rotating among them — running one for a brief turn,
setting it aside, running another. That node showed *how* the setting-aside works: the save
of registers, the switch of the memory map, the load of the next task's state. But it
deliberately left a hole. When the timer fires — that is, when the hardware timer raises its
periodic [[interrupt]] and the kernel regains control — the kernel asks "should someone else
run now, and if so, *who*?", and something must answer. The scheduler is that answer.

So draw the line sharply. The **scheduler is a policy** — a decision procedure that selects,
from the tasks eligible to run, the one that should run next and the length of its turn. The
**[[context-switch]] is the mechanism** — once the scheduler has named a winner, the context
switch does the physical work of swapping the loser out and the winner in. They are
different layers of the same act: deciding versus doing. A node that explained only the
swapping would be teaching [[context-switch]] again; what is new here is the *choosing*.

A "task" throughout is just *the unit the scheduler schedules* — a runnable line of
execution the kernel can place on a CPU. (Linux happens to treat the threads inside a program
and standalone programs uniformly as such units, but that distinction belongs to its own
topic; here a task is simply a candidate for the CPU.)

### Runnable versus blocked — who is even a candidate

The scheduler never chooses from *all* tasks, only from the ones that can actually use the
CPU this instant. A task is **runnable** when it has work to do right now and is only waiting
for a turn on the core. A task is **blocked** (the *sleeping* state from [[context-switch]])
when it has asked for something not yet available — bytes from a disk, a packet from the
network — and literally cannot proceed until that arrives. A blocked task is *not a candidate*:
handing it the CPU would accomplish nothing, since its very next step is to wait. So the
scheduler considers only the **runnable set**, and that set is fluid. When a task blocks it
leaves the set (and yields the core early, via a [[context-switch]]); when its awaited event
arrives the kernel marks it runnable again and it rejoins, becoming a candidate once more.
Half of scheduling is simply tracking this membership: a CPU should never sit idle while a
runnable task waits, and never be spent on a task that can only wait.

### Why a scheduler is hard — three goals that fight

If there were only ever one runnable task, no policy would be needed; you would run it. The
difficulty is that there are usually several, and what makes one task happy makes another
suffer. The scheduler is balancing three goals that genuinely conflict:

- **Fairness** — every runnable task should make progress; none should starve while others
  hog the CPU. A naive "always run the same favorite" policy maximizes that favorite but
  freezes everyone else.
- **Responsiveness (low latency)** — an interactive task (a keystroke handler, a task waiting
  on the user) should get the CPU *soon* after it becomes runnable, so the system feels snappy.
  This argues for interrupting a long-running computation promptly to let the just-woken
  interactive task in.
- **Throughput** — the machine should spend its cycles doing the tasks' real work, not on the
  overhead of switching between them. Recall from [[context-switch]] that each switch costs
  real time, both the direct save/restore and the indirect cost of cold caches afterward. This
  argues *against* interrupting often.

Responsiveness and throughput pull in opposite directions, and that tension is the heart of
the design — addressed next.

### The central tension: how long is a slice?

The single most consequential knob is the **time slice**: how long a chosen task runs before
the scheduler is invoked to reconsider. It is set by the conflict just named.

Make slices **short** and the scheduler revisits its choice often, so a newly runnable
interactive task waits only a little before its turn — responsiveness is good. But every slice
boundary is a potential [[context-switch]], and that node established the price: short slices
mean many switches, and the indirect cost (cold caches, a flushed cache of address translations
that must rebuild for the incoming task) can grow until the machine spends more effort saving,
restoring, and re-warming than computing — the *thrashing* regime. Make slices **long** and the
opposite holds: few switches, low overhead, high throughput — but a task that becomes runnable
just after another's long slice begins must wait out that whole slice, so the system feels
laggy. There is no slice length that is best for everything; a fair time-sharing scheduler picks
one long enough to amortize the switch that precedes it (so throughput stays decent) yet short
enough that interactive tasks are not left waiting (so responsiveness stays acceptable) — a few
milliseconds, in practice. *Why not "as short as possible"?* Precisely because the
[[context-switch]] is not free; the slice must outlast the switch that sets it up.

### How a fair time-sharing scheduler decides

Fairness can't mean "everyone runs at once" — only one task fits on a core. It means *equal
shares of CPU time over a window*. The trick that delivers this is bookkeeping. The scheduler
keeps, for each runnable task, a running tally of how much CPU time it has already received.
Call it the task's accumulated time. The rule is then simple to state: **when it is time to
choose, pick the runnable task that is furthest behind its fair share** — the one with the
least accumulated time. That task runs for a slice; while it runs its tally climbs; soon it is
no longer the most-behind, and at the next decision point some other task is picked. Repeated,
this rule keeps everyone's accumulated time near-equal — which *is* fairness — without ever
needing to run two tasks literally at once.

**Priorities** bend the share deliberately. Each task carries a priority — on Linux, a "nice"
value, where being *nicer* means voluntarily claiming a smaller share. Instead of counting raw
CPU time, the scheduler counts *weighted* time: a high-priority task's tally climbs more slowly
per real second it runs, so it looks "behind" more often and is chosen more often, earning a
larger slice of the CPU — while the bookkeeping that guarantees fairness still operates,
now over weighted shares. (Linux's current implementation refines the raw "least accumulated
time" pick into picking, among tasks that are behind their fair share — the *eligible* ones —
the one whose requested slice is due soonest, which sharpens latency for interactive tasks; the
governing idea remains weighted fair sharing.)

Crucially, a task that **blocks early gives its slice back**. If a task is handed a slice but,
partway through, makes a request that blocks — it asks to read a file and the data isn't in
memory — it cannot use the rest of its turn. It transitions to blocked, leaves the runnable
set, and yields the core immediately through a [[context-switch]]; the scheduler picks again
right then rather than letting the core idle. This is why interactive and I/O-heavy tasks
coexist gracefully with compute-heavy ones: they spend most of their time blocked (waiting on
input), barely accumulate CPU time, and so are almost always "most behind" and get picked
promptly the instant they wake — exactly the responsiveness goal, falling out of the same
fair-share bookkeeping.

### Worked instance: three CPU-bound tasks on one core, then one blocks

Take one CPU core and three runnable tasks — call them **P**, **Q**, **R** — each a tight
compute loop (say each is summing a huge array, so each *always* wants the CPU and never blocks
on its own). Equal priority. Let the time slice be a round 10 ms, and start every tally at 0 ms
of accumulated CPU time.

1. **First decisions.** All three are tied at 0 ms accumulated, so the scheduler breaks the tie
   (say in order) and runs **P** for a 10 ms slice. P's tally → 10 ms; Q and R still 0. Next
   decision: Q and R are most-behind at 0; run **Q** 10 ms → tally 10. Then **R** 10 ms →
   tally 10. Now P=Q=R=10 ms.
2. **Round-robin emerges.** The pattern repeats: P → 20, Q → 20, R → 20, and so on. Over any
   window each of the three accumulates the same CPU time, so each receives **~1/3 of the
   core** — fairness, delivered by the "run the most-behind" rule, not by any explicit
   "one-third" instruction. Each slice boundary is a [[context-switch]] (save the outgoing
   task, load the next), so this fairness is bought with switching overhead — bearable because
   a 10 ms slice dwarfs the ~microsecond switch beside it.
3. **One task blocks on disk.** Now suppose, 4 ms into one of **R**'s slices, R's loop reaches
   a point where it must read a chunk from disk that isn't cached. R issues the read; the data
   is not ready; **R blocks**. It has used only 4 ms of its 10 ms slice. Per the early-block
   rule, R immediately transitions to blocked, *leaves the runnable set*, and yields the core
   through a [[context-switch]] right now — the kernel does not let the core idle for R's
   remaining 6 ms.
4. **The other two split the CPU.** With R out of the runnable set, the scheduler chooses only
   between **P** and **Q**. They alternate 10 ms slices, so each now gets **~1/2 of the core** —
   a bigger share than before, simply because there is one fewer candidate. R, meanwhile,
   accumulates *no* CPU time while it waits; its tally is frozen.
5. **R wakes.** Eventually the disk delivers R's data. The kernel marks R **runnable** again,
   and R rejoins the candidate set. Because R's tally stopped climbing while it slept, it is now
   the *most behind* of the three — so at the very next decision the scheduler picks **R**, and
   a [[context-switch]] brings it back in to resume right where its read returned. The three
   then settle back toward the ~1/3-each round-robin.

The non-degenerate things this instance shows, that a simpler one would hide: the runnable set
*changing size* (3 → 2 → 3) and the shares automatically re-dividing with it (1/3 → 1/2 → 1/3);
a slice ending **early and involuntarily by blocking** (4 ms of 10), not just by the timer
expiring; and the fair-share tally doubling as the responsiveness mechanism — a freshly woken
task is favored *because* it fell behind while blocked, with no separate "boost interactive
tasks" rule needed. Had all three merely run to the timer forever, the blocking branch and the
wake-up-favoring would never fire, and the example would teach only round-robin, not what a
scheduler is for.

(Some tasks need a stricter guarantee than "a fair share eventually" — a deadline that must be
met, such as audio that will glitch if its task is late. Handling those is *real-time
scheduling*, a different policy with its own topic; the fair time-sharing scheduler described
here is the general-purpose default.)

## Prerequisites

- [[context-switch]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "The scheduler's job" (picking who runs next
  thousands of times a second; weighted fair sharing via per-task accumulated runtime; the
  eligible/most-behind selection and earliest-deadline refinement; runnable tasks as the
  candidate set; the scheduler runs every few milliseconds or when a task blocks) and
  "Scheduler & context switching" (the timer-interrupt, blocking, and wake-up triggers, and
  the switch cost that makes frequent switching hurt — the throughput side of the slice-length
  tension).
