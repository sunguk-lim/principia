---
id: sk-buff
title: Socket Buffer (sk_buff)
summary: The socket buffer, written sk_buff in the kernel, is the data structure that represents one packet the whole time it is inside the network-stack — the single object every layer…
type: concept
tags: [networking]
prereqs: [network-stack]
sources: ["linux-internals-complete.html — section 'The journey of a packet — send', the 'Under the hood' note: 'The packet data structure is called sk_buff (socket buffer). Instead of copying data between layers, each layer just adds a pointer to its header at the front of the same buffer — very efficient, no data copying.'"]
status: explained
created: 2026-06-23
updated: 2026-06-29
---

# Socket Buffer (sk_buff)

## Summary

The **socket buffer**, written `sk_buff` in the kernel, is the data structure that *represents one
packet* the whole time it is inside the [[network-stack]] — the single object every layer holds,
reads, and edits as the packet travels down to the wire or up from it. Its defining trick is how it
stores the packet. The packet's actual bytes live in **one** block of memory the kernel allocated
once; the `sk_buff` itself is a small record sitting beside that block, holding **pointers** that
mark where, inside the block, the live data currently begins and ends. Because the layers of the
[[network-stack]] do their work by *adding* a header in front of the data (going down) or *removing*
one (going up), the `sk_buff` lets a layer do that by **moving a pointer** rather than by copying
the bytes. When the transport layer prepends its header, it slides the "data starts here" pointer
*backward* over some empty space reserved at the front, then writes its header into that newly
exposed gap — the payload behind it never moves. When the next layer down prepends its header, it
slides the pointer back further still. The same `sk_buff`, pointing into the same untouched
payload, is handed from layer to layer. The whole point is speed: networking touches every byte of
every packet at enormous rates, so re-copying the payload at each of the four-plus layers would be
ruinous, whereas nudging a pointer on a shared buffer makes wrapping and unwrapping a packet nearly
free.

## Grounded explanation

### Where this sits: the thing that *is* the packet inside the stack

The [[network-stack]] node described the journey of a packet as an abstract story: the program's
bytes become a transport segment inside a network packet inside a link frame, each layer prepending
its own **header** (a short, fixed-purpose block of bytes one layer puts in front of the data it was
given) on the way down, and stripping it again on the way up. That story left one question open:
*what concrete object is being passed from layer to layer, and prepended-to, and stripped?* The
answer is the `sk_buff`. It is not a layer and not the socket; it is the **representation of a single
packet in flight** — the kernel's in-memory embodiment of "the thing currently descending (or
ascending) the stack." The concept of this node is precisely that representation: its layout, and
the pointer discipline that lets encapsulation and decapsulation happen without moving the payload.

A clarifying note on the name. *Socket buffer* is a slight misnomer inherited from history: an
`sk_buff` is not a long-lived buffer attached to a socket but a **per-packet** structure. One
`send` of a megabyte may be carved into many packets, each its own `sk_buff`; a steady stream of
arriving packets is a stream of separate `sk_buff`s. Read "socket buffer" as "the buffer-bearing
record for one packet that the stack hands around."

### The layout: a small record pointing into one allocated block

Picture two things allocated together. First, a contiguous **block of memory** — call its extent
from its very first byte to its very last byte the *data area*. Second, the **`sk_buff` record**, a
small bookkeeping structure that does *not* contain the packet bytes; instead it holds four
pointers that mark positions *inside* that block. Define each precisely, because the entire
mechanism is just these four moving:

- **`head`** — points at the very first byte of the allocated block. This never moves; it is the
  fixed origin, the left wall.
- **`end`** — points just past the very last usable byte of the block. Also fixed; it is the right
  wall. The distance from `head` to `end` is the total capacity that was allocated.
- **`data`** — points at the first byte of the *live* content right now: where the current
  outermost header (or, before any header exists, the payload) begins. This one **moves**.
- **`tail`** — points just past the last byte of the live content right now. This moves too, when
  content is appended at the back, but for the send story it largely stays put.

