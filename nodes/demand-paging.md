---
id: demand-paging
title: Demand Paging
summary: Demand paging is the kernel's policy of refusing to commit real physical memory to a mapped region until the program actually touches it.
type: concept
tags: [os/memory]
prereqs: [page-table, page-fault, interrupt, mmu]
sources:
  - linux-internals-complete.html ("Demand paging — memory that doesn't exist yet", "What happens when RAM runs out?")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Demand Paging

## Summary

**Demand paging** is the kernel's policy of refusing to commit real physical memory to a
mapped region until the program actually *touches* it. When a process asks for memory, the
kernel sets up the [[page-table]] records for the whole region but marks every entry **not
present** — no physical frame is attached. The first read or write to such a page cannot be
translated by the hardware, so it raises a [[page-fault]] that traps into the kernel; the
kernel then grabs one physical frame (or loads the page's data from a file or disk), fills in
the [[page-table]] entry, and re-runs the faulting instruction, which now succeeds. The
program never notices the detour. The payoff is that memory is materialized **lazily** —
only the pages truly used cost real RAM — so a program can reserve a gigabyte (or far more
than the machine even has) instantly and at near-zero cost, paying only for the slice it
touches. The same fault machinery also lets the kernel cope when RAM fills: it can **evict**
a little-used page out to disk, freeing its frame, and fault it back in on the next access —
fast in the common case, but ruinous if the system spends all its time shuttling pages
in and out.

## Grounded explanation

### Where this picks up — the loose end the page table left

The [[page-table]] node established the whole machinery of address translation: each process
owns a book of entries, one per virtual page (a 4 KB block of its address space), and each
entry either names the physical **frame** (a 4 KB block of real RAM) holding that page or is
marked **not present**. It also established the decisive event: when the hardware translator
(the MMU) walks the [[page-table]] and finds the entry it needs is *not present*, it cannot
finish the translation, so it stops the instruction and raises a **page fault** — a trap that
hands control to the kernel. The [[page-table]] node deliberately stopped there, saying only
that the kernel "decides what to do." Demand paging *is* that decision, applied as a
deliberate, system-wide strategy. It is not a new data structure; it is a *policy* for how
the kernel chooses to fill in [[page-table]] entries — namely, as late as possible.

Define the term precisely. **Demand paging** means: a [[page-table]] entry for a region the
process is entitled to use is left **not present** — pointing at no frame — until the moment
the program demands it by actually accessing that page. Only the access ("the demand")
triggers the kernel to attach a real frame. "On demand," not "in advance."

### The why — programs reserve vastly more than they touch

Why would a kernel go to the trouble of faulting on first touch instead of just handing over
the memory up front? Because the gap between what a program *reserves* and what it *uses* is
enormous. A process maps in its entire executable and every shared library it links against,
even though it may call only a handful of functions. It allocates generous buffers "just in
case." It reserves a large region for a stack or a hash table that will mostly stay empty. If
the kernel committed a physical frame for every page the moment it was reserved, most of that
RAM would sit attached to pages that are never read or written — pure waste, multiplied across
every process on the machine.

The insight of demand paging is that **a reserved page costs nothing but a [[page-table]]
entry until it is touched.** Setting an entry to "not present" is just writing a small record;
it consumes no frame. So reserving a region becomes almost free and almost instant, no matter
how large, because the expensive part — finding and attaching real frames — is deferred to the
exact pages that turn out to be used, and skipped entirely for those that never are. The
kernel can even promise, in total, more memory than physically exists (this loose accounting
is called **overcommit**), betting correctly that not every reserved page will be touched. The
invariant that makes this safe to the program is that *from the program's point of view nothing
is different*: a touched page behaves exactly as if it had been backed by RAM all along, because
the fault is repaired before the faulting instruction is allowed to complete.

### The mechanism — how one fault becomes one frame

Here is the step that looks like magic and the justification for it. The program executes an
instruction that reads or writes some virtual address. The [[mmu]] splits that address as the
[[page-table]] node described — a page number and an offset — and walks the [[page-table]] to
the entry for that page number. The entry is **not present**. The [[mmu]] therefore cannot produce
a physical address; it stops the instruction *before it completes* and raises a page fault — a
hardware exception that, like any [[interrupt]], preempts the CPU and forces it into a kernel
handler — transferring control to the kernel.

The kernel's fault handler now runs. It first asks whether the faulting address falls inside a
region the process is actually allowed to use. If not — a stray pointer into unmapped space —
this is an error, and the kernel kills the process (the familiar segmentation fault). But if
the address *is* in a valid region, the kernel treats the fault as the expected first-touch
signal and does the work that was deferred:

1. It obtains the page's data and a frame to hold it. For freshly allocated memory there is no
   prior content, so it takes any free physical frame and fills it with zeros (a brand-new page
   must not leak whatever another process left behind). For a page whose contents live
   elsewhere — code or data from an executable on disk, or a page that was earlier moved out of
   RAM — it reads those bytes into the frame from that backing store.
2. It writes the [[page-table]] entry for the faulting page: present now, pointing at the frame
   it just filled, with the appropriate permission bits.
3. It returns control to the *same* instruction that faulted.

That last point is the crux of why this is invisible. A page fault is a **restartable**
exception: the instruction did not run and fail — it was paused mid-translation. When the
kernel returns, the CPU re-executes that very instruction from the start. This time the MMU
walks the [[page-table]], finds the entry **present**, reads the frame, and completes the
access normally. The program's register and memory state are exactly what they would have been
had the page always been there. The justification, then, is not "the kernel patched up a
crash"; it is "the hardware deliberately leaves a translation gap unfinished, lets the kernel
fill the [[page-table]] entry, and then retries — the gap was always meant to be filled this
way." The fault is the hardware politely asking the kernel to finish a mapping, not a sign that
something broke.

One more property follows directly: this cost is paid **once per page**. After the first touch,
the [[page-table]] entry is present, and every later access to that page is translated purely in
hardware with no kernel involvement. So a region's faults are bounded by the number of distinct
pages it actually touches, after which it is free.

### Worked instance — `malloc(1 GB)` that costs nothing

Take a concrete case that exercises the whole mechanism. A program calls `malloc(1 GB)` — it
asks for one gigabyte of memory. With 4 KB pages, one gigabyte is 1 GB ÷ 4 KB = 262,144 pages.

**At allocation time.** The kernel creates [[page-table]] mappings for all 262,144 pages and
marks every one **not present**. It attaches *no* physical frames. The call returns essentially
instantly, and the physical RAM consumed is about **zero** — a few hundred KB of [[page-table]]
records, not a gigabyte of data. This is why the same program could "allocate" 100 GB on a 16 GB
machine: the reservation is just not-present entries, and entries are cheap. (Tools report this
split as two numbers: the *virtual size* — how much the process asked for, ~1 GB here — versus
the *resident set* — how much real RAM it actually occupies, ~0 here.)

**First write.** The program writes a single byte to one address in that region — say the page
at virtual page number 0x700. The MMU walks the [[page-table]] to entry 0x700, finds it **not
present**, and raises a page fault. The kernel's handler confirms 0x700 is inside the allocated
region, takes one free physical frame — say frame 0x8F7 — fills its 4 KB with zeros, sets
[[page-table]] entry 0x700 to "present → frame 0x8F7, writable," and restarts the write. The
write lands in frame 0x8F7. Real RAM now in use for this gigabyte: **one frame, 4 KB.** The
other 262,143 entries are still not present and still cost nothing.

**Touching more.** Each new page the program first touches repeats this: one fault, one frame,
4 KB more resident. If the program ends up writing to, say, 256 distinct pages, it has taken
256 faults and is using 256 × 4 KB = 1 MB of real RAM — out of a gigabyte reserved. The
resident footprint grows strictly **page by page, on demand**, tracking actual use rather than
the reservation. That gap — 1 GB promised, 1 MB spent — is the entire point of demand paging
expressed in numbers.

(A closely related trick, kept separate here, lets two processes *share* the same physical
frames read-only after one is cloned from the other, and only fault-and-copy a frame when one of
them writes — "copy-on-write." It rides on the same fault mechanism but is its own topic.)

### When RAM runs out — eviction, the OOM killer, and thrashing

Demand paging defers the cost of frames, but it cannot conjure frames that do not exist. So
consider the hard case: a fault arrives — a program touched a valid not-present page and is
owed a frame — but every physical frame is already in use. The kernel needs to free one.

Its tool is **eviction**, the mirror image of faulting in. The kernel picks a page that is
currently resident but looks least useful (for instance, one not accessed in a long time),
writes its contents out to a reserved area on disk (a region called **swap**), and marks that
page's [[page-table]] entry **not present** again — its data is now safely on disk, not in any
frame. The freed frame is handed to the faulting page. Later, when the evicted page's owner
touches it again, *that* access faults too; the kernel reads the saved bytes back from swap
into a fresh frame and restores the entry. Note the cost difference this exposes: a first-touch
fault that just needs a zeroed frame is cheap (no disk), but a fault that must wait on a disk
read to bring a page back from swap is far slower. Both are repaired the same way; only the
source of the page's data differs.

If even swap fills — RAM and disk both exhausted, and a fault still demands a frame that cannot
be produced — the kernel has no graceful move left. It invokes the **OOM (out-of-memory)
killer**: it scores the running processes by how much memory they are hogging and how
expendable they are, picks a victim, and kills it outright to reclaim its frames. Brutal, but
the alternative is the whole system seizing up.

There is a degenerate regime worth naming. If the genuinely-in-use ("working") set of pages is
larger than physical RAM, every page the kernel evicts to satisfy one fault is one that some
process needs again almost immediately — so it faults straight back in, forcing yet another
eviction. The machine spends nearly all its time shuttling pages between RAM and disk and almost
none running the programs. This collapse is called **thrashing**, and it is the failure mode
that bounds how far overcommit and demand paging can be pushed: the scheme is a triumph when the
touched set fits in RAM, and a disaster when it does not.

## Prerequisites

- [[page-table]]
- [[page-fault]]
- [[mmu]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "Demand paging — memory that doesn't exist yet":
  `malloc(1GB)` creating 262,144 not-present [[page-table]] entries with ~0 bytes of physical
  RAM, the first write triggering a page fault (interrupt #14) whose handler allocates a frame,
  zero-fills it, updates the entry to present, and resumes the faulting instruction invisibly to
  the program; the virtual-size vs resident-set distinction; and the minor/major/invalid fault
  taxonomy (first-touch needs no disk, swapped-out pages need a disk read, invalid addresses get
  SIGSEGV), with each page costing one fault on first access and none thereafter. Section "What
  happens when RAM runs out?": overcommit promising more memory than exists, and the OOM killer
  scoring and killing a process when physical RAM plus swap are exhausted.
