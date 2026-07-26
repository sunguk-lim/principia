---
id: seccomp
title: seccomp
summary: seccomp (secure computing mode) is a kernel facility that lets a process install a filter restricting which system-calls it — and every child it later spawns — is allowed to make.
type: concept
tags: [os/virtualization]
prereqs: [system-call]
sources: ["linux-internals-complete.html — 'Namespaces + cgroups aren't enough' (Seccomp — a syscall filter; Docker default profile blocks ~60 dangerous syscalls; the syscall instruction still fires, kernel returns EPERM), 'Defense in depth — four layers', 'What Docker actually does' (step 7: applies seccomp filter), experiment '5 — See seccomp blocking a syscall' (reboot → Operation not permitted; /proc/self/status Seccomp: 0=disabled, 2=filter mode)"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# seccomp

## Summary

**seccomp** (secure computing mode) is a kernel facility that lets a process install a
**filter** restricting *which* [[system-call]]s it — and every child it later spawns — is
allowed to make. The filter is a tiny program the kernel runs on **each** [[system-call]],
inspecting the syscall number (and its arguments) and returning a **verdict**: allow the call
to proceed, refuse it by handing back an error, or kill the process outright. The point is to
shrink the kernel's **attack surface**. A normal program needs only a few dozen of the kernel's
~350 [[system-call]]s; once a seccomp filter forbids the rest, a process that is later
compromised or simply buggy can no longer reach the dangerous kernel paths (rebooting the
machine, mounting filesystems, loading kernel modules) it would need to do real damage. Because
the [[system-call]] is the *only* gateway from a process to the kernel's privileged operations,
filtering [[system-call]]s bounds everything that process can ever ask the kernel to do. This
makes seccomp a core hardening layer for sandboxes and containers.

## Grounded explanation

### The defining idea: a gate placed in front of the only gate

From [[system-call]] we have the one fact this entire concept rests on: a process can do
*nothing* privileged on its own. To touch a disk, reboot the machine, mount a filesystem, or
load kernel code, it must make a [[system-call]] — fill a register with a **syscall number**
(the integer naming the service it wants), execute the `syscall` instruction, and let the
trusted kernel perform the work. That gateway is the *only* path from an unprivileged process
to privileged power. Every dangerous thing a process could ever do passes through it.

seccomp's defining move follows directly: if the [[system-call]] is the single gate, then
placing a **checkpoint inside that gate** bounds the process completely. seccomp is not a new
gate and it is not the [[system-call]] mechanism itself (that is the prerequisite). It is a
**filter the kernel consults on every [[system-call]] before dispatching it** — a guard who
reads each note slid under the door and decides whether the kernel is even allowed to act on
it. Once installed, the filter is **irrevocable** and is **inherited** by any child process, so
the restriction cannot be shed by spawning a helper.

### What the filter is, and the verdict it returns

The filter is a small program — written in a restricted bytecode the kernel can run safely and
quickly (a form historically borrowed from packet-filtering, sometimes called BPF, *Berkeley
Packet Filter*). For our purposes the only thing that matters is what it computes. On every
[[system-call]] the process attempts, the kernel runs this filter and hands it the syscall
number (and, if the filter chooses, the call's arguments). The filter inspects them and returns
exactly one **verdict**:

- **Allow** — the [[system-call]] proceeds normally; the kernel dispatches it as if seccomp were
  not there.
- **Return an error** — the kernel does **not** perform the service. Instead it makes the
  [[system-call]] fail immediately, putting an error code into the return register. The
  conventional code here is `EPERM` ("operation not permitted"). Recall from [[system-call]]
  that failure already rides home through the same return channel as success, as a negative
  value the caller reads as an error — so the program sees an ordinary "permission denied" and
  the kernel did no work.
- **Kill** — the kernel terminates the offending process on the spot, on the theory that a
  process attempting a forbidden [[system-call]] is either exploited or broken and should not be
  allowed to continue.

A filter is typically written as an **allowlist**: name the handful of [[system-call]]s the
program legitimately needs, allow those, and give everything else the error-or-kill verdict.

### Why it works: bounding power by bounding the gateway

The justification is the attack-surface argument, and it is worth stating precisely. The
kernel exposes roughly **350** distinct [[system-call]]s. Any given program uses only a small
subset — a typical service might genuinely need a few dozen (reading and writing file
descriptors, allocating memory, exiting). The remaining hundreds are, for that program, pure
**surface**: code paths the program never intends to use but which a compromised version of it
*could* invoke. Several of those unused [[system-call]]s lead to genuinely dangerous kernel
operations — rebooting the host, mounting filesystems, replacing the running kernel, loading
modules, or attaching a debugger to another process.

Here is the key insight. An exploit does not get to invent new powers; it can only reach the
kernel the way every program does — through a [[system-call]]. An attacker who hijacks a process
and wants to, say, load a malicious kernel module *must* issue the [[system-call]] that does so.
If a seccomp filter has already forbidden that [[system-call]], the attacker's path is severed
**before the kernel does any work**: the dangerous service is never reached, regardless of how
cleverly the process was compromised. seccomp does not try to detect attacks; it removes the
*reachable* dangerous operations from the process's vocabulary entirely. A capability the
process can no longer name is one no exploit through that process can use.

This is also why seccomp is described as a **defense-in-depth** layer for containers. (A
container is just a name for an ordinary process to which several kernel-level restrictions have
been applied together — among them seccomp.) Even if other isolation layers are bypassed, a
process whose seccomp filter forbids the dangerous [[system-call]]s still cannot reach them. As
a concrete reference point, Docker installs a **default** seccomp profile that blocks roughly
**60** dangerous [[system-call]]s — `reboot()`, `mount()`, `kexec_load()` (replace the kernel),
`init_module()` (load a module), and so on — for every container, unless an operator
deliberately relaxes it.

### A worked instance: a sandbox that allows four calls and denies the rest

Make it concrete with a small sandbox. It installs a seccomp filter that **allows** exactly
four [[system-call]]s and gives every other [[system-call]] the error verdict (`EPERM`):

- `read` — pull bytes from an already-open file descriptor.
- `write` — push bytes to an already-open file descriptor.
- `brk` — grow the process's heap (its memory allocator needs this).
- `exit` — terminate cleanly.

This is a genuine allowlist, not a degenerate one: it permits real work (the program can read
its input, compute, allocate memory, write its output, and quit) while excluding everything
else. Now trace two [[system-call]]s through it.

**An allowed call.** The sandboxed code calls `write` to emit a result. Following the
[[system-call]] mechanism: it loads `write`'s syscall number into the number register and
executes `syscall`. The CPU crosses into kernel mode and lands at the kernel's single entry
address — but **before** dispatching, the kernel runs the seccomp filter, passing it the number
for `write`. The filter checks its allowlist, finds `write`, and returns **Allow**. The kernel
proceeds exactly as the prerequisite describes: it dispatches to the `write` handler, does the
work, and returns the byte count in the result register. seccomp was invisible.

**A denied call.** Now suppose the sandboxed code is exploited and tries to escalate by calling
`reboot()` (to crash the host) or `mount()` (to expose the real filesystem). Steps are
identical at first — the process cannot know it will be refused, so it loads `reboot`'s syscall
number and fires `syscall`. The CPU crosses into kernel mode and lands at the same entry
address. The kernel runs the seccomp filter with the number for `reboot`. It is **not** on the
allowlist, so the filter returns the **error** verdict. The kernel does **not** dispatch to the
`reboot` handler — no shutdown is even attempted. Instead it makes the [[system-call]] fail at
once, placing `EPERM` in the result register. Control returns to the process, which reads its
result register and sees "operation not permitted." (Running `reboot` inside a default Docker
container produces exactly this: `Operation not permitted`, and no reboot happens.) Had the
filter chosen the **kill** verdict instead, the kernel would simply have terminated the process
at that point rather than returning an error.

The decisive observation: in the denied case the `syscall` instruction *did* fire and the CPU
*did* enter the kernel — yet the dangerous operation was **never performed**, because the
seccomp filter rendered its verdict *before* dispatch. An exploit whose plan required `reboot`,
`mount`, or `kexec_load` is dead on arrival: the [[system-call]]s it depends on are simply not
in the process's vocabulary anymore.

A process can report whether it is under such a filter: on Linux, reading its status shows a
`Seccomp` field — `0` means no filter is installed (every [[system-call]] is permitted), while
the filter mode reports a non-zero value, signaling that each [[system-call]] now passes the
guard first.

## Prerequisites

- [[system-call]]

## Sources

- `linux-internals-complete.html` — "Namespaces + cgroups
  aren't enough" (Seccomp defined as a syscall filter; Docker's default profile blocks ~60
  dangerous syscalls — `reboot()`, `mount()`, `kexec_load()`, `init_module()`; "the `syscall`
  instruction still fires, but the kernel immediately returns EPERM before doing any work"),
  the "Defense in depth — four layers" box (seccomp as the layer that means "can't call
  dangerous syscalls"), "What Docker actually does" (step 7: "Applies seccomp filter (blocks
  dangerous syscalls)"), and experiment "5 — See seccomp blocking a syscall"
  (`reboot` → `Operation not permitted`; `/proc/self/status` `Seccomp:` field with `0=disabled,
  2=filter mode`).
