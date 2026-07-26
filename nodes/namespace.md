---
id: namespace
title: Namespace
summary: A namespace is a kernel feature that gives a process (and the children it creates) an isolated view of one class of system resource — so the process sees only its own slice of…
type: concept
tags: [os/virtualization]
prereqs: [process]
sources:
  - linux-internals-complete.html ("Namespaces — isolation that already existed", "Combining them = a container")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Namespace

## Summary

A **namespace** is a kernel feature that gives a [[process]] (and the children it
creates) an *isolated view* of one class of system resource — so the process sees only
its own slice of that resource and is blind to everything else of the same kind on the
machine. The kernel keeps one global pool of each such resource (the running processes,
the network interfaces, the filesystem tree, the hostname, and so on). Normally every
process shares the same view of each pool. A namespace breaks that sharing for *one*
resource class: the process inside it gets a fresh, private instance of that pool. The
striking part is that the kernel does not run different code for it — it runs the *same*
code, then filters the answer according to which namespace the asking process belongs to.
This is how you make a [[process]] believe it has a machine to itself without any
virtualization, and it is the *isolation* half of what people call a "container."

## Grounded explanation

### What problem a namespace solves

Recall what a [[process]] is: a running instance of a program, to which the kernel grants
private memory, its own open files, and a unique numeric identity (its PID, the
process identifier). That privacy covers the resources the kernel hands out *per process*.
But many important resources are not per-process — they are *global*, shared by every
process on the machine:

- the set of all running processes (and therefore the whole space of PID numbers);
- the network — the interfaces, the routing rules, the port numbers;
- the filesystem tree — the single hierarchy of directories every process navigates;
- the machine's hostname;
- the channels processes use to talk to each other directly (shared-memory regions and
  the like);
- the table mapping user-identity numbers to the privileges they carry.

On an ordinary system there is exactly *one* of each of these, and every process looks at
the same one. That sharing is usually fine, but sometimes you want a [[process]] to be
unable to see or touch the rest of the machine's instance of one of these resources — for
security (a sandbox), for separation (two tenants on one server), or to fool a program
into thinking it owns the whole box. A namespace is precisely the kernel mechanism that
delivers that: an *isolated view of one global resource class*.

### The defining idea: a private instance of one global pool

A namespace is a kind of container — in the literal sense of "a box that holds members"
— for one resource class. (Set aside the software product also called a "container"; that
is a separate, larger idea built partly out of namespaces, and is discussed only in plain
prose at the end.) The kernel defines several *types* of namespace, one per resource class
it knows how to isolate:

- a **PID namespace** isolates the space of process numbers;
- a **network namespace** isolates the network stack (interfaces, addresses, routes,
  ports);
- a **mount namespace** isolates the filesystem tree (which directories are visible and
  where);
- a **UTS namespace** isolates the hostname;
- an **IPC namespace** isolates inter-process communication channels (shared memory,
  semaphores);
- a **user namespace** isolates the mapping of user-identity numbers to privileges, so a
  process can be the all-powerful user (number 0, "root") *inside* while being an ordinary
  unprivileged user *outside*.

When the machine boots, the kernel creates **one initial namespace of each type** and every
process inherits all of them. So you have always been inside namespaces — there was just
one of each, so you never noticed, the way you are always in some time zone but only think
about it when two zones disagree. Isolation begins only when someone asks the kernel to
create an *additional* namespace of some type and place a [[process]] in it. From that
moment the process — and every child it spawns, since children inherit their parent's
namespaces — sees the *new* instance of that one resource, not the original.

Crucially, every [[process]] belongs to *exactly one* namespace of *each* type at all
times. Putting a process in a new PID namespace says nothing about its network or
filesystem view; those stay whatever they were unless separately changed. So isolation is
chosen resource-by-resource, like flipping independent switches.

### The why: same kernel code, filtered answer

Here is the one step that looks like magic, and the identity that dissolves it. You might
expect that "isolating" a resource means running special isolated code. It does not. The
kernel runs the **exact same code** for an isolated process as for any other. The only
difference is that, just before returning a result, the kernel checks *which namespace the
caller is in* and adjusts the answer to that namespace's instance of the resource.

Think of a hotel receptionist who hands every guest a different list of room numbers — not
because there are different hotels, but because each guest is configured to see a different
slice. The building is one; the *view* is per-guest.

Concretely: when any process asks "what is my process number?", it makes the same request
into the same kernel routine. The kernel looks at the asker's PID namespace and answers
with the asker's number *within that namespace*. A process in the original namespace gets
its real, system-wide number; a process that is the first member of a fresh PID namespace
gets the number **1** — because inside its own private process-number space it really is
the first process, the root of its own little process tree. (Recall from [[process]] that
every system's process tree is rooted at PID 1, the first process the kernel starts; a new
PID namespace simply gives the isolated process its *own* PID-1 root.) Same request, same
code, two different truthful answers — because "the process number" is only defined
*relative to a namespace*.

