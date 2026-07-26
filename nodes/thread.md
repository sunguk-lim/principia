---
id: thread
title: Thread
summary: A thread is an independent flow of execution running inside a process — one "line" of activity stepping through the program's instructions.
type: concept
tags: [os/process]
prereqs: [process, context-switch]
sources:
  - linux-internals-complete.html ("Threads vs processes — it's all clone()")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Thread

## Summary

A **thread** is an independent *flow of execution* running inside a [[process]] — one
"line" of activity stepping through the program's instructions. A plain [[process]] has
exactly one such flow; a **multithreaded** [[process]] has several that run, or rapidly
take turns, at the same time. The defining fact is what those threads share and what they
keep private: all threads of one [[process]] **share** that process's memory and open
files, but each thread has its **own** stack, its own copy of the CPU registers, and its
own **program counter** (the marker of which instruction it is about to execute next). So
the threads see the same data but each tracks its own position in the code. On Linux there
is no deep boundary between "thread" and "process" — both are made by the *same* creation
request to the kernel, and the only difference is a set of flags choosing what gets shared
versus copied. Sharing memory makes threads cheap to create and cheap to communicate
through, at the price of having to coordinate their access to the shared data by hand.

## Grounded explanation

### Starting from the process: one flow, or many

Recall what a [[process]] is: a running instance of a program, to which the kernel grants a
private memory region (its **address space** — its instructions, its data, its stack for
function calls, its heap), a set of open **file descriptors** (the small integers naming
files and connections it has opened), a unique identity, and a record in the kernel's
table. In the simplest case a process does *one thing at a time*: there is a single point
of execution walking through the instructions, calling functions, returning from them.

A **thread** is that point of execution itself. The word names the *flow* — the moving
"reading head" stepping through the code — not the resources around it. A process with one
thread (the default) is what we have been picturing all along. A process with *several*
threads has several such heads moving through the same program concurrently: it can be
formatting a document while also saving it to disk while also redrawing the window, three
flows of execution inside one program.

To make "flow of execution" concrete we need three pieces of private state that *every*
flow must carry:

- **A program counter (PC).** A flow is always "about to run" some specific instruction;
  the program counter is the marker holding *which* one. Two flows in the same program can
  sit at two different instructions — even inside the same function — because each has its
  own PC.
- **A set of CPU registers.** The processor computes in a handful of fast scratch
  locations called registers (holding, say, the operands of the arithmetic it is doing
  right now). Each flow has its own working values there.
- **A stack.** Recall the stack is the scratch space for function calls — where a flow
  records "I am inside function `f`, which was called from `g`," along with each call's
  local variables. Two independent flows are in different places in the call structure, so
  each needs its own stack.

These three together are the flow's **execution state**: where it is and what it is in the
middle of doing. A thread *is* an execution state plus the agreement to share everything
else with its siblings.

### What is shared and what is private — the crux

Here is the heart of the concept. Take a process with three threads and lay out, item by
item, which things the threads share and which each keeps to itself.

**Shared across all threads of the process** (one copy, everyone sees it):

- The **address space** — the same instructions, the same heap, the same global data. If
  thread 1 stores the number 5 into a variable, thread 2 reads that same variable and sees
  5. There is no copying; it is literally the same memory.
- The **open file descriptors** — if one thread opens a file, the others can use it.

**Private to each thread** (each gets its own):

- Its **program counter**, its **registers**, and its **stack** — its execution state, as
  above. A local variable a thread declares inside its own function lives on *its* stack
  and the others do not see it.

So threads are *mostly shared, narrowly private*: they share the whole world of data and
diverge only in where each one currently is in the code. Contrast this with two separate
single-threaded processes, which share *nothing* — each has its own private address space
and the kernel forbids one from touching the other's memory. That contrast is the whole
point, and the next section explains why the line falls exactly where it does.

### The why: on Linux, "thread" and "process" are one mechanism with different flags

It is tempting to imagine the kernel has two distinct gadgets — a "make a process" button
and a "make a thread" button. It does not. The source's central claim is blunt: *a thread
is just a process that shares memory with another process.* Inside the kernel there is only
one kind of bookkeeping record per flow of execution, and only one creation request that
makes a new one. That request takes a set of **flags**, and each flag answers one yes/no
question: *should this new flow SHARE a given resource with its creator, or get its OWN
COPY?*

- Turn the **share-memory** flag **off** and the new flow gets its own private copy of the
  address space. It cannot see the creator's variables. We call the result a separate
  **[[process]]**.
- Turn the **share-memory** flag **on** (and likewise share the open file descriptors) and
  the new flow runs in the *same* address space as its creator, seeing the same variables.
  We call the result a **thread** of that process.

