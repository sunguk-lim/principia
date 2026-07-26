---
id: page-fault
title: Page Fault
summary: A page fault is the hardware trap the CPU raises the instant a memory access cannot be satisfied by the page-table — either the looked-up entry maps nothing valid, or the entry…
type: concept
tags: [os/memory]
prereqs: [page-table, interrupt]
sources:
  - linux-internals-complete.html ("Demand paging", "Copy-on-write", page-fault classification)
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Page Fault

## Summary

A **page fault** is the hardware trap the CPU raises the instant a memory access cannot be
satisfied by the [[page-table]] — either the looked-up entry maps nothing valid, or the entry
exists but the access violates its permission bits (for example, writing a page the entry marks
read-only). The faulting instruction is paused, and control jumps into the kernel's **page-fault
handler**, which classifies the cause and decides what to do. There are three outcomes. A
**minor fault** — the needed data is already in RAM (or can be made instantly, as a freshly
zeroed page) and the handler only has to fix up the [[page-table]] mapping; it is cheap. A
**major fault** — the page's data lives on disk and must be read in, a slow I/O. An **invalid
fault** — the access is simply not allowed (an address that maps nothing the program may use, or
a forbidden permission), so the kernel delivers a **SIGSEGV** signal (the "segmentation fault")
and usually kills the process. The fault matters far beyond error handling: it is the single hook
that makes a whole family of "lazy" memory features work. The kernel implements them by
*deliberately* leaving [[page-table]] entries absent or restricted and then doing the real work
inside the handler when the access finally arrives.

## Grounded explanation

### What a page fault is, and why "fault" is not a failure

Recall what the [[page-table]] does on every memory access: the hardware translation unit looks up
the virtual page being accessed, and the entry it finds tells it which physical frame holds that
page and what the program is allowed to do with it (present, readable, writable, user-accessible).
A **page fault** is what happens when that lookup *cannot complete the access* — and there are
exactly two ways it can fail. Either the entry does not validly map the page at all (it is marked
not-present, or the address falls in a region with no entry), or the entry is present but the
operation breaks one of its permission bits (a write to a page whose entry says read-only, an
ordinary program reaching for a kernel-only page). In both cases the hardware stops mid-access and
*traps* into the kernel.

The word "fault" is misleading if read as "malfunction." In CPU terminology a fault is a
**restartable exception**: the hardware hits something it cannot resolve on its own, pauses the
current instruction *before it completes*, transfers control to a kernel routine registered for
this exception, and — crucially — is prepared to **re-run the very same instruction** once the
kernel has fixed the situation. It is the same designed mechanism as a hardware [[interrupt]], not a
bug. The instruction that "faulted" frequently succeeds the second time, with the program never
aware anything happened. This restartability is the whole reason a fault can be used to do useful
work rather than only to report an error.

### The handler, and the two independent questions it asks

When the fault fires, control lands in the kernel's **page-fault handler** — a function the kernel
registered for this exception. The hardware hands it two facts: *which* virtual address was being
accessed, and *what kind* of access it was (read, write, or instruction fetch). From these the
handler must classify the fault, and it does so by answering two **independent** questions.

The first question is: **are you even allowed here?** Besides the [[page-table]] the kernel keeps,
per process, a separate record of which virtual address ranges are legitimate at all — which
ranges are "the heap," "the stack," "this mapped file," and with what permissions. (A
[[page-table]] entry can be deliberately absent for a page that is nonetheless *allowed*; the list
of allowed ranges is the authority on legitimacy, the [[page-table]] is the authority on where the
page currently sits.) If the faulting address lies in no allowed range, or the attempted operation
is forbidden there (writing where only reading is permitted), the access is **invalid**.

The second question, asked only if the access is allowed, is: **where is the page right now?** It
might need nothing but a fresh empty frame; it might already exist in RAM and need only a mapping
fix-up; or its actual data might be sitting on disk and have to be fetched. The first question is
the *valid-versus-invalid* axis; the second is the *minor-versus-major* axis. They are independent,
which is exactly why a write to a shared-but-read-only page is a cheap **minor** fault (allowed,
the data is in RAM, it just needs a private copy) while a write to read-only program code is an
**invalid** fault (the page is present, but you have no right to write it). Same operation — a
write to a present, read-only page — opposite verdicts, because the *allowed?* axis differs.

### The three outcomes

**Minor fault.** The access is allowed and the data is already in RAM (or can be conjured
instantly as a page of zeros). The handler does no disk I/O — it just allocates or locates the
frame and writes the correct entry into the [[page-table]], then restarts the instruction. This is
fast. A minor fault happens **once per page, on first access**: afterward the [[page-table]] entry
is valid and the translation hardware handles that page entirely on its own, with no further
faults. So first-touching a 1 MB region costs roughly 256 minor faults (one per 4 KB page) and
then zero faults thereafter.

**Major fault.** The access is allowed, but the page's data is not in RAM — it has been pushed out
to disk to reclaim memory, or it belongs to a file that has not yet been read in. The handler must
issue a disk read, wait for the I/O to finish, place the data in a frame, fix the [[page-table]]
entry, and only then restart the instruction. Because disk is orders of magnitude slower than RAM,
a major fault is the expensive kind.

