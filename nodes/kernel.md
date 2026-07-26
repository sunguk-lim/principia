---
id: kernel
title: Kernel
summary: The kernel is the privileged core program of an operating system.
type: concept
tags: [os/kernel]
prereqs: [memory-hierarchy]
sources:
  - "Linux internals study guide (etc/linux-internals-complete.html) — 'The kernel itself', 'What is the kernel, physically', 'The kernel's subsystems', 'How the kernel runs — three entry points'"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Kernel

## Summary

The **kernel** is the privileged core program of an operating system. A *program* is
just a list of machine instructions plus its data; a *process* is one running program
with its own private slice of memory; the *CPU* is the chip that executes instructions
one after another. The kernel is loaded into memory once, at boot, and stays resident
there for the whole life of the machine. But it is *not* a program with a loop that runs
on its own. It has **no continuous thread of control**: between events it is just code
and data sitting in memory, doing nothing. It comes alive only when something **enters**
it — a program asking for a service (a *system call*), or a hardware device demanding
attention (an *interrupt*). While entered, it runs with full hardware privilege and does
the things ordinary programs are forbidden to do: talk directly to devices, and decide
which slice of physical memory ([[memory-hierarchy]]) each process is allowed to touch.
The single defining idea: the kernel is **reactive code that mediates every program's
access to the CPU, memory, and devices** — a referee that is entered on demand, not a
player that runs alongside you.

## Grounded explanation

### What the concept *is*: a resident, privileged, reactive program

Start from three plain words.

- A **program** is a stored list of instructions (the things the CPU can do — add, copy
  a number from one place to another, jump) together with the data those instructions
  work on. On disk it is just a file.
- The **CPU** is the chip that fetches one instruction, does it, fetches the next, and so
  on, forever. It can only ever be running *one* stream of instructions at a time per
  core.
- A **process** is one program *in the middle of running*: it has been given its own
  private region of memory to keep its instructions and data in, and the CPU is (some of
  the time) executing its instructions.

Now the puzzle the kernel solves. A machine has *one* CPU (or a handful of cores), *one*
pool of physical memory, and *one* set of devices — keyboard, disk, network card. But it
wants to run *many* processes, none of which can be trusted to share politely or to poke
the hardware correctly. If every process could write to any byte of physical memory, one
buggy process would corrupt another. If every process could send raw commands to the disk
controller, two of them would scribble over each other's files. Something has to sit
*in the middle* and arbitrate. That something is the kernel.

The kernel is therefore distinguished from ordinary programs by three properties at once:

1. **Resident.** It is loaded into memory once, at boot, and never leaves. Physically it
   is one large binary file (~10–15 MB) that, when started, decompresses itself into a
   fixed region of memory and stays there for the whole life of the machine.
2. **Privileged.** The CPU itself enforces two modes: a *restricted* mode for ordinary
   programs and an *unrestricted* mode. The kernel's code runs in the unrestricted mode,
   so it — and only it — may execute the instructions that touch hardware directly or
   that change which physical memory a process can reach. An ordinary process attempting
   those instructions is stopped by the CPU.
3. **Reactive.** It has no `main()` loop of its own. Picture not a person doing a job but
   a city's infrastructure — roads, traffic lights, water pipes. The infrastructure does
   not "run"; it *activates* whenever a car drives or a tap opens. Likewise the kernel
   sits dormant in memory and executes only when triggered.

Hold property 3 carefully, because it is the most counter-intuitive and it *is* the
concept. The kernel is **one program with one address space**, but it is more like a huge
library of functions than like a running application. Nothing in it executes until a
trigger calls one of those functions.

### The WHY: how a program with no loop "runs" — entry points

If the kernel has no loop of its own, how does its code ever execute? Through a small,
fixed set of **entry points**: special functions the CPU is wired to jump to when a
specific event occurs. (A function the system calls *for you* when an event fires — rather
than one you call explicitly — is a **handler**; an entry point is a handler the CPU
itself invokes.) There are three everyday ones, plus a fourth that the memory machinery
needs.

