---
id: kernel-thread
title: Kernel Thread
summary: A kernel thread (kthread) is a schedulable task — it has a numeric identity and is run by the scheduler exactly like a process — but it lives entirely inside the operating-system…
type: concept
tags: [os/kernel]
prereqs: [process]
sources: ['linux-internals-complete.html — kernel threads (the one exception; kswapd/kworker background work)']
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Kernel Thread

## Summary

A **kernel thread** (kthread) is a schedulable task — it has a numeric identity and is
run by the scheduler exactly like a [[process]] — but it lives *entirely inside the
operating-system kernel* and owns **no user memory**. It never loads or executes a user
program; it runs only the kernel's own code, doing ongoing background housekeeping such as
reclaiming memory or flushing data to disk. It is "the one exception" to the rule that the
kernel only runs when something outside it triggers it: the kthread is the kernel's *own*
thread of execution, one it can park to sleep and have the scheduler wake later, without
the weight of a full user [[process]].

## Grounded explanation

### The rule a kthread is the exception to

Start with how the kernel normally runs, because a kthread is defined by *breaking* that
pattern. The **kernel** is the privileged resident code that manages the hardware and
creates and schedules every [[process]]. Crucially, the kernel is **not itself a
process**: it has no identifying number, it does not appear in the system's process
listing, and it has no thread of its own that runs forever. It is best pictured as the
*road* the cars (processes) drive on, not as a car. The kernel only executes when
something **triggers** it from outside:

- a **system call** — a [[process]] deliberately asking the kernel for a service (read a
  file, send on the network);
- an **interrupt** — a hardware device signalling that something happened (a key was
  pressed, a disk finished, a network packet arrived);
- a **timer tick** — a periodic hardware pulse that lets the kernel check whether the
  running [[process]] should be replaced by another.

This is what "the kernel is **reactive**, not active" means: between triggers it is
dormant; each trigger wakes it, it does the work, and it goes back to waiting. (Triggers
arrive hundreds of times a second, so from the outside it looks perpetually busy, but
there is no standing kernel program looping on its own.) That is the rule.

### What a kthread is — the exception

Some kernel work does not fit that reactive shape. Consider reclaiming memory when the
machine runs low: nobody *asks* for it with a system call, and no single device interrupt
corresponds to "memory is getting full." The work is **ongoing and asynchronous** — it
must be done *eventually*, on the kernel's own initiative, and it may need to **sleep**
(do nothing, consuming no processor time) until conditions call for it, then **wake** and
run. The reactive model has no place to put such a task: there is no event to hang it on,
and the kernel has no thread of its own to carry it.

A **kernel thread** is the kernel's answer. It is a real schedulable **task**, meaning the
scheduler treats it like any runnable thing: it can be running, sleeping, or waiting, and
the scheduler decides when it gets a processor. In that respect it is *exactly* like a
[[process]] — it even carries a unique numeric identity (a **PID**, process identifier,
the same kind of number a [[process]] has) and shows up in the system's task listing. This
is why the source calls kthreads "the only kernel code that *runs* in the traditional
sense": unlike the rest of the reactive kernel, a kthread has its own scheduling and is a
thing the scheduler can point at and run.

But it differs from a [[process]] in the one way that defines the concept: **it has no
user address space.** Recall that an ordinary [[process]] is a running instance of a user
*program* and is given its own private region of memory holding that program's
instructions, data, and stack. A kthread has *none* of that. It never loads a program file
and never executes user instructions. It runs only code that already lives inside the
kernel, and it operates in the processor's most-privileged mode — the kernel's mode, where
code may touch hardware directly — with no private user memory mapped at all. So it is a
[[process]]-shaped *schedulable identity* wrapped around *kernel code only*: the schedulability of a process,
without the user program or the user memory.

### The why — a proactive thread without process baggage

Put the two halves together and the design choice is clear. The kernel needs a way to
perform work that is **its own initiative** and **continuous**, not a reaction to a single
outside event. To do that work it needs something the scheduler can run, pause, and resume
— i.e. a *task*. So the kernel manufactures its own tasks. By making them real
schedulable entities, the kernel gets to use the very machinery it already has for
processes: the kthread can block waiting for a condition (sleeping, using no processor),
and the scheduler will wake it when the condition arrives, then give it a processor turn
like anything else.

