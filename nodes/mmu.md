---
id: mmu
title: Memory Management Unit
summary: The memory management unit (MMU) is the piece of hardware inside the CPU that turns every virtual address a program uses — the addresses it computes and dereferences — into the…
type: concept
tags: [os/memory]
prereqs: [page-table, virtual-memory, page-fault]
sources:
  - linux-internals-complete.html ("Virtual addresses vs physical addresses"; "Pages — memory is managed in 4KB chunks")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Memory Management Unit

## Summary

The **memory management unit** (MMU) is the piece of hardware inside the CPU that turns
every **virtual address** a program uses — the addresses it computes and dereferences — into
the **physical address** of an actual byte in RAM, and it does this on *every single* memory
access. The [[page-table]] is the per-process book that records, for each virtual page, which
physical frame holds it; the MMU is the reader of that book and the agent that performs the
lookup. On each access it splits the address into a **page number** and an **offset**, looks
the page number up by walking the [[page-table]] (whose root address sits in a dedicated CPU
register), retrieves the physical frame, and pastes the untouched offset back on to form the
physical address. If the lookup finds no valid entry, or the entry forbids the kind of access
being made, the MMU cannot finish: it stops the instruction and raises a [[page-fault]] —
a hardware trap that hands control to the kernel. The reason this work lives in hardware at all is speed — a
translation must happen before *any* load or store can touch memory, so doing it in software
would tax every instruction. To make the common case even faster the MMU keeps a tiny on-chip
cache of recent translations called the **TLB**, so most accesses skip the walk entirely. The
MMU is therefore what makes [[virtual-memory]] practical: the kernel writes the map, but the MMU
silently consults it at full speed on every reference.

## Grounded explanation

### What the MMU is — the hardware reader of the book

