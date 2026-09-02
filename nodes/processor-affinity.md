---
id: processor-affinity
title: Processor Affinity
summary: Processor affinity restricts the CPUs on which a thread may run, trading scheduler freedom for stable cache and hardware locality.
type: concept
tags: [os/process]
prereqs: [thread, scheduler]
sources: [https://man7.org/linux/man-pages/man2/sched_setaffinity.2.html]
status: explained
created: 2026-09-02
updated: 2026-09-02
---

# Processor Affinity

## Summary

**Processor affinity** is the allowed set of CPUs on which a [[thread]] may execute. Restricting that set can preserve cache and hardware locality, while an overly narrow set can prevent the [[scheduler]] from balancing load.

## Grounded explanation

Normally the [[scheduler]] may migrate a runnable [[thread]] among CPUs to share work. An affinity mask changes the eligible set. If CPUs 0–3 are allowed, the scheduler may choose any of those four but must not run the thread on CPU 4.

### Worked example

Suppose a worker alternates between CPU 1 and CPU 9 on a two-socket machine. Its hot data repeatedly leaves one socket's caches and is fetched near the other. Setting the worker's affinity to CPUs 0–3 keeps it on one side, reducing migration and making its hardware neighborhood stable. If all eight workers are pinned only to CPU 0, however, they serialize there while other CPUs sit idle. Affinity establishes a boundary; it does not choose a good boundary automatically.

Affinity can be a hard restriction or a preference depending on the system interface. The key trade-off is locality versus flexibility. Measure both run-queue contention and memory/device distance before treating pinning as an optimization.

## Prerequisites

- [[thread]]
- [[scheduler]]

## Sources

- Linux `sched_setaffinity(2)` manual — CPU masks and scheduler restrictions.
