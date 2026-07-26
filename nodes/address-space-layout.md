---
id: address-space-layout
title: Address Space Layout
summary: Address space layout is the standard floor plan the kernel imposes on a virtual-memory address space.
type: concept
tags: [os/memory]
prereqs: [virtual-memory, page-table]
sources:
  - linux-internals-complete.html ("What a process's memory looks like" §6 — the standard region map; "One map per process — isolation"; mmap/brk syscalls)
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Address Space Layout

## Summary

**Address space layout** is the standard floor plan the kernel imposes on a
[[virtual-memory]] address space. Recall that [[virtual-memory]] hands each running
program its own private, contiguous range of fake addresses — but that range is *not* a
featureless expanse the program scatters data across at random. It is divided into a
fixed set of **regions**, each with one job and one permission setting. From the lowest
addresses upward: a deliberately **unmapped null page** at address 0; the **text**
segment (the program's machine-code instructions, read-only and executable); the
**global/static data** segment (variables that live for the whole program); the **heap**
(memory the program requests at run time, which **grows upward** toward higher
addresses); a **memory-mapped region** in the middle (shared libraries and large
allocations); and near the top, the **stack** (the bookkeeping for function calls, which
**grows downward** toward lower addresses). Heap and stack grow *toward each other*
across a vast unused gap. This is not arbitrary tidiness: giving each region its own
permission lets the kernel mark code as runnable-but-unwritable and data as
writable-but-not-runnable — a security wall — and lets read-only code be shared across
processes. The same layout appears in every process, but each process's copy is private,
because each has its own [[virtual-memory]] map.

![Address space layout: one address column from low to high — unmapped null page at 0, text 0x400000 (R+X), global/static data 0x601000 (R+W), heap growing up from 0x602000 via malloc/brk, a vast unused gap, mmap region around 0x7f... (shared libc), stack near 0x7fff... growing down; R/W/X badges show no region is both writable and executable, and runaway recursion drives the stack pointer past its band into the gap where the kernel finds no mapping — SIGSEGV|960](address-space-layout.svg)

## Grounded explanation

### Where this starts: a private address space, not yet furnished

From [[virtual-memory]] we have the key fact this node builds on: every running program
is handed its **own** address space — a private, contiguous range of virtual addresses,
conventionally starting near 0 and reaching enormous size (on the order of 128 TB on a
64-bit machine). A *virtual address* is just a number the program uses to name a byte;
the program's own translation map turns it into a real location in RAM, and no other
program shares that map, so the same number means different things in different programs.

[[virtual-memory]] tells us the address space *exists* and is *private*. It does not tell
us how the program arranges its contents inside that space. That arrangement is this
node's subject. The space is far too large to fill, so the question is: at *which*
addresses does the machine code go, the variables, the run-time allocations, the call
bookkeeping? The answer is a convention — the same in every process — called the
**address space layout**.

### The regions, from low addresses to high

Picture the address space as a tall column of bytes, address 0 at the bottom, the highest
address at the top. The layout carves it into named **regions** (also called segments).
Define each one, because each has a distinct purpose and, crucially, a distinct
*permission* — a rule the kernel encodes in each region's [[page-table]] entries saying
what kind of access is allowed: **read** (you may look at the bytes), **write** (you may
change them), and **execute** (the CPU may treat the bytes as instructions and run them).

- **The null page** sits at the very bottom, at address 0. It is deliberately left
  **unmapped** — no real memory backs it, and the program's map has no entry for it. Its
  whole purpose is to be *absent*. A *pointer* is a variable holding an address; a common
  bug is a pointer that was never set and holds the value 0 (called the **null pointer**).
  When the program follows such a pointer — *dereferences* it, i.e. tries to read or write
  the byte it names — it touches address 0, which is unmapped, and the hardware refuses,
  killing the program with a fault (the familiar *segmentation fault*). Leaving page 0
  unmapped turns a silent corruption into a loud, immediate crash.

- **The text segment** holds the program's **machine code** — the actual binary
  instructions the CPU executes, produced by compiling the source program. It lives at low
  addresses, just above the null page. Its permission is **read + execute, not write**:
  the CPU must be able to run these bytes, and the program may read them, but nothing may
  *change* them while the program runs. ("Text" is the traditional Unix name for code; it
  has nothing to do with human-readable text.)

- **The global/static data segment** holds variables that exist for the program's entire
  lifetime — *global* variables (visible throughout the program) and *static* ones (kept
  alive between uses). It sits just above the text segment. Its permission is
  **read + write, not execute**: these are data the program changes, not instructions to
  run. It has two parts that differ only in starting value. Variables given an explicit
  initial value in the source are stored *with* that value baked into the program file.
  Variables that start at zero need no stored value at all — the kernel simply hands the
  program fresh zeroed memory for them. This zero-start sub-region is historically called
  the **BSS**; the name is a meaningless relic, but the idea is worth keeping: zero-valued
  globals cost nothing to store on disk because "all zero" needs no recording.

- **The heap** is the region for memory the program asks for *while running*, when it
  cannot know in advance how much it will need (say, to hold a list whose length depends
  on user input). The program requests a block by calling an allocation routine
  (`malloc`), which under the hood asks the kernel to extend the heap's upper edge — the
  classic syscall for this is `brk`, which simply moves the boundary marking the top of
  the heap. Because that edge moves to *higher* addresses as more is requested, the heap
  **grows upward**. It sits just above the data segment and is **read + write**.

- **The memory-mapped region** lives in the wide middle of the space. *Memory-mapping*
  means making some external thing appear directly as a range of addresses the program can
  read and write as if it were ordinary memory; the syscall that does this is `mmap`. Two
  things land here. First, **shared libraries** — pre-compiled bundles of code (like the C
  standard library, `libc`) that many programs use; rather than copy that code into every
  program, the kernel maps the one read-only copy into each program's space here. Second,
  large run-time allocations and mapped files, which the allocator places here rather than
  on the heap. The code parts are read-execute; the data parts read-write.

- **The stack** sits near the *top* of the address space and holds the bookkeeping of
  function calls. Each time the program calls a function, a **stack frame** is pushed: a
  block holding that call's *local variables* (named values that exist only during the
  call), the *return address* (where to resume in the caller when the function finishes),
  and saved registers. When the function returns, its frame is discarded. Frames are added
  at *lower* addresses than the previous one, so the stack **grows downward** — toward the
  heap rising to meet it. It is **read + write**.

