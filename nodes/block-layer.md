---
id: block-layer
title: Block Layer
summary: The block layer is the kernel layer that sits between a filesystem — reached through the vfs — and the driver for an actual storage device.
type: concept
tags: [os/filesystem]
prereqs: [vfs, device-driver, dma, interrupt, queue]
sources: ["linux-internals-complete.html — §7 'The complete I/O chain' (the Block layer step: 'translates file block 0 → disk sector 386560'; the Disk-driver step building a DMA scatter-gather list), 'Device drivers' (block devices = fixed-size, randomly-addressable blocks vs character devices; the .read_block/.write_block driver interface), 'Reading a file' (page-cache hit/miss path)"]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Block Layer

## Summary

The **block layer** is the kernel layer that sits between a filesystem — reached
through the [[vfs]] — and the driver for an actual storage device. The filesystem
decides *which* pieces of a file are needed; it asks for them in terms of **logical
blocks**, fixed-size numbered chunks of the file (say, 4 kilobytes each). The storage
device, however, does not understand "block 0 of this file." It understands only its
own **sectors** — the fixed-size, individually addressable units the hardware reads and
writes (historically 512 bytes, often 4 kilobytes on modern disks), numbered straight
across the whole device. The block layer's job is to turn a request for a file's logical
block into a concrete device operation on a specific range of sectors, and — this is the
part that makes it more than a translator — to collect all such requests for a given
device into a **queue**, where it **merges** requests that touch neighbouring sectors and
lets an **I/O scheduler** reorder them into an efficient sequence before handing them to
the driver. The driver then triggers the physical transfer. The payoff is twofold: every
filesystem can run over every storage device without knowing the device's specifics, and a
storm of small, scattered file accesses is reshaped into a smaller number of ordered,
device-friendly operations.

## Grounded explanation

### Where it sits, and why there is a layer here at all

Recall the path a file read takes. A program calls `read` on a descriptor; the [[vfs]]
routes that call to the owning filesystem's read routine (ext4, say). That routine knows
the file's layout on disk — which device blocks hold which parts of the file. But the
filesystem does *not* know how to make a particular SSD or spinning disk actually move
bytes; that is the device driver's job, and every model of device speaks a different
hardware protocol. Between "the filesystem knows what it wants" and "the driver knows how
to command this exact hardware" sits the block layer.

