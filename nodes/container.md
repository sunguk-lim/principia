---
id: container
title: Container
summary: A container is not a special kind of machine and not a tiny virtual computer.
type: concept
tags: [os/virtualization]
prereqs: [namespace, cgroup, vfs, system-call, overlayfs]
sources:
  - linux-internals-complete.html ("Combining them = a container", "What Docker actually does", "Build a container with raw commands", "Container vs VM — the fundamental difference")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Container

## Summary

A **container** is not a special kind of machine and not a tiny virtual computer. It is an
**ordinary process** — a running program the kernel schedules on the same CPUs as everything
else — that the kernel has wrapped in a *combination* of three features that already existed
on their own. [[namespace]]s give the process an isolated **view** (its own process numbers,
its own network, its own filesystem tree), so it cannot see the rest of the machine.
[[cgroup]]s give it resource **limits** (a ceiling on memory, a slice of CPU), so it cannot
consume the whole machine. And a layered root filesystem — built on the [[vfs]] — gives it its
own **"disk"**: a read-only image of files with a thin writable layer stacked on top, so each
container gets a private root directory without copying gigabytes of files. None of these three
is new; the word "container" is simply a name for **all three applied at once to one regular
process**. That combination is why a container starts in milliseconds and costs megabytes: it
shares the host's one kernel rather than booting a second operating system of its own.

## Grounded explanation

### The concept is a combination, not a new primitive

The single most important idea is this: **there is no "container" object inside the kernel.**
If you searched the kernel for a thing called a container, you would not find one. What you
would find are three independent mechanisms, each built years apart for its own reason, each
still used on its own today. A container is what you get when you point all three at the same
process at the same time. To understand a container, then, is to understand *which three* and
*what each contributes* — so we take them one at a time, then assemble.

**First, isolation — a [[namespace]].** Recall what a [[namespace]] does: it gives a process an
*isolated view* of one class of global resource, by having the kernel run its normal code and
then filter the answer according to which namespace the asking process belongs to. There are
several types — one isolates the space of process numbers (so the isolated process can be number
**1**, the root of its own little process tree, while the host sees it as some ordinary number),
one isolates the network (its own interfaces, ports, routing), one isolates the filesystem tree
(which directories are visible and where), one isolates the hostname, and so on. A container
puts its process into a fresh namespace of *each* type, so the process sees its own processes,
its own network, and its own mounts, and is blind to the host's. This is the answer to **"what
can this process see?"** — and the [[namespace]] node already shows it is cheap: just a small
bookkeeping object per isolated resource, no second kernel, no emulated hardware.

**Second, limits — a [[cgroup]].** Recall what a [[cgroup]] does: it names a *group* of
processes and attaches **caps** (ceilings) to it — a memory cap, a CPU cap, an I/O cap, a cap on
how many processes the group may spawn — which the kernel enforces at the moment the group asks
for the resource. Over the CPU cap, the group is *throttled* (paused until its quota refreshes,
because CPU time renews). Over the memory cap, the kernel performs an *out-of-memory kill*
scoped to that group (because held memory does not free itself, so a holder must be terminated).
A container puts its process into a cgroup with caps set, so it cannot starve the rest of the
machine. This is the answer to **"how much can this process use?"** — the budget, enforced.

Notice that these first two are *orthogonal*, exactly as the prerequisites stress: a
[[namespace]] controls **visibility**, a [[cgroup]] controls **quantity**. They were designed
independently and are used independently. A container is one place they happen to be combined,
not the reason either exists.

**Third, a private root filesystem — built on the [[vfs]].** A process needs files: the
program to run, its libraries, its configuration. We want each container to see its *own* root
directory — its own `/bin`, `/etc`, `/lib` — without physically copying those files for every
container, which would be slow and waste disk. The solution is a **layered filesystem**, and it
is exactly the kind of thing the [[vfs]] makes possible. Recall the [[vfs]]: the kernel layer
that presents one uniform set of file operations (`open`, `read`, `write`) over many different
backends, by routing each call to the backend that owns the file. One such backend is a
*stacking* filesystem (its common implementation is [[overlayfs]], mentioned here only as a
name): it presents a single directory tree assembled from **two layers stacked on top of each
other** — a **read-only lower layer**, the shared image of files that may be common to thousands
of containers, and a thin **writable upper layer**, private to this one container. When the
container *reads* a file, the [[vfs]] routes the read through the stacking backend, which returns
the file from the upper layer if present, otherwise from the shared lower layer. When the
container *writes* a file, the change goes into its private upper layer — the shared lower layer
is never touched, so other containers sharing it are unaffected. The container believes it has
its own full root disk; in reality it shares one read-only copy and owns only its own changes.
This is the answer to **"what disk does this process have?"** — a private root, built by
stacking, with no bulk copying.

### The why: a container is light because it shares the host kernel

Now the central justification — why anyone bothers to combine these three rather than reaching
for the older, heavier tool that also gives isolation: the **virtual machine (VM)**.

A VM achieves isolation at a *lower* layer. A piece of software called a **hypervisor** carves
the physical hardware into slices and runs, inside each slice, a *complete second operating
system* — its own kernel and all — under the illusion of having its own hardware. That is strong
isolation: the guest has its own kernel, so a bug in the guest's kernel cannot reach the host's.
But it is expensive. The guest operating system must be shipped (gigabytes), it must **boot**
(seconds to minutes), and the host must keep an entire duplicate kernel and emulated hardware
running for it. You are, in effect, shipping a whole computer.

