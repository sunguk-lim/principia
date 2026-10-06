---
id: linux-filesystem-hierarchy
title: Linux Filesystem Hierarchy
summary: The Linux filesystem hierarchy is a set of path conventions that separates host configuration, installed software, variable data, and transient runtime state beneath one root.
type: concept
tags: [os/filesystem]
prereqs: [vfs]
sources: [https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html]
status: explained
created: 2026-10-07
updated: 2026-10-07
---

# Linux Filesystem Hierarchy

## Summary

The filesystem hierarchy gives operators a starting map for *where a kind of file is expected*, not a promise that every application uses the same directory. The [[vfs]] presents paths under a single root even when those paths lead to different disks, mounts, or kernel-backed filesystems.

## Grounded explanation

The Filesystem Hierarchy Standard (FHS) distinguishes purpose and lifetime. `/etc` is for host-specific configuration. `/usr` contains shareable, mostly read-only software and data; `/usr/local` is a conventional place for locally installed software. `/var` holds variable state such as logs and service data. `/run` is runtime data that need not survive a reboot. `/home` holds ordinary users' homes, while `/root` is conventionally the root user's home. `/tmp` is temporary and must not be assumed durable. `/dev` exposes device entries; `/proc` and `/sys` expose kernel-backed information rather than ordinary persistent files.

A path name alone does not tell you where bytes live. A container can show a different root, a bind mount can place `/var/lib/app` on another volume, and a service can log to journald or a remote sink instead of `/var/log/app`. Distribution packages, service unit settings, and application configuration can override the expected path. FHS is therefore a search heuristic, not an inventory of the running host.

For a failed service, identify the actual process and service unit, inspect its effective configuration and mounts, then follow its configured paths. If `/var` is full, measure the filesystem and directory usage before deleting anything; do not assume logs are the only cause. For a persistence test, write a harmless test artifact through the service's configured data path, restart in a controlled environment, and verify where it appears and whether it survives. This separates path convention, mount mapping, access permission, and lifecycle.

## Prerequisites

- [[vfs]]

## Sources

- [Linux Foundation, Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html): normative purpose and hierarchy conventions; deployed systems may diverge.
