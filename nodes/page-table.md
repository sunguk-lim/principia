---
id: page-table
title: Page Table
summary: A page table is the per-process lookup structure that records, for each virtual page, which physical frame currently holds it — the "translation book" the CPU's address hardware…
type: concept
tags: [os/memory]
prereqs: [page]
sources:
  - linux-internals-complete.html ("Page tables — the translation book")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Page Table

## Summary

A **page table** is the per-process lookup structure that records, for each virtual
[[page]], which physical frame currently holds it — the "translation book" the CPU's address
hardware consults on *every* memory access to turn a virtual address into a physical one.
A [[page]] already split each virtual address into a **page number** (which 4 KB block) and
an **offset** (how far into it); the page table is precisely where the page-number-to-frame
record lives, and the offset rides through untouched. Each process gets its **own** page
table, which is exactly what makes one process's address space private from another's: the
same virtual address translates to a different physical frame in each, or to nothing at all.
Each entry carries not just a frame but **permission bits** (present, readable, writable,
user-accessible), so an access that hits an unmapped entry or violates its permissions traps
into the kernel as a **page fault**. Because a single flat table covering a modern address
space would be astronomically large while almost all of that space is unused, real page
tables are **multi-level** — a tree that stores branches only for the regions actually mapped
— and a small hardware cache called the **TLB** remembers recent translations so the lookup
need not be repeated for every access.

## Grounded explanation

### What the page table is, and why it must exist

A [[page]] left one thing unbuilt. It established that memory is diced into fixed 4 KB blocks,
that a whole virtual page is mapped onto a whole physical **frame** (a 4 KB block of real
RAM), and that translating a virtual address therefore means translating only its **page
number** — which 4 KB block it falls in — while its **offset** — how far into that block it
sits — is copied across unchanged. What it deliberately did not say is *where the
page-number-to-frame records actually live*. That store is the page table.

