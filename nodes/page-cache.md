---
id: page-cache
title: Page Cache
summary: The page cache is the kernel's use of otherwise-idle RAM to hold recently or frequently used file data, kept in page-sized units (4 KB blocks), so that file I/O issued through the…
type: concept
tags: [os/filesystem]
prereqs: [page, vfs, inode, system-call]
sources:
  - linux-internals-complete.html ("Page cache — RAM as a disk cache", "Writing — not what you think", "The complete I/O chain")
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Page Cache

## Summary

The **page cache** is the kernel's use of otherwise-idle RAM to hold recently or
frequently used file data, kept in [[page]]-sized units (4 KB blocks), so that file I/O
issued through the [[vfs]] mostly lands in fast RAM instead of on slow disk. The motive is a
raw speed gap: reading from RAM takes microseconds, while reading from a disk takes
milliseconds — roughly a thousand times longer. So when a program does `read` on a file, the
kernel first checks whether the file's pages are already sitting in the cache. If they are (a
**cache hit**), it copies straight from RAM and never touches the disk; if they are not (a
**cache miss**), it fetches them from disk, *keeps a copy* in the cache, and hands them back —
so the next read of the same data is a hit. Writing is the surprising half: a `write` normally
just updates the page in the cache, marks it **dirty** (changed in RAM but not yet on disk),
and returns immediately. The bytes are flushed to disk *later* by a background mechanism. A
successful `write` therefore does **not** mean the data is safely on disk — only an explicit
flush (the `fsync` call, discussed in plain prose below) forces that. The cache buys huge speed
and lets writes be batched, at the cost that un-flushed dirty pages are lost if the machine
crashes before they reach disk.

