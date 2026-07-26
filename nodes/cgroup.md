---
id: cgroup
title: Cgroup
summary: A cgroup (control group) is a kernel feature that limits, accounts for, and prioritizes the resource usage of a group of processes — how much CPU time they may consume, how much…
type: concept
tags: [os/virtualization]
prereqs: [process]
sources:
  - linux-internals-complete.html ("Cgroups — resource limits that also existed independently", "Combining them = a container")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Cgroup

## Summary

A **cgroup** (control group) is a kernel feature that **limits, accounts for, and
prioritizes the resource usage of a group of [[process]]es** — how much CPU time they may
consume, how much memory they may hold, how much disk bandwidth they may use, even how many
[[process]]es they may create. You place one or more [[process]]es into a cgroup and attach
**caps** (ceilings) to it; the kernel then enforces those caps as those [[process]]es run.
The point is control over *quantity*: a cgroup is the knob by which the kernel partitions a
machine's finite capacity among groups of [[process]]es, so that one greedy group cannot
starve all the others.

## Grounded explanation

### The gap that cgroups fill

Recall what a [[process]] already is: the kernel's unit of *isolation and accounting*. The
kernel gives each [[process]] its own private memory and its own open files, and records in
that [[process]]'s table slot what it holds, so it can keep [[process]]es from touching one
another and can reclaim everything when one exits.

Notice what that does *not* give you: any ceiling on *how much* a [[process]] may take while
it is alive. A single [[process]] is free to keep requesting memory until the machine has
none left, or to spin on the CPU so hard that every other [[process]] barely runs, or to
fork (create children) without bound until the kernel's process table is full. Isolation
answers "can A read B's data?" (no). It says nothing about "can A consume so much that B
cannot make progress?" — and the answer, by default, is *yes*. That is the gap.

Worse, the natural unit of the problem is rarely a single [[process]]. A web service is
typically not one [[process]] but a *family* of them — a parent and the children it spawned
(the parent-child tree). You want to cap the **whole family** together: "this entire service
may use at most 512 MB," not "each of its [[process]]es may use 512 MB." The kernel needs a
way to name a *group* of [[process]]es and treat that group as a single accountable unit.
That named group, with its caps, is the cgroup.

### What a cgroup is, precisely

A **cgroup** is a kernel-maintained object with two parts:

1. **A membership set** — a list of [[process]]es that belong to this group. Every
   [[process]] on the system is in exactly one cgroup at a time; you move a [[process]] in
   by adding it to the group. When a [[process]] creates a child, the child starts out in
   the *same* cgroup as its parent, so an entire spawned family lands in one group
   automatically.

2. **A set of limits and counters, one per resource.** For each resource the kernel can
   control — CPU time, memory, disk (block) I/O bandwidth, the number of [[process]]es — the
   cgroup holds (a) a **cap**, the maximum the group is allowed, and (b) a running
   **counter**, the amount the group is currently using. Define the terms once:

   - **memory cap** — the largest total amount of RAM (memory the [[process]]es are actively
     holding) the whole group may occupy at once.
   - **CPU cap** — a fraction of CPU time, expressed as "this group may use at most *X* units
     of CPU time out of every *Y* units of wall-clock time." A cap of "50,000 out of 100,000"
     means the group may run on a CPU for at most half of every period — i.e. **50% of one
     CPU's time**.
   - **I/O cap** — a ceiling on bytes-per-second the group may read from or write to a disk.
   - **PID cap** — the maximum number of live [[process]]es the group may contain at once (a
     [[process]] identifier, the PID, is the per-[[process]] number from the prerequisite;
     capping their *count* bounds how many the group can spawn).

The kernel exposes this object as a **directory** in a special filesystem (conventionally
under `/sys/fs/cgroup/`). The directory's name is the cgroup's name; the caps are plain text
files inside it. To set the memory cap you literally write the number into a file
(`memory.max`); to read current usage you read a file (`memory.current`). No special
programming interface is needed — controlling a group of [[process]]es is just reading and
writing small files, which is why a cgroup is easy to inspect and script.

### How the kernel enforces caps — the two mechanisms that matter

A cap would be meaningless if the kernel did not *check* it. Enforcement happens at the two
moments where a [[process]] asks for the resource, and it takes two distinctly different
shapes depending on the resource — this contrast is the heart of the concept.

**CPU: throttling (reversible delay).** The kernel constantly decides which runnable
[[process]] to put on a CPU. Before letting a group's [[process]] run, it checks that
group's CPU counter against its CPU cap *for the current period*. If the group has already
used its whole quota this period, the kernel does not run it — it **throttles** it: marks
the group as not-runnable until the next period begins, then lets it run again with a fresh
quota. CPU time is *renewable* (a new slice arrives every period), so over-use is punished by
*waiting*, never by death. The group simply runs slower than it wants; it always eventually
catches up.

