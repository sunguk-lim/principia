---
id: virtual-memory
title: Virtual Memory
summary: Virtual memory is the trick that gives every process its own private, imaginary view of memory.
type: concept
tags: [os/memory]
prereqs: [process, memory-hierarchy]
sources:
  - linux-internals-complete.html ("Virtual memory & pages", "Virtual addresses vs physical addresses", "One map per process — isolation")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Virtual Memory

## Summary

**Virtual memory** is the trick that gives every [[process]] its *own private,
imaginary view of memory*. Each process sees a clean, contiguous range of memory
addresses — numbered as if it started near zero and owned the whole machine — even
though dozens of processes are sharing one physical bank of RAM. The addresses a
process names are **virtual addresses**: not real locations in RAM, but labels in its
private illusion. On *every* memory access, the operating system and a dedicated piece
of CPU hardware **translate** the virtual address the process used into the actual
**physical address** — the real spot in RAM (the fast, scarce top rungs of the
[[memory-hierarchy]]) where the byte lives. Because each process carries its *own*
translation map, two processes can use the identical virtual address and never collide:
the maps send them to different physical bytes. That single mechanism buys two things at
once — **isolation** (a process literally cannot name another's memory, so a bug stays
fenced in) and **abstraction** (a program is written and compiled for fixed addresses
without knowing, or caring, where in real RAM it will land).

## Grounded explanation

### The problem virtual memory solves

Start from the bare hardware. A machine has one physical block of RAM — say 16 GB —
which is the fast, scarce upper region of the [[memory-hierarchy]]: small in capacity
compared to disk, but the only place a CPU can directly read and write the numbers it is
working on. Now recall that a [[process]] is a running program, and the kernel's job
includes running *many* processes at once — a browser, a shell, a music player, two
hundred of them. (The kernel — the privileged resident program that manages the hardware
and creates processes — was established when we built up the [[process]].)

Here is the danger. A process refers to memory by **address** — a plain number naming a
byte, like "byte number 0x400000." If every process named raw physical RAM directly, two
processes would inevitably pick the *same* number, and the second would overwrite the
first's data. Worse, a buggy or malicious process could write to the number where the
kernel's own data sits and corrupt the whole system. With one shared pool of real
addresses, there is no wall between any two programs. The [[process]] node *promised*
that each process gets a private memory region the others cannot touch — virtual memory
is the mechanism that actually delivers that promise.

### The idea: give each process a private, fake address space

Define two terms precisely, because everything hinges on the distinction.

- A **physical address** is a real location in RAM — an actual byte in the chip. There is
  exactly one set of these, shared by the whole machine.
- A **virtual address** is the address a *process* uses. It is a number in that process's
  own private numbering, which does **not** correspond directly to any fixed spot in RAM.

The trick of virtual memory is this: each process is handed its own **address space** — a
huge, private, contiguous range of virtual addresses, conventionally starting near 0 — and
told, in effect, "this is all yours." The process reads and writes these virtual addresses
as if it alone owned the machine. It never sees a real RAM address at all.

A house-numbering analogy makes the illusion concrete. Imagine 200 tenants, each convinced
they live in a mansion with rooms numbered 0 to 1000. In reality the building has only 100
physical rooms. A building manager keeps, for each tenant, a private little lookup sheet:
*this* tenant's "room 5" is really physical room 37; *that* tenant's "room 5" is really
physical room 82. When a tenant says "go to my room 5," the manager quietly consults that
tenant's sheet and walks them to the right real room. No tenant ever learns a real room
number, and two tenants asking for "room 5" are sent to different real rooms — so they
never collide. The tenants are processes, "room numbers" are virtual addresses, the real
rooms are physical RAM, and the per-tenant lookup sheet is the per-process translation map.

### How a virtual address becomes a physical one

The illusion is maintained by **translation on every access**. Whenever a process touches
memory — runs an instruction, follows a pointer, reads a variable — the virtual address it
named must be turned into a physical address before RAM can be reached. Doing this in
software on every access would be hopelessly slow, so it is done by a dedicated chip inside
the CPU, the **Memory Management Unit (MMU)**. The kernel builds the translation map; the
MMU performs the lookup at hardware speed on each access.

How does the map avoid storing one entry per individual byte (which would need a table as
large as memory itself)? It works in **pages** — fixed-size chunks of memory, typically
4096 bytes (4 KB). Both the virtual address space and physical RAM are carved into
page-sized chunks. The map records, for each *virtual page*, which *physical page* it lands
on. A given virtual address is split into a **page number** (which 4 KB chunk) and an
**offset** (how far into that chunk). The MMU translates only the page number — looks up
"virtual page X lives at physical page Y" — and copies the offset through unchanged. So
mapping is per-page, not per-byte, which keeps the map small. (The map itself is a layered
data structure the kernel maintains per process — its full structure, and the
once-per-page setup cost of populating it, are the subject of separate nodes; here it is
enough that *a per-process map exists and the MMU consults it on every access*.)