![Animated 15-step mechanism figure of the page cache, worked file report.dat (256 × 4 KB pages, fd = 3): a left CONTROL STRUCTURE panel steps through ACT I read #1 MISS (disk → cache → buf, all 256 blocks copied unchanged at ≈5 ms/block — the longest dwell), ACT II read #2 HIT (served from cache, no disk I/O), ACT III write 512 B (page 0 flips to v1 DIRTY in cache while disk block b0 still holds stale v0, returns instantly), then two mutually exclusive futures: IV-A writeback (writeback thread flushes p0, disk b0 becomes v1 = cache ✓ clean) vs IV-B crash first (power-loss bolt, dirty p0 LOST, disk stale forever). Three true-shape lanes — PROGRAM user space buffers, PAGE CACHE kernel RAM page slots with a resident-pages counter 0/256 → 256/256, DISK block device b0…b255 — are joined by two transfer tracks (cache↔buffer RAM ≈5 µs/copy; disk↔cache ≈5 ms/block) that light up while used; a legend keys every glyph (traced page 0, idle pages, absent/allocated slots, key-event accent, bytes in transit, transfer track, crash bolt, v0/v1).|960](page-cache.svg)

## Grounded explanation

### Where the page cache sits, and what it caches

Recall the two prerequisites. A [[page]] is the fixed 4 KB block in which the kernel manages
memory: memory is handed out, mapped, and accounted for one whole page at a time, never byte by
byte. The [[vfs]] is the kernel layer that receives every file system call — `open`, `read`,
`write`, `close` — on a descriptor and routes it to the backend that owns that descriptor (an
ext4 disk filesystem, a network share, a device, and so on). When the backend is a real disk
filesystem, the actual bytes live on a disk, and a disk is *slow*: a mechanical or even a
solid-state disk needs on the order of **milliseconds** to serve a block, because the request
has to leave the CPU, cross to the storage hardware, and come back. RAM, by contrast, is served
in **microseconds** — about a thousandfold faster.

The page cache is the kernel's answer to that gap. It is a region of RAM, organised in 4 KB
pages exactly like the rest of memory, in which the kernel keeps **copies of file data it has
recently moved between disk and a program**. It sits *beneath* the VFS interface: when VFS
forwards a disk-backed `read` to that filesystem's read routine, that routine consults the page
cache before it ever asks the disk for anything. The program above sees only the ordinary,
backend-independent `read` the VFS node describes; it has no idea a cache exists. The cache is a
pure optimisation hidden under the uniform interface.

One structural point matters before the mechanism. The cache uses **whatever RAM is otherwise
free** — it is not a small reserved buffer but a greedy occupant of unused memory. This is why a
freshly idle machine, after touching many files, reports very little "free" RAM and a large
amount classified as cache: that memory is *not* wasted, it is file data held speculatively, and
the kernel will instantly give it back the moment a process genuinely needs RAM. Holding the data
costs nothing — the RAM would otherwise sit empty — so the kernel holds as much as it can.

### Reading: hit and miss

Here is the read mechanism, and the *why* of each branch. Every term is defined as it appears.

A program issues a `read` [[system-call]] on a file-descriptor. VFS routes it to the disk
filesystem's read routine, which now asks one question: **are the requested pages of this file
already in the page cache?** Two cases, and they must both be enumerated because each exercises a different path:

- **Cache hit** — the pages are present. The kernel copies the bytes from the cache (RAM) into
  the program's buffer and returns. The disk is *never involved*. Time scale: microseconds. This
  is the common, fast case for any data touched more than once.
- **Cache miss** — the pages are absent (this happens the very first time anyone reads that
  region, or after the cache copy was evicted to make room). The kernel must go to disk: it
  allocates fresh page-cache pages to receive the data, asks the disk for the relevant blocks,
  waits while the disk transfers them *into those cache pages*, and then copies from the cache
  into the program's buffer. Time scale: milliseconds, dominated by the disk. The crucial extra
  step is that the data **stays in the cache** after the copy. The miss has thereby *populated*
  the cache, so the next read of the same region will be a hit.

The key insight — the reason this is worth doing at all — is that real workloads **reuse data**.
A program that reads a configuration file, a library, or a database index reads the same bytes
again and again; a directory listing, a recompile, a web server serving the same asset to many
clients, all re-touch the same files. The first touch pays the slow disk price *once* and seeds
the cache; every later touch rides RAM speed. If data were never reused the cache would be
useless, but because reuse is the norm, paying the disk cost once and amortising it over many
fast hits is an enormous net win. This is exactly why the second `cat` of a file is instant: the
first `cat` was a string of cache misses that filled the cache, and the second is all hits.

### Writing: "not what you think"

Writing is where intuition fails, and it is the heart of this concept. The natural assumption is
that `write(fd, data, len)` returning successfully means the bytes are now safely on disk. **It
does not.**

What actually happens on a normal disk-backed write: the kernel copies the program's data into
the relevant page-cache page in RAM, marks that page **dirty** — meaning *modified in RAM but not
yet written back to disk* — and then `write` **returns immediately**. At that instant the new
bytes exist only in RAM. The program continues, believing its write is done, while the disk still
holds the old contents (or nothing).

The dirty data reaches disk *later*, by one of two routes:

- **Background writeback.** A dedicated kernel thread wakes periodically (on the order of seconds),
  hunts down dirty pages, transfers them to disk, and then marks them **clean** (RAM and disk now
  agree). The program is not involved and does not wait for this.
- **An explicit flush.** A program that needs its data durable *right now* calls `fsync` on the
  descriptor (this is plain prose, not a prerequisite node). `fsync` blocks — it does not return —
  until every dirty page for that file has physically reached the disk. This is why databases such
  as PostgreSQL or MySQL call `fsync` after committing a transaction: only after `fsync` returns
  can they promise the transaction survives a crash. (A related option, `O_DIRECT`, asks the
  kernel to bypass the page cache for a file entirely and talk to the disk directly; it is
  mentioned here only in plain prose to show the cache *can* be opted out of.)

Now the **why** behind this seemingly reckless design — deferring the write rather than doing it
immediately — and its central trade-off:

- **The gain.** Returning from `write` at RAM speed instead of disk speed makes writing
  programs run far faster, and deferral lets the kernel **batch** work. Many small writes to the
  same page coalesce into one disk transfer; many separate dirty pages are written together in an
  efficient sweep; a file written and then quickly deleted may never hit the disk at all. Most
  real workloads write in *bursts*, so batching the burst into a few large, well-ordered disk
  operations is dramatically cheaper than a slow disk trip per `write`.
- **The cost.** Between the `write` and the eventual flush, the only copy of the new data is the
  dirty page in **volatile** RAM. If the machine loses power or crashes in that window, those
  un-flushed dirty pages **vanish** — the write is lost even though `write` reported success. The
  durability the program assumed it had, it did not have until the data was flushed. This is the
  price of the speed, and it is precisely why durability-critical software calls `fsync` instead of
  trusting a bare `write`.

### A worked instance: read a file twice, then write it

Take a concrete file: **`report.dat`, exactly 1 MB** = 1,048,576 bytes. In [[page]] units that is
1,048,576 ÷ 4096 = **256 pages** exactly (a clean fit, chosen here only for the page count; the
non-degenerate behaviour we care about is the hit/miss/dirty distinction, exercised below). Assume
the cache starts empty of this file, and use round figures: a disk block costs about **5 ms** to
fetch, a RAM copy about **5 µs** — a 1000× gap.

**Step 1 — first read (all misses).** The program opens the file (VFS resolves the path to its
[[inode]] and gives back a file-descriptor, fd = 3) and reads all 1 MB. Every one of the 256 pages is
absent, so every page is a **cache miss**: the kernel allocates 256 page-cache pages, pulls the
256 blocks off the disk into them, and copies them out to the program. The disk work dominates —
order of *milliseconds per block*, call it tens of milliseconds total for the run. Critically, all
256 pages now **remain in the page cache**.

**Step 2 — second read (all hits).** The program reads the same 1 MB again. Now every page is
present, so every access is a **cache hit**: the kernel copies 256 pages straight from RAM, ~5 µs
each, and the disk is never touched. The whole read finishes in roughly *microseconds-scale*
time — about a thousand times faster than Step 1. Nothing changed in the program's code between
the two reads; the identical `read` calls were served once from disk and once from RAM, and only
the cache state differed. *This is the entire payoff of the read side.*

**Step 3 — write (returns instantly, not yet durable).** The program now overwrites the first
512 bytes of the file: `write(3, newbytes, 512)`. The kernel finds the affected page — page 0,
already in the cache from Step 1 — copies the 512 new bytes into it, marks that page **dirty**,
and `write` **returns immediately**, in microseconds. The program moves on. At this moment the new
512 bytes exist *only* in the dirty cache page in RAM; the disk still holds the old contents of
page 0.

**Step 4 — the fork in the road.** Two futures:

- *Normal case:* a few seconds later the writeback thread finds page 0 dirty, transfers it to
  disk, and marks it clean. The new bytes are now durable, and a subsequent read (hit, from the
  same cache page) and the disk copy agree. Had the program called `fsync(3)` right after Step 3,
  this flush would have happened at once and `fsync` would have blocked until it completed —
  guaranteeing durability immediately instead of seconds later.
- *Crash case:* the power fails one second after Step 3, before writeback runs. The dirty page 0
  was only in volatile RAM, so the new 512 bytes are **lost**; on reboot the file still holds its
  pre-write contents. The `write` had returned "success," yet the data is gone — exactly the
  hazard the deferred design carries, and exactly what `fsync` exists to prevent.

The instance is deliberately non-degenerate: Step 1 forces the miss path, Step 2 forces the hit
path, and Step 3–4 force the dirty-then-flush-or-lose path — so the read cache, the write cache,
and the durability gap are each actually exercised rather than collapsed away.

## Prerequisites

- [[page]]
- [[vfs]]
- [[inode]]
- [[system-call]]
## Sources

- `linux-internals-complete.html` — section "Page cache — RAM as a
  disk cache" (the kernel keeps recently read file data in RAM; `read` checks the cache first;
  cache hit copies from RAM with the disk untouched, ~microseconds; cache miss fetches from disk,
  stores a copy, ~milliseconds, and the next read becomes a hit; the cache uses all free RAM and
  is reclaimed on demand). Section "Writing — not what you think" (`write` copies into the cache,
  marks pages dirty, and returns before the data is on disk; a background writeback thread flushes
  dirty pages later; `fsync` forces an immediate, blocking flush; a power loss between `write` and
  flush loses the data). Section "The complete I/O chain" (the full `cat /etc/hostname` path:
  VFS resolves the path and routes `read` to ext4, which consults the page cache first — hit
  returns from RAM, miss continues down to the disk and refills the cache).