**Memory: the OOM kill (irreversible).** Memory is different — it is *held*, not spent and
renewed. When a [[process]] in the group asks the kernel for more memory, the kernel checks
the group's memory counter against its memory cap. Under the cap, the request is granted.
Over the cap, there is no "wait until next period" — the memory the group is holding will not
free itself. So the kernel invokes the **OOM killer** ("out of memory"): it picks a
[[process]] *within that cgroup* and terminates it, forcing it to release its memory. Recall
from the prerequisite that when a [[process]] exits the kernel immediately reclaims its
memory; the OOM kill weaponizes exactly that reclamation. Crucially, the killer's blast
radius is confined to the *offending group* — it kills inside the cgroup that broke its own
cap, not random [[process]]es elsewhere. The over-using family pays for its own excess.

That asymmetry — CPU over-use is throttled (paused, reversible), memory over-use triggers a
kill (terminated, irreversible) — is not arbitrary. It follows directly from the nature of
each resource: time is renewable so you can make a group *wait*; held memory is not, so the
only way back under the cap is to *take it away* by killing a holder.

### The why: a knob to partition a machine fairly

Now the justification that ties it together. The kernel's broad job is to let many
[[process]]es share one machine without ruining one another. Isolation (the [[process]]'s
private memory) handles *interference by access*. But on a shared machine — a server running
many services, a cloud host running many customers' workloads — there is a second danger:
*interference by consumption*. One runaway group of [[process]]es, through no malice, can hog
all the CPU or eat all the memory, and every other group grinds to a halt. There was no
built-in defense against that.

The cgroup is precisely that defense: a unit the kernel can attach a *budget* to, and a
guarantee that the budget is enforced at the moment of use. With caps in place, the machine's
capacity is **partitioned**: each group is promised it will not be drowned out, and each
group is prevented from drowning out the rest. This is the foundation of resource limits in
modern systems — the per-service limits an init system applies to every background service,
and the per-customer CPU and memory quotas a cloud provider sells, are all cgroup caps
underneath.

It is worth stating what a cgroup deliberately is *not*. There is a separate, orthogonal
kernel feature — **namespaces** — that controls what a [[process]] can *see*: which other
[[process]]es, which files, which network it perceives as existing. Namespaces are about
*visibility* (isolation); cgroups are about *quantity* (limits). They were designed
independently, for different purposes, and are used independently: an init system puts every
service in its own cgroup with no isolation at all. The well-known "container" is simply the
*combination* — a [[process]] given both restricted vision (namespaces) and a resource budget
(a cgroup) at once. But the cgroup half stands on its own; it is the budget, nothing more.

### Worked instance: a worker pool capped at 512 MB and half a CPU

Make it concrete. You run a batch service: a parent [[process]], call it PID **800**, that
spawns four worker children — PIDs **801, 802, 803, 804** — to crunch data. You want the
*whole pool* to use at most **512 MB of memory** and **50% of one CPU**, so the database and
the shell on the same machine stay responsive. Trace it.

1. **Create the group and set caps.** You make a cgroup named `workers` and write its caps:
   `memory.max = 512M`, and a CPU cap of "50,000 out of 100,000" — meaning in every period of
   100,000 time-units the group may run for at most 50,000, i.e. **half of one CPU**. Both are
   just numbers written into files in the `workers` directory.

2. **Enroll the family.** You add PID 800 to `workers`. Because a child inherits its parent's
   cgroup, when 800 spawns 801–804 they *all* land in `workers` automatically. The cgroup's
   membership set is now {800, 801, 802, 803, 804}; its counters start near zero.

3. **CPU under load — throttling fires.** All four workers go full-tilt; left alone they would
   happily consume four whole CPUs. Each period, the kernel adds their CPU time to the group's
   CPU counter. Partway through every period the counter hits 50,000 — the cap. The kernel
   **throttles** the group: 801–804 are made not-runnable and sit idle for the rest of that
   period, even though CPUs are free. At the next period the counter resets to 0 and they run
   again. Averaged over time the pool draws exactly **50% of one CPU**, never more — so the
   database and shell, in *their own* cgroups, keep their CPU and stay responsive. No
   [[process]] died; the workers just progress at half-a-CPU's pace.

4. **Memory over the cap — an OOM kill fires.** A bug makes worker 803 allocate without
   bound. The group's memory counter climbs: 300 MB, 480 MB, then 803 requests another 64 MB
   that would push the group past 512 MB. The kernel checks `workers`' counter against its cap,
   sees the request would exceed it, and — because held memory cannot be made to "wait" —
   invokes the **OOM killer scoped to `workers`**. It terminates 803. The instant 803 exits,
   the kernel reclaims 803's memory (exactly the prerequisite's clean-reclamation behavior),
   the group's counter drops back under 512 MB, and 800, 801, 802, 804 keep running. The kill
   stayed *inside* the offending cgroup: not one byte of the database's memory was touched.

5. **The rest of the system, untouched.** Throughout both events, every [[process]] *outside*
   `workers` ran as if nothing happened. That is the whole payoff: the pool was held to its
   budget — paused when it overspent CPU, pruned when it overspent memory — while the machine's
   remaining capacity was protected and fairly available to everyone else.

Notice how each piece earned its place: the *membership set* let "the worker family" be one
accountable unit; the *CPU cap* produced a reversible throttle because CPU time renews; the
*memory cap* produced an irreversible OOM kill because held memory does not; and the kill's
*scope* — the cgroup, not the machine — is exactly what keeps one group's excess from becoming
everyone's problem.

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — sections "Cgroups — resource limits that also existed
  independently" and "Combining them = a container".
