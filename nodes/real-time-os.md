---
id: real-time-os
title: Real-Time OS
summary: A real-time operating system (RTOS) is an operating system that guarantees a task will run within a fixed, predictable amount of time after the event that needs it — every single…
type: concept
tags: [os/virtualization]
prereqs: [scheduler, interrupt]
sources:
  - linux-internals-complete.html ("Real-time doesn't mean fast", "How an RTOS scheduler differs", "Where real-time matters", "PREEMPT_RT")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Real-Time OS

## Summary

A **real-time operating system** (RTOS) is an operating system that *guarantees* a task
will run within a fixed, predictable amount of time after the event that needs it —
**every single time**, not on average. The defining word is **deadline**: a result that is
correct but arrives late is counted as a **failure**, exactly as if it were wrong. So the
property an RTOS sells is not speed but **determinism** — a *bounded worst-case* delay you
can name in advance ("never more than 50 microseconds") and rely on. This is a sharp break
from the ordinary [[scheduler]], which optimizes the *average* — fairness across tasks and
total work done — and in exchange lets any one task wait an *unbounded* time when the
machine is busy. An RTOS replaces that fair [[scheduler]] with one that obeys **strict
priority**: the highest-priority ready task runs essentially immediately, preempting
anything of lower priority, so the task that has a deadline is never left waiting behind
work that does not. The price is real: an RTOS often does *less* total work per second than
a general-purpose system. It trades throughput for a promise about timing.

## Grounded explanation

### "Real-time" does not mean "fast"

The phrase misleads almost everyone on first contact, so fix it before anything else.
**Real-time** means **guaranteed response time**: when some event happens — a sensor
reading arrives, a timer ticks — the system promises to respond within a fixed, known
deadline, say 10 microseconds. The promise is not "usually 10 microseconds" or "10
microseconds on average." It is **every time, no exceptions**. A system can be blazingly
fast on average and still *not* be real-time, because "fast on average" permits the
occasional slow case, and in a real-time setting that one slow case is a failure.

That last point is the whole concept in one sentence: **a correct answer delivered after
its deadline is a failure.** If a controller is supposed to nudge a motor every millisecond
and it computes a perfect correction but delivers it 5 milliseconds late, the motor has
already overshot — the lateness *is* the bug, even though the arithmetic was right. So an
RTOS is judged not by how quickly it usually responds but by the *worst* response it can
ever produce. Designers care about one number: the **worst-case latency** — the longest
possible gap between the triggering event and the response. An RTOS is precisely an OS that
makes that worst-case number small *and* guaranteed, rather than merely making the common
case small.

### Hard versus soft: how bad is a missed deadline?

Not every deadline carries the same stakes, and the field splits on this.

- **Hard real-time** — missing a deadline is **catastrophic**: someone is hurt, or equipment
  is destroyed. An airbag that fires a few milliseconds late, an anti-lock brake that reacts
  too slowly, a pacemaker that does not fire at the right instant, motor control that lets a
  robot arm overshoot into a wall. Here the deadline is *not negotiable* — the system is only
  correct if it meets it **always**.
- **Soft real-time** — missing a deadline **degrades quality** but is survivable. Audio and
  video are the standard cases: if the task that feeds the sound card is occasionally late, you
  hear a click or a dropout, which is annoying but not dangerous, and the next sample is fine.
  Misses should be rare, but the system does not fail catastrophically when one happens.

The distinction matters because it sets *how strong* the guarantee must be. Hard real-time
demands a provable worst-case bound on every relevant path; soft real-time can tolerate a
statistical "almost always," which is much cheaper to provide.

### Why an ordinary scheduler cannot promise this

Recall what the general-purpose [[scheduler]] is built to do. It is a **fair, time-sharing**
policy: it tracks how much CPU time each runnable task has received and steers the next
**time slice** — the bounded turn a task gets before the scheduler reconsiders — toward
whichever task is most behind its fair share. Over a window, every task gets a roughly even
cut. That is exactly the right design for a server or a desktop, where the goal is that no
task starves and the machine stays busy doing useful work. But notice what it *refuses* to
promise: it never says "*this particular* task will run within *N* microseconds." Its
guarantee is about long-run averages, not about any single deadline. Three properties of
such a system each inject delay that has **no fixed upper bound**:

1. **The policy is fairness, not urgency.** When a task that urgently needs the CPU becomes
   runnable, the fair [[scheduler]] does not drop everything for it. It weighs that task's
   accumulated CPU time against everyone else's and may decide some *other* task is more
   behind and should run first. Worse, on a general-purpose system the scheduler typically
   only reconsiders its choice at periodic **timer ticks** — every one to ten milliseconds.
   So an urgent task that becomes ready just after a tick can wait the better part of a tick
   period before it is even *considered*. For a 1-millisecond deadline, a delay of "up to 10
   milliseconds, sometimes" is fatal.

2. **The kernel disables interrupts in places.** To protect its own shared data while
   updating it, the kernel sometimes briefly turns off the very [[interrupt]]s that would
   signal an urgent external event. During such a window the event sits unprocessed. In a
   large general-purpose kernel these protected sections are many and their durations are not
   individually bounded — one might do a quick update, the next might allocate memory or touch
   something slow — so the blackout can last an *unknown* amount of time.

3. **Background housekeeping intrudes unpredictably.** A big kernel is always doing other
   work — reclaiming memory, flushing data to disk, resolving contention for locks. Any of
   these can stall your task at an unpredictable moment, which is why the *same* operation
   can take 5 microseconds one time and 5 milliseconds the next.

None of these is a *bug* — they are the cost of a feature-rich system optimized for average
throughput. But together they mean the worst-case latency is effectively unbounded: you
cannot write down a number and prove the system will always beat it. That is precisely the
guarantee a hard real-time application needs and that an ordinary [[scheduler]] structurally
cannot give.

### What an RTOS does instead

An RTOS attacks each of those three sources of delay directly, and the heart of it is a
different [[scheduler]] policy.

**Strict priority preemption replaces fairness.** Every task is assigned a fixed priority.
The rule is absolute and simple: **the highest-priority runnable task runs, period.** There
is no fair-share bookkeeping, no notion of "you've had your turn, let someone else go." The
moment a higher-priority task becomes ready, the RTOS **preempts** — immediately performs the
switch away from whatever lower-priority task is running and into the urgent one — without
waiting for the next timer tick. "Higher priority always beats lower priority, always" is the
entire policy. This is what makes the worst-case bound *possible*: the task with the deadline
is given top priority, and then, by construction, nothing lower can ever delay it. Fairness is
*deliberately abandoned* — a low-priority task on an RTOS genuinely can be starved for as long
as a higher-priority task wants the CPU, and that is considered correct behavior, because the
high-priority task is the one with the deadline.

**Interrupt-disabled windows are kept tiny and bounded.** Because an urgent event reaches the
system as an [[interrupt]] — a hardware signal that preempts the CPU and forces it into a kernel
handler — the longest stretch during which interrupts are turned off directly caps how late a
response can be. So an RTOS kernel is written so that every interrupt-disabled
section is short and has a *measured, known* worst-case length — a handful of instructions, not
an open-ended "and maybe something slow." The kernel developers measure these paths and publish
the bound. This is what converts "unknown blackout" into "never blocked for more than X
microseconds."

**The kernel is kept tiny, so there are fewer places for delay to hide.** A general-purpose
kernel is enormous — tens of millions of lines, with caches, swapping, filesystems, networking,
firewalling — and any of that machinery can introduce a surprise stall. A typical RTOS kernel
is minute by comparison: essentially a [[scheduler]], simple memory allocation, and interrupt
handling, and little else. (Small embedded RTOS kernels such as FreeRTOS run to only a few
thousand lines.) It usually does without virtual-memory paging and swapping entirely, since a
page that must be fetched from disk is itself an unbounded delay. The less code there is, the
fewer paths that need a proven bound — and the easier it is to *guarantee* the worst case.

The insight tying these together is that **a guarantee is only as strong as the worst path
through the system.** You cannot bound the whole by being fast on average anywhere; you must
make *every* path that could delay the urgent task short and measured. Strict priority bounds
the scheduling delay, short critical sections bound the interrupt delay, and a tiny kernel
removes the housekeeping delays — and only with all three can you write down a worst-case
latency and stand behind it.

A note on the in-between: the general-purpose Linux kernel is *not* a real-time OS for the
reasons above, but a kernel patch set called **PREEMPT_RT** (merged into mainline Linux in late
2024) retrofits it toward bounded latency, mainly by making almost all kernel code preemptible
so a high-priority task can cut in nearly anywhere. It brings worst-case latency down to roughly
50–100 microseconds — good enough for **soft** real-time work like audio production — but still
short of a dedicated RTOS guaranteeing single-digit microseconds for **hard** cases like
pacemakers or brakes. It moves Linux toward predictability without giving up its features, and
so cannot fully close the gap.

### Worked instance: a motor controller on a 1-millisecond deadline

