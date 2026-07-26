---
id: page
title: Page
summary: A page is the fixed-size block — almost always 4 KB (4096 bytes) — in which memory is managed.
type: concept
tags: [os/memory]
prereqs: [virtual-memory]
sources:
  - linux-internals-complete.html ("Pages — memory is managed in 4KB chunks")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Page

## Summary

A **page** is the fixed-size block — almost always **4 KB** (4096 bytes) — in which
memory is managed. [[virtual-memory]] gives each process a private range of virtual
addresses that the kernel must connect to real spots in physical RAM; rather than tracking
that connection one byte at a time, the system carves *both* sides into equal blocks. A
slice of the virtual address space, 4 KB wide, is a **page**; a slice of physical RAM, the
same 4 KB wide, is a **frame**. The kernel then maps whole pages onto whole frames and
records only *that* — "this virtual page lives in that physical frame" — instead of one
record per byte. The reason is pure economy: byte-by-byte bookkeeping would demand a
mapping record for every single byte of memory, which is impossibly large. Because every
page is exactly 4 KB, any virtual address splits cleanly into a **page number** (which page
it belongs to) and an **offset** (how far into that page it sits), and only the
page-to-frame relationship has to be stored — the offset rides through translation
untouched.

## Grounded explanation

### Where the page comes from

Start from what [[virtual-memory]] already established. Each process is handed its own
private range of **virtual addresses** — numbers it uses to name memory — and on every
access the hardware must turn the virtual address into a **physical address**, a real
location in RAM. That requires a *map* from virtual locations to physical ones. The open
question virtual-memory deliberately left to a separate node was: at what granularity does
that map work?

The naive answer is "per byte" — store, for each individual virtual byte, which physical
byte it corresponds to. This is hopeless. A modern machine has billions of bytes of RAM,
and the virtual space is larger still; a map with one entry per byte would itself be as
large as (or larger than) the memory it describes, leaving no room for anything else. The
map must be *far* smaller than the memory it governs, so it cannot afford to name every
byte.

The page is the answer to that problem. Instead of mapping bytes, the system manages memory
in **fixed-size blocks**, and maps a whole block at once.

### What a page is, and its partner the frame

Define the terms precisely.

- A **page** is a fixed-size, contiguous block of the **virtual** address space —
  conventionally 4 KB, i.e. 4096 bytes. The entire virtual space is sliced into these equal
  blocks, back to back: the first page covers virtual bytes 0 through 4095, the next covers
  4096 through 8191, and so on.
- A **frame** (or *physical page*) is a block of the same size, 4 KB, but cut out of
  **physical RAM**. Real RAM is sliced into frames the same way the virtual space is sliced
  into pages.

The two have *identical size* on purpose: that is what lets a whole page drop into a whole
frame with nothing left over and nothing missing. The kernel's map therefore records, for
each virtual page, which physical frame currently holds it — one record per page, not per
byte. A page is the **unit of mapping**: the smallest amount of memory the system relocates,
accounts for, or hands out as a single indivisible piece.

### Why fixed-size blocks shrink the bookkeeping

Here is the central pay-off, stated as a number. With 4 KB pages, one mapping record now
covers 4096 bytes of memory instead of one. That is a 4096-fold reduction in the number of
records the map must hold — the map shrinks by the same factor the page is wide. The map
stays small *because* the block is large; the whole reason for choosing a fixed block size
is to make the map affordable.

But fixed-size blocks buy something subtler than a smaller map, and it is the real magic:
they make a virtual address *splittable by arithmetic alone*, with no lookup needed for the
within-block part. Because every page is exactly 4096 bytes and the blocks are laid out back
to back from zero, the position of any byte is fully described by two pieces:

- its **page number** — which 4 KB block it falls in, i.e. the address divided by 4096; and
- its **offset** — how far into that block it sits, i.e. the remainder after dividing by
  4096, a value from 0 up to 4095.