This is also why a namespace is cheap and why it provides isolation without
virtualization. There is no second kernel, no emulated hardware, no copied operating
system. A namespace is just a small bookkeeping object the kernel keeps in memory: a
member list, a unique identifier, a count of how many processes currently point at it, and
the resource-specific data (a PID namespace carries its own process-number counter
starting at 1; a network namespace carries its own routing table; and so on). Each
[[process]]'s kernel record holds pointers to the set of namespaces it belongs to; on a
normal system all those pointers lead to the same default objects, and creating a new
namespace just makes one new object and re-points one process at it. The kernel destroys a
namespace the instant its reference count falls to zero — that is, when the last process
in it has gone. The isolated process is, in every other respect, an ordinary [[process]]
scheduled on the same CPUs by the same kernel.

It is worth stressing — because the history makes the point — that namespaces long predate
the popular "container" tools. Mount namespaces appeared in 2002 to give hosting customers
separate filesystem views on a shared server; network namespaces let engineers test
routing in isolation; PID namespaces powered browser sandboxes years before such tools
existed. The kernel feature is the primitive; the tools are a convenience layer on top.

### Worked instance: launching a process into new PID, mount, and network namespaces

Make it concrete. Suppose you are a process on the host — say a shell with real,
system-wide PID **5432** — and you ask the kernel to start a new [[process]] that lives in
three fresh namespaces at once: a new **PID** namespace, a new **mount** namespace, and a
new **network** namespace. You leave its UTS namespace alone (do not give it a new
hostname) on purpose, so we can watch one switch stay *off* while the others are *on* —
that keeps the example non-degenerate by showing both the isolated and the
still-shared cases. Trace what the new process experiences versus what the host sees.

1. **Its process number.** The new process is the first member of its PID namespace, so
   when it asks the kernel for its own number the kernel — running the same routine as
   always, then consulting the asker's PID namespace — answers **1**. Inside, it is PID 1,
   the root of its own process tree. Yet the host is unchanged: from the host's original
   PID namespace the very same task is just another process with some ordinary number, say
   **5440**. *One task, two truthful numbers*, because each is relative to a different
   namespace. This is the key insight made tangible.

2. **The other processes.** When the new process lists all running processes, the kernel
   filters that list to its PID namespace. It sees only itself (PID 1) and any children it
   has started — perhaps just the process-listing command, PID 2. It cannot see, name, or
   send a signal to PID 5432 or any other host process; for it, they do not exist. The
   host, meanwhile, still sees its hundreds of processes including this one.

3. **Its filesystem.** Because it is in a new mount namespace, the set of mounted
   directories is its own. You can give it a different directory as its root, so it sees a
   private, smaller filesystem tree; mounting or unmounting things inside it does not
   disturb the host's tree, and vice versa.

4. **Its network.** In a new network namespace it starts with its own, near-empty network
   stack — its own interfaces, its own routing rules, its own set of ports — separate from
   the host's. None of the host's network connections are visible to it, and a port it
   opens does not collide with the host's ports. (To talk to anything it must first be
   given a connection into this private stack, but that wiring is a separate topic.)

5. **The switch left off.** When it asks the machine's hostname, it shares the host's UTS
   namespace, so it gets back the *host's* hostname — unchanged. This is the control case:
   the resources we isolated look private; the one we did not isolate looks shared. That
   contrast is the whole concept in one screen.

Step back and notice what just happened. With no virtualization — no second kernel, no
emulated hardware — a perfectly ordinary [[process]] has been made to believe it is PID 1
on a machine with no other processes, its own filesystem, and its own network, while
remaining, from the host's point of view, just task 5440 sharing the same kernel and CPUs.
The only thing that changed is *which instance of each resource the kernel reports to it* —
and only for the resources whose switch we flipped.

### Where a namespace sits relative to the bigger picture

Because the isolation is per-resource and built from cheap kernel objects, namespaces are
the *isolation* ingredient of what the industry calls a **container**. A container is not a
new kernel concept; it is a name for a *combination* — namespaces to control what a process
can **see**, plus a separate mechanism called **cgroups** to limit what it can **use**
(how much memory or CPU), plus a layered filesystem and some privilege restrictions, all
applied to one regular [[process]]. Each of those pieces existed and was used on its own for
years before container tooling packaged them together. Namespaces are specifically the part
that answers "what does this process see?" — and that is the whole of the concept here.
(Cgroups and containers are their own subjects.)

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — sections "Namespaces — isolation that already existed"
  (the eight namespace types; the "same kernel code, filtered response" mechanism; where
  namespaces physically live) and "Combining them = a container" (namespaces as the
  isolation half of a container).
