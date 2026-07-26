---
id: init-process
title: Init Process
summary: The init process is the first process that runs in userspace — the very first ordinary program the kernel launches at the end of boot — and it is given the identifier PID 1.
type: concept
tags: [os/kernel]
prereqs: [process]
sources:
  - linux-internals-complete.html ("PID 1 starts — the first process", "Wait — is the kernel a process? Is it PID 1?", "Every process has a parent")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Init Process

## Summary

The **init process** is the first [[process]] that runs in userspace — the very first
ordinary program the kernel launches at the end of boot — and it is given the identifier
**PID 1**. ("Init" is short for *initialization*; "PID" is the unique number that names a
[[process]].) The kernel creates this one [[process]] by hand; from then on every other
[[process]] is a descendant of it, so the whole running system is a single family tree with
PID 1 at the root. Init has three defining jobs. **First**, it launches and watches over all
the system's background services — networking, logging, remote login, and so on (on modern
Linux the program that does this is called `systemd`). **Second**, it is the **reaper of
orphans**: when a [[process]] dies before collecting its child's exit result, that abandoned
child is handed to PID 1, which collects the result so the child does not linger forever as a
zombie. **Third**, it is special to the kernel itself — if PID 1 ever exits, the kernel
**panics** (stops the whole machine), because the system has no root and no final backstop
without it.

## Grounded explanation

### What init is, and why something has to be first

Recall from [[process]] two facts that this node rests on entirely. (1) A [[process]] is a
running program that the kernel creates, tracks in its process table, and names with a unique
number, its **PID** (process identifier). (2) Every [[process]] is created by another
[[process]] — its **parent** — so following "who created me" links upward, all [[process]]es
trace back to one root with no parent of its own, called **PID 1**. The [[process]] node
named that root but did not say *what it is* or *what it does*; that is this node's subject.

Here is the puzzle that forces init to exist. If every [[process]] must be created by an
existing [[process]], then the very first one cannot be — there is nothing yet to create it.
So the kernel must create that first [[process]] *itself*, directly, as its final act of
booting, rather than by the usual "a [[process]] asks for a child" path. ("Booting" is the
startup sequence that runs when a computer is powered on; its last step is to hand control to
userspace.) The [[process]] the kernel starts this way is the **init process**, and the
kernel labels it **PID 1**. "Userspace" simply means the ordinary, unprivileged world where
normal programs run, as opposed to the kernel's own privileged code; init is a normal
userspace program — the kernel is *not* a [[process]] and has no PID. Init is special only in
the three ways below.

### Role 1 — it launches and supervises every system service

Once it is running, PID 1's first task is to bring the system to life: it reads its
configuration and starts all the long-running background programs the system needs. A
long-running background program of this kind is called a **service** (or *daemon*) — for
example the program that answers network logins, the one that records log messages, or the
one that runs scheduled jobs. Each [[process]] init starts is, by the rule from [[process]],
a *child* of PID 1. The services those children start are PID 1's grandchildren, and so on.
Because init is the first [[process]] and the ancestor of all of them, the entire set of
running [[process]]es forms one tree rooted at PID 1 — exactly the tree the [[process]] node
described. Init is the *root* of that tree, and it does not merely start the services and
forget them: it stays running for the whole life of the system and supervises them, which
matters for its second role. (On modern Linux the specific program serving as PID 1 is named
`systemd`; older systems used one called `init`. The name is incidental — the role is the
concept.)

### Role 2 — it is the reaper of orphans

This is the subtlest role, and it builds directly on the zombie lifecycle from [[process]].
Recall that chain: when a [[process]] exits, the kernel keeps a tiny record holding its
**exit status** (a small code saying whether it succeeded or failed). That finished-but-not-
cleaned-up [[process]] is a **zombie**. The record stays until the *parent* collects it by
asking the kernel for the exit status — an act called **reaping** the child. Only then is the
record freed and the PID reusable. A parent that never reaps leaves zombies piling up, each
holding a record and a PID forever.

Now the problem init solves. What if a parent [[process]] *dies before* its child, leaving no
one to reap that child when it eventually exits? Such a parentless child is an **orphan**. An
orphan with no one to reap it would, on exiting, become a zombie that *nothing* ever cleans up
— a permanent leak. The kernel prevents this by **reparenting**: the instant a child is
orphaned, the kernel rewrites that child's parent link to point at **PID 1**. Init is written
to accept these inherited children and to reap any of them that exits. So PID 1 is the
**reaper of orphans**: the guaranteed final parent that collects the exit status of any
[[process]] whose original parent abandoned it. This is *why* the tree invariant from
[[process]] always holds — "every live [[process]] has a valid parent, and every exited
[[process]] is eventually reaped" — because PID 1 is the catch-all parent that makes the
second half true even when the original parent vanishes.

