---
id: dma
title: Direct Memory Access
summary: When a device — a disk, a network card, a GPU — needs to move a block of data into or out of main memory (the RAM rung of the memory-hierarchy), there are two ways to do it.
type: concept
tags: [os/kernel]
prereqs: [memory-hierarchy, interrupt]
sources:
  - "Linux internals guide (etc/linux-internals-complete.html), §'How data actually moves' — programmed I/O (MOV), DMA delegation, scatter-gather, interrupt-on-completion"
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Direct Memory Access

## Summary

When a device — a disk, a network card, a GPU — needs to move a block of data into
or out of main memory (the RAM rung of the [[memory-hierarchy]]), there are two ways
to do it. The naive way is to make the processor (the CPU, the chip that executes the
program's instructions) carry every byte itself: read a byte from the device, write it
to memory, repeat, a million times for a megabyte. **Direct Memory Access (DMA)** is
the alternative: a separate piece of hardware — a *DMA engine*, typically built into
the device's own controller — performs the bulk move **directly between the device and
memory, without the CPU touching any of the bytes**. The CPU's only job is to *program*
the transfer up front (say where to read from, where to write to, and how many bytes),
after which it walks away and runs other work; when the move finishes, the engine raises
an **[[interrupt]]** — a hardware signal that preempts whatever the CPU is doing and
forces it into a kernel handler — to report "done." The why is an economics argument straight out of the [[memory-hierarchy]]: the
CPU is the scarce, expensive, fast resource, and spending its cycles shuttling bytes one
at a time is a waste; DMA offloads that drudgery to cheap dedicated hardware so the CPU
can compute instead of acting as a delivery truck. DMA is the primitive beneath fast
disk I/O, networking, and CPU↔GPU transfers.

## Grounded explanation

### The baseline it replaces: the CPU moves bytes by hand (programmed I/O)

To see what DMA *is*, first see what it removes. At the most fundamental level the CPU
moves data by executing **move instructions** (on x86 these are literally called `MOV`):
the CPU places an address on the **memory bus** — the physical wires connecting the chip
to RAM — and either reads the word stored there or writes a word to it. ("Word" here
just means the fixed-size chunk the CPU moves at once, a handful of bytes.) A device like
a disk controller exposes its data through a small **register** — a named storage slot on
the device that the CPU can read like a memory address. So the hand-carried way to pull
data off a disk, called **programmed I/O**, is a loop: the CPU reads a word from the disk
controller's register into itself, then writes that word out to RAM, then repeats. For a
1-gigabyte file that is on the order of a billion such read-then-write steps, and during
every one of them the CPU is fully occupied. It cannot run your other programs; it is a
courier hauling boxes one at a time. That is the waste DMA exists to eliminate.

### What DMA *is*: delegating the bulk move to a dedicated engine

DMA replaces the carrying with **delegating**. The device's controller contains its own
small circuit — the **DMA engine** — that can itself put addresses on the memory bus and
write (or read) RAM directly, exactly as the CPU would, but autonomously. The CPU no
longer moves the bytes; it only issues an order. Concretely the CPU writes a few values
into the controller — a **transfer descriptor** — that say:

- the **source** — where the bytes come from (e.g. which disk blocks),
- the **destination address** — where in RAM to put them,
- the **length** — how many bytes to move.

Then the CPU sets a "go" bit and turns away to run other processes. The DMA engine
streams the whole block — kilobytes, megabytes, gigabytes — directly between the device
and RAM, byte after byte, with the CPU uninvolved. When the last byte has landed, the
engine raises an **interrupt**: an electrical signal on a dedicated line that interrupts
whatever the CPU is doing and makes it jump to a short *handler* routine, which here just
notes "the data you asked for is now in RAM." The defining structure of DMA is therefore
a split of labor: the CPU does a tiny, constant amount of *setup* work no matter how big
the transfer is, and the engine does all the per-byte *movement* work in parallel with
the CPU's other computation.

### Why it works: don't spend the scarce fast resource on bulk movement

The justification is the central lesson of the [[memory-hierarchy]]: the CPU is the
fast, scarce resource, and moving a large block of bytes is a slow, bandwidth-limited
chore. If the CPU performs that chore with a `MOV` loop, two bad things happen. First,
the CPU's cycles — which could be doing useful arithmetic — are burned entirely on
copying. Second, and more subtly, dragging a megabyte through the CPU drags it through
the CPU's small fast caches (the upper rungs of the [[memory-hierarchy]]): the streamed
data, used once and never again, *evicts* the genuinely hot data the CPU was working on,
so the program runs slower even after the copy finishes. This is **cache pollution**.
DMA avoids both: the bytes flow on a path (device → memory bus → RAM) that never enters
the CPU or its caches, so the engine moves the block at memory bandwidth while the CPU's
fast rungs stay full of *its* working set. The invariant DMA maintains is that the CPU's
involvement is **O(1) in the transfer size** — a fixed descriptor setup plus one
interrupt — rather than O(bytes). Bulk movement is handed to hardware whose only job is
bulk movement; the expensive general-purpose chip is freed for what only it can do.

### Worked instance: reading 4 KB from disk, two ways

Take a concrete, non-degenerate transfer: read **4 kilobytes** (4096 bytes) from a disk
into RAM at address `X`. Suppose the CPU moves 8 bytes per `MOV` and runs at, say, 3
billion cycles per second.

**Programmed I/O (the baseline).** Moving 4096 bytes 8 at a time is `4096 ÷ 8 = 512`
loop iterations, and each iteration is at minimum a read from the device register plus a
write to RAM — call it a few cycles, but the device read alone stalls the CPU for far
longer because the disk is slow. Even ignoring the stalls, the CPU executes on the order
of a thousand instructions *and is unavailable for anything else* for the entire duration
of the read. For one 4 KB block that is tolerable; multiply by the millions of blocks in
real I/O and the CPU does nothing but copy.

**DMA.** The CPU instead writes the descriptor — source = the disk blocks holding those
4 KB, destination = RAM address `X`, length = 4096 — and sets the go bit. That is a
handful of register writes, perhaps a few dozen cycles, *independent of the 4096*. Then
the CPU returns to running other programs. The disk controller's DMA engine reads the 4
KB off the platter or flash and streams it straight into RAM at `X`. When byte 4096 has
been written, the engine raises an interrupt; the CPU briefly enters its handler, learns
the block is ready, and moves on. The crucial contrast: in programmed I/O the *4096*
appears as a loop count the CPU must personally grind through, whereas in DMA the *4096*
is just a number the CPU hands off — it never appears in the CPU's instruction stream at
all. Scale the block from 4 KB to 4 GB and the CPU's cost under DMA barely changes (same
descriptor, same one interrupt), while under programmed I/O it grows a millionfold. That
flat cost is the entire point.

