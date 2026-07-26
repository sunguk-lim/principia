---
id: swap
title: Swap
summary: Swap is a reserved area on disk — a dedicated disk partition or a regular file — that the kernel uses as an overflow extension of physical RAM.
type: concept
tags: [os/memory]
prereqs: [demand-paging, page-fault]
sources:
  - linux-internals-complete.html ("What happens when RAM runs out?", major-fault row of the fault taxonomy, "Virtual vs physical, restated")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Swap

## Summary

**Swap** is a reserved area on disk — a dedicated disk partition or a regular file — that the
kernel uses as an overflow extension of physical RAM. When RAM fills up and the kernel needs a
free physical frame (a 4 KB block of real memory) but has none, it picks a resident page that
looks little-used, copies that page's contents *out* to the swap area, and frees the frame. The
page's data now lives on disk instead of in RAM. Later, when some program touches that
evicted page, the access faults and [[demand-paging]] brings the page back *in* from swap into a
fresh frame. So swap turns "out of RAM" into "some pages are slower to reach" rather than an
immediate failure: it is exactly the backing store that the page-out / page-in machinery of
[[demand-paging]] reads from and writes to. The catch is speed. Disk is on the order of 100,000
times slower than RAM, so parking genuinely cold pages there is nearly free, but if the pages a
program is *actively using* do not fit in RAM, every page the kernel evicts is needed again almost
at once — the system collapses into **thrashing**, spending nearly all its time moving pages
between RAM and disk instead of running code.

## Grounded explanation

### Where this picks up — the disk side of the page-out half

[[demand-paging]] established two halves of one mechanism. The half it dwelt on is **paging in**:
a page-table-style entry is left "not present," and the first touch of the page raises a
restartable **page fault** that the kernel repairs by attaching a real frame, after which the
instruction reruns and succeeds invisibly. The other half is **eviction** (paging out): when RAM
is full and a fault still needs a frame, the kernel takes a resident page, marks its entry "not
present" again, and reuses its frame elsewhere — and to do that without destroying the page's
data, it must first stash those bytes *somewhere*. [[demand-paging]] named that destination in
passing and moved on. **Swap is that destination, treated as its own thing.**

Define it precisely. **Swap** (also called swap space) is storage on a *disk* set aside to hold
the contents of pages that the kernel has decided to remove from RAM. It is not RAM and not part
of any program's files; it is scratch space owned by the kernel for one purpose — holding
evicted page data until it is needed again. It takes one of two physical forms, which behave
identically for our purposes: a whole **swap partition** (a slice of the disk formatted for this
role) or a **swap file** (an ordinary file on an existing filesystem that the kernel treats as
swap). Either way, the idea is the same: a chunk of slow disk that the kernel can pour
overflowing memory into.

A **page** here means a 4 KB unit of a program's memory, and a **frame** means a 4 KB unit of
real physical RAM that can hold one page's worth of data — the same vocabulary [[demand-paging]]
used. Swap is measured in those same 4 KB units: when a page is "swapped out," its 4 KB of data
sits in 4 KB of swap on disk, and the frame it used to occupy is now free.

### The why — extend usable memory without lying to the program

Why have swap at all? Because the alternative, when RAM runs out, is failure: a program asks to
touch a valid page, no frame is free, and there is nowhere to put the data of any current page to
make room — so the kernel can only refuse, killing the program. Swap removes that dead end. By
giving the kernel a place to *set aside* the contents of pages that are not being used right now,
it lets the total amount of memory programs can have *touched and filled* grow beyond the size of
physical RAM, up to **RAM plus swap**. The machine behaves as if it had more memory than it
physically does.

The key insight that makes this honest rather than a trick is that **most of a running system's
pages are cold at any given moment.** A program loads its whole executable and every library, but
runs only a little of it; it allocates buffers it rarely revisits; a background application you
have not clicked in an hour is just sitting there, its pages untouched. Those cold pages are
occupying frames they are not earning. Swap lets the kernel reclaim exactly those frames —
demote the cold data to disk, hand the freed RAM to whatever is actually working — and the
program never knows, because the moment it *does* touch a demoted page, [[demand-paging]] faults
it back in before the instruction completes. The invariant is the same one [[demand-paging]]
guarantees: from the program's point of view a page is always there when accessed; swap only
changes *how long* the access takes, never *whether* it succeeds. Swap is therefore the concrete
embodiment of the line "the physical backing every process shares is RAM plus swap" — swap is the
*plus*.

### The mechanism — page out, then page in

Trace the two directions, because swap is defined by being the disk endpoint of both.

**Paging out (eviction).** The kernel decides it needs a free frame and has none. It chooses a
victim page that is currently resident — preferring one that has not been accessed in a long time,
on the bet that "not touched recently" predicts "not touched soon," so reclaiming it is least
likely to hurt. It then writes that page's 4 KB of contents out to a free slot in the swap area on
disk. Once the bytes are safely on disk, it changes the page's translation entry to "not present"
and records *where in swap* the data now lives, then releases the frame for reuse. The page still
logically belongs to its program and is still inside a valid region; it has simply been relocated
from RAM to disk. This write-out is the kernel's, not the program's — the program is not even
running at that instant and is unaware its page was moved.