A container makes the opposite trade. It does **not** run a second kernel at all — the contained
process is scheduled by the **host's one kernel**, on the host's CPUs, through the host's
[[system-call]]s, the same as every other process. The three mechanisms above only *change what that one
kernel reports and allows*: a [[namespace]] filters what the process sees, a [[cgroup]] caps what
it may use, the layered [[vfs]] root gives it its own files. Because there is no guest kernel to
boot, starting a container is essentially just starting a process in some fresh namespaces — it
happens in **milliseconds**, and it costs **megabytes** (only the process and its private upper
filesystem layer), not gigabytes. The price of this lightness is *weaker isolation*: since every
container shares the one host kernel, a flaw in that kernel can in principle affect all of them
at once, whereas a VM's separate kernel contains such a flaw. That is the whole trade — a
container is cheap precisely *because* it shares the kernel; a VM is heavy precisely *because* it
does not.

So the key insight, stated plainly: **a container is an ordinary process that has been given a
private view (namespaces), a budget (a cgroup), and a private root filesystem (a layered VFS
mount) — and nothing more.** It only *looks* like a machine; it is one line in the host's process
list.

### Worked instance: building one container by hand

Make it concrete by assembling a container from raw parts, with no container tooling involved —
which proves the point that a container is just the three features combined. Suppose you are a
shell on the host with a real, system-wide process number of, say, **5432**, and you want to run
a program (say an interactive shell, `bash`) as a container limited to **512 MB** of memory.

1. **Give it an isolated view (namespaces).** You ask the kernel to launch the program into
   three fresh [[namespace]]s at once — a new **PID** namespace, a new **mount** namespace, and a
   new **network** namespace. As the [[namespace]] node showed, the new process is the first
   member of its PID namespace, so when it asks the kernel "what is my number?", the kernel runs
   its usual code, consults the asker's PID namespace, and answers **1**. Inside, the process is
   PID 1, root of its own process tree, and can see no other processes. From the host's side the
   very same task is just an ordinary process with some number like **5440**. In its new network
   namespace it has its own near-empty network stack; in its new mount namespace it has its own
   set of mounts. (We deliberately leave its hostname namespace alone, so it still reads the
   *host's* hostname — a reminder that each switch is independent, and that we only flipped the
   ones we chose.)

2. **Give it a budget (a cgroup).** You create a [[cgroup]] and write `memory.max = 512M` into
   it — a number written into a file, as the [[cgroup]] node described — then place this process
   into the group. Now the kernel will enforce the 512 MB ceiling: as long as the process and any
   children stay under 512 MB, allocations succeed; if they try to exceed it, the kernel performs
   an out-of-memory kill *scoped to this cgroup* — terminating a holder inside the group to force
   memory back, never touching the host's other processes. The container literally cannot grow
   past half a gigabyte, no matter what it does.

3. **Give it a private root (a layered VFS filesystem).** You hand it a **stacked** root
   directory: a shared, read-only lower layer holding a base system image (a `/bin`, `/lib`,
   `/etc` shared with other containers) and a private, empty writable upper layer for this one.
   You make that stacked tree the process's root directory. Now every file operation it issues
   goes, through the [[vfs]], to the stacking backend: reads come from its upper layer if present
   else the shared lower layer; writes land only in its private upper layer. It sees a complete
   root filesystem and can modify it freely, yet not one byte of the shared image was copied to
   create this container, and nothing it writes is visible to any other container.

4. **Step back and see what you built.** You now have a single ordinary process that (a) thinks
   it is PID 1 on a quiet machine of its own, with its own network and mounts, (b) is hard-capped
   at 512 MB of memory, and (c) has its own root filesystem stacked over a shared image. It boots
   nothing — there is no second kernel; it started in milliseconds as a plain process launch. It
   weighs almost nothing — only itself plus its small writable layer. To the host, it is task
   **5440** in the process list, scheduled by the one host kernel beside everything else. That is
   a container, and you assembled it from exactly three pre-existing pieces: a [[namespace]]
   (view), a [[cgroup]] (limit), and a layered [[vfs]] root (disk). The popular container tools
   (Docker and the like) do precisely these same steps for you and add a convenient image format
   and command line on top — but the kernel work, and therefore the concept, is just this
   combination.

### What a container is *not*

To pin the concept down by its boundary: a container is *not* a virtualization technology in the
VM sense — there is no hypervisor, no guest kernel, no emulated hardware. It is *not* a single
kernel feature — the kernel has no "container" object; remove any one of the three pieces and you
have something less than a container (a process with limits but no isolation, or with isolation
but no private files). And it is *not* the same as the tooling that builds it — the three
mechanisms predate that tooling by years and are used independently all the time (an init system,
for instance, puts ordinary services into [[cgroup]]s with no isolation at all). The container is
exactly the union: one regular process, an isolated view, a resource budget, and a layered root.

## Prerequisites

- [[namespace]]
- [[cgroup]]
- [[vfs]]

## Sources

- `linux-internals-complete.html` — sections "Combining them = a container" (a container is the
  combination of namespaces + cgroups + a layered filesystem applied to one regular process; the
  features predate the tooling), "What Docker actually does" (the concrete sequence: set up the
  layered root, create a cgroup with `memory.max=512M`, launch into new PID/net/mount namespaces,
  the result being one regular process — same kernel, same CPU), "Build a container with raw
  commands" (assembling the same thing by hand: fresh PID/mount/network namespaces, the host
  hostname still showing through the un-isolated switch, the cgroup memory cap), and "Container
  vs VM — the fundamental difference" (a container shares the host kernel and starts in
  milliseconds with low overhead, whereas a VM runs its own kernel via a hypervisor and boots in
  seconds — the lightness-for-isolation trade).