### Scatter-gather: one transfer over many non-contiguous buffers

The basic descriptor above assumes the destination is one contiguous run of RAM. Reality
is messier: a file's blocks may be scattered across the disk, and the RAM pages that
receive them are typically scattered across physical memory too (because the operating
system hands out memory in fixed-size *pages* placed wherever room exists, not in one
long stretch). Issuing a separate DMA — with its own setup and its own completion
interrupt — for each little fragment would claw back much of the CPU savings.

**Scatter-gather DMA** fixes this. Instead of one source/destination/length triple, the
CPU builds in RAM a **scatter-gather list**: an array of such entries, one per fragment —
"read this from here, put 4 KB at RAM `0x10000`; read that, put 4 KB at `0x85000`; read
the next, put 8 KB at `0x200000`; …end." The CPU then programs the engine with a single
pointer to that list and one "go." The engine walks the list entry by entry on its own,
placing each chunk at its own address — *gathering* fragments on a read, *scattering* them
on a write — and raises just **one** interrupt when the whole list is done. So a single
delegated command moves a pile of non-contiguous buffers, and the CPU's involvement is
still O(1): build the list, point at it, get one interrupt. Modern NVMe SSDs handle
thousands of scatter-gather entries per command, moving gigabytes of fragmented data
while the CPU does other work — which is why modern I/O is fast: the CPU barely
participates in the actual movement.

### Where it shows up

The same delegate-program-and-be-interrupted pattern recurs everywhere data crosses
between a device and the RAM rung of the [[memory-hierarchy]]. A disk read DMAs blocks
into memory. A network card DMAs an arriving packet into RAM and interrupts the CPU to
process it, and DMAs an outgoing packet from RAM onto the wire. A GPU transfer programs a
DMA engine to stream a buffer from host RAM across the link into the GPU's own memory (and
back). In each case the CPU's role has shifted from *moving bytes* to *telling hardware to
move bytes* — which is exactly what frees the scarce fast resource the [[memory-hierarchy]]
taught us to conserve.

## Prerequisites

- [[memory-hierarchy]]
- [[interrupt]]

## Sources

- Linux internals guide (`etc/linux-internals-complete.html`), section "How data actually moves" — programmed I/O via `MOV` instructions as the baseline, DMA as delegation (the CPU tells the disk controller where to put data, then runs other processes while the controller writes RAM directly and fires a completion interrupt), and scatter-gather DMA (a CPU-built list of address/length entries the controller walks through, one interrupt at the end). Boot-stage evolution and the "CPU's role shifts from moving bytes to telling hardware to move bytes" framing are from the same and adjacent sections.
