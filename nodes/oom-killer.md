---
id: oom-killer
title: OOM Killer
summary: "The OOM (out-of-memory) killer is the kernel's last resort for the one situation demand-paging cannot bluff its way out of: a page fault demands a physical frame, every frame is…"
type: concept
tags: [os/memory]
prereqs: [demand-paging, page-fault, swap]
sources:
  - linux-internals-complete.html ("What happens when RAM runs out?", §6 "The OOM killer — the kernel's last resort")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# OOM Killer

## Summary

The **OOM (out-of-memory) killer** is the kernel's last resort for the one situation
[[demand-paging]] cannot bluff its way out of: a [[page-fault]] demands a physical frame, every
frame is already in use, and there is no way to free one — not by reclaiming caches, not by
writing some page out to [[swap]], because both physical RAM and swap are full. There is no
graceful answer left. The kernel cannot give a frame it does not have, and stalling the
faulting program forever or failing the access would often take down more than one process.
So the kernel deliberately *destroys* a process to recover its frames. It assigns every
running process an **oom_score** — a number that grows with how much memory the process is
using — and sends a kill signal to the highest-scoring one, the biggest memory hog. That
process's frames are freed instantly, the faulting program gets one, and the system survives.
The score is tunable per process (via an adjustment knob, **oom_score_adj**) so an operator
can mark some processes as preferred victims and others as nearly untouchable. The whole
predicament exists *because* [[demand-paging]] lets the kernel **overcommit** — promise more
memory than the machine physically has — on the bet that not everything will be touched at
once; the OOM killer is what runs when that bet loses.

## Grounded explanation

### Where this picks up — the fault that cannot be served

The [[demand-paging]] node ended at exactly the cliff this concept walks off. There, the
kernel materializes physical memory lazily: a process can reserve a region, but the kernel
attaches no real **frame** (a fixed-size block of physical RAM, 4 KB on a typical machine) to
any page until the program first *touches* it. The first touch of a page that has no frame
raises a **page fault** — the hardware pauses the instruction and asks the kernel to attach a
frame and finish the mapping. Normally the kernel just hands over a free frame and resumes.
When free frames run low, it makes more by **eviction**: it writes some currently-resident,
little-used page out to [[swap]] (a reserved area on disk that holds pages displaced from RAM)
and reuses that page's freed frame.

[[demand-paging]] noted that this defers the cost of frames but cannot conjure frames that do
not exist, and named the breaking point without explaining it. That breaking point is this
node. Picture the moment precisely: a [[page-fault]] arrives — a program touched a
valid page that is owed a frame — but **every physical frame is occupied**, and eviction is no
escape because **[[swap]] is also full**, so there is nowhere to write a page out to in order to
free its frame. The kernel is asked to produce a frame and has no source for one. This is the
out-of-memory condition: not "low on memory," but "a fault is owed a frame and none can be
created by any ordinary means."

### The why — overcommit makes this inevitable, and killing beats the alternatives

To see why a kernel ever lands here, recall the bet [[demand-paging]] makes. Because a reserved
page costs nothing until touched, the kernel hands out far more *promised* (virtual) memory than
it has *physical* RAM, trusting that processes touch only a fraction of what they reserve. This
practice of promising more than exists is called **overcommit**. Almost always it pays off — the
sum actually touched stays under the physical limit, and no one notices the promises were
oversubscribed. But overcommit is a bet, and bets can lose: if enough processes touch enough of
their promised pages at the same time, the *touched* total exceeds physical RAM plus swap, and
then some fault must go unserved. Overcommit is what makes the out-of-memory condition reachable
at all; without it the kernel would refuse a promise it could not keep, up front, instead of
discovering at fault time that it cannot keep one.

Now the design question: faced with an unservable fault, what *should* the kernel do? Consider
the alternatives. It could fail the access — but a program touching its own validly reserved
memory does not expect that touch to fail, and most have no code to cope; failing it typically
crashes the program anyway, and possibly several. It could suspend the faulting program until
memory appears — but if every process is in the same bind, memory never appears, and the machine
hangs, frozen, helping no one. Against those, deliberately killing **one** process is the least-bad
move: the chosen victim's entire memory is reclaimed at once, which is usually enough to satisfy
the pending fault and several after it, and every *other* process keeps running. The key insight is
that the resource the kernel needs — frames — is exactly what a dead process gives back. So the
kernel does not try to shave memory from everyone; it picks one process and takes *all* of its
frames. The invariant it preserves is **system liveness**: better that one program dies than that
the whole machine seizes.

### The mechanism — score, pick, kill

