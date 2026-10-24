---
id: origin-private-file-system
title: Origin-Private File System
summary: The origin-private file system provides browser-managed persistent byte storage scoped to a web origin, with quota and lifecycle constraints distinct from working memory.
type: concept
tags: [web/storage]
prereqs: [http, memory-hierarchy]
sources: [https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system]
status: explained
created: 2026-10-25
updated: 2026-10-25
---

# Origin-Private File System

## Meaning

The origin-private file system (OPFS) stores files in browser-managed storage private to a web origin. An origin is the scheme, host and port identifying a web security scope, not a user's account. Private here means a separate browser-managed namespace, not encryption, a secret vault or proof that every script running in that origin is trustworthy.

## Mechanism

A page obtains its OPFS directory and accesses named files through browser handles. The browser controls physical backing and quotas; a logical file need not correspond one-to-one to a user-visible disk file. The [[http]] origin serving the application determines the namespace. Another host or port can see a different store even on the same machine.

OPFS is storage, not GPU residency. [[memory-hierarchy]] distinguishes persistent capacity from live host and device buffers. Reading part of a model into memory still consumes memory and I/O bandwidth. Synchronous access handles are available in workers to avoid blocking the main page; main-thread file operations use asynchronous interfaces. Check actual bytes read or written and handle interruption rather than assuming one call transfers the requested range.

## Worked example

An application wants 12 GiB of model files. The browser reports a 15 GiB quota with 5 GiB already used. The estimated remaining space is 10 GiB, insufficient for the full download even though the physical disk may have hundreds of GiB free. If a replacement needs old and new versions to coexist, a nominal 8 GiB artifact can require more than 8 GiB of free quota during staging. Storage estimates can change; allocation errors remain authoritative.

Keep a version manifest, complete-download marker and integrity checks before treating a stored artifact as ready. Site-data clearing deletes OPFS, and browser eviction or policy can affect persistence. Explain retention and recovery rather than making it the only unrecoverable copy. Test quota exhaustion, partial downloads, interrupted writes, origin changes and restart behavior. Persistent local weights avoid repeated network downloads only while the correct files remain available; they do not eliminate per-inference disk reads or GPU transfer costs.

## Check your understanding

Does a large OPFS file imply equally large resident RAM or VRAM? No. Storage capacity and the live working set are different budgets.

## Prerequisites

- [[http]]
- [[memory-hierarchy]]

## Sources

- <https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system>