It is worth saying plainly what the block layer is *not*, so the spine of this node is
clear. It is **not** the [[vfs]] (that is the prerequisite — the dispatcher that picks
*which* filesystem owns a call). It is **not** the filesystem (which decides *which* file
blocks are needed and where they live on the device). And it is **not** the device driver
(the final piece of code that writes the device's hardware registers). The block layer is
the **request-management layer in between**: it takes the filesystem's "I need these
blocks" and produces, for the driver, "transfer these sector ranges," having first queued,
merged, and ordered the work across everything else asking the same device.

The reason this is its own layer comes in two parts.

First, **decoupling.** The source draws the storage world in two halves. A **character
device** delivers a *byte stream* — a keyboard, a terminal, `/dev/null` — read or written
a byte or a chunk at a time, with no notion of position you can jump around in. A **block
device** is the other kind: a disk, an SSD, a USB stick — storage organized as fixed-size
blocks that support **random access**, meaning you may read block #500 and then block #3
with no penalty in principle. The block layer is the half of the kernel that handles block
devices. Because it presents one uniform notion — "a numbered array of fixed-size sectors
you can address in any order" — any filesystem can be built on top of it, and that
filesystem then runs unchanged over any block device. The filesystem talks blocks; the
block layer talks sectors to whichever driver is plugged in underneath. Neither needs to
know the other's specifics.

Second, **efficiency through queueing.** This is the non-obvious part, and the rest of the
node is about it.

### The defining mechanism: a per-device queue that merges and schedules

Each block device has its **request [[queue]]** — a list, held in memory, of the read and
write operations currently waiting to go to that device. When the filesystem needs a
block, the block layer does not rush it straight to the driver. It builds a *request*
describing the sector range and the destination in memory, and drops it into the queue.
Two things then happen to the requests sitting in that queue before any of them leave.

**Merging.** If a newly arriving request asks for sectors that are immediately adjacent to
sectors an already-queued request covers, the block layer fuses the two into one larger
request. Ten separate "read one block" requests for ten consecutive blocks become a single
"read ten blocks" request. This matters because the fixed cost of issuing an operation to a
device — and, on a spinning disk, of positioning the read head — is paid *once per request*,
not once per block; one big contiguous transfer is far cheaper than ten small ones that
happen to be next to each other.

**Scheduling.** The component that decides the *order* in which queued requests are handed
to the driver is the **I/O scheduler**. Its freedom to reorder is exactly what the random-
access nature of a block device permits. What "a good order" means depends on the hardware,
and this is the key insight that justifies having a tunable scheduler at all rather than a
fixed rule:

- On a **spinning disk**, a physical head must move to the right track before it can read;
  jumping between far-apart sectors wastes milliseconds in *seek* time. So a scheduler for
  spinning media tends to order requests by ascending sector number — service them roughly
  in the order the head would sweep past them, like an elevator visiting floors in order
  rather than darting up and down. Fewer, shorter head movements; much higher throughput.
- On an **SSD**, there is no head and no seek; any sector is reachable in the same time.
  Ordering by sector buys little, so the scheduler instead optimizes for *fairness* (no one
  process starving the device) and *latency* (a small urgent read should not wait behind a
  giant background write). Some setups even run a near-passthrough scheduler that does almost
  no reordering, because the device's own controller already parallelizes internally.

So the same queue mechanism serves opposite goals on different media, and the scheduler is
the swappable policy that picks the goal. The invariant the block layer maintains throughout
is that the *set* of bytes transferred is exactly what the filesystem asked for — merging and
reordering change only the *grouping and sequence* of the transfers, never their content.

When a request finally reaches the front and is dispatched, the driver does the hardware-
specific work: it programs the device to move the requested sectors directly into the
waiting memory (this direct memory transfer, set up by the driver and carried out by the
device's own circuitry while the processor does other work, is what the source calls a [[dma]]
scatter-gather transfer — kept here as plain prose). When the device signals completion, the
data is in memory and the original `read` can return.

### A worked instance: reading bytes 5000–6000 of a file

Take a concrete request. A program holds an open file and asks to read the byte range
5000–6000. Follow it down.

1. The program's `read` enters the kernel and the [[vfs]] routes it to the filesystem's
   read routine, exactly as the [[vfs]] node describes.
2. The filesystem consults the file's on-disk layout and maps that byte range to **logical
   block #N** of the file — suppose, with 4-kilobyte blocks, bytes 4096–8191 are block #1,
   so the range 5000–6000 falls entirely inside logical block #1. The filesystem also knows,
   from the file's block map, that logical block #1 currently lives at **sectors 386560
   through 386567** on the device (eight 512-byte sectors make up one 4-kilobyte block).
   This is precisely the source's "file block → disk sector" translation.
3. Before reaching the block layer, the kernel checks the page-cache — its in-memory
   store of recently used file data, held in page-sized chunks. If the block is already
   there (a cache hit), the bytes are handed back at once and the device is never touched —
   the block layer does nothing. To exercise the mechanism, assume it is *not* in the cache
   (a miss), so the work proceeds down.
4. The block layer builds a request — "read sectors 386560–386567 into this memory page" —
   and places it on this device's queue. Suppose another queued request, from a different
   read in flight, already covers **sectors 386552–386559**, the block immediately before
   ours. The block layer **merges** the two into one request for sectors 386552–386567, a
   single sixteen-sector transfer instead of two eight-sector ones.
5. The **I/O scheduler** slots this merged request into the queue at the position its policy
   dictates — on a spinning disk, in sector order relative to the other pending requests, so
   the head sweeps past it in one pass.
6. When the request reaches the front, the [[device-driver]] takes over: it programs the
   storage device's hardware registers and sets up the DMA transfer that moves those sixteen
   sectors directly into the waiting memory. The device signals completion via [[interrupt]]; the
   kernel copies the wanted bytes (5000–6000, which sit inside the block now in memory) into
   the program's buffer, and `read` returns.

The instance is deliberately non-degenerate: it triggers the real translation (a non-trivial
byte range mapped to a specific multi-sector run), a real merge (an adjacent queued request
exists, so the fusing branch fires), and a real scheduling decision (the request is ordered
against others) — rather than a lone request that would slip through with nothing to merge
or reorder.

### Why this is the shape of the layer

Step back to the WHY. The filesystem's view of the world is "files made of logical blocks";
the device's view is "a flat numbered array of sectors I can read in any order." Something
must bridge those two views, and bridging them *once*, in a shared layer, is what lets every
filesystem coexist with every block device. That is the decoupling. But once all of a
device's traffic is funnelled through one place, that place gets something for free: a
global view of everything the device is about to be asked to do. The block layer spends that
view on merging and scheduling — turning many small, scattered, independently-issued
accesses into fewer, larger, well-ordered device operations. A bare translator would leave
the device thrashing between distant sectors; the queue is what makes the access pattern
efficient. The layer earns its place by doing both jobs at once.

## Prerequisites

- [[vfs]]
- [[device-driver]]
- [[dma]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "The complete
  I/O chain" (the chain `read` → VFS → filesystem → page cache → **Block layer**, shown
  translating "file block 0" → "disk sector 386560", → **Disk driver** building a DMA
  scatter-gather list → disk hardware → interrupt on completion), "Device drivers" (the
  block-device-vs-character-device split: block devices handle fixed-size 512-byte/4KB
  blocks with random access — disks, SSDs, USB storage — and the kernel's
  `.read_block`/`.write_block` driver interface that each hardware driver fills in), and
  "Reading a file" (the page-cache hit/miss path that decides whether a request ever
  descends to the block layer at all). The per-device request **queue**, request
  **merging**, and the **I/O scheduler**'s media-dependent ordering (seek-minimizing order
  on spinning disks; fairness/latency on SSDs) are the standard block-layer mechanism that
  the source's single "file block → disk sector" step stands in for.
