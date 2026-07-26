---
id: tcp
title: TCP
summary: TCP (Transmission Control Protocol) is the rule set that runs at the transport layer of the network-stack — the layer whose header names which program — and its job is to turn…
type: concept
tags: [networking]
prereqs: [network-stack, socket]
sources: ["linux-internals-complete.html — 'TCP — reliable delivery'"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# TCP

## Summary

**TCP** (Transmission Control Protocol) is the rule set that runs at the transport layer of the
[[network-stack]] — the layer whose header names *which program* — and its job is to turn that
stack's crude, unreliable delivery into a clean, reliable one. By itself the stack only makes a
*best-effort* promise: it will *try* to carry each chunk of bytes to the far machine, but a chunk
may be **dropped** entirely (a busy relay throws it away), may arrive **out of order** (two chunks
take different paths and the later one wins the race), or may arrive **duplicated** (a chunk thought
lost was resent, then the original showed up too). TCP sits on top of that and hides every one of
those failures, so that the two programs at the ends experience a single, **ordered, gap-free,
exactly-once stream of bytes** — what you put in one end comes out the other end in the same order,
complete, with nothing missing and nothing doubled. It achieves this with a handful of cooperating
mechanisms: a **handshake** that opens a connection and agrees on a starting count; **sequence
numbers** that label every byte so the receiver can reorder and spot gaps; **acknowledgments and
retransmission** that detect loss and resend; **flow control** that keeps a fast sender from
drowning a slow receiver; and **congestion control** that keeps every sender from collectively
drowning the network in between. The contrasting choice, **UDP**, skips all of this: it just hands
each chunk to the stack and hopes — faster, but on its own if anything goes wrong.

## Grounded explanation

### Where this picks up: the stack only promises "best effort"

From [[network-stack]] we have the whole road between two programs. A program pushes bytes into one
mouth of the pipe (the [[socket]] endpoint), and they descend layer by layer — each layer wrapping them
in one more **header**, a small label glued to the front saying what that layer needs. The transport
layer's header names *which program* (a port); the network layer's header names *which host* (a
routable address — on the internet this is the **IP** protocol); the link layer's header names the
*next device on this one cable*. Across the world the bytes hop through many relays, and at the far
machine each layer peels its own header back off until the original bytes surface at the listening
endpoint.

That node was careful about *one thing it did not promise*. The stack carries a chunk **best
effort**: it will attempt delivery, but it guarantees nothing. A relay with a full queue simply
**drops** the chunk and moves on — no apology, no notice. Two chunks sent back to back may take
different routes and **arrive reversed**. A chunk can even arrive **twice**. IP, the network layer,
washes its hands of all of this; its only duty is "point this packet at that host and forward it."

This is the gap TCP exists to close. The concept of *this* node is **not** the transport layer in
general (that the stack already introduced as "the layer that names which program"), and **not** any
single trick below. The concept is the **discipline that converts best-effort packet delivery into a
reliable ordered byte stream** — the contract "whatever you write, the other side reads, intact and
in order" — and the cooperating mechanisms that uphold it. TCP is one specific protocol that can
occupy the transport-layer slot; UDP is another that occupies the same slot and declines to do any
of this.

### The one idea: number the bytes, and confirm what arrived

Before the mechanisms, the single insight they all rest on. TCP treats the data not as separate
chunks but as **one long numbered ribbon of bytes**. Conceptually, the very first byte of the
connection is byte number 1, the next is byte 2, and so on without end. Whenever TCP hands a piece of
that ribbon to the [[network-stack]] for delivery, the transport header it writes carries a
**sequence number** — the number of the *first* byte in that piece. (A *piece* of the ribbon
travelling as one unit is a **segment** — the very bundle the [[network-stack]] called a segment, now
seen from inside.)

Two facts fall out of numbering, and together they are almost the whole protocol:

- The receiver can **reorder**. However scrambled the segments arrive, their sequence numbers say
  exactly where each belongs on the ribbon. The receiver lays them out by number, not by arrival
  time, and only hands the program a stretch of ribbon once it is contiguous from where it left off.
- The receiver can **detect a gap**. If it has bytes 1–100 and the next segment it receives starts
  at 201, it *knows* bytes 101–200 are missing — there is a hole at a known place — rather than
  silently accepting corruption.

To close the loop, the receiver continuously tells the sender how far the gap-free ribbon now
reaches, using an **acknowledgment** (an "ack"): a number sent back meaning "I have every byte up to
*here*; send me the next one." This is **cumulative** — acking byte 100 confirms *everything* through
100 at once. The sender keeps a copy of every byte it has sent but not yet seen acked; once an ack
covers a byte, that copy can be discarded, because it is now safe at the other end.

### Mechanism 1 — the three-way handshake: agree before you talk

A connection cannot start counting from a fixed "byte 1" agreed in advance, because both sides must
also confirm *each can hear the other* and pick a starting number that an old, stale connection's
leftover packets won't accidentally match. TCP opens every connection with a **three-way handshake**,
three segments carrying no program data, only control flags and starting numbers:

1. The initiator sends a **SYN** ("synchronize") segment carrying its own chosen starting sequence
   number — say it picks 1000, meaning "my first real data byte will be numbered 1001."
2. The other side replies with a **SYN-ACK**: it *acks* the initiator's SYN (ack = 1001, "I heard
   your 1000, ready for 1001") *and* sends its own SYN with its own starting number — say 5000.
3. The initiator sends a final **ACK** of that (ack = 5001, "I heard your 5000").

After these three messages each side knows the other is reachable and knows where the other's byte
count begins, so every later sequence number and ack is unambiguous. *Why three and not two?* Because
each direction's starting number must be both **sent and acknowledged**, and the middle message
folds the reply's ack and the reply's own SYN into one — two SYNs and two ACKs, packed into three
segments. Closing the connection is the mirror image, with a **FIN** ("finish") flag in place of SYN.

### Mechanism 2 — acknowledgment and retransmission: recover from loss

Numbering and acking only *detect* loss; recovering it is the next mechanism. When the sender
transmits a segment, it starts a **timer**. One of two things tells it the segment was lost:

- **Timeout.** If no ack covering that segment's bytes arrives before the timer expires, the sender
  assumes the segment (or its ack) was dropped and **retransmits** the saved copy.
- **Duplicate acks.** Because acks are cumulative, a receiver that gets bytes *past* a gap can only
  keep re-sending the *same* ack — "still waiting at byte 100" — each time a later, out-of-order
  segment arrives. The sender, seeing the same ack number arrive several times in a row, infers a
  specific segment is missing and resends it *immediately*, without waiting for the full timeout.
  This is faster than a timeout and is the common case on a healthy network with occasional loss.

Either way, the lost bytes are eventually delivered, slotted into their place on the ribbon by
sequence number, and the receiver advances its cumulative ack past them. **Deduplication** is free:
if a segment arrives that the receiver already has (a needless retransmission, or a delayed
duplicate), its sequence numbers cover bytes already on the ribbon, so the receiver simply discards
it. Loss, reordering, and duplication — the three best-effort failures — are all answered by the same
numbered-ribbon-plus-cumulative-ack machinery.

### Mechanism 3 — flow control: don't overrun a slow receiver

Reliability raises a new problem: a fast sender could shovel bytes faster than a slow receiver can
consume them. The receiver buffers arriving bytes until its program calls to read them; if the sender
outruns the program, that buffer overflows and the very bytes TCP promised to deliver are dropped —
self-defeating. **Flow control** prevents this with a number the receiver advertises in every ack:
the **window** — "beyond what I've already acked, I have room for *this many* more bytes; do not send
past that." The sender may have at most one window's worth of un-acked bytes outstanding at any
moment. When the receiver's program drains the buffer, the receiver advertises a larger window; if
the program stalls and the buffer fills, it advertises a smaller window, even zero ("stop"). The
sender's outstanding data is thus clamped to whatever the *receiver* can currently absorb. This is
strictly about the **two endpoints' speeds** — it knows nothing about the network in between.

### Mechanism 4 — congestion control: don't overrun the network

The window above protects the *receiver*. But the [[network-stack]]'s relays in the middle are a
shared, finite resource too: if every sender blasts at full window size at once, the relays' queues
overflow and they drop packets *en masse* — which triggers everyone's retransmissions, which adds
*more* traffic, which causes more drops, a ruinous feedback loop called **congestion collapse**.
**Congestion control** is each sender independently restraining itself to protect that shared middle,
using loss as its only signal (the network sends no explicit "I'm full" message — a dropped packet
*is* the message). The sender keeps a second, private limit — a **congestion window** — and the
amount it may have outstanding is the *smaller* of this and the receiver's advertised window. It
manages the congestion window in two phases:

- **Slow start.** A new connection has no idea what the path can bear, so it starts small and
  *probes* by ramping up fast: every time a window's worth of data is acked successfully, it roughly
  doubles the congestion window. Growth is exponential, quickly finding the rough ceiling.
- **AIMD — additive increase, multiplicative decrease.** Once probing past the early phase, the
  sender nudges the window up by a small fixed amount per successful round (additive increase,
  cautious) but, the instant it detects loss, **halves** the window (multiplicative decrease,
  drastic). Gentle up, sharp down. *Why this asymmetry?* Because it is self-correcting toward a fair,
  stable share: each sender backing off hard on loss relieves the congestion immediately, while the
  slow climb keeps everyone from re-saturating the path at once. Many independent senders following
  the same rule settle around a roughly equal division of the bottleneck instead of colluding into
  collapse.

### A worked instance: one lost segment, recovered, and the program never knows

Let a program send 300 bytes over an established connection whose data numbering begins at byte 1.
TCP cuts the ribbon into three segments of 100 bytes and hands each to the [[network-stack]] with a
sequence number:

- **Segment A** — sequence 1, bytes 1–100.
- **Segment B** — sequence 101, bytes 101–200.
- **Segment C** — sequence 201, bytes 201–300.

The receiver's window is large (say 1000), so flow control permits all three outstanding at once. The
three descend the stack, get wrapped in their IP and link envelopes, and race across the world. Now
the non-degenerate twist: **segment B is dropped** by a congested relay, while A and C survive.

Trace the receiver. A arrives → it now holds the gap-free ribbon 1–100, and acks "next expected =
101." Then C arrives — but the receiver is still missing 101–200, so it *cannot* extend the gap-free
stretch past 100. It stores C off to the side (held by its sequence number, not delivered to the
program yet) and re-sends the *same* ack: "next expected = 101." Its program has so far been handed
only bytes 1–100; C is buffered, invisible to the program, waiting for the hole to fill.

Trace the sender. It saw the ack for 101 once (after A). Now C's arrival makes the receiver emit
"next expected = 101" *again* — a **duplicate ack**. (Had more out-of-order segments followed, more
duplicates would pile up.) On enough duplicate acks — or, failing that, when segment B's timer simply
expires — the sender concludes B specifically is lost and **retransmits** segment B (sequence 101,
bytes 101–200) from its saved copy, without resending A or C.

The retransmitted B arrives. The receiver slots bytes 101–200 into the hole; now the ribbon is
contiguous 1–200, and — crucially — C (201–300) was already sitting in its place, so the ribbon is
actually contiguous all the way to **300**. The receiver hands its program bytes 101–300 in one go
and acks "next expected = 301." The sender, seeing everything through 300 acked, discards all three
saved copies. Meanwhile its congestion window was **halved** the moment it inferred the loss, so it
will now climb back up gently per AIMD.

The point: the program on the receiving end called to read and got bytes **1 through 300, in order,
exactly once** — it never saw the drop, never saw C arrive before B, never saw a duplicate. Every
best-effort failure was absorbed below it. That invisibility *is* TCP. The instance is non-degenerate
on purpose: it triggers loss, reordering (C before B), the duplicate-ack fast path, retransmission of
*only* the missing segment, in-order delivery of buffered data once the gap fills, and the congestion
backoff — the whole machinery in one run. Had no segment been lost, the loss/retransmit/duplicate-ack
branches would never fire and the example would hide most of the protocol.

### The contrast, in one line

**UDP** sits in the same transport-layer slot and does *none* of this — no handshake, no sequence
numbers, no acks, no retransmission, no flow or congestion control — so it is faster and lower-latency
but unreliable, which is the right trade only when an occasional lost or out-of-order packet is
cheaper to tolerate than to fix (live video, games, simple lookups).

## Prerequisites

- [[network-stack]]
- [[socket]]

## Sources

- `linux-internals-complete.html` — section "TCP — reliable
  delivery" (TCP as the protocol that "makes unreliable networks feel reliable," run by the kernel as
  a per-connection **state machine** that handles **reliability** — retransmitting lost packets,
  **ordering** — reassembling out-of-order packets, **flow control** — slowing a sender for a slow
  receiver, **congestion control** — backing off to avoid collapse, and **deduplication** — dropping
  duplicate packets, all invisibly so the program's `recv` "just returns the correct data in order";
  and the contrasting **UDP** Q&A — no reliability, ordering, or flow control, faster for DNS, video,
  and gaming where speed beats perfection). The specific mechanisms named here — the three-way SYN /
  SYN-ACK / ACK handshake, byte-level sequence numbers, cumulative acks with timeout and duplicate-ack
  retransmission, the receiver-advertised window, and slow start / AIMD congestion control — are the
  standard means by which the five behaviors that section attributes to TCP are actually achieved,
  expanded here from the source's anchor.