Make it concrete with a single example that exercises the whole distinction. A control task
**C** must read a position sensor and apply a correction to a motor **once every
millisecond** — that is its **period** and its deadline: each correction must be delivered
before the next 1 ms tick, or the motor, running open-loop for too long, overshoots and the
arm is damaged. The actual computation is cheap: reading the sensor and computing the
correction takes only, say, 40 microseconds of CPU time. So there is plenty of slack *if* C
can get on the CPU promptly each period. The danger is never the compute time — it is the
*waiting*.

**On a fair [[scheduler]].** Put C on a general-purpose, fair, time-sharing system alongside
a burst of ordinary background work — call it **B**: several tasks compiling code, serving
web requests, indexing files. All of them are runnable and hungry for CPU. Now trace one bad
period:

1. C delivers a correction at time 0 and blocks, waiting for its next 1 ms wake-up. It leaves
   the runnable set; the fair [[scheduler]] hands the core to the B tasks, which begin their
   time slices.
2. At time ~1 ms C's timer fires and C becomes **runnable** again — it now needs the CPU to
   compute and deliver this period's correction before time ~2 ms.
3. But the fair [[scheduler]] does not preempt for C. It only reconsiders at its next tick,
   and when it does it weighs C's accumulated CPU time fairly against the B tasks. C used some
   CPU recently, the B tasks are also "behind," and the policy may run a B slice first. A
   chain of such decisions, plus a moment when the kernel had interrupts disabled to protect a
   data structure, plus a page of B's memory that had to be fetched, stacks up. C ends up
   getting the core only at, say, time ~12 ms.
4. C's 40-microsecond computation then runs and the correction is delivered — at ~12 ms,
   **eleven deadlines missed**. The motor ran uncorrected for over ten periods. The arm
   overshot. The answer was numerically perfect and **the system failed**, because *late is a
   failure*.

Crucially, on a different run the very same code might deliver on time — the fair scheduler's
delay is *unbounded and unpredictable*, which is exactly why you cannot trust it for a hard
deadline.

**On an RTOS.** Now give C the **highest priority** and run it on an RTOS. The B tasks all sit
at lower priority. Re-trace:

1. C delivers a correction at time 0 and blocks until its 1 ms wake-up. With C off the runnable
   set, the RTOS [[scheduler]] runs the lower-priority B tasks — there is no one more important
   to run, so they make progress in the slack.
2. At ~1 ms C becomes runnable. Because C is the highest-priority runnable task, the RTOS
   **preempts immediately**: it stops whichever B task is mid-execution right now — not at the
   next tick, *now* — and switches to C. The kernel's interrupt-disabled sections are bounded,
   so even the worst-positioned wake-up reaches C within the published bound; suppose the RTOS
   guarantees the high-priority task is running within **50 microseconds** of becoming ready.
3. C's 40-microsecond computation runs and the correction is delivered by about 1 ms + 50 µs +
   40 µs ≈ 1.09 ms — comfortably before the ~2 ms deadline. **Every** period, on the worst run
   as on the best, because the 50-microsecond figure is a guaranteed worst-case bound, not an
   average.

Note the trade the RTOS made, plainly visible here: while C was blocked, the B tasks got the
core, but the *instant* C needed it they were thrown off without ceremony, and they will be
thrown off every single period forever. Over a second, B is repeatedly interrupted and its
total throughput is *lower* than the fair system would have given it — the RTOS may even be the
slower machine overall. That is the deal: the RTOS gives up average throughput and fairness to
B in order to keep an unbreakable promise to C. For a motor, a brake, or a pacemaker, that is
exactly the right trade — and it is the trade that defines what a real-time OS *is*.

## Prerequisites

- [[scheduler]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "Real-time OS": "Real-time doesn't mean fast"
  (real-time = guaranteed, bounded response time every time, not average speed; late-but-correct
  is failure), "Why Linux can't guarantee this" (the fair scheduler, periodic ticks,
  interrupt-disabled windows, and kernel housekeeping each adding unbounded latency), "How an
  RTOS scheduler differs" (strict-priority immediate preemption; bounded interrupt latency via
  short measured critical sections; tiny kernel with fewer hiding places for delay; FreeRTOS
  line counts), "Where real-time matters" (anti-lock brakes, industrial robots adjusting a motor
  every 1 ms, pacemakers, flight control — the hard cases — versus servers/desktops where Linux
  is fine), and "PREEMPT_RT — making Linux sort-of real-time" (the patchset, mainline since late
  2024, ~50–100 µs worst case, good for audio but not for hard deadlines; throughput-vs-
  predictability trade-off).
