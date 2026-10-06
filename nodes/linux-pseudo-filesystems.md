---
id: linux-pseudo-filesystems
title: Linux Pseudo-Filesystems
summary: Linux pseudo-filesystems such as procfs and sysfs present kernel and device state as paths whose contents are generated or mediated by the kernel rather than stored as ordinary disk files.
type: concept
tags: [os/filesystem]
prereqs: [vfs, kernel]
sources: [https://docs.kernel.org/filesystems/proc.html, https://docs.kernel.org/filesystems/sysfs.html]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Linux Pseudo-Filesystems

## Summary

`/proc` and `/sys` look like directories, but they expose kernel-managed views of live state. The [[vfs]] lets programs open and read them through familiar file operations; the [[kernel]] supplies their values. They are not a backup location for durable application data.

## Grounded explanation

procfs exposes process information and selected system controls. For example, `/proc/<pid>/status` describes a current process, while `/proc/meminfo` reports memory counters. The set of process paths changes as processes start and exit. Reading a file is a snapshot-like observation, not an atomic picture of the whole machine. Access can also be limited by permissions and mount options.

sysfs represents kernel objects, devices, drivers, and attributes under `/sys`. A device's attributes may be readable or writable depending on the kernel interface and permissions. These paths can change with hardware, kernel versions, or namespace context. Writing an exposed attribute can have an immediate effect; treat it as an operation, not as editing a normal text document.

A useful diagnostic distinction is *observation versus storage*. If a service reports a missing device, inspect the relevant `/sys` entry and the process's view of the device, but do not copy `/sys` as if it were a durable file tree. If CPU or memory counters seem inconsistent, record timestamps and read the documented field semantics before comparing them. Containers can mount restricted or virtualized views, so the path visible to one process may not describe the entire host.

Validate a diagnosis by checking the official kernel description for the specific file, the running kernel and mount namespace, and a second observation such as process logs or device state. Avoid assuming that a field is stable merely because its path is stable.

## Prerequisites

- [[vfs]]
- [[kernel]]

## Sources

- [Linux kernel, procfs documentation](https://docs.kernel.org/filesystems/proc.html)
- [Linux kernel, sysfs documentation](https://docs.kernel.org/filesystems/sysfs.html)
