---
id: clone
title: clone()
summary: clone() is the single Linux system call that creates a new task — and the surprising claim of this node is that it is the only one.
type: concept
tags: [os/process]
prereqs: [fork-exec, thread, system-call, virtual-memory, file-descriptor, namespace]
sources:
  - linux-internals-complete.html ("clone() — the real syscall behind everything", "Modern Linux actually uses clone(), not fork()", "Threads vs processes — it's all clone()", "task_struct")
status: explained
created: 2026-06-23
updated: 2026-06-29
---

# clone()

## Summary

**`clone()`** is the single Linux system call that creates a new task — and the surprising
claim of this node is that it is the *only* one. The everyday distinctions you know —
"making a process," "starting a thread," "launching a container" — are not three separate
kernel mechanisms but **one** call invoked with different **flags**. A flag is a single
on/off switch passed to `clone()`, and each flag answers one yes/no question: *should the
new task SHARE a particular resource with its creator, or get its OWN COPY of it?* Turn every
sharing flag **off** and the new task is a duplicate of the caller with its own private
memory and its own copies of the open files — which is exactly the `fork()` of
[[fork-exec]]. Turn the share-memory and share-files flags **on** and the new task runs
inside the caller's *same* memory — which is exactly a [[thread]]. Turn on a third kind of
flag that gives the new task its *own isolated view* of system resources, and you have the
first task of a container. The unifying insight is that the kernel represents *every* task —
process or thread alike — with the same internal record, so the only thing that ever differs
between them is the sharing pattern the flags select. Collapsing creation into one
flag-parameterized primitive is what lets Linux treat a thread as just a lightweight process
and build a container out of the very same call.

## Grounded explanation

### One record per task: why there is nothing to distinguish

