---
id: process
title: Process
summary: A process is a running instance of a program.
type: concept
tags: [os/process]
prereqs: [kernel]
sources:
  - linux-internals-complete.html ("What is a process", "Process states", "Every process has a parent")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Process

## Summary

A **process** is a *running instance of a program*. A program is passive: a file of
machine instructions sitting on disk, doing nothing. A process is that program *in
execution* — loaded into memory with live state and actively making progress. The
[[kernel]] is what turns the one into the other, and it treats the process as its basic
**unit of resource ownership and isolation**: every process gets its own private memory,
its own set of open files, a unique numeric identity, and a record in a kernel-managed
table. Because the kernel hands these out per-process and tracks them per-process, it can
keep processes from interfering with one another and can cleanly account for and reclaim
everything a process used once it finishes.

## Grounded explanation

### Program vs. process — the distinction that defines the concept

Start with two words that are easy to conflate. A **program** is a *file*: a sequence of
machine instructions stored on disk, for example the file `/usr/bin/ls`. On its own it is
inert — "dead bytes," changing nothing. A **process** is what exists when the [[kernel]]
loads such a file into memory and begins executing its instructions, while keeping track
of where execution currently is and what the program has done so far. That bookkeeping —
the instructions plus all the *live state* of one execution — is the process.

The relationship is one-to-many: a single program can be running as many processes at
once. Ten browser tabs may be ten separate processes all executing the *same* browser
binary; each has its own independent live state and none can see into the others. This is
the first clue to the concept's purpose: the unit we care about at runtime is the
*execution*, not the file.

### What the kernel gives each process

Recall that the [[kernel]] is the privileged resident program that manages the hardware
and creates and schedules processes. When it makes a process, it endows that process with
four things — and tracking these four things *per process* is exactly what makes "process"
a meaningful unit:

1. **A private memory region (its address space).** Each process is given its own view of
   memory: its instructions, its data, its stack (scratch space for function calls), and
   its heap (memory it requests as it runs). One process cannot read or write another's
   memory. (The mechanics of how that private view is built and protected are covered
   elsewhere; here it suffices that the kernel guarantees the privacy.)

2. **A set of open file descriptors.** A *file descriptor* is a small integer the process
   uses to refer to something it has opened — a file, a terminal, a network connection.
   The set belongs to that one process; the kernel knows which descriptors each process
   holds.

3. **A unique PID (process identifier).** This is a number naming the process — the value
   you see in process-listing tools. No two live processes share a PID, so the kernel (and
   you) can name any process unambiguously.

4. **A slot in the kernel's process table.** The kernel keeps one record per process —
   conceptually a row in a big table it owns. That record holds the process's PID, its
   current state (defined next), a pointer to its private memory, its open file
   descriptors, the identity it runs as (which user), and who created it. *Every* process
   on the system has exactly one such record; this table *is* the kernel's authoritative
   list of what is alive.

### Process states — what a process is doing right now

A process is not always actually executing on a CPU; most of the time it is waiting. The
[[kernel]] records, in that process's table slot, which of a small set of **states** the
process is currently in. The states form the *life* of a process:

- **Running / runnable (ready):** either actually executing on a CPU at this instant, or
  ready to and just waiting for the kernel to give it a turn. (A machine has only a few
  CPUs but many processes, so the kernel rapidly rotates runnable processes onto the CPUs;
  that rotation is its own topic. The point here is that "wants the CPU" is a state.)
- **Sleeping / blocked:** waiting for something that has not happened yet — data from a
  disk read, bytes from the network, a timer to expire. A sleeping process consumes no CPU;
  the kernel will wake it (mark it runnable again) when the awaited event arrives. Most
  processes on a system sit here most of the time.
- **Stopped:** paused — for instance by a debugger, or by the user pressing a "suspend"
  key. It will not run again until something explicitly resumes it.
- **Zombie:** *finished*, but not yet cleaned up. This state is the subtle one and is worth
  understanding precisely (next paragraph).

A **zombie** is a process that has *exited* — its program has run to completion and it is
no longer executing or holding memory — yet its table slot still exists, holding one last
thing: its **exit status** (a small code reporting whether it succeeded or failed). Why
keep the slot? Because the process that created it may want to know *how* it ended. The
kernel therefore preserves the minimal record until the creator asks for the exit status —
an act called **reaping** the child. Once reaped, the slot is freed and the PID becomes
reusable. If the creator never reaps, zombies accumulate: harmless individually (they use
no memory, only a slot and a PID) but a sign of a buggy parent, since PIDs are finite.

### Every process has a parent — the process tree

