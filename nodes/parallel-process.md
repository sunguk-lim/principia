---
id: parallel-process
title: Parallel process
summary: Parallel processes are two or more processes that run simultaneously — each making progress on its own stream of instructions at the same time as the others, with no guaranteed…
type: concept
tags: [parallel-computing]
prereqs: [process, thread, scheduler, context-switch, address-space-layout, page-table]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-24
---

# Parallel process

## Summary

**Parallel processes** are two or more [[process]]es that run simultaneously —
each making progress on its own stream of instructions at the same time as the others,
with no guaranteed relative order between them. The key property that makes them
*parallel* rather than merely *concurrent* is that each process has its own **private
address space** (see [[address-space-layout]]): one process cannot directly read or write
another's memory. Data must therefore be *sent* between them, never simply shared.
The operating system sustains this picture by giving each process a turn on the CPU via
[[context-switch]]es, managed by the [[scheduler]], while keeping their memory maps
entirely separate. [[thread]]s within a single process are explicitly excluded: they share
memory and do not count as parallel processes in this sense.

## Grounded explanation

### What a process brings to the picture

Recall from [[process]] that a process is a running instance of a program to which the
kernel grants four things: a unique PID, a slot in the process table, a set of open file
descriptors, and — most importantly here — a **private address space**. That address
space is the program's exclusive view of memory: its code, its heap, its stack, its
globals. No other process can name or touch these bytes. The kernel enforces this
isolation structurally, not by checking each access at runtime.

The structure of that address space — how code, data, heap, and stack are arranged inside
it — is described by [[address-space-layout]]. What matters for parallel processes is the
consequence: because each process has its *own* separate layout with its *own* page table,
two processes can both operate on variables called `x` in their respective programs without
any interference. Their `x`s live at the same virtual address but the kernel loads a
different [[page-table]] for each process, so those identical virtual addresses map to
entirely different physical bytes.

### How two processes run "at the same time"

A single CPU core executes one instruction stream at a time. The illusion of simultaneous
progress is produced by the [[context-switch]]: the kernel pauses one process by saving its
CPU registers (including program counter and stack pointer) into its process-table slot,
then loads another process's saved registers and resumes it. The paused process is
unaware it was ever stopped; when it gets the CPU back, it continues from the exact
instruction it was on, with the exact values it held.

The [[scheduler]] decides *which* process runs next and for how long. It maintains the
set of runnable processes, picks the most-deserving candidate (by a fairness policy),
grants it a time slice, and relies on a [[context-switch]] to carry that decision out.
The result is that many processes each perceive a dedicated CPU while physically sharing
one (or a few) cores.

On a machine with multiple cores, true physical simultaneity is also possible: the
scheduler places different processes on different cores, and their instruction streams
advance in real parallel, not just in rapid alternation. Either way — time-sliced or
truly simultaneous — the abstract picture is the same: independent actors making progress
concurrently, in no guaranteed relative order.

### Why private memory is the defining constraint

Contrast parallel processes with [[thread]]s. A thread is an independent flow of execution
that *shares* its parent process's address space. Threads communicate for free — one writes
a value and the other simply reads it — but at the price of isolation: one thread's bug can
corrupt data every sibling depends on, and a fatal fault takes the whole process down.

Parallel processes run in *separate* address spaces. They cannot accidentally corrupt each
other because the kernel forbids cross-process memory access entirely. This isolation is
precisely what the [[address-space-layout]] machinery enforces: each process has its own
[[page-table]], so no virtual address in process A names any byte in process B. The cost is
that data cannot be shared implicitly — it must be *transferred*. Message-passing
communication patterns exist precisely because parallel processes have private memory.

### Concrete instance: two processes summing independent halves of an array

Suppose you have an array of a billion integers and want their sum. A single [[process]]
works through them sequentially. To run in parallel, you spawn a second process (the kernel
allocates a fresh PID, a new process-table slot, and a *separate* address space for it).
Each process independently receives its half — because they cannot share the array, the
data must be copied or passed to the child — and each sums its half entirely within its
own private memory. Neither can see the other's partial sum; neither can corrupt the other's
loop counter. The [[scheduler]] gives both processes turns on the CPUs; [[context-switch]]es
move CPU state in and out as their turns rotate. When both finish, they communicate their
partial sums (via a message, a pipe, or shared-memory IPC that explicitly creates a mapping
visible to both) and the totals are added. The result is correct regardless of which
process finishes first, because each worked on entirely independent data in entirely
independent address spaces.

This instance makes the structure visible: *independent actors* (two separate processes),
*private memories* (separate address spaces enforced by [[address-space-layout]]),
*simultaneous execution* (managed by [[scheduler]] and [[context-switch]]), and
*no shared state* (data transferred explicitly, not accessed directly).

## Prerequisites

- [[process]]
- [[thread]]
- [[scheduler]]
- [[context-switch]]
- [[address-space-layout]]
- [[page-table]]

## Sources
