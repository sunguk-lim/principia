---
id: tlb
title: Translation Lookaside Buffer
summary: A translation lookaside buffer (TLB) is a small, very fast hardware cache, built into the CPU, that remembers recent virtual-page-to-physical-frame translations so the processor…
type: concept
tags: [os/memory]
prereqs: [page-table, mmu, context-switch]
sources:
  - linux-internals-complete.html (§5 "Context switching"; glossary "TLB"; "the kernel is the manager, the MMU is the enforcer")
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Translation Lookaside Buffer

## Summary

A **translation lookaside buffer** (TLB) is a small, very fast hardware cache, built into
the CPU, that remembers recent virtual-page-to-physical-frame translations so the processor
can skip the expensive lookup through the [[page-table]] on almost every memory access. The
[[page-table]] is the authoritative book of where each virtual page lives, but it is a
*multi-level tree*, so consulting it means reading several tables in RAM — slow to do on
every single access. The TLB is the sticky note beside that book: it holds just the handful
of translations the program is using right now. On each access the hardware checks the TLB
first. A **TLB hit** returns the frame almost instantly (roughly one clock cycle); a **TLB
miss** falls back to the full tree walk through the [[page-table]] (several memory reads),
and the result is then stored in the TLB so the next access to that page is a hit. The TLB
works because programs have **locality**: they touch the same few pages over and over, so a
tiny cache covers the overwhelming majority of accesses and makes translation nearly free.
Its one sharp cost: because each process has its own [[page-table]], switching processes can
force the TLB to be emptied — a **TLB flush** — leaving the new process with cold,
un-cached translations, which is a large part of why context switches are expensive.

## Grounded explanation

### What the TLB is, and the problem it removes

The [[page-table]] left one thing painful. It established that every memory access — every
instruction fetch, every pointer dereference — must first translate a virtual address into a
physical one, and that the structure holding those translations is a *multi-level tree*: to
turn one virtual page number into a physical frame, the address hardware starts at the top of
the tree and walks down through several tables, each stored in RAM, picking the next table at
each level until it reaches the leaf entry holding the frame. That tree is what makes the
[[page-table]] affordable in storage — it spends memory only on the regions a process
actually uses. But it makes each translation *expensive in time*: a single address lookup now
costs several reads from RAM, and a read from RAM is far slower than the CPU's own clock.
Paying that on *every* access would mean every memory reference drags a multi-step walk behind
it, and the machine would crawl.

The translation lookaside buffer is the fix. Define it precisely: the **TLB** is a small,
very fast cache — a few dozen to a few thousand slots — sitting inside the [[mmu]], the
hardware unit that performs address translation on every memory access, where each slot stores
one recently used translation: a virtual page number paired with the physical frame number it
maps to (plus the permission bits the [[page-table]] entry carried). A **cache**, in this sense, is just a small fast store that keeps copies of a few
items from a larger slow store, so that repeated requests for those items are answered from
the fast copy instead of going all the way to the slow original. The slow original here is the
[[page-table]] in RAM; the fast copy is the TLB inside the chip.

### How a lookup uses it: hit and miss

On every memory access, the address hardware does the same thing first: it takes the virtual
page number and checks whether the TLB already holds a translation for it. Two outcomes:

A **TLB hit** — the page number is in the TLB. The hardware reads the frame straight out of
the matching slot and is essentially done; this costs on the order of a single clock cycle, so
fast that the translation is nearly invisible. The whole tree walk through the [[page-table]]
is skipped entirely.

A **TLB miss** — the page number is *not* in any slot. Now there is no shortcut: the hardware
must do the full walk down the [[page-table]] tree, several reads from RAM, to find the frame.
But it does one more thing: once the walk produces the frame, that virtual-page-to-frame pair
is **written into the TLB**, evicting some older slot if the TLB is full. This is the key move
— the miss *pays the full cost once and caches the result*, so the very next access to that
same page will be a hit and cost almost nothing.

So the TLB does not replace the [[page-table]]; it sits in front of it. The [[page-table]]
remains the complete, authoritative record of every mapping; the TLB is a fast cache of the
few mappings in active use, refilled from the [[page-table]] on each miss.

### Why it works: locality makes a tiny cache enough

The reason a cache this small can cover almost every access is **locality**: real programs do
not scatter their memory references uniformly across their whole address space. They touch the
same few pages repeatedly over any short stretch of time — the page holding the loop they are
running, the page holding the array they are scanning, the page holding their stack. A program
might use gigabytes of address space over its whole life yet, in any given moment, be working
inside just a handful of pages. A cache only needs enough slots to hold *that handful*. So
even though it stores a tiny fraction of all translations, it answers the overwhelming
majority of accesses from the fast path. The invariant the TLB maintains is simple: any
translation it reports as a hit is one the [[page-table]] would have produced by a full walk —
it is a faithful copy, never an independent source of truth. That is why it is safe to trust a
hit without re-walking the tree.

