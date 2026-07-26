---
id: copy-on-write
title: Copy-on-Write
summary: Copy-on-write (COW) is the trick that makes fork-exec's fork() instant and memory-cheap.
type: concept
tags: [os/memory]
prereqs: [demand-paging, fork-exec, page-table, page-fault]
sources:
  - linux-internals-complete.html ("Copy-on-write — how fork() is instant", "Python's copy-on-read problem")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Copy-on-Write

## Summary

**Copy-on-write (COW)** is the trick that makes [[fork-exec]]'s `fork()` instant and
memory-cheap. `fork()` is *supposed* to give the child a private copy of all the parent's
memory — but physically duplicating it would mean copying every byte the parent holds, possibly
gigabytes, before the child runs a single instruction. COW defers that copying. Instead of
duplicating memory, the kernel lets parent and child **share the very same physical memory**,
and marks every shared chunk **read-only** in both. As long as both processes only *read*, they
share one copy and nothing is duplicated. The first time either one *writes* to a shared chunk,
the hardware refuses the write and traps into the kernel — the *exact* same fault-on-access
mechanism [[demand-paging]] uses to do work lazily — and the kernel responds by copying just
*that one* chunk into fresh memory, handing the writer its own private writable copy, and
resuming the write. Hence "copy on write": the copy happens at the moment of the write, and only
for the chunk actually written. The cost of `fork()` becomes proportional to what the child
later *modifies*, not to how much memory the parent has.

## Grounded explanation

### The problem COW solves: `fork()` promises a copy it cannot afford to make

Recall from [[fork-exec]] what `fork()` is supposed to do. It **duplicates the calling process**:
afterward two processes exist, and the child is a near-identical copy of the parent — same code,
and crucially the *same contents of memory*, the same variables holding the same values, but in
the child's *own* private memory. "Private" matters: if the parent later changes a variable, the
child must not see the change, and vice versa. They start equal and then drift apart
independently. [[fork-exec]] already flagged, in an aside, that the kernel does not literally copy
the bytes up front; this node is that aside, made the whole story.

To see why a literal copy is unacceptable, recall the other half of [[fork-exec]]: the
overwhelmingly common idiom is `fork()` *immediately followed by* `exec()` in the child. And
`exec()` **throws the entire inherited memory away** — it replaces the program running in the
process, discarding all the old code and data to load a fresh program from disk. So in the common
case, the child's faithful copy of the parent's memory lives for microseconds and is then
deleted, untouched. Eagerly duplicating gigabytes only to discard them an instant later is pure
waste. Even when the child does *not* `exec()` (the worker-copy pattern from [[fork-exec]]), it
typically reads most of its memory and writes only a little. Either way, copying everything up
front pays a huge cost for a copy that is mostly never needed.

So the design tension is sharp. The child needs the *illusion* of a private copy of all the
parent's memory — full, independent, writable. But materializing that illusion eagerly is
ruinous. COW is how the kernel delivers the illusion while paying only for the parts that turn
out to matter.

### The mechanism: share read-only, then copy on the faulting write

First, the substrate, in plain terms. A process does not address physical memory directly. Its
memory is divided into fixed-size chunks — **pages**, typically 4 KB each — and the kernel keeps a
per-process **[[page-table]]**: a lookup that, for each page of the process's view of memory, records
*which* physical page of RAM it currently maps to and *what access* is permitted there (in
particular, read-only versus read-write). The hardware consults this table on every memory access
and enforces the permission. This is the same machinery [[demand-paging]] relies on: a mapping the
kernel controls, and a hardware check that can raise a **[[page-fault]]** — trap into the kernel —
when an access is not (yet) permitted, letting the kernel step in, do some work, fix up the
mapping, and resume the instruction as if nothing happened.

COW uses that machinery in three moves.

**Move 1 — at `fork()`, share instead of copy.** The kernel does *not* allocate new physical
pages for the child or copy any contents. It gives the child a page table whose entries point at
the *parent's existing physical pages* — the very same RAM — and then, for every page that could
be written, marks the entry **read-only in both the parent's and the child's tables**. (Pages that
were already read-only, like program code, need no change — they were never going to be written
anyway.) The only thing duplicated up front is the page table itself, which is tiny compared to
the memory it describes. The kernel also keeps, per physical page, a small count of how many
processes are currently sharing it — a **reference count** — so it knows when a page is still
shared versus owned by one process alone. After this move, parent and child have *identical*
views of memory, backed by *one* physical copy, and zero bytes have been copied.

**Move 2 — reads just work.** Because both mappings are valid for reading, any read by either
process succeeds directly against the shared physical page, with no fault and no kernel
involvement. Two processes reading the same data is harmless — they cannot disturb each other by
looking. This is why the common case is free: a child that only reads, or that `exec()`s before
writing, never triggers any copying at all.

**Move 3 — the first write faults, and *that* is when the copy happens.** Suppose the child tries
to write to one of the shared pages. The hardware checks the child's [[page-table]] entry, sees
read-only, and refuses — raising a [[page-fault]] that traps into the kernel, exactly the
fault-and-resume pattern of [[demand-paging]]. The kernel inspects the situation and recognizes
it: this page is marked read-only *not* because the memory is meant to be immutable, but because
it is a shared COW page and someone is now writing it. So the kernel:

1. allocates a **fresh physical page**;
2. copies the contents of the shared page into that fresh page;
3. updates the *writer's* page-table entry to point at the fresh page and marks it **read-write**;
4. decrements the shared page's reference count, since one fewer process now shares it.

Then it resumes the faulting instruction, which now writes successfully into the writer's own
private page. The other process keeps pointing at the original page with its original contents,
unaffected. The illusion is preserved exactly: each side now has its own copy of *this* page and
can diverge freely — and the copy was made precisely when, and only because, a write demanded it.

There is one detail worth stating so the invariant is airtight. If a page ends up shared by only
*one* remaining process — its reference count has fallen back to one — the kernel can quietly
restore that lone owner's entry to read-write without copying anything, because there is no longer
anyone to protect the data from. The read-only mark is not about the data being constant; it is
purely a tripwire that says "more than one process is relying on these exact bytes, so intercept
the next write." When that stops being true, the tripwire is removed.

The key insight — the *why* behind the whole trick — is that **read sharing is safe and write
sharing is not**. Two processes can read one physical copy forever with no conflict; the moment a
write would let one of them change what the other sees, and *only* then, do they actually need
separate copies. COW spends nothing until that exact moment arrives, page by page. The cost is
therefore proportional to the *writes* the child performs, not to the total memory it inherited.

### Worked instance: a 1 GB process forks and the child writes one page

Take a process using **1 GB** of writable memory. With 4 KB pages, that is
`1,073,741,824 / 4,096 = 262,144` pages, each backed by its own physical page of RAM.

**At `fork()`.** The kernel builds the child's page table with 262,144 entries, all pointing at
the parent's existing 262,144 physical pages, and flips every one of those pages to read-only in
*both* tables, bumping each page's reference count to 2 (parent + child). **Bytes of memory data
copied: 0.** This is why the source can say a process can `fork()` in microseconds regardless of
its size — the work is proportional to the page table, not the gigabyte behind it. Right now the
child is a perfect logical copy backed entirely by shared physical pages.

**The child writes to one page.** The child stores a value into a single variable that happens to
live on one particular page — call it page *P*. The hardware sees *P*'s entry is read-only in the
child and faults into the kernel. The kernel recognizes a COW fault, allocates **one** fresh
physical page, copies *P*'s 4 KB of contents into it, repoints the child's entry for *P* at the
fresh page marked read-write, and drops *P*'s reference count from 2 back to 1. The write then
completes into the child's private copy. Total memory copied for this entire write:
**exactly one 4 KB page.** The other `262,143` pages remain shared, read-only, untouched — still
one physical copy each, serving both processes.

So a `fork()` of a 1 GB process followed by a single write costs 4 KB of copying, not 1 GB — a
factor of about 262,000 saved. And note the branch this instance deliberately exercises: it is
*not* the degenerate "child writes nothing" case (which would copy zero and hide the whole
fault-and-copy path), nor the "child rewrites everything" case (which would eventually copy all
262,144 pages and collapse COW's benefit). It is the realistic middle — a few writes — where COW's
selectivity is the entire point: you pay for the handful of pages you dirty and share the rest.

**And if the child `exec()`s instead.** Had the child followed the common [[fork-exec]] idiom and
called `exec()` right after the `fork()`, *all* 262,144 shared pages would simply be discarded as
the new program's address space is laid out. Not even page *P* would have been copied, because no
write would have occurred first. The 1 GB duplication an eager copy would have performed is, in
this case, work that produces nothing — exactly the waste COW exists to avoid.

### A real-world wrinkle: Python's "copy-on-read"

COW assumes that reading is free because reading does not write. A high-level language can quietly
break that assumption, and the source gives the classic example. In CPython, every object carries
a small **reference count** in its header — a number tracking how many references point at it —
and Python *increments* that count whenever the object is merely touched: passed to a function,
iterated over, even "read" in a loop. But incrementing a counter that lives *inside the object's
page* is a **write** to that page. So a forked Python worker that only intends to *read* a large
shared structure ends up writing a refcount into nearly every page it touches, tripping a COW
fault and copying each page anyway — "copy-on-read" in effect — and Python's periodic
cycle-collecting garbage collector makes it worse by scanning objects the worker never meant to
read. The shared pages COW worked to preserve get copied regardless. (Mitigations exist —
keeping bulk data outside Python's refcounted object model, or freezing existing objects so the
collector stops scanning them — but the lesson stands: COW only saves you to the extent your
reads stay *actually* read-only down at the level of physical pages.)

## Prerequisites

- [[fork-exec]]
- [[demand-paging]]
- [[page-table]]
- [[page-fault]]

## Sources

- `linux-internals-complete.html` — section "Copy-on-write — how fork() is instant" (parent and
  child share the same physical pages marked read-only; a write triggers a page fault; the kernel
  allocates a new page, copies the 4 KB, and gives the writer a private writable copy while the
  other keeps the original; `fork()` of a multi-GB process is near-instant because only the page
  table is duplicated, and most children `exec()` so the copy never happens), and "Python's
  copy-on-read problem" (per-object reference counts make merely reading objects a write to their
  pages, so forked Python workers trigger COW copies on data they only meant to read, with the
  garbage collector compounding it).