The [[page-table]] gave us a complete, per-process book of translations: for every virtual
page (a 4 KB block of a process's address space), one entry recording which physical **frame**
(a 4 KB block of real RAM) currently holds it, together with permission bits saying what is
allowed. But a book is inert. Something has to *open* it on every memory access, follow it down
to the right entry, and act on what it finds. That something is the **memory management unit**,
or MMU: a dedicated circuit built into the CPU whose entire job is address translation.

Be precise about the division of labor, because it is the heart of this node. The kernel
*builds and owns* the [[page-table]] — it decides which virtual page maps to which frame and
writes those entries. The MMU *reads* the [[page-table]] — it never decides mappings, it only
looks them up and enforces them. The kernel is the author; the MMU is the reader. Crucially the
MMU is **hardware**, not a kernel routine: it is wired into the path between the CPU's
execution units and memory, so that no load or store can reach RAM without passing through it.
A program never sees a real RAM address; it only ever names virtual addresses, and the MMU is
the silent translator standing between the program's view and physical memory.

### Why it must be hardware — translation is on the critical path of every access

Here is the *why*, the justification for the whole design. A program touches memory
constantly: every instruction must be fetched from memory, and a large fraction of
instructions also read or write data. Every one of those touches names a virtual address, and
*every* virtual address must be translated to a physical one before the RAM chips can be told
which byte to deliver. Translation is therefore not an occasional bookkeeping chore — it sits
on the critical path of essentially every operation the CPU performs.

If that translation were done in software — a few instructions of kernel code run before each
access — then every single load and store would balloon into many instructions, and the
machine would crawl. The only way to make per-access translation affordable is to do it in
**hardware**, in parallel with the rest of instruction execution, so that it adds almost
nothing to each access. That is the reason the MMU exists as a circuit rather than as code:
the [[page-table]] makes virtual memory *correct*, but only doing the lookup in hardware makes
it *fast enough to use*. The MMU is what turns the idea of private virtual address spaces from
a theoretical scheme into something a real computer can run.

### How it translates — split, walk, recombine

The mechanism the MMU runs on each access has three steps, and the first and third are pure
bit-shuffling while only the middle one is a lookup.

**Split.** A virtual address is cut into two fields. The low bits — twelve of them for a 4 KB
page, since 4 KB is 2¹² bytes — are the **offset**: how far into its page the byte sits. The
remaining high bits are the **page number**: which page the byte belongs to. This split is the
same one the [[page-table]] node used; the MMU is the unit that physically performs it on the
wires.

**Walk.** The offset needs no lookup — a byte's position inside its page is identical in the
virtual page and in the physical frame, because a page and a frame are both exactly 4 KB and
the bytes inside keep their order. So only the page number must be translated, and that is the
[[page-table]] lookup. The MMU finds the root of the current process's [[page-table]] in a
dedicated CPU register — on x86 this register is called **CR3**, and it holds the physical
address where that process's table begins — and **walks** the [[page-table]] from there: it
uses successive slices of the page number to descend through the table's levels until it
reaches the leaf entry for this page. The kernel reloads this root register on every process
switch, which is exactly why the same virtual address translates differently for different
processes: the MMU is reading a different book each time.

**Recombine.** The leaf entry yields a physical frame number (and the permission bits, checked
below). A frame's starting address in RAM is its frame number shifted up by twelve bits, since
frames are spaced 4 KB apart. The MMU pastes the original, untouched offset onto that frame
base, and the result is the physical address. Only the high part of the address changed — the
page number became a frame number; the offset rode straight through.

### When it cannot translate — the page fault

The walk does not always succeed, and the MMU's behavior when it fails is as much a part of
its job as success. Two things can go wrong, both detected by the MMU while reading the leaf
entry. First, the entry may be **absent** — marked not-present, meaning no frame currently
backs that virtual page (perhaps none was ever allocated). Second, the entry may be present but
its permission bits may **forbid** the access — a write aimed at a read-only page, or an
ordinary program reaching for a kernel-only page. In either case the MMU cannot produce a valid
physical address, so it does the only safe thing: it **stops the instruction in flight** and
raises a **page fault**, a hardware exception that transfers control to the kernel.

A page fault is not necessarily an error — it is the MMU politely handing an unresolvable
access back to the kernel to decide. The kernel may discover the page is legitimate but not yet
backed by RAM, allocate a frame, fill in the [[page-table]] entry, and restart the instruction
— at which point the MMU re-runs the translation and now succeeds. Or the kernel may find the
address is genuinely invalid and kill the process. Either way, the MMU's role ends exactly at
the boundary "no valid, permitted entry → trap to the kernel." It resolves what it can in
hardware and escalates the rest.

### Why the TLB — caching to avoid re-walking

The walk has a cost: descending the multi-level [[page-table]] means the MMU itself reads
several entries from memory to translate one address — and it must do this *before* the
program's own access can even start. Paying that on every access would undo the very speed the
hardware was built to provide. The escape is that programs are repetitive: they touch the same
handful of pages again and again — the page holding the current code, the page holding the
stack, a few data pages. So the MMU keeps a small, extremely fast on-chip cache of its most
recent page-number-to-frame results, called the **TLB** (translation lookaside buffer). On
each access the MMU checks the TLB first; if the page's translation is already there — the
common case — it uses the cached frame immediately and skips the walk entirely. Only on a
miss does it walk the [[page-table]] in memory, and it records the result in the TLB on the way
out. The [[page-table]] is the complete, authoritative book; the TLB is the MMU's sticky note
of the few pages in active use.

### Worked instance: one hit and one fault, in hardware

Take a process running with 4 KB pages, so the offset is the low twelve bits — the low three
hex digits — of every address. Suppose its [[page-table]] maps virtual page **0x401** to
physical frame **0x12** (present, readable), and has *no* entry for virtual page **0x800**.

**A successful access.** The program executes a load from virtual address **0x401234**. The MMU
splits it: the low three hex digits **0x234** are the offset, and the rest, **0x401**, is the
page number. The offset is set aside untouched. The MMU reads the current process's
[[page-table]] root from the CPU register (CR3 on x86) and walks down to the leaf entry for
page 0x401. The entry is present and permits reading, so translation proceeds. The frame number
is **0x12**; its base in RAM is 0x12 shifted up by twelve bits, i.e. **0x12000**. The MMU pastes
the saved offset back on: 0x12000 + 0x234 = **physical 0x12234**. It hands that physical address
to the memory system, the byte is fetched, and the load completes. Sanity-check the arithmetic:
the virtual address was page 0x401 × 0x1000 + 0x234, the physical address is frame 0x12 × 0x1000
+ 0x234 — the page number changed from 0x401 to 0x12, the offset 0x234 was preserved exactly.
That is the entire translation, and on a TLB hit the walk would have been skipped and the frame
read straight from the cache.

**A faulting access.** Now the program accesses virtual address **0x800000** — page number
**0x800**, offset **0x000**. The MMU splits it the same way and walks the [[page-table]] toward
page 0x800, but that page has no valid entry: it is marked not-present. The MMU cannot produce a
frame, so it stops the instruction and raises a **page fault** into the kernel. What happens
next is the kernel's call, not the MMU's: if 0x800000 lies in a region the process is allowed to
use, the kernel allocates a frame, writes the [[page-table]] entry, and restarts the
instruction — and the MMU's *second* attempt at the very same address now finds a present entry
and succeeds; if 0x800000 is a wild address in no valid region, the kernel terminates the
process. The contrast between the two accesses is the point: the same hardware unit, running the
same split-walk-recombine procedure on every reference, turns one address into a physical byte
in nanoseconds and the other into a kernel trap — and which outcome occurs is decided entirely
by what the MMU finds when it reads the [[page-table]] entry.

## Prerequisites

- [[page-table]]
- [[virtual-memory]]
- [[page-fault]]

## Sources

- `linux-internals-complete.html` — section "Virtual addresses vs physical addresses": the MMU
  introduced as "a hardware chip in the CPU called the MMU (Memory Management Unit)" that
  performs virtual-to-physical translation "on every single memory access — every MOV
  instruction, every pointer dereference," with the kernel setting up the translation tables and
  the MMU doing the translation "at full speed." Section "Pages — memory is managed in 4KB
  chunks": the worked split of a virtual address into page number + offset and the MMU looking
  the page number up in the page table, keeping the offset, to form the physical address.
  Adjacent material supplies the CR3 register holding the per-process page-table root (swapped on
  context switch), the TLB caching recent translations so the MMU need not re-walk the table,
  and the page-fault path the MMU takes when a lookup finds no present/permitted entry.