The kernel turns "kill one process" into a definite choice with a number. It computes, for every
candidate process, an **oom_score**: a value that rises roughly in proportion to how much physical
memory the process is consuming. The bigger the memory hog, the higher its score — because killing
a big consumer frees the most frames per casualty, getting the system the furthest out of trouble
with a single death. The score is not purely mechanical, though: each process carries an adjustment
value, **oom_score_adj**, that an operator can set to bias the decision. A negative adjustment
lowers a process's effective score, protecting it (the most critical system process is pinned to
the most protective value so the killer will essentially never choose it); a positive adjustment
raises the score, volunteering a process to die earlier. This is how an administrator declares a
policy — "sacrifice these expendable workers before you ever touch the core services" — that the
raw memory-usage number alone would not express.

Having scored everyone, the kernel selects the **highest-scoring** process and issues the
strongest possible kill: a signal the target cannot catch, block, or ignore, so it stops
immediately with no chance to refuse or clean up. (On Linux this is `SIGKILL`; the point is only
that it is unconditional and instant.) The instant that process ends, the kernel reclaims **all**
the frames it held — those frames return to the free pool. The pending [[demand-paging]] fault is
now serviceable: the kernel takes one of the just-freed frames, completes the mapping the fault was
waiting on, and resumes the faulting instruction as if nothing unusual had happened. The program
that faulted never learns that another process died so it could continue. From its point of view,
its first touch of a page simply took a little longer than usual.

### Worked instance — 8 GB RAM, 2 GB swap, 14 GB promised

Take a machine with **8 GB of physical RAM** and **2 GB of swap** — so the absolute ceiling on
memory that can be backed at once is 8 + 2 = **10 GB**. Thanks to overcommit, the kernel has
nonetheless handed out reservations totaling **14 GB** across several processes, betting they will
not all be touched. Suppose the largest single process, call it **P_big**, has touched **6 GB** of
real memory; the rest of the processes together have touched another **3.5 GB**. Touched total so
far: 6 + 3.5 = 9.5 GB, which still fits inside the 10 GB ceiling (RAM is full and 1.5 GB of swap is
in use), so everything is running — slowly, because the machine is already leaning on swap, but
running.

Now P_big touches one more fresh page it was promised but had never accessed. That touch is a
[[demand-paging]] fault: P_big is owed a frame. The kernel looks for one. There are no free frames
(all 8 GB of RAM is occupied). It tries eviction — write some resident page to swap to free its
frame — but swap has only 0.5 GB left and the kernel cannot make meaningful progress; effectively,
**RAM + swap are exhausted** at the 10 GB ceiling and a fault is still owed a frame that cannot be
produced. The out-of-memory condition has arrived.

The kernel runs the OOM killer. It scores every process. P_big, holding 6 GB resident, has by far
the highest oom_score — no other process is close, and none carries an oom_score_adj that would
demote it below the others. The kernel selects **P_big** and sends it the unconditional kill. P_big
dies, and its **6 GB of frames** return to the free pool at once. RAM occupancy drops from 8 GB to
2 GB. The kernel now easily serves the pending fault — it grabs one of the freed frames, finishes
P_big's... no: P_big is gone; it finishes the fault for *whichever* process needs it next — and the
machine, suddenly with gigabytes of headroom, returns to normal speed. One process was sacrificed;
every other process, and the system itself, lived.

### The slow death before the kill — thrashing

One caveat shapes how this feels in practice. The OOM killer does not fire the instant RAM fills;
it fires only when RAM **and** swap are both exhausted. In the gap between those two points — RAM
full but swap still has room — the kernel keeps the system limping along by evicting pages to swap
and faulting them back. If the genuinely-in-use set of pages is larger than RAM, this turns
pathological: nearly every page the kernel evicts to serve one fault is one some process needs again
almost immediately, so it faults straight back in, forcing another eviction. The machine spends
almost all its time shuttling pages between RAM and disk and almost none running programs — a
crawling, near-frozen state called **thrashing**. So the lived experience of running out of memory
is usually not a clean snap but a long, agonizing slowdown (thrashing) that *ends* in the OOM
killer's abrupt kill once swap, too, gives out. The kill, brutal as it is, is often the moment the
machine becomes usable again.

## Prerequisites

- [[demand-paging]]
- [[page-fault]]
- [[swap]]

## Sources

- `linux-internals-complete.html` — section "What happens when RAM runs out?", §6 "The OOM
  killer — the kernel's last resort": [[demand-paging]] enabling **overcommit** (promising more
  memory than physically exists on the bet that not all is touched); the failure when physical
  RAM plus swap are exhausted and a page fault arrives with no frame to give; the kernel's answer
  of picking a process to sacrifice — "typically the one using the most memory that isn't
  critical" — and killing it to free RAM, "Brutal, but the alternative is the entire system
  freezing." Under-the-hood detail: the killer **scores every process based on memory usage**,
  each process has an **oom_score_adj** that can be tuned, PID 1 is protected at score −1000, and
  container processes can be given higher scores so they die first; observable via
  `/proc/self/oom_score` and `/proc/self/oom_score_adj`. Thrashing is carried over from the same
  document's swap/eviction discussion (the working set exceeding RAM forcing constant
  evict-and-refault) as the slowdown preceding the kill.