The live packet at any instant is the bytes between `data` and `tail`. Two empty regions flank it.
The gap between `head` and `data` — reserved, unused space at the *front* — is called the
**headroom**. The gap between `tail` and `end` — unused space at the *back* — is the **tailroom**.
Headroom is the protagonist of this node: it is the deliberately-left empty room into which the
lower layers will write their headers.

### The two operations: prepend by moving `data` back, strip by moving `data` forward

Only two pointer moves matter, and they are exact inverses.

**Prepend a header of length `n` (used going down the stack, when a layer wraps the packet in its
own envelope):** move `data` *backward* by `n` bytes — that is, toward `head`, consuming `n` bytes
of headroom — and then write the `n`-byte header into the region `data` now points at. After the
move, the live packet runs from the new (smaller) `data` to the unchanged `tail`; it has grown at
the front by exactly the header, and **not one byte of the old content was touched or copied**. The
header simply occupied space that was already sitting empty in front of it. (In the kernel this
operation is named `skb_push`; the name is incidental — what matters is "slide `data` back, gaining
a header in front.") This is why the [[network-stack]]'s "envelope inside an envelope" works in
place: each outer envelope is written into headroom, not by relocating the inner letter.

**Strip a header of length `n` (used going up the stack, when a layer removes its own envelope to
reveal what is inside):** move `data` *forward* by `n` bytes — toward `tail`, away from `head`. The
header is now *behind* `data` and therefore no longer part of the live packet; the live content now
begins at whatever followed that header, which is the next inner layer's header (or, at the top, the
payload itself). Again nothing was copied; the bytes still sit in the same place, but the `data`
pointer has skipped past them, so the layer above sees only what is in front of it. (Kernel name:
`skb_pull`. Incidental.)

That symmetry is the core identity to hold onto: **prepend is "`data` minus `n`," strip is "`data`
plus `n`," and the payload bytes never move under either.** A layer reads the packet as "everything
from `data` onward"; pushing or pulling the single `data` pointer is what makes a header appear or
disappear from that view.

There is one preparatory step that makes prepending possible at all. When the `sk_buff` is first
created for an outgoing packet, the kernel does not put the payload at `head`; it first sets `data`
(and `tail`) some distance *in* from `head`, deliberately leaving headroom — enough empty front
space for all the headers the lower layers will later prepend. (Kernel name: `skb_reserve`.) Without
this reservation there would be nowhere to slide `data` back *into*, and a prepend would run off the
front of the block. Reserving headroom up front is the quiet enabling move behind the whole no-copy
scheme.

### The WHY: copying every payload at every layer would be ruinous

Here is the non-obvious justification, the thing that makes the design more than a curiosity. The
[[network-stack]] has four or more layers, and *every* packet passes through *all* of them in order;
a busy machine moves millions of packets a second, and a payload can be over a kilobyte. The naive
implementation — each layer builds a fresh, larger buffer holding `[its header] + [everything it was
handed]`, copying the handed bytes into the new buffer — would copy the entire payload once per
layer per packet. At, say, four layers that is four full payload copies on the way out and four more
on the way in: eight passes over every byte of every packet, pure overhead, doing nothing but
relocating identical bytes so that a few header bytes can sit in front of them. At line rate this
saturates memory bandwidth and starves the actual work.

The `sk_buff` removes that cost entirely. Because the payload is laid down **once** in a buffer with
pre-reserved headroom, and every subsequent header is written into that headroom while the `data`
pointer slides, the payload is written exactly once and read only when genuinely needed (for a
checksum, or by the network card). Encapsulation and decapsulation reduce to pointer arithmetic on a
shared block. The invariant the structure maintains — *the payload bytes occupy fixed addresses for
the packet's entire life inside the stack; only the four pointers move* — is exactly what buys the
speed. That invariant is the whole insight.

### A worked instance: sending "GET /" down the stack, watching only the pointers

