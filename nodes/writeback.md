---
id: writeback
title: Writeback
summary: Writeback is the deferred flushing of dirty pages from the page-cache out to persistent disk.
type: concept
tags: [os/filesystem]
prereqs: [page-cache, kernel-thread, dma, interrupt]
sources:
  - linux-internals-complete.html ("Writing — not what you think")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Writeback

## Summary

**Writeback** is the deferred flushing of *dirty* pages from the [[page-cache]] out to
persistent disk. Recall from [[page-cache]] that an ordinary `write` does **not** put your data
on disk: the kernel copies the bytes into the cached RAM page, marks that page **dirty**
(changed in RAM but not yet matching disk), and `write` returns in microseconds — the data is
still only in volatile memory. Writeback is the *separate, later* act that actually carries those
dirty pages to disk and marks them **clean** (RAM and disk now agree). It is performed by
dedicated background kernel threads (historically called *flusher* threads) and is triggered by
one of three things: **time** (a page that has been dirty longer than a threshold, on the order
of 5–30 seconds, is due to be written), **memory pressure** (the kernel needs to reclaim RAM and
must first save any dirty pages it wants to evict), or an **explicit `fsync`** (a program demands
its file be made durable *now* and blocks until writeback of that file's dirty pages completes).
The reason for deferring rather than writing immediately is throughput: holding writes in the
cache lets the kernel **batch** many small writes into few large disk transfers, reorder them to
suit the disk, and absorb bursts — a large speed win. The price is durability: a crash or power
loss in the gap between `write` and writeback loses every un-flushed dirty page, which is why
durability-critical programs call `fsync`.

## Grounded explanation

### What writeback is, and what it is not

The [[page-cache]] node already establishes the read side and the *moment of the write*: the
cache holds file data in RAM, a `read` is served from the cache when possible, and a `write`
merely updates the cached page, marks it **dirty**, and returns at once. That is where the
page-cache story stops — the data is sitting in RAM, changed, owing a trip to disk. **Writeback
is that trip.** It is not the caching of reads, and it is not the `write` call itself; it is the
distinct, deferred process that takes the *outstanding* dirty pages and reconciles disk with RAM.

Two terms carry the whole concept, so fix them precisely. A cached page is **dirty** when its
contents in RAM have been modified but the disk copy has not yet been updated — RAM and disk
disagree, and RAM holds the truth. A page is **clean** when RAM and disk match — either it was
never modified, or its last modification has already been written out. Writeback is exactly the
transition **dirty → clean**: it writes the page's current RAM contents to the page's home
location on disk, and the moment that transfer is confirmed, the page is marked clean. A clean
page owes the disk nothing and can be dropped from RAM for free; a dirty page may **not** be
dropped until it has been written, because dropping it would destroy the only up-to-date copy.

### Who does it, and the three triggers

Writeback is not done by your program and not done inside `write`. It is done by **background
[[kernel-thread]]s** — long-lived threads inside the kernel whose job is to scan the cache for dirty
pages and push them to disk, asynchronously, while application code runs on undisturbed. The
actual transfer to the disk hardware is done by **[[dma]]** (direct memory access — the disk
controller copies the page's bytes straight from RAM to the storage device without the CPU
shuffling each byte), after which the device raises an [[interrupt]] to report completion and the
kernel marks the page clean.

What *starts* a writeback of a given dirty page is one of three triggers; each must be named
because each covers a different situation:

- **Time / age threshold.** The kernel does not let a page stay dirty forever. A flusher thread
  wakes periodically and writes out pages that have been dirty longer than a configured age — in
  practice on the order of 5 to 30 seconds. This bounds how much recent work is at risk and keeps
  the backlog of unwritten data from growing without limit. This is the "normal," unforced route.

- **Memory pressure.** The page cache occupies otherwise-free RAM (the [[page-cache]] point that
  it greedily uses idle memory). When a process genuinely needs RAM and the kernel must reclaim
  cache pages to satisfy it, it can discard *clean* pages instantly — but a *dirty* page it wants
  to reclaim must be **written out first**, because that page is the only current copy. So memory
  pressure forces writeback of the dirty pages standing in the way of reclamation, sooner than the
  age threshold would have.

- **Explicit `fsync`.** A program that needs its data on disk *right now* calls `fsync` on the
  file descriptor. Unlike the two background triggers, `fsync` is synchronous: it **blocks** —
  it does not return — until writeback of every dirty page belonging to that file has physically
  reached the disk. `fsync` is the program reaching in and demanding immediate writeback, then
  waiting for proof of completion.

### The why: batching for throughput, paid in durability

The natural question is why the kernel defers at all — why not write each page to disk the moment
it is dirtied, and avoid the whole risk? The answer is **throughput**, and it rests on how disks
behave. A disk trip is slow (milliseconds) and has large fixed overhead per request; the marginal
cost of moving *more* bytes in one trip is comparatively small. Deferring writes lets the kernel
exploit that asymmetry in three ways:

- **Coalescing.** If a program writes the same page many times in quick succession — common, e.g.
  appending to a log line by line — only the *final* state of that page needs to reach disk. A
  hundred `write`s to one page can become one disk write. Better still, a file written and then
  deleted before any writeback runs may **never** touch the disk at all.
- **Batching and reordering.** Many separate dirty pages accumulated over a few seconds can be
  written together in one efficient sweep, and the kernel can order them to suit the device
  instead of issuing a slow, isolated trip per `write`.
- **Burst absorption.** Real workloads write in bursts. Returning from `write` at RAM speed lets
  the application keep running while the burst drains to disk in the background, so the slow disk
  never becomes the application's pacing bottleneck.

The invariant that makes this safe *enough* is the age threshold: no dirty page outlives it by
much, so the window of unwritten data is bounded. But the trade-off is unavoidable and is the
sharp edge of the whole design: in the gap between a `write` returning and writeback completing,
the new data lives **only** in the dirty page in **volatile** RAM — memory whose contents are
lost when power is removed. If the machine crashes or loses power in that window, those un-flushed
dirty pages **vanish**, and the data is gone even though `write` reported success. A successful
`write` therefore promises *eventual* writeback under normal operation, **not** durability. The
only way to convert "in the cache" into "guaranteed on disk" is to force writeback and wait for
it — which is precisely what `fsync` does, and why a database calls `fsync` after committing a
transaction before it tells the client the commit succeeded.

### A worked instance: a 1 KB write and its three possible fates

Take a program that writes **1 KB** (1024 bytes) into an already-open file, and trace it against
a round disk cost of about **5 ms** per disk transfer versus about **5 µs** for a RAM copy — a
1000× gap.

**The write.** The program calls `write(fd, buf, 1024)`. The kernel finds (or allocates) the
single cached page covering that file region, copies the 1024 bytes into it, marks that page
**dirty**, and `write` **returns** — in microseconds. The program proceeds to its next line. At
this instant the new kilobyte exists *only* in that dirty RAM page; the disk still holds the old
contents. This is the page-cache write behaviour; nothing has been flushed yet.

Now the page sits dirty, and exactly one of three things happens to it — the three triggers,
each exercised:

- **Time route (the default).** No one forces anything. Roughly 5–30 seconds later a flusher
  thread wakes, sees this page has exceeded the dirty-age threshold, DMA-transfers its 1024 bytes
  to the disk (~5 ms), receives the completion interrupt, and marks the page **clean**. The data
  is now durable. The program never noticed and never waited.

- **Memory-pressure route (forced early).** Suppose two seconds after the write — *before* the
  age threshold — another process demands a large amount of RAM. The kernel decides to reclaim
  cache pages, but our page is dirty, so it cannot simply be dropped: the kernel **writes it out
  first** (~5 ms), marks it clean, and only then reclaims it. The same disk write happened, just
  earlier than the timer would have caused, driven by the need for memory.

- **`fsync` route (forced now, and waited on).** Suppose instead the program calls `fsync(fd)`
  immediately after the `write`. `fsync` triggers writeback of this file's dirty page at once and
  **blocks** — it does not return — for the ~5 ms until the DMA transfer completes and the page is
  clean. Only then does `fsync` return, and only now may the program treat the kilobyte as
  durable. This route costs the program the full disk latency, by design: that wait is the
  durability guarantee.

**The crash case, against all three.** If, in the time route, power fails one second after the
`write` — before any flusher thread ran — the dirty page was only in volatile RAM, so the
kilobyte is **lost**; on reboot the file holds its pre-write contents, even though `write` had
returned success. Had the program taken the `fsync` route and the crash come *after* `fsync`
returned, the kilobyte would survive — that is the entire reason `fsync` exists. The instance is
non-degenerate because it actually runs each of the three triggers to a different outcome (timed
flush, forced-early flush, and forced-and-waited flush) and shows the un-flushed window where a
crash still loses data.

## Prerequisites

- [[page-cache]]
- [[kernel-thread]]
- [[dma]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "Writing — not what
  you think": `write(fd, data, len)` copies the data into the page cache and marks the pages
  **dirty** (modified but not yet on disk), then returns immediately, so the data is in RAM not on
  disk; a kernel thread called **writeback** periodically flushes dirty pages to disk in the
  background ("Later (5–30 seconds): [writeback] kernel thread wakes up → finds dirty pages → DMA
  transfer to disk → marks pages as clean"); or `fsync(fd)` forces it, blocking until all dirty
  pages for that file are on disk (databases such as PostgreSQL and MySQL call `fsync` after every
  transaction); and a power loss before the flush loses the recent, still-in-RAM writes. Supporting
  detail from the same document: the page's **dirty bit** ("has this page been written to?") and
  the experiment reading `/proc/meminfo` showing `Dirty:` (data in page cache not yet written) vs
  `Writeback:` (data currently being written to disk). Memory pressure as a writeback trigger
  follows from the page-cache fact that the cache uses free RAM and dirty pages cannot be reclaimed
  until written.