So heap and stack start at opposite ends of the unused middle and grow *toward each
other*, with the memory-mapped region in between and an enormous empty gap separating
them. This opposition is the layout's most distinctive structural fact, and it has a
practical consequence, returned to below.

### The why — permissions per region buy security and sharing

Why split the space into regions at all, instead of letting the program lay out its bytes
however it likes? The decisive reason is that a region is the unit at which the kernel
sets **permissions**, and per-region permissions deliver two things a flat space cannot.

The first is **security through separated rights**. Notice the deliberate asymmetry:
**code is executable but not writable; data is writable but not executable.** That single
split blocks a whole class of attacks. An attacker who finds a bug letting them write
bytes into the program's memory would love to write in their own malicious instructions
and have the CPU run them. But the regions they *can* write — data, heap, stack — are
marked non-executable, so the CPU refuses to run anything there; and the one region that
*is* executable — the text segment — is read-only, so they cannot write into it. The bad
move is not *detected and blocked* by a guard checking each access individually; it is
*structurally impossible*, because no single region grants both "writable" and
"executable" at once. (This is the same flavor of argument as in [[virtual-memory]], where
isolation worked because another process's memory was simply *unnameable* rather than
guarded — here the dangerous combination is simply *ungranted*.)

The second payoff is **sharing read-only code**. Because the text segment is guaranteed
never to be written, the kernel can keep one physical copy of a shared library's code in
RAM and point *every* program's memory-mapped region at that same copy. Nothing can
corrupt it, because nothing can write it, so sharing is safe. A flat read-write space
could not do this: if any program might scribble on the code, no two could safely share
it. (The mechanics of one physical copy serving many maps belong to [[virtual-memory]];
what the layout contributes is the *read-only guarantee* that makes the sharing safe.)