Where do processes come from? *Another process makes them.* The only way a new process
comes into being is for an existing process to ask the [[kernel]] to create one — the new
process is the **child**, the creator is its **parent**. The kernel records the parent in
the child's table slot. (The standard mechanism a parent uses is to duplicate itself and
then have the copy load a different program; the details belong to other nodes. What
matters for the concept is the *relationship* the kernel records.)

Follow these parent links and every process traces back through ancestors to a single
root: **PID 1**, the first process the kernel starts after boot. PID 1 has no
process-parent (the kernel itself started it). So the set of all processes forms a **tree**
rooted at PID 1, each node a process, each edge a "created-by" link.

This raises a question the kernel must answer: what if a parent finishes *before* its
child? The child would be left with a dangling parent link and, worse, no one to eventually
reap it. The kernel resolves this by **reparenting**: any such **orphan** is automatically
re-attached to PID 1, which is written to always reap the children it inherits. So the tree
invariant — every live process has a valid parent, and every exited process will eventually
be reaped — is never broken.

### The why: process = unit of isolation and accounting

Now the justification, which ties all of the above together. The [[kernel]]'s job includes
protecting programs from one another and from itself, and reclaiming hardware when a program
is done. It needs a *unit* to attach those guarantees to. Making **the process** that unit
is the key design choice, and it pays off in three ways:

- **Isolation by construction.** Because memory and file descriptors are granted
  *per process* and the kernel never lets one process touch another's, a crashing or
  malicious process is fenced into its own address space. The blast radius is one process.
- **Clean accounting.** Because every resource is recorded in the offending process's table
  slot, the kernel always knows exactly what each process holds — useful for limiting,
  charging, and inspecting.
- **Clean reclamation.** When a process exits, the kernel walks that one slot and frees
  everything tied to it: its memory, its open file descriptors, its CPU claim. Nothing
  leaks, *precisely because* everything was owned by a single, well-defined unit. The only
  thing deliberately kept back is the exit status — and the zombie state plus reaping is the
  mechanism that releases even that, on the parent's schedule.

So the states and the parent-child tree are not separate trivia: they are the lifecycle of
the kernel's resource unit, from creation (by a parent) through running/sleeping (holding
resources) to exit and reaping (releasing them).

### Worked instance: the lifecycle of one `ls`

Trace a single, concrete process from birth to cleanup. You are typing at a command
**shell** — itself a process, say with PID 1200 — and you run `ls`.

1. **Creation.** The shell asks the [[kernel]] to create a child. The kernel allocates a
   fresh slot in its process table, assigns a new unique PID — say **1201** — and records
   the parent as 1200. The child is then made to load the program `/usr/bin/ls` into its
   private memory. At this instant the file `/usr/bin/ls` (the *program*) has become a
   *process*: PID 1201, parent 1200, with its own address space and its own open file
   descriptors (it inherits ones pointing at your terminal, so its output reaches your
   screen).

2. **Running.** PID 1201 is **runnable**; the kernel schedules it onto a CPU and it begins
   executing — reading the directory.

3. **Sleeping (a non-degenerate detail).** To read the directory, `ls` must wait on the
   disk. While that I/O is outstanding it enters the **sleeping** state — off the CPU,
   consuming nothing. This step matters: it shows a process is not "running" for most of
   its short life. When the disk data arrives, the kernel marks PID 1201 **runnable**
   again; it gets a CPU, formats the file names, and writes them to the terminal.

4. **Exit.** `ls` finishes and exits with a status meaning "success." The kernel reclaims
   PID 1201's memory and closes its file descriptors immediately. But it does *not* yet
   discard the table slot: it keeps the slot holding the exit status. PID 1201 is now a
   **zombie**.

5. **Reaping.** The shell (PID 1200), which had been waiting for its child to finish, now
   asks the kernel for that exit status — it **reaps** PID 1201. The kernel hands over the
   status, frees the last slot, and PID 1201 ceases to exist; the number 1201 may later be
   reused. The shell, seeing "success," prints its next prompt.

Notice what each state did: *runnable* meant "wants the CPU," *sleeping* meant "waiting on
the disk," *zombie* meant "done but my parent hasn't collected my result," and the
parent-child link (1200 → 1201) is exactly what told the kernel *who* would reap the
result. Had the shell exited mid-`ls`, PID 1201 would have been reparented to PID 1 and
reaped there instead — the tree invariant holding throughout.

## Prerequisites

- [[kernel]]

## Sources

- `linux-internals-complete.html` — sections "What is a process?", "Process states — what
  is a process doing right now?", and "Every process has a parent".