Trace one concrete outgoing packet, the same request the [[network-stack]] node followed: a program
sends the payload `"GET /"` (treat it as 5 bytes for the trace) over a connection. Use small,
illustrative header sizes so the arithmetic is visible: a 20-byte transport (TCP) header, a 20-byte
network (IP) header, and a 14-byte link (Ethernet) header. The instance is non-degenerate on
purpose — it exercises all three prepends and shows the payload's address staying fixed across every
one.

1. **Allocate with headroom.** The kernel allocates one block and, before placing any data, reserves
   headroom for the three headers to come. Say it reserves 54 bytes (20 + 20 + 14). It sets `data`
   54 bytes in from `head`, then copies `"GET /"` from the program's memory to that position and
   sets `tail` 5 bytes past `data`. State: `head` at offset 0, `data` at 54, `tail` at 59, and the
   payload `"GET /"` physically occupying offsets 54–58. Remember those offsets — **they will not
   change again.**

2. **Transport layer prepends its 20-byte header.** Move `data` back by 20: from offset 54 to
   offset 34. Now write the transport header (source/destination port, etc.) into offsets 34–53 —
   space that was empty headroom a moment ago. The live packet is now offsets 34–58:
   `[transport header] + "GET /"`. The string `"GET /"` is still at offsets 54–58, byte for byte
   untouched.

3. **Network layer prepends its 20-byte header.** Move `data` back by 20 more: from 34 to 14. Write
   the network header (source/destination host address) into offsets 14–33. Live packet: offsets
   14–58, `[network header] + [transport header] + "GET /"`. The payload is *still* at 54–58; the
   transport header is *still* at 34–53. Nothing was recopied — only `data` moved.

4. **Link layer prepends its 14-byte header.** Move `data` back by 14: from 14 to 0 — exactly
   reaching `head`, which is why 54 bytes of headroom were the right amount to reserve. Write the
   Ethernet header (source/destination hardware address) into offsets 0–13. Live packet: offsets
   0–58, the complete frame `[Ethernet] + [network] + [transport] + "GET /"`. The payload sits where
   it always sat, at 54–58.

5. **Hand to the network card.** The card reads the live region `data`→`tail` (offsets 0–58) and
   turns it into a signal on the wire. Over the entire descent, the five payload bytes were written
   *once* (step 1) and never moved; the three headers were each written directly into reserved
   headroom; and the "packet" handed from layer to layer was the same `sk_buff`, distinguished only
   by where its `data` pointer sat.

Now the mirror image at the receiver, to show strip as the exact inverse. The arriving frame's bytes
are placed in a buffer with `data` at the very front (offset 0), pointing at the Ethernet header.
The link layer reads that header, then moves `data` forward by 14 — past the Ethernet header — so
`data` now points at the network header; the Ethernet bytes are physically still there but behind
`data` and thus no longer part of the live packet. The network layer reads the host address, then
moves `data` forward by 20 to reveal the transport header. The transport layer reads the port to
find the destination program, then moves `data` forward by 20 to reveal `"GET /"`. At each step a
header "disappeared" by a single forward nudge of `data`, with zero copying — the precise undoing of
the sender's backward nudges. The payload that surfaces is byte-for-byte what was sent, having
ridden one shared buffer the entire way.

## Prerequisites

- [[network-stack]]

## Sources

- `linux-internals-complete.html` — section "The journey of a
  packet — send", whose "Under the hood" note states the governing idea this node expands: "The
  packet data structure is called `sk_buff` (socket buffer). Instead of copying data between layers,
  each layer just adds a pointer to its header at the front of the same buffer — very efficient, no
  data copying." The same section's layer-by-layer send diagram (socket layer copies the program's
  bytes into the `sk_buff`; the TCP, IP, and Ethernet layers each prepend their header to that same
  buffer) supplies the worked send trace, and the companion "Receiving a packet — the reverse"
  section supplies the mirror strip-on-the-way-up trace. The explicit `head`/`data`/`tail`/`end`
  pointer layout, the headroom/tailroom terminology, and the reserve-then-push-then-pull mechanics
  are the standard Linux `sk_buff` model, named here to make the source's one-sentence "adds a
  pointer to its header at the front of the same buffer" concrete.