- **Entry point 1 — system call.** A process executes a special `syscall` instruction
  meaning "I need a service I'm not allowed to do myself." The CPU switches to the
  privileged mode and jumps to the kernel's syscall entry point, which looks up *which*
  service was requested (open a file, read bytes, send a packet) and runs the matching
  handler. When it finishes, it switches the CPU back to restricted mode and returns to
  the process. This is the **front door**: every request from a program comes through it.
- **Entry point 2 — hardware interrupt.** A device (keyboard, network card, disk)
  raises an electrical signal. The CPU *stops whatever it is doing mid-stream*, switches
  to privileged mode, and jumps to the handler registered for that device. The handler
  deals with the event and returns; the interrupted work resumes as if nothing happened.
- **Entry point 3 — timer tick.** A hardware timer fires every few milliseconds and,
  like any interrupt, jumps into the kernel. This handler runs the **scheduler** — the
  part of the kernel that decides which process the CPU should run next — so that one
  process cannot hog the CPU forever. It is the kernel's heartbeat.
- **Entry point 4 — exception / fault.** When a process does something the CPU cannot
  immediately complete — most importantly, touching a memory address that is not yet
  mapped to physical memory — the CPU *traps* into a registered kernel handler, exactly
  like an interrupt. We will use this one in the walkthrough.

**Between** triggers, the CPU is either running some ordinary process or, if every
process is asleep, sitting in a low-power halted state waiting for the next interrupt.
The kernel itself is doing *nothing* — it is just bytes in memory. The key insight, and
the thing to remember: **the kernel is not a program that runs alongside your processes;
it is code your processes enter temporarily (via system calls) and that hardware invokes
temporarily (via interrupts). It is always present, but only active when triggered.**
Triggers arrive hundreds of times per second, so from the outside this looks like
"constantly active," but it is really a fast cycle of wake → handle → sleep.

### What the kernel owns: the subsystems

That "library of functions" is organized internally into **subsystems**, each owning one
domain. They are not separate programs in separate places — after boot they all live in
one continuous region of memory, share data structures, and call one another directly.
The organization is into *roles*, not walled-off compartments. The major ones:

- **Process management & scheduler** — creates and ends processes and answers *"which
  process runs on which core, and when?"* (entry point 3 drives this).
- **Memory manager** — owns the mapping from each process's private addresses to actual
  physical memory, and decides who gets which bytes. This is the subsystem grounded in
  [[memory-hierarchy]], discussed next.
- **Filesystem** — presents a uniform `open / read / write / close` interface no matter
  what the underlying storage is.
- **Networking** — turns a program's "send these bytes" into packets on the wire and
  back.
- **Device drivers** — the per-device translators. A *driver* is kernel code that
  converts the kernel's generic request ("read block 500") into the exact register
  writes a *specific* piece of hardware understands. The kernel says the same thing to
  every disk; the driver is the bilingual interpreter that makes a particular disk obey.
  Because a driver runs with full privilege, a bug in one driver can crash the whole
  machine — once loaded, the driver *is* the kernel.

### Grounding the memory role in [[memory-hierarchy]]

[[memory-hierarchy]] establishes that a machine's storage is a ladder of stores —
fast-but-tiny registers and on-chip memory near the top, larger-but-slower main memory
(DRAM) below — and that **moving a byte from a far level costs far more than doing
arithmetic on it**: on a representative chip, the time to fetch one byte from main memory
is worth on the order of *dozens* of arithmetic operations. The kernel's memory manager
is what *governs that ladder on every process's behalf.* Two consequences follow directly.

First, **the kernel decides who occupies which physical bytes.** Each process believes it
has its own clean expanse of memory addresses, but those are not real physical locations;
the memory manager keeps a translation from each process's private addresses to actual
physical bytes in main memory, and enforces that one process can never name another's
physical bytes. This is exactly the arbitration that made the kernel necessary in the
first place — applied to the *bottom rungs* of the hierarchy (DRAM and main memory), which
is the only level large enough to hold many processes at once.