Start from what the two prerequisites already established. [[fork-exec]] showed that a new
process is born when an existing one asks the kernel to duplicate it: `fork()` makes a
near-identical copy — same code, same memory contents, copies of the open file descriptors
(the small integers naming a task's open files and connections) — but with a fresh identity.
[[thread]] showed that a *thread* is a flow of execution that instead **shares** its
creator's memory and open files, keeping private only its own execution state, and made the
blunt claim we now cash out: a thread "is just a process that shares memory with another
process," and both are made by the *same* creation request.

Here is the fact underneath both. Inside the kernel, each task — whether you would casually
call it a process or a thread — is tracked by **one and the same kind of record**, a large
data structure the kernel calls a `task_struct`. That record holds everything the kernel
knows about the task: its identity number, whether it is running or sleeping, a pointer to
its memory map, a pointer to its table of open file descriptors, who created it, and more.
*Every* task on the system has exactly one such record; the kernel keeps a big list of them.
Crucially, the record looks the same for a "process" and for a "thread" — there is no
separate "thread record" and "process record." So the kernel has no two-things to tell apart
in the first place. What we *call* the difference between a process and a thread is entirely a
difference in how two of these identical records are *related*: do they point at the same
memory and the same open-files table, or at separate ones?

Because there is only one kind of record, it follows that there can be only one operation
that makes one. That operation is `clone()`.

### `clone()`: the one creation primitive, parameterized by flags

`clone()` is the [[system-call]] that creates a new task by making a new `task_struct`. By
itself that is unremarkable — what makes it the *universal* primitive is its argument: a set
of **flags**. A flag is a single switch, named in the source with the prefix `CLONE_`, and
each switch governs *one* resource of the new task. The switch chooses between two outcomes
the source states plainly:

- **SHARE** — the new task and its creator use the *same* one. A change made through one is
  seen through the other, because there is only one underlying thing.
- **OWN COPY** — the new task gets a *separate duplicate*. Afterward the two are independent;
  a change to one does not touch the other.

The two flags that matter most are the one governing **memory** (in the source, `CLONE_VM` —
"VM" for the task's [[virtual-memory]], its address space) and the one governing the **open
[[file-descriptor]]s** (`CLONE_FILES`). Each, set on, means SHARE that resource; left off, the new
task gets its own copy. So `clone()` is not a fixed behavior but a *dial*: you tell it,
resource by resource, what the child should share and what it should duplicate, and the new
`task_struct` is wired up accordingly. The familiar operations are simply three settings of
this dial.

A genuine wrinkle to name, because it trips everyone: the flag names are *not* consistent
about which direction "on" means. For memory and files, the flag *on* means SHARE
(`CLONE_VM` on = share memory). But for the third family of flags discussed below — the ones
whose names contain `NEW` — the flag *on* means the opposite: give the child its OWN fresh
copy. The word `NEW` in the name flips the sense. This is a quirk of Linux's naming, not a
deep fact; what stays constant underneath is that every flag still just picks SHARE-or-OWN
for one resource.

### The three settings: fork, thread, container

Now enumerate the cases — all three, so the worked instance below is not degenerate — by
reading off what each flag setting does to memory, files, and one more resource.

**Setting 1 — all sharing flags off: `clone()` becomes `fork()`.** With `CLONE_VM` off and
`CLONE_FILES` off, the new task gets its OWN COPY of the address space and its OWN COPIES of
the file descriptors. That is precisely the duplicate-the-caller behavior of [[fork-exec]]'s
`fork()`: a fully independent process-level copy that can later `exec()` a different
program. The source is explicit that ``fork()`` is a thin wrapper that calls `clone()` with
all the sharing flags off — so `fork()` is not a different mechanism, it is a *name* for one
configuration of `clone()`.

**Setting 2 — share memory and files: `clone()` makes a [[thread]].** Turn `CLONE_VM` *on*
and `CLONE_FILES` *on*. Now the new task runs in the *same* address space as its creator,
seeing the same variables, and through the same open files. That is exactly the
shared-everything arrangement [[thread]] defined: the new flow keeps private only its own
execution state (its own stack, registers, and program counter — the marker of which
instruction it is about to run), while memory and files are one shared world. A "thread" is
nothing more than `clone()` with these two share-flags on. This is why [[thread]] could
assert there is no deep boundary between thread and process: both are this one call, and the
boundary is which way two flags are set.

**Setting 3 — give the task its own isolated views: the first task of a container.** Beyond
sharing-or-copying memory and files, `clone()` offers the `NEW`-family flags (the source
names `CLONE_NEWPID`, `CLONE_NEWNET`, `CLONE_NEWNS`, and others). Each of these gives the new
task its OWN COPY of a **[[namespace]]** — a kernel object that gives a process an isolated
view of one category of system resource (its own slice of process IDs, network interfaces,
or filesystem tree, depending on the type). To make that concrete: the PID namespace governs *which set of
process-identity numbers a task can see and use*; the network namespace governs *which
network interfaces and addresses it sees*; the mount namespace governs *which filesystem
tree it sees*. Normally every task shares the system's default namespaces — one shared view
of all process IDs, one network, one filesystem tree. But `clone(CLONE_NEWPID | CLONE_NEWNET
| CLONE_NEWNS | ...)` builds the new task fresh copies of those views, so that *inside* its
world it might be the only process it can see, on its own network, looking at its own
filesystem — while still being an ordinary task on the host, running on the same kernel
through the same system calls. A task created this way is the first process of a container.
So a container, too, is not a new mechanism: it is `clone()` with the `NEW`-family flags on.

The point sharpens once all three sit side by side: process, thread, and container are not
three kinds of thing the kernel knows about. They are three settings of one dial. The kernel
internally distinguishes none of them — it is all the same `task_struct`, made by the same
`clone()`, differing only in the flags.

### The why: collapse creation into one flag-parameterized call

Why is this worth treating as its own idea, rather than three separate calls that happen to
share code? Because the *collapse itself* is the design contribution, and two capabilities
fall straight out of it.

First, **a thread becomes a lightweight process for free.** If thread-creation and
process-creation were different gadgets, the kernel would carry two schedulers, two records,
two sets of rules. Instead, because a thread is *the same* `clone()` with two share-flags
flipped, every piece of machinery the kernel already has for tasks — scheduling them onto
CPUs, accounting their time, waiting on them — applies to threads unchanged, with no
duplicate apparatus. The thread is "lightweight" precisely because it reuses the one task
mechanism and merely skips building a private address space.

Second, **containers cost almost nothing to invent.** Having one creation call that already
takes per-resource SHARE/OWN flags means isolation is just *more flags of the same kind*.
Adding the `NEW`-family did not require a new "container" subsystem in the creation path; it
required new flags on a call that was already flag-driven. That is why a container "starts in
milliseconds — just a `clone()` call": it is the ordinary task-creation primitive with a few
extra switches thrown, not a heavyweight separate construction.

The invariant that makes all of this sound is the one-record fact from the start: because
there is exactly one `task_struct` per task and exactly one `clone()` to make it, *every*
form of task creation is forced to be the same operation under the hood. The flags are the
only place variation can live. Unify creation into one primitive and the entire
"process vs. thread vs. container" zoo reduces to choosing what to share.

### Worked instance: the same call, three flag-vectors

Trace one creator task issuing `clone()` three times, changing only the flags, and read off
what each produces. Hold fixed that the creator owns some memory and some open files.

1. **`clone(flags = none)`** — every sharing flag off, no `NEW`-flag on. Memory: OWN COPY.
   Files: OWN COPY. Namespaces: shared with creator (default). Result: a fully independent
   duplicate of the caller — its own memory, its own copies of the descriptors. This is
   `fork()`; the child can now `exec()` a different program, exactly the two-step dance of
   [[fork-exec]]. If the creator next writes to one of its variables, the child does *not*
   see the change — separate memory.

2. **`clone(CLONE_VM | CLONE_FILES)`** — share-memory on, share-files on. Memory: SHARE.
   Files: SHARE. Namespaces: shared. Result: a new flow of execution inside the *same*
   program, with its own stack and registers but the creator's memory and files. This is a
   [[thread]]. Now if the creator writes 5 into a shared variable, this new task reads that
   same variable and sees 5 — the very behavior [[thread]] built its shared-counter example
   on. The single bit flipped versus case 1 (memory: OWN COPY → SHARE) is the *entire*
   difference between "a second process" and "a second thread."

3. **`clone(CLONE_VM | CLONE_FILES | CLONE_NEWPID | CLONE_NEWNS)`** — share memory and files
   with the creator, *but* take an OWN COPY of the PID-number view and the filesystem-tree
   view. Memory: SHARE. Files: SHARE. PID namespace: OWN. Mount namespace: OWN. Result: a
   task that shares some things with its creator yet sees a fresh, isolated set of process
   IDs and its own filesystem tree — the kind of partly-isolated task that a container's
   first process is built from. The three vectors differ only in their flags; the call, the
   resulting `task_struct`, and the kernel handling it are identical.

Read the three rows together and the claim is plain: one call, three flag-vectors, three
things we give three different names — process, thread, container — and *nothing else
differs*. That is what "it's all `clone()`" means.

## Prerequisites

- [[fork-exec]]
- [[thread]]
- [[system-call]]
- [[virtual-memory]]
- [[file-descriptor]]
- [[namespace]]

## Sources

- `linux-internals-complete.html` — section "clone() — the real syscall behind everything"
  (`fork()` and thread creation as flag-configurations of one universal `clone()`; per-resource
  SHARE vs. OWN COPY; the side-by-side `fork()` = sharing flags off, `thread` =
  `CLONE_VM | CLONE_FILES`, `container` = `CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS`; the
  inconsistent flag naming where `NEW` flips the sense; "it's all `task_struct`"), the
  "Modern Linux actually uses clone(), not fork()" note (`fork()` as a wrapper around
  `clone()` with all share flags off), the `task_struct` description (~6KB per-task record
  holding pid, state, memory map, files, parent, nsproxy/namespaces), and "Threads vs
  processes — it's all clone()" (a thread is a process that shares memory; both are the same
  `clone()` with different flags). Namespace meaning (PID/net/mount as isolated views, created
  by `clone()`) drawn from the same source's namespaces/containers discussion.