### Role 3 — it is special to the kernel; if it dies, the kernel panics

The kernel treats PID 1 unlike any other [[process]] in one decisive way: **if PID 1 ever
exits, the kernel panics.** A **kernel panic** is the kernel's controlled halt of the entire
machine — it stops everything, because it has reached a state from which it cannot safely
continue. Why is the death of one [[process]] fatal when the death of any other is routine?
Because of the two roles above. PID 1 is the *root* of the [[process]] tree, so without it
the tree has no root and newly orphaned [[process]]es would have nowhere to be reparented;
and PID 1 is the *final reaper*, so without it the backstop that prevents permanent zombies is
gone. The system genuinely cannot function without that root and that backstop, so the kernel
refuses to limp along — it stops. This is the deepest reason init is special: not because of
what it computes, but because the kernel's own guarantees about the [[process]] tree depend on
PID 1 always being there.

### The why, in one line

Tie the three roles together. Every [[process]] needs a parent to eventually reap it, and the
tree of services needs a root to grow from. **PID 1 is simultaneously that root and that final
backstop.** Role 1 makes it the root all services descend from; role 2 makes it the reaper
that closes the lifecycle for every orphan; role 3 is the kernel enforcing that this root and
backstop can never go missing. Init is the single [[process]] the whole [[process]] model
leans on to stay consistent.

### Worked instance: a double-forking daemon, and the orphan it creates

Run a concrete case that triggers the reaping role rather than a degenerate one where the
parent is always present. Many services deliberately use a trick called a **double fork** to
detach themselves from whoever launched them, and that trick *produces an orphan on purpose* —
so it exercises role 2 exactly.

Suppose you start a service, and the [[process]] doing the launch is the service's
"setup" [[process]], say **PID 4000**.

1. **First creation.** PID 4000 asks the kernel to create a child — the actual worker that
   will do the service's job. The kernel assigns it a fresh PID, say **PID 4001**, and records
   its parent as 4000. (This "create a child" step is the ordinary [[process]] creation from
   the [[process]] node.)

2. **The setup process exits immediately.** Here is the deliberate move: PID 4000 now exits
   right away, on purpose, so that the launching command returns at once and the worker is left
   running on its own in the background. The moment 4000 exits, its child **PID 4001 becomes an
   orphan** — its parent is gone.

3. **The kernel reparents the orphan to PID 1.** As described in role 2, the instant 4001 is
   orphaned the kernel rewrites 4001's parent link to point at **PID 1**. From now on, as far
   as the kernel's records show, PID 1 is the parent of the worker.

4. **The worker runs, then exits.** PID 4001 does its job for as long as the service is needed,
   then eventually exits with an exit status meaning "success." Per the zombie lifecycle from
   [[process]], the kernel keeps 4001's record holding that exit status, and 4001 is now a
   **zombie** awaiting reaping.

5. **PID 1 reaps it — no lingering zombie.** Because PID 1 is now 4001's parent and is written
   to reap its inherited children, init asks the kernel for 4001's exit status. The kernel
   hands it over, frees the last record, and PID 4001 ceases to exist; its PID can be reused.
   No zombie is left behind. Had PID 1 *not* been the universal reaper, 4001 would have become
   a permanent zombie the moment it exited, since its original parent (4000) was long gone.

**Contrast — kill PID 1.** Now run the opposite case to see role 3. Suppose instead you manage
to make PID 1 itself exit (say, it crashes). There is no parent above PID 1 to reap it and no
root to reparent anyone to. The kernel does not pick a replacement; it **panics** and halts the
whole machine. The very same [[process]] whose disappearance is routine at PID 4001 is fatal at
PID 1 — and the difference is entirely the three roles above.

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — sections "PID 1 starts — the first process" (PID 1 is the
  first userspace process, ancestor of all others, started via `execve("/sbin/init")`; the Q&A
  "What if PID 1 dies?" → kernel panic, PID 1 as reaper and tree root), "Wait — is the kernel a
  process? Is it PID 1?" (init is a Ring-3 userspace process created by the kernel as its last
  boot step; the kernel itself is not a process), and "Every process has a parent" (the
  userspace tree rooted at PID 1 and reparenting of orphans).