### The why, part 1 — isolation

Now the first payoff, and the deeper reason the design works. Each [[process]] has its
**own** translation map. The map is what gives meaning to a virtual address; without
*your* map, the number 0x400000 means nothing. A process can name only the virtual
addresses in its own space, and its own map sends those only to the physical pages the
kernel chose for it. There is simply *no virtual address a process can write down that
names another process's physical page* — the vocabulary to refer to someone else's memory
does not exist in its address space. Isolation is therefore not a guard that *checks* each
access and forbids the bad ones; it is structural — the bad access is **unnameable**. A
process that runs wild and scribbles all over its own address space can corrupt only
itself. The blast radius of a memory bug is exactly one process, which is precisely the
per-process privacy the [[process]] node guaranteed.

### The why, part 2 — abstraction

The second payoff is for the programs themselves. A program is compiled ahead of time, on
some other machine, long before it runs. The compiler must bake fixed addresses into the
code — "the function starts at 0x400000," "this global lives at 0x600000." But at compile
time nobody knows where in physical RAM the program will eventually be loaded, or what else
will be running alongside it, or whether that physical spot will even be free. Virtual
memory dissolves the problem: the program is compiled against *virtual* addresses, which
are always available and always laid out the same way, and the kernel is free to place the
real pages anywhere in physical RAM it likes — the map hides the placement. Every program
gets to pretend it loaded into a fresh, empty, identical machine.

This abstraction has a second face. Because a virtual address space is just a numbering, a
process can be granted a virtual space far *larger* than the physical RAM that exists — up
to ~128 TB on a 64-bit machine, on a box with only 16 GB of RAM. Most of that space is
never actually touched, so no real RAM need back it; and the portion that *is* used but
doesn't fit in RAM can be parked on disk (the slow, roomy bottom of the
[[memory-hierarchy]]) and pulled up into RAM only when accessed. The address space is
*virtual* precisely so it need not be bounded by the physical store behind it. What every
process truly shares, and what is genuinely finite, is the physical backing — RAM plus
disk — even though each process's private virtual view is enormous.

### Worked instance: two processes, the same address, no collision

Make it concrete with the smallest example that actually triggers the mechanism — two
processes, not one, so the *whole point* (non-colliding identical addresses) is visible.
A degenerate single-process example would hide exactly the thing worth seeing.

Run two processes, A and B. Each was compiled against virtual addresses, and as it happens
**both use the virtual address 0x400000** for their code — a completely ordinary
collision, since both were built the same way and each thinks it starts near 0. Under raw
physical addressing this would be a catastrophe: two programs claiming byte 0x400000 of the
one real RAM.

Under virtual memory it is a non-event. Trace it:

1. Process A executes an instruction at its virtual address **0x400000**. The MMU consults
   **A's** map: A's virtual page containing 0x400000 is mapped to physical page **0x12000**
   (a real spot in RAM). The CPU reads the byte there.
2. Process B executes an instruction at its virtual address **0x400000** — the *same
   number*. The MMU consults **B's** map: B's virtual page is mapped to physical page
   **0x57000**, a different real spot. The CPU reads the byte there.

Same virtual address, *0x400000* in both; different physical bytes, *0x12000* versus
*0x57000*. When A writes to its 0x400000, only A's map and A's frame 0x12000 are involved;
B's 0x400000 still points at B's own frame 0x57000, untouched. A cannot even *name*
0x57000 — that physical page is reachable only through B's map, which A does not have.

Trace the offset, too, to see paging at work. Suppose A reads its virtual address
**0x400210**. Split it: page number 0x400, offset 0x210. The MMU translates the page —
A's virtual page 0x400 → physical page 0x12 — and carries the offset 0x210 across
unchanged. The byte fetched is physical 0x12210. Change only the process, keep the virtual
address: B's 0x400210 becomes physical 0x57210. The offset (how far into the page) is the
process's business; the page number (which real page) is the kernel's — and that split is
what lets one small map relocate a whole 4 KB chunk at a time.

So the same virtual label resolves to different physical bytes purely because the two
processes carry different maps. That is the entire mechanism, and from it both payoffs
fall out at once: A and B coexist in one RAM without colliding (**isolation**), and each
was free to be compiled for a fixed, convenient address it could rely on regardless of
where it physically landed (**abstraction**).

## Prerequisites

- [[process]]
- [[memory-hierarchy]]

## Sources

- `linux-internals-complete.html` — sections "Virtual memory & pages" (the problem, and
  the solution of giving every process its own fake address space), "Virtual addresses vs
  physical addresses" (the MMU translating on every access; the page-number/offset split),
  and "One map per process — isolation" (two processes sharing virtual 0x400000 mapped to
  different physical frames).