Second, **because main memory is the slow rung, the kernel hands it out lazily.** Since a
byte of main memory is expensive to touch and there is only so much of it, the kernel does
not give a process physical memory until the process actually reaches for an address. The
*first* touch of an un-backed address is precisely entry point 4 (a fault): the CPU traps
into the kernel, the memory manager finds a free physical page, records the new mapping,
and lets the instruction resume. The hierarchy explains *why* this is worth the trouble —
physical memory is a scarce, costly resource on the ladder, so the manager that rations it
is one of the kernel's central jobs.

### Worked walkthrough: what the kernel does when you press one key

Take a concrete, non-degenerate event — you press the key **`l`** at a shell prompt — and
trace it through the entry points. It is non-degenerate because it exercises a real
hardware interrupt, a real subsystem buffer, a scheduler decision (a process actually
moves from asleep to running), and a return through a system call — none of the steps
collapse away.

Set the scene. The shell program (call it `bash`) earlier executed a `read` **system
call** (entry point 1) asking "give me a character from the keyboard." There was no
character yet, so the kernel marked `bash` **asleep** — not on the CPU, not consuming
cycles — and recorded that `bash` is waiting on this keyboard. The CPU went on to other
work or halted. The kernel is now dormant; nothing of it is executing.

1. **Hardware signals.** Your finger closes a switch in the keyboard. The keyboard
   controller raises an interrupt line to the CPU.
2. **Interrupt entry (entry point 2).** The CPU abandons whatever it was doing, switches
   to privileged mode, and jumps to the keyboard interrupt handler inside the kernel.
   *This is the kernel waking up* — code that was inert a microsecond ago is now running.
3. **The driver reads the device.** The keyboard driver reads the raw key code from the
   controller's register (a privileged hardware access an ordinary process could not do)
   and converts it to the character `'l'`.
4. **The character goes into a buffer.** The handler places `'l'` into the keyboard's
   input buffer — a small kernel-owned data structure in main memory (the bottom of the
   [[memory-hierarchy]] ladder, the only rung roomy enough to be the shared meeting point
   between an interrupt and a sleeping process).
5. **Wake the waiter.** The handler checks: *is any process asleep waiting on this
   keyboard?* It finds `bash`. It marks `bash` **runnable** again — moving it from asleep
   to ready-to-run — and the interrupt handler returns. The kernel goes dormant once more.
6. **The scheduler picks it up.** At the next timer tick (entry point 3) the scheduler
   sees that `bash` is runnable and gives it the CPU.
7. **The system call returns.** Now `bash` resumes inside the `read` call from step 0; the
   kernel copies `'l'` out of its buffer into `bash`'s own memory, switches the CPU back
   to restricted mode, and returns from the call. From `bash`'s point of view, `read`
   simply returned the character `'l'`.
8. **Echo and sleep again.** `bash` makes a `write` system call to put `'l'` on the
   screen, then calls `read` once more — and, finding no next character, the kernel marks
   it asleep again. Back to a dormant kernel and an idle CPU. Elapsed time: microseconds.

Notice what the trace demonstrates. The kernel never *ran on its own* at any step. It was
**entered** twice (once by hardware at step 2, once by the program at step 0/step 7),
each time did a bounded piece of work, and each time went back to sleep. It performed the
privileged acts no process may do (reading the device register, moving a process between
asleep and runnable, copying across the memory boundary), and it mediated every contact
between the program and the hardware. That is the whole concept in one keystroke: a
resident, privileged, reactive program that brokers all access to the CPU, to memory, and
to devices.

## Prerequisites

- [[memory-hierarchy]]

## Sources

- Linux internals study guide (`etc/linux-internals-complete.html`) — sections "The kernel itself" / "What is the kernel, physically?" (the resident single-binary framing and the city-infrastructure analogy), "The kernel's subsystems" (scheduler, memory manager, filesystem, networking, drivers), and "How the kernel 'runs' — three entry points" plus the "press a key" walkthrough (the reactive entry-point model and the keystroke trace).
