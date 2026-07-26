---
id: content-addressable-memory
title: Content-Addressable Memory
summary: "Content-addressable memory (CAM), also called associative memory, is hardware that realizes the [[key-value]] mapping's associative access physically: you present a search word (the key) and the memory compares it against every stored word at once, in a single cycle, returning the address(es) where it matches — the inverse of ordinary RAM (address in → data out), and the hardware answer to 'given this content, where is it?', bought with a comparator at every cell (so it is fast and parallel but area- and power-hungry, hence small and used where one-cycle lookup is worth it: TLBs, cache tag matching, router forwarding tables)."
type: concept
tags: [os/memory]
prereqs: [key-value]
sources:
  - "https://en.wikipedia.org/wiki/Content-addressable_memory — Content-addressable memory (associative memory): parallel search-by-content, match lines, binary vs ternary CAM, uses in TLBs/caches/routers"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# Content-Addressable Memory

## Summary

**Content-addressable memory** (CAM) — also called **associative memory** — is a kind
of memory hardware that you query **by content instead of by address**. With ordinary
memory (RAM) you supply an *address* and it returns the *data* stored there; a CAM does
the opposite: you supply a *data word* — the thing you are looking for — and it returns
the **address** where that word is stored (or a simple "found / not found"). It does this
by comparing your search word against **every stored word simultaneously**, in a single
step, rather than checking them one at a time. CAM is the hardware realization of the
*associative access* that a [[key-value]] mapping defines abstractly: "given this key's
content, get what's attached to it," answered directly in silicon. The price of that
one-cycle parallel search is a comparison circuit at every storage cell, which makes CAM
fast but physically expensive — large, power-hungry — so real CAMs are small and reserved
for the few places where instant lookup pays for itself, above all address translation and
routing.

## Grounded explanation

### The operation it provides: associative access, in hardware

A [[key-value]] mapping is the abstract idea of reaching data by the *content* of a key
rather than by a position: you ask for the value *of* `"alice"`, never "which slot is Alice
in?" That node draws the crucial contrast — **positional** access (an array: you must know
the index `7`) versus **associative** (content-addressed) access (a mapping: the key itself
is the address). Content-addressable memory is what that associative access *is* when built
as a physical memory rather than as a software data structure. So the two live at different
layers: [[key-value]] says *what* associative access means (get/set/delete keyed by content);
CAM is one concrete machine that provides it — and provides it in a very particular way, by
brute-force parallel comparison in hardware.

### RAM vs. CAM — the direction of the arrow

Fix the contrast with the memory everyone knows first. **Random-access memory (RAM)** is
*address-addressed*: it is a row of numbered cells, you hand it a cell number (an address),
and it hands back the bits stored in that cell. The address is a *position* — exactly the
positional access [[key-value]] contrasts against. To find *where* a particular data value
sits, RAM is no help on its own: you would have to read cell 0, compare, read cell 1,
compare, and so on — a linear scan.

CAM inverts the arrow. It is *content-addressed*: you hand it a **search word** (a data
value), and it returns the **address** whose stored word equals it. Written as the two
mappings:

- **RAM:** address → data
- **CAM:** data → address

That inversion is the whole concept. CAM is the memory that answers "*where is this
content?*" directly, which is precisely the question associative ([[key-value]]) access
asks — now resolved by the memory itself in one operation instead of by a scan.

### How it does it: a comparator at every cell, all firing at once

The reason a CAM can answer in one step is structural, and it is the "magic-looking" part
worth justifying. In a CAM, **every stored word has its own comparison circuit.** When you
broadcast the search word to the whole array, each stored word compares itself against the
search word *in parallel* — bit by bit, a stored word matches only if all its bits equal the
corresponding search bits — and each row raises a single **match line** if it agrees. Because
all rows compare at the same time, the search takes **one cycle regardless of how many words
are stored**: an *encoder* then turns the raised match line(s) into the address of the
match. This is the exact opposite of scanning a [[key-value]] structure in software, where
lookup cost grows with the data; CAM trades that time cost for *hardware* — it spends a
comparator per cell so that time no longer scales with size.