**Paging in (return).** Sometime later the program executes an instruction that touches that very
page. The hardware finds the entry "not present" and raises a [[page-fault]] — the ordinary
[[demand-paging]] fault, restartable as always. But now the handler sees that this is not a
brand-new page needing a zeroed frame; the entry records that the data is sitting in swap. So the
kernel grabs a free frame, issues a **disk read** to copy the 4 KB back from swap into that frame,
updates the entry to "present, pointing at the new frame," and reruns the instruction, which now
succeeds. The page is back in RAM, identical to before it left.

Here is the one cost distinction that is the whole reason swap deserves its own treatment.
[[demand-paging]] separated faults by cost: a fault that just needs a fresh zeroed frame is cheap
because it touches no disk, while a fault whose data must be read back from disk is far slower
because it must wait on the disk. **A page-in from swap is the slow kind.** The frame allocation
is instant, but the disk read is not: the CPU cannot proceed until the bytes arrive, and disk
latency dwarfs memory latency by roughly five orders of magnitude. Reaching a page that is in RAM
costs tens of nanoseconds; reaching a page that has been swapped out costs the disk read —
comparatively forever. That single fact governs everything good and bad about swap.

### The why-it-can-be-catastrophic — the working set and thrashing

Because a page-in from swap is so slow, swap is only a good deal when the slow path is taken
*rarely*. Whether it is rare depends on one quantity: the **working set** — the set of pages a
program (or the whole system) is actually using over the current stretch of time, as opposed to
the far larger set it merely has reserved. Swap works beautifully when the working set fits in
RAM, because then the only pages that ever get evicted are cold ones outside the working set, and
they are, by definition, not touched again soon — so the expensive disk reads almost never happen.
The cold data rests on cheap disk; the hot data stays in fast RAM; everyone wins.

The disaster comes when the working set is *larger* than physical RAM. Now every page the kernel
evicts to satisfy one fault is a page that something needs again almost immediately. That page
faults straight back in (a slow disk read), which forces the kernel to evict yet another page that
*it* needs, which faults back in, and so on. The machine enters a regime where almost every memory
access is a disk round-trip and almost no useful instructions execute between them. This collapse
is called **thrashing**: the system is busy at 100% yet accomplishes nearly nothing, because it
spends its time shuttling the same hot pages between RAM and swap. This is the boundary on how far
swap can stretch memory — it converts "not enough RAM" into "slower memory" only as long as the
hot data fits; past that point it converts it into a grinding standstill, the precursor to the
kernel running entirely out of RAM-plus-swap and resorting to killing a process outright to
reclaim memory.

### Worked instance — a backgrounded app, then two greedy ones

Take a machine with, say, 8 GB of RAM and a swap area on disk, running an active editor in the
foreground and a large application minimized in the background.

**Pressure, then eviction.** The foreground editor starts touching more pages (opening big files),
and RAM fills. A fault arrives needing a frame, but none is free. The kernel looks for cold pages
and finds plenty in the background app — you have not clicked it in twenty minutes, so its pages
have not been accessed. It writes a batch of those pages out to swap, 4 KB each, marks their
entries "not present" with a swap location recorded, and hands the freed frames to the editor. The
editor speeds along; the background app's data is now resting on disk. Nothing has been lost — and
crucially, nothing has felt slow, because the evicted pages were not being used.

**The slow return.** Later you click back to the background app. Its first instruction touches a
page that was swapped out. Fault → the handler sees the data is in swap → it allocates a frame and
issues a disk read to pull the 4 KB back → updates the entry → reruns the instruction. Multiply
that by the hundreds of pages the app touches as it redraws, each a separate disk read, and you get
the familiar lurch: the app is *sluggish for a moment on return*, then smooth once its working set
is back in RAM. That sluggishness is precisely the page-in cost of swap, paid once per evicted page
as it is reclaimed.

**The collapse.** Now suppose instead that *both* applications stay active and their combined
working sets total 10 GB — more than the 8 GB of RAM. To give the editor the page it needs, the
kernel must evict a page the background app is using; the instant the background app runs, it
faults that page back in (slow disk read), which forces evicting a page the editor is using; the
editor faults it back in; and the cycle never settles. Both apps now run at disk speed instead of
RAM speed — orders of magnitude slower — and the machine crawls. That is thrashing: the same swap
mechanism that was invisible and free in the first scene becomes ruinous here, purely because the
hot set no longer fits in RAM.

## Prerequisites

- [[demand-paging]]
- [[page-fault]]

## Sources

- `linux-internals-complete.html` — section "What happens when RAM runs out?": overcommit
  promising more memory than physically exists, and physical RAM **plus swap** being the shared
  pool that can be exhausted. The fault-taxonomy table's **major fault** row: "the page's data
  lives on disk — swapped out … the kernel must do I/O," cost "Slow — disk read" (vs. a minor
  fault's "Fast — no disk") — the source of the RAM-vs-disk speed gap that defines swap's payoff
  and danger. The "Virtual vs physical, restated" box: each process can reserve far more than
  RAM, but "the sum of all *touched* pages across every process cannot exceed RAM + swap," fixing
  swap as the disk extension of the physical backing. The `kswapd` kernel thread that "watches
  memory pressure … moves unused pages to swap," and `SwapTotal` (swap space on disk) in
  `/proc/meminfo`, naming the physical swap area.