**Invalid fault.** The access is not allowed: the address maps nothing the program may use, or the
operation violates a permission it cannot have. There is nothing legitimate to fix, so the handler
gives up on the access and delivers a **SIGSEGV** (segmentation violation) signal to the process.
A process can choose to catch this signal, but by default it has no handler for it and the kernel
terminates the process — this is the familiar **segmentation fault** crash.

### Why the page fault is central: it is the hook for lazy memory

Here is the point that makes this concept load-bearing rather than a footnote about errors. Every
"lazy" or shared-memory feature the kernel offers is built by *deliberately* leaving a
[[page-table]] entry absent or restricted, so that the next access to that page is guaranteed to
fault — and then putting the real work inside the handler. The fault is the trigger that lets the
kernel defer work until the exact moment it is unavoidable.

Three examples, all implemented this way. **Demand paging**: when a program asks for a large block
of memory, the kernel creates the virtual mapping but marks the [[page-table]] entries not-present
and allocates no physical frames; only when a page is actually touched does the resulting minor
fault cause the handler to hand out a real frame. This is why a program can "allocate" far more
than physical RAM as long as it never touches most of it. **Copy-on-write**: when a process forks a
child, the kernel does not copy memory; it points both [[page-table]]s at the *same* physical
frames and marks every shared page read-only. Reads work fine. The first time either side *writes*,
the read-only bit forces a fault; the handler recognizes it as copy-on-write, makes a private copy
of just that one page for the writer, and lets both continue — so the copy happens only for pages
actually modified. **Swap**: when RAM is scarce the kernel writes a rarely-used page out to disk and
clears its present bit; a later access faults (a major fault), and the handler reads the page back
before resuming. (The same trap underlies memory-mapped files, where file contents are read in
page by page on first access.) In every case the [[page-table]] entry is *intentionally* left in a
state that forces the fault, and the fault handler is where the feature actually lives.

### Worked instance: three accesses, three outcomes

Take one process and watch three different memory accesses, each hitting a different branch of the
handler's classification.

**(1) First touch of freshly allocated memory → minor fault.** The program called `malloc` for a
new region, so the kernel created the virtual mapping but left those [[page-table]] entries marked
not-present, backing no physical frame. The program now writes to an address in that region, say
`0x700000`. The translation hardware looks up the entry, sees *not present*, and raises a page
fault. The handler asks question one — is `0x700000` in an allowed range? Yes, it is in the region
just allocated. Question two — where is the page? It is brand-new, so there is no data to fetch; the
handler allocates one physical frame, fills it with zeros, and writes a present, writable entry
into the [[page-table]] pointing the page at that frame. No disk was touched, so this is a **minor**
fault. The faulting write instruction is restarted and now succeeds. Touch the same page again later
and there is no fault at all — the entry is valid.

**(2) Access to a page that was swapped out → major fault.** Earlier, under memory pressure, the
kernel wrote one of this process's pages to disk and cleared its present bit. The program now reads
that page. The lookup finds *not present* and faults. Question one: allowed? Yes — this page belongs
to a legitimate region; it is merely not resident. Question two: where is it? Its data is on disk.
So the handler issues a disk read, waits for the bytes to arrive, places them in a freshly allocated
frame, updates the [[page-table]] entry to present and pointing at that frame, and restarts the
read. Because real disk I/O happened, this is a **major** fault — the same restart-the-instruction
mechanism as case (1), but slow.

**(3) Dereference of a null or garbage pointer → invalid fault → SIGSEGV.** The program dereferences
a wild pointer, say address `0x0`. The lookup finds no valid mapping and faults. Question one:
allowed? No — `0x0` lies in no range the process may use. The handler stops here; the second
question is never reached because there is nothing legitimate to satisfy. There is no frame to
allocate and no data to fetch, so the handler delivers **SIGSEGV** to the process, which by default
terminates it. This is the crash a programmer sees as a "segfault."

The three cases share one machine and one trap, and differ only by the two answers the handler
computes. Cases (1) and (2) are both *allowed*, separated only by whether disk I/O was needed
(minor versus major); case (3) is *not allowed* at all (invalid). That branching is the entire
behavior of the concept: a page fault is the [[page-table]]'s failure-to-translate handed to the
kernel, and the kernel's classification of that failure decides whether the access is quietly
completed, completed after a slow disk read, or refused with a fatal signal.

## Prerequisites

- [[page-table]]
- [[interrupt]]

## Sources

- `linux-internals-complete.html` — section "Demand paging — memory that doesn't exist yet": the
  page fault as CPU interrupt #14 when a page-table entry is "not present," and the handler's
  four-step response (allocate a frame, zero it, fill in the entry, restart the faulting
  instruction) as the mechanism behind demand paging; the "Not every page fault is the same"
  card defining a fault as a *restartable exception* and laying out the two independent axes
  (allowed? via the valid-region/VMA check, and where-is-the-page? for minor vs major) plus the
  three-kind table (minor = needs a frame, in RAM or zeroed, fast; major = data on disk, slow
  I/O; invalid = not allowed, kernel sends SIGSEGV); the note that a minor fault happens once per
  page on first access and the page then translates purely in hardware. Section "Copy-on-write —
  how fork() is instant": fork sharing frames marked read-only and the first write triggering a
  fault whose handler copies the one page. Adjacent material on swap/overcommit and the glossary
  entries for "Page fault" and "Copy-on-write."