A third, smaller payoff is **independent growth**. Heap and stack have unpredictable,
unrelated sizes — a program might recurse deeply (much stack) yet allocate little (small
heap), or the reverse. Placing them at opposite ends of a huge gap lets each grow as far
as it needs without a fixed wall between them; the kernel only has to ensure they do not
eventually meet.

### Worked instance: sketch a real process map, low to high

Take a concrete process on a 64-bit machine and walk its map from the bottom up. The
specific numbers are illustrative addresses of the kind you would actually see; what
matters is their order and the permission on each region.

| Region | Example address | Permission | Holds |
|---|---|---|---|
| Null page | `0x0` | (unmapped) | nothing — faults on touch |
| Text (code) | `0x400000` | read + execute | the program's instructions |
| Global/static data | `0x601000` | read + write | globals, statics, zero-start (BSS) |
| Heap | starts `0x602000`, grows ↑ | read + write | `malloc`'d run-time data |
| *(large gap)* | | | empty, unmapped |
| Memory-mapped | `0x7f...` region | read + execute / read + write | shared `libc`, mapped files |
| Stack | near `0x7fff...`, grows ↓ | read + write | call frames, locals, return addresses |

Read it as a story. The CPU begins executing instructions in the **text** segment at
`0x400000`; those bytes are read-execute, so they run but cannot be overwritten. A global
counter the program declared lives in **data** at `0x601000`, read-write, so the program
updates it freely but the CPU will not execute it. The program calls `malloc` to hold some
input; the allocator advances the **heap** edge upward from `0x602000`, handing back an
address in that growing region. The program calls into a `libc` function; that code sits
in the **memory-mapped** region up around `0x7f...`, the single shared copy. Meanwhile
every function call pushes a frame onto the **stack** near `0x7fff...`, each new frame at a
*lower* address than the last.

Now trigger the collision the gap exists to absorb. Suppose a function calls itself
without ever stopping — runaway *recursion*. Each call pushes another frame, so the stack
grows downward, frame after frame, marching from `0x7fff...` toward lower addresses. With
no base case, it never unwinds; eventually it descends past the end of the region the
kernel reserved for the stack and touches an unmapped address in the gap. The hardware
refuses, and the program dies — this is the **stack overflow**. Symmetrically, a program
that keeps `malloc`'ing without freeing pushes the heap edge ever higher; a truly runaway
heap climbs through the gap from below. The huge empty gap is what lets either grow far
before trouble; the layout's job is to keep the two from silently overwriting each other —
instead, exhausting the gap produces a clean fault.

### One layout, private copies, and a deliberate shuffle

Two final points tie the layout back to its prerequisite. First, *the same layout appears
in every process* — every program sees text low, stack high, heap growing up toward a
descending stack. Yet these are not the same bytes: each process has its **own**
[[virtual-memory]] map, so two processes can both place their code at virtual `0x400000`
and never interfere, exactly as [[virtual-memory]]'s isolation guarantees. The layout is a
shared *convention*; the contents are private.

Second, a security refinement. If every program always loaded its regions at the *same*
fixed addresses, an attacker would know in advance precisely where the code and stack sit,
making attacks far easier to aim. So the kernel applies **address space layout
randomization (ASLR)**: each time a program starts, it shifts the base addresses of the
regions by a random amount. The *order* and *purpose* of the regions are unchanged — text
still below data, stack still near the top — but their exact starting addresses differ
from run to run, so an attacker can no longer assume where anything lives. The layout is
fixed in structure, deliberately unpredictable in placement.

## Prerequisites

- [[virtual-memory]]
- [[page-table]]

## Sources

- `linux-internals-complete.html` — section "What a process's memory looks like" (§6): the
  standard region map (null page, text, global/static data including BSS, heap growing up,
  memory-mapped region for shared libraries and large allocations, stack growing down) with
  each region's permissions; the `brk` and `mmap` syscalls (heap extension and memory
  mapping); "One map per process — isolation" (the same layout in every process, but each
  process's copy private via its own page table, and read-only shared-library code mapped
  once into many processes).