That trade is the defining cost, and it is severe. A comparator at every bit of every word
is far more transistors, area, and power than a plain RAM cell that only has to store and
recall. So CAMs are **small and expensive** relative to RAM of the same capacity, and their
constant power draw matters. This is why you never build main memory out of CAM; you build a
*little* CAM exactly where a single-cycle content lookup is worth the silicon.

A common variant widens what "match" means: a **ternary CAM (TCAM)** lets each stored bit be
`0`, `1`, or **don't-care**, so one entry can match a whole *range* of search words. That is
what makes CAM the natural fit for router forwarding tables, where a destination address must
be matched against network prefixes ("anything starting with these bits") rather than exact
values.

### Where it earns its keep

Every classic use is a place that must answer "*is this content present, and where?*" on
essentially every operation, where even a fast software lookup would be too slow:

- **The [[key-value]] connection made physical — the TLB.** A translation lookaside buffer
  holds recent "virtual page → physical frame" pairs and must, on *every* memory access,
  check whether the current virtual page is among them. That is an associative lookup keyed by
  page number, and a *fully-associative* TLB implements it as a CAM: the page number is the
  search word, all stored page numbers compare at once, and a match line yields the frame in
  one cycle. (This is the hardware under the "check the TLB first" step of address
  translation.)
- **Cache tag matching.** A CPU cache must decide whether the data for an address is already
  resident by comparing the address's tag against the tags of candidate lines — an
  associative comparison, done by CAM-style match logic so a hit/miss is known immediately.
- **Router forwarding.** A network router matches each packet's destination against a table of
  address prefixes; a TCAM matches all prefixes in parallel and returns the best route in one
  step, which is how high-speed routers forward at line rate.

### Worked instance — searching by content in one step

Take a tiny CAM with four rows, each storing an 8-bit word, and give it real contents:

```
addr 0:  0110 1010
addr 1:  1111 0000
addr 2:  0110 1010     <- same word as addr 0
addr 3:  0000 0001
```

Now present the **search word** `0110 1010` (you are asking "*where is this value stored?*",
not "what is at some address"):

1. The search word is broadcast to all four rows **at the same time**.
2. Each row compares in parallel: row 0's stored `0110 1010` equals the search word → its
   **match line goes high**; row 1 (`1111 0000`) differs in several bits → match line low;
   row 2 (`0110 1010`) equals it → match line **high**; row 3 differs → low.
3. In this **one** step the CAM reports that the content is present and lives at **addresses 0
   and 2** (an encoder resolves the raised lines; a CAM typically also exposes a plain "match
   found" flag). No row was examined before any other — all four comparisons happened together.

Contrast the same task on address-addressed RAM: you would read address 0 and compare, then
1, then 2, then 3 — four sequential steps for four words, and `N` steps for `N` words. The
CAM answered in **one** step for four words, and would still answer in one step for four
thousand — because the cost moved from *time* (a scan) into *hardware* (a comparator per row).
That single-cycle, size-independent search-by-content is the entire contribution of
content-addressable memory: the [[key-value]] mapping's associative access, made a physical
primitive.

## Prerequisites

- [[key-value]] — the abstract operation CAM realizes: *associative* (content-addressed)
  access, reaching data by the content of a key rather than by a position. CAM is the
  hardware that provides exactly this "given the content, find it" access as a one-cycle,
  parallel physical primitive, in contrast to the positional access of ordinary RAM.

## Sources

- "Content-addressable memory," Wikipedia — https://en.wikipedia.org/wiki/Content-addressable_memory (search-by-content vs. RAM's address-by-content; parallel match lines; binary vs. ternary CAM; and the standard uses in TLBs, cache tag stores, and router forwarding tables).