### The sharp cost: per-process tables force a flush

Here is the TLB's one genuinely hard problem, and it comes directly from a fact about the
[[page-table]]: there is a *separate* [[page-table]] per process. The same virtual page number
means a different physical frame in process A than in process B, because each consults its own
book. The CPU has a register that points at "the [[page-table]] to use right now" (on x86-64
it is named CR3), and switching from process A to process B means reloading that register to
point at B's book.

But the TLB is full of *A's* translations — A's virtual-page-to-frame pairs. The instant the
register swings to B's [[page-table]], every one of those cached translations is wrong: B's
same page numbers map to entirely different frames. If the hardware kept trusting them, B would
read A's memory. So the safe move is to **flush** the TLB on the switch — throw away its
contents — so that no stale translation survives. (A *flush* is exactly that: emptying the
cache so every slot is marked invalid.) The consequence is that B begins life with a **cold**
TLB: its first access to every page it uses is a miss, forcing a full walk through B's
[[page-table]], until enough accesses have happened to *warm* the TLB back up. This re-warming
cost — many forced misses right after a switch — is a major reason a [[context-switch]] (the act
of saving one process's state and loading another's so they can share one CPU) is expensive,
and why a system that switches between processes too frequently loses performance.

There is a partial escape, used by real hardware: a **tagged TLB**, where each slot also
records *which process* the translation belongs to (an address-space identifier, ASID). With
tags, a switch no longer has to flush — B's lookups simply ignore slots tagged for A, and A's
translations can still be sitting there, valid, if A runs again soon. Tagging trades a little
slot space for avoiding the cold-start penalty.

### Worked instance: a loop, then a context switch

Take a program running a tight loop that scans an array, and suppose the loop's code and the
array together live in two virtual pages, call them page **P** (the code) and page **Q** (the
array data). Walk through what the TLB does, deriving each step from the one before.

**First iteration.** The CPU fetches an instruction from page P. It checks the TLB for P:
nothing there yet — a **miss**. So it walks P down the [[page-table]] tree (several RAM reads),
finds P maps to some frame, and writes "P → that frame" into a TLB slot. Then the instruction
accesses the array on page Q: again a **miss**, again a full walk, and "Q → its frame" is
written into a second TLB slot. The first iteration therefore paid two full [[page-table]]
walks.

**Every later iteration.** The loop runs again from the same page P and touches the same array
page Q. Now both lookups are **hits**: P and Q are already in the TLB, so each translation
returns its frame in about one cycle, and *no* walk happens. A loop of a million iterations
thus pays the walk cost essentially twice — on iteration one — and runs the other 999,999
iterations with translation nearly free. This is locality turned directly into speed: a
two-slot working set, cached once, serves the entire loop.

**Then a context switch.** The timer interrupt fires and the scheduler switches to another
process, B. The kernel reloads the page-table register to B's [[page-table]] and, with an
untagged TLB, **flushes** it — P and Q's slots are discarded. When our program eventually runs
again, its loop starts cold: the very next fetch from page P is a **miss** once more, forcing a
fresh walk, and so is the first touch of Q. The two warm slots it had built up are gone; it
must re-walk the [[page-table]] to rebuild them. That re-walk on resume — multiplied across
every page a process was using — is the concrete shape of the "context switches are expensive"
claim: the cost is not just saving and loading registers, it is the cold TLB the switched-to
process inherits.

The contrast across the example is the whole point. Within an undisturbed loop the TLB makes
translation vanish — one walk, then a million free hits. Across a process switch the same TLB
becomes a liability that must be emptied for safety, and the new process pays misses until it
warms back up. The TLB is exactly this trade: a tiny fast copy of the [[page-table]] that
makes per-access translation nearly free as long as a process keeps running, at the price of
going cold whenever the machine turns its attention to a different [[page-table]].

## Prerequisites

- [[page-table]]
- [[mmu]]

## Sources

- `linux-internals-complete.html` — glossary entry "TLB" (a CPU cache for recent
  virtual-to-physical address translations; a TLB miss forces a page-table walk); §5
  "Context switching", which names step 3 (switching the page-table pointer, the `CR3`
  register, to the incoming process) as the expensive part *because* the TLB "gets partially
  flushed," costing ~1–5 microseconds and making frequent context switches hurt performance;
  and the memory-management passage "the kernel is the manager, the MMU is the enforcer,"
  where on every context switch the kernel loads the incoming process's page-table base into
  `CR3` and the TLB "is flushed or tagged so stale entries are not reused." The minor-fault
  passage also notes that after a page's first touch the MMU translates it purely in hardware
  "with the TLB caching the translation."