Define it precisely. A **page table** is a data structure, built and owned by the kernel,
that maps each virtual page number to the physical frame currently holding that page. One row
of it — one **page table entry** (PTE) — answers exactly one question: "virtual page *X* lives
in physical frame *Y* (and here is what you're allowed to do with it)." The hardware unit that
performs address translation, the **MMU** (memory management unit, a part of the CPU), reads
this structure on *every single* memory access — every instruction fetch, every pointer
dereference — to convert the virtual address the program used into the physical address the
RAM chips understand. The kernel writes the book; the MMU reads it at full speed.

Why must such a thing exist at all? Because the translation a [[page]] described is not
magic — somebody has to *remember* the mapping. The page number cannot be turned into a frame
number by arithmetic (unlike the offset, which needs no lookup); the assignment of pages to
frames is arbitrary and changes over time, so it has to be looked up in stored data. The page
table is that stored data. It is the concrete realization of the "map" the [[page]] kept
referring to.

### Why each process has its own — privacy falls out of it

A page table is **per-process**: every process has its own separate book. This single fact is
what delivers private address spaces. Process A and process B can both use the virtual
address 0x400000, yet A's page table sends that page to one physical frame and B's sends it
to a completely different frame — so neither can name, let alone touch, the other's memory.
The kernel keeps a special CPU register pointing at "the page table to use right now"; when
the scheduler switches from A to B, it reloads that register to point at B's table, and from
that instant the very same virtual address resolves somewhere else. Privacy is therefore not
an extra mechanism bolted on — it is the direct consequence of the MMU consulting a
*different book per process*.

### What an entry holds: a frame plus permission bits

A page table entry is more than a frame number. Alongside "which physical frame" it carries a
handful of **permission and status bits** that govern the access:

- a **present** bit — is this page actually backed by a frame in RAM right now?
- a **writable** bit — may this page be written, or only read?
- a **user** bit — may an ordinary (non-kernel) program touch this page at all?

On each access the MMU checks these *before* completing the translation. If the present bit is
clear (no frame mapped yet), or the access violates a permission — a write to a read-only
page, or a user program reaching for a kernel-only page — the MMU cannot finish. It stops the
instruction and raises a **page fault**: a trap that hands control to the kernel to decide
what to do (find or create a frame, or kill the offending process). The fault is the page
table's enforcement edge — the moment the stored permissions actually bite.

### Why multi-level: the table must be sparse

Here is the central design problem, and the reason a page table is shaped the way it is. A
64-bit machine can name an enormous virtual space (Linux uses 48 of those bits per process by
default — 256 TB). With 4 KB pages, that is 256 TB ÷ 4 KB ≈ 64 billion pages. A **flat** page
table — one entry per possible page, laid out as a single array indexed by page number —
would need 64 billion entries *per process*. At 8 bytes each that is half a terabyte of table
to describe a process that may be using a few megabytes. Multiply by hundreds of processes and
it is hopeless. A flat table is impossible for the same reason byte-by-byte mapping was
impossible in the [[page]] node: the bookkeeping dwarfs the thing it describes.

The escape is that the space is **sparse**: a real process maps only a few small regions —
some code, some data, a stack — and the vast middle is never touched. We want a structure that
spends storage *only* on the regions actually in use. The answer is a **multi-level** (tree-
structured) page table. Instead of one giant array, the page number's bits are split into
several groups, and each group indexes one level of a tree. The top-level table has one entry
per *coarse* slice of the address space; that entry either says "this entire slice is
unmapped" (and stops — no lower tables exist for it) or points to a next-level table that
subdivides the slice further; and so on, until the final level holds the actual page-to-frame
entries. To translate, the MMU starts at the top (a register holds the address of the
top-level table for the current process) and **walks down**, using one bit-group at each level
to pick the next table, until it reaches the leaf entry with the frame number.

The win is exactly the sparseness we wanted: for any coarse slice the process never uses, the
single top-level entry is marked empty and *none* of the lower tables for that slice are ever
allocated. An entire unused branch of the tree costs one entry instead of billions. The tree
stores detail only where the process actually lives. (On x86-64 Linux this tree is four levels
deep by default; the count is a detail — the idea is the sparse tree.)

This sparse tree has one cost: the MMU must now read several tables in memory — one per level —
to translate a single address. Doing that on *every* access would be ruinously slow. So the
hardware keeps a tiny, fast cache of the most recent virtual-page-to-frame results, the **TLB**
(translation lookaside buffer). When a translation is in the TLB — the common case, because
programs reuse the same pages over and over — the MMU skips the whole walk and uses the cached
frame directly. The page table is the authoritative, complete book; the TLB is the sticky note
of the few pages you're using right now.

### Worked instance: two translations through one table

Take a process whose final-level page table contains these two entries (frame numbers and
permissions shown), and a 4 KB page so the offset is the low 12 bits (the low 3 hex digits),
exactly as the [[page]] node split addresses:

- entry **0x401** → frame **0x12**, present, readable, writable
- entry **0x999** → *(no entry — this slice was never mapped)*

**Translation 1 — a hit.** The program accesses virtual address **0x401234**. Split it as a
[[page]] does: the low 3 hex digits are the offset, **0x234**, and everything above is the
page number, **0x401**. The MMU walks the tree down to leaf entry 0x401, finds it **present**,
reads frame **0x12**, and checks permissions — say the program is reading, which the entry
allows. Now assemble the physical address. The frame's base in RAM is the frame number shifted
up by 12 bits (frames are 4 KB apart): frame 0x12 begins at physical 0x12000. Paste the
unchanged offset onto it: 0x12000 + 0x234 = **physical 0x12234**. Check by the [[page]]
identity, page number × 4096 + offset: virtual 0x401234 = 0x401 × 0x1000 + 0x234, and the
physical address is frame 0x12 × 0x1000 + 0x234 — the page number changed from 0x401 to 0x12,
the offset 0x234 rode through untouched. That is the page table's whole job in one line: swap
the page number for a frame number, keep the offset.

**Translation 2 — a fault.** Now the same program accesses virtual address **0x999000** —
page number **0x999**, offset **0x000**. The MMU walks the tree, but the slice containing 0x999
was never mapped: the entry is not present. The MMU cannot produce a frame, so it stops the
instruction and raises a **page fault** into the kernel. From here it is the kernel's decision,
not the page table's: if 0x999 falls in a region the process is allowed to use, the kernel can
allocate a fresh frame, fill in the entry, and restart the instruction (this on-first-touch
allocation is *demand paging*, its own topic); if 0x999 is a wild address in no valid region,
the kernel kills the process with a segmentation fault. The page table's role ends precisely at
"no valid entry → trap to the kernel" — it is the structure that both *answers* the lookup when
it can and *signals the fault* when it cannot.

The contrast between the two translations is the point. The same single table, walked the same
way, turns one access into a physical address in nanoseconds and the other into a kernel trap —
and which happens is decided entirely by whether the looked-up entry exists and permits the
access. That is what a page table *is*: the per-process book whose presence, contents, and
permission bits decide, on every access, where a virtual page really lives or whether touching
it is even allowed.

## Prerequisites

- [[page]]

## Sources

- `linux-internals-complete.html` — section "Page tables — the translation book": the page
  table as a per-process "virtual page X → physical page Y" book, the CR3 register that the
  context switch swaps so the same virtual address maps differently per process, page table
  entries carrying permission bits (present, read/write, user/supervisor, dirty, accessed) and
  the user/supervisor bit enforcing kernel-page protection; plus the adjacent "Pages" section
  for the MMU performing the lookup on every access, the multi-level (PGD→PUD→PMD→PTE) tree for
  the 48-bit space, and the fault discussion noting the TLB caches translations so the MMU need
  not re-walk the table each time.