Together, (page number, offset) name the byte exactly: byte = page number × 4096 + offset.
Since 4096 is 2¹², this division and remainder are not real arithmetic the hardware must
compute — they are just *a cut in the bits*. The **low 12 bits** of the address are the
offset (because 2¹² = 4096 distinct positions fit in 12 bits); every bit above the low 12 is
the page number. Translating an address then means translating only the page number — look
up "virtual page X is in physical frame Y" — and copying the offset straight across
unchanged, because the byte's position *within* a 4 KB block is the same whether that block
sits in the virtual space or in its physical frame. The map handles the page number; the
offset needs no map at all. This is precisely why the page-number/offset split that
virtual-memory used in its trace works: the split is a free consequence of the block being a
fixed power-of-two size.

(The actual structure that stores the page-to-frame records — the *page table* the kernel
builds per process — and the trick of leaving most pages unbacked until a process first
touches them — *demand paging* — are each their own concept and are not the page itself.
Here the page is simply the fixed-size unit that makes both of those possible.)

### Worked instance, part 1: an allocation rounds up to whole pages

Take a concrete request. A program asks for **10 KB** of memory — 10240 bytes. Memory is
handed out only in whole pages, so the kernel cannot give exactly 10240 bytes; it must give
enough *whole 4 KB pages* to cover the request. Divide: 10240 ÷ 4096 = 2.5. Two pages cover
only 8192 bytes, which is short, so the kernel rounds **up** to **3 pages**:

- Page 1 — 4096 bytes, fully used.
- Page 2 — 4096 bytes, fully used. (8192 bytes covered so far.)
- Page 3 — only 10240 − 8192 = **2048 bytes** are actually wanted, but the whole 4096-byte
  page is committed to this allocation anyway.

So a 10 KB request consumes 3 pages = 12288 bytes of address space, of which 12288 − 10240 =
**2048 bytes in the last page are reserved but unused**. That wasted tail is called
**internal fragmentation** — memory lost *inside* an allocated page because allocation is
quantized to whole pages and the request rarely lands on an exact page boundary. It is the
direct, unavoidable cost of managing memory in fixed-size blocks: the same fixed size that
shrank the map by 4096× also forces every allocation to round up, wasting on average about
half a page at the end. Note this instance is deliberately *non-degenerate* — 10 KB is not a
multiple of 4 KB, so the rounding and the leftover both actually appear; a tidy 8 KB request
would have hidden the fragmentation entirely.

### Worked instance, part 2: splitting a real address

Now split a single virtual address into its two parts to see the bit-cut directly. Take the
virtual address **0x00401234** with 4 KB pages.

The offset is the **low 12 bits** of the address. In hexadecimal, each digit is 4 bits, so
12 bits is exactly the **low 3 hex digits**. Read them off 0x00401234: the low 3 digits are
**0x234**. So the offset = 0x234 = 564 in decimal — this byte sits 564 bytes into its page,
and 564 is comfortably below 4096, as every offset must be.

The page number is everything *above* those low 12 bits — drop the low 3 hex digits and keep
the rest: 0x00401234 → **0x401**. Check it by the defining identity, page number × 4096 +
offset: 0x401 = 1025 in decimal, and 1025 × 4096 + 564 = 4,198,400 + 564 = 4,198,964, which
is exactly 0x00401234. The split reproduces the original address, so it is correct.

The reading, then, is: address 0x00401234 lives in **virtual page 0x401**, at **offset
0x234** within it. To find the real byte, the system looks up only page 0x401 in the map to
learn which physical frame holds it — say frame 0x9C2 — and pastes the unchanged offset
0x234 onto it, giving physical address 0x9C2234. The whole 4 KB page moved as one block; the
offset 0x234 picked the same byte inside it on both sides. That single look-up-the-page,
keep-the-offset move — affordable only because memory is diced into fixed 4 KB pages — is
what the page, as a concept, exists to enable.

## Prerequisites

- [[virtual-memory]]

## Sources

- `linux-internals-complete.html` — section "Pages — memory is managed in 4KB chunks":
  memory divided into fixed 4 KB pages so the map handles pages rather than individual
  bytes, both virtual and physical memory carved into pages/frames, and the
  page-number/offset split of a virtual address (the offset carried through translation
  unchanged).