That is the entire distinction. "Thread" versus "process" is not a difference in kind; it
is a difference in *one bit* — do you share the address space or copy it? Everything that
feels special about threads (they see each other's data; they are cheap) and everything
special about processes (they are isolated) follows mechanically from that single choice.
This is *why* the definitions in the previous section look the way they do: the private
items (PC, registers, stack) are private because *every* independent flow needs its own
execution state no matter what; the shared items (memory, files) are shared *precisely
because* the creator asked, via the flags, to share them.

(How the kernel then juggles many flows onto a few CPUs — rapidly switching the running
flow's execution state in and out — a [[context-switch]] — under a component called the
scheduler — is a separate topic. What matters here is the structure, not the timing.)

### The tradeoff: cheap communication versus lost isolation

Why would you ever choose threads over just running several processes? And why would you
ever *not*? The shared address space is both the gift and the curse.

**The gift — cheap creation and cheap communication.** Making a separate process means the
kernel must set up a whole new private address space; making a thread skips that, since the
address space already exists and is merely shared — so a thread is lighter to create. More
importantly, two threads communicate *for free*: one writes a value into shared memory and
the other simply reads it, with no copying and no asking the kernel to ferry data between
two private address spaces. The shared world *is* the communication channel.

**The curse — you lose isolation and must synchronize by hand.** Recall that the
[[process]] earns its keep as the kernel's unit of isolation: a crashing or misbehaving
process is fenced into its own address space, so the blast radius is one process. Threads
deliberately tear that fence down *inside* a process. Because they share one address space,
one thread that corrupts memory can wreck the data every sibling depends on; a fatal fault
takes the whole process down, all threads with it. And because several flows now touch the
*same* variables at once, you must add explicit coordination so they do not trip over each
other. The next section shows exactly how that tripping happens.

### Worked instance: three threads incrementing one shared counter

Make it concrete with the smallest example that still exposes the danger. One process runs
a program with a single shared global variable, `counter`, starting at `0`. The program
launches **three threads**; each thread runs the *same* loop:

```
repeat 1000 times:
    counter = counter + 1
```

Because the three threads share one address space, there is exactly **one** `counter` — all
three threads read and write that same memory location. Each thread, however, runs its loop
on its *own* stack, with its *own* program counter walking its *own* copy of the loop. So
the *intent* is plain: three threads × 1000 increments each = `counter` should end at
**3000**.

Now look at what `counter = counter + 1` actually is. It is **not** one indivisible step.
The CPU performs it as three sub-steps, using a private register inside the thread:

1. **Read** the current value of `counter` from shared memory into the thread's register.
2. **Add** 1 to the value in that register.
3. **Write** the register's value back to `counter` in shared memory.

The register is private, but `counter` is shared — and a thread can be paused *between* any
two of these sub-steps (the system is free to switch which flow runs at almost any moment).
That gap is where it breaks. Trace one bad interleaving, with `counter` currently `41`:

- **Thread A** does step 1: reads `counter` (41) into its register. Now it is paused.
- **Thread B** runs: reads `counter` (still 41) into *its* register, adds 1 (42), writes
  42 back to `counter`. Now `counter` is 42.
- **Thread A** resumes from where it left off: it already holds 41 in its register, adds 1
  to get 42, and writes **42** back to `counter`.

Two increments happened — A's and B's — but `counter` advanced only from 41 to 42 instead
of to 43. One increment **vanished**. This is a **race**: the result depends on the exact,
unpredictable order in which the threads' sub-steps interleave. Run the program repeatedly
and `counter` ends at some unpredictable number *less than or equal to* 3000 — almost never
the 3000 you intended.

Notice precisely why this is a *thread* problem and not a process problem. Two separate
processes each have their *own* private `counter`; they could never collide on a shared one
in the first place — but then they also could not share a single running total at all. It
is the very thing that makes threads useful (one shared variable, no copying) that creates
the bug.

The fix is a **lock**: a coordination object a thread must acquire before touching
`counter` and release afterward, with the rule that only one thread may hold it at a time.
A thread that wants the lock while another holds it simply waits. Wrapping the three
sub-steps inside "acquire lock → read, add, write → release lock" forces the read-add-write
to complete as an uninterrupted unit, so no second thread can slip in between a read and its
matching write. With the lock in place the program reliably ends at 3000. That extra
acquire/release ceremony — needed *only* because the data is shared — is the concrete price
of the thread's cheap shared memory, and it is exactly the synchronization burden the
tradeoff above warned about.

## Prerequisites

- [[process]]
- [[context-switch]]

## Sources

- `linux-internals-complete.html` — section "Threads vs processes — it's all clone()":
  a thread is a process that shares memory; both are created by the same `clone()` request,
  differing only in which flags select SHARE versus OWN COPY for memory and file
  descriptors.