Yet a full user [[process]] would be the wrong tool: a user address space, a loaded
program, the user/kernel privilege boundary — all of that is *baggage* for code that is
already inside the kernel and only ever runs kernel code. Stripping the user address space
away leaves precisely what is needed: a bare, schedulable kernel-side worker. That is the
key insight — **a kthread is the kernel borrowing the scheduler's "task" abstraction for
itself, minus the parts of a process that only a user program needs.**

### Where kthreads come from, and the family you can see

Because they are not started by any user program, kthreads cannot descend from the normal
ancestor of user processes. They are created by the **kernel itself**. There is a single
special kthread, identified as **PID 2** and named `kthreadd`, whose only job is to spawn
the others; every kthread is its descendant. So kthreads form their *own* family of tasks,
separate from the tree of ordinary user processes. In a task listing they are
conventionally shown with their names in **square brackets** — that bracketing is the
visible signal that the entry is a kthread (kernel code, no user program) rather than a
real user [[process]].

The recurring kthreads are the kernel's "janitors," each handling one strand of
background work:

- **kswapd** — watches **memory pressure** (how close the machine is to running out of
  fast memory) and, when memory fills up, moves seldom-used pages of memory out to slower
  backing storage (**swap**) to free room.
- **writeback** (also seen as flush/writeback threads) — periodically **flushes dirty
  pages to disk**: a "dirty" page is one whose contents were changed in fast memory but
  not yet saved to disk; writeback copies it out so the change is made durable.
- **kworker** — runs **deferred work**: when the kernel is handling a hardware interrupt
  it does the bare minimum immediately and queues the slower part to finish later, off the
  interrupt; kworker is the task that later drains that queue.
- **ksoftirqd** — handles **soft interrupts**, the lower-priority follow-up processing of
  events such as arriving network packets, when that follow-up work piles up.
- **kcompactd** — defragments physical memory so that larger contiguous chunks can be
  found when needed.

None of these is a user program. Each is a standing strand of the kernel's own
maintenance, given a schedulable body so it can sleep until needed and run when called.

### Worked instance: kswapd under memory pressure

Trace one concrete kthread through a full cycle, contrasting it at each step with an
ordinary [[process]].

1. **Idle (sleeping).** Memory is plentiful. **kswapd** — a task with its own PID (say
   the entry shown as `[kswapd0]`), but with *no* user address space and *no* program
   loaded — is in the **sleeping** state. It consumes no processor time. (An ordinary
   [[process]] also sleeps when waiting, e.g. for disk data; the state is the same, but
   that process *has* user memory and a loaded program sitting idle, whereas kswapd has
   neither.)

2. **The trigger that is not an event.** Programs keep allocating memory and free memory
   runs low — this is *memory pressure*. There is no single system call or device
   interrupt that says "reclaim memory now"; this is exactly the asynchronous,
   on-the-kernel's-own-initiative work the reactive model cannot express. The kernel's
   memory bookkeeping notices the pressure crossing a threshold and **wakes kswapd**: it
   marks the task runnable.

3. **Running — but only kernel code.** The scheduler hands kswapd a processor turn, just
   as it would an ordinary runnable [[process]]. kswapd now runs: it scans pages of
   memory, picks ones not recently used, writes those it must preserve out to swap, and
   marks the freed memory available again. Every instruction it executes is *kernel* code
   in the privileged mode; at no point does it run a user program, because there is no user
   program and no user memory to run it in.

4. **Back to sleep.** Once free memory is comfortably above the threshold, kswapd has
   nothing more to do. It puts itself back to **sleep** — off the processor, consuming
   nothing — and waits to be woken the next time pressure returns. The cycle repeats for
   the life of the machine.

The contrast is the whole point. A normal user [[process]] running `ls` is a *program in
execution*: it was created by another process, given a private user address space, loaded
with the `/usr/bin/ls` instructions, and run to produce output for a user. kswapd is none
of that: created by the kernel (under `kthreadd`, PID 2), no user address space, no loaded
program, never producing output for a user — yet it is a first-class schedulable task with
a PID, woken and run by the scheduler. It is the kernel's *own* proactive thread of
execution, which is exactly why the source frames it as the one exception to the otherwise
purely reactive kernel.

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — sections "The one exception: kernel threads",
  "Wait — is the kernel a process? Is it PID 1?", and the "Memory housekeeping in the
  background" step (kswapd, writeback, kcompactd as background kernel threads).
