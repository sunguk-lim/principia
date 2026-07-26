---
id: udp
title: UDP
summary: UDP (User Datagram Protocol) is the minimal transport layer of the network-stack — the bare-bones alternative to TCP.
type: concept
tags: [networking]
prereqs: [network-stack]
sources: ["linux-internals-complete.html — 'TCP — reliable delivery' and its 'What about UDP?' Q&A; the DNS resolution Q&A ('a UDP packet out, a UDP packet back')"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# UDP

## Summary

**UDP** (User Datagram Protocol) is the *minimal* transport layer of the [[network-stack]] — the
bare-bones alternative to TCP. Recall that in the [[network-stack]] the transport layer is the one
whose header names **which program** the bytes are for, using a **port** (a number identifying one
program's endpoint on a machine). UDP does exactly that and almost nothing else: it wraps the
program's data in a tiny header — a *source port*, a *destination port*, a *length*, and a
*checksum* (a small error-detecting number) — and hands the resulting bundle, called a **datagram**,
straight to the network layer to be carried to the destination host. That is the whole protocol.
It is **connectionless**: there is no setup conversation between the two machines before data flows;
the sender just emits a datagram at any moment, addressed to a host and a port, with no prior
agreement that anyone is listening. And it is **unreliable**: UDP adds no machinery on top of what
the [[network-stack]] already does, so a datagram may be lost, duplicated, or arrive out of order,
and UDP will neither notice nor fix it — no acknowledgments, no retransmission, no reordering, no
slowing the sender down. The reason to choose such a stripped-down protocol is precisely what it
*lacks*: with no connection to establish and no waiting for confirmations, it has tiny overhead and
no setup delay, so it wins wherever speed matters more than guaranteed delivery, or where the
application would rather handle reliability itself.

## Grounded explanation

### Where this sits: one of the two transport layers of the network stack

The [[network-stack]] node established the layered path that bytes travel down the kernel and out the
wire: the program's data is wrapped, layer by layer, into a *segment* (transport header naming a
**port** — which program), inside a *packet* (network header naming a **host address** — which
machine, the part that is routed across the world), inside a *frame* (link header naming a hardware
device — one hop). That node noted, in passing, that the transport layer "is usually the protocol
**TCP** … or sometimes **UDP**, which does not" make the byte stream reliable, and explicitly left
reliability "as its own concept elsewhere." **This node is that elsewhere, for UDP.** The concept
here is *not* the port (that belongs to the [[network-stack]]) and *not* the layering discipline
(also the prerequisite). The concept is UDP **as a transport choice**: the particular, minimal set
of guarantees UDP offers — and, more tellingly, the long list of guarantees it deliberately refuses
to offer — and the reasoning for why refusing them is sometimes the right design.

A clarifying frame from the [[network-stack]]: that node's whole insight was that each layer "treats
the layer below it as a dumb pipe." The network layer of the [[network-stack]] is, by itself, an
*unreliable* pipe — it forwards a packet hop by hop toward a host and makes no promise it will
arrive. UDP is the transport protocol that **passes that unreliability straight through** to the
application instead of papering over it. Everything else about UDP follows from that one decision.

### A few terms, defined before we lean on them

- A **datagram** is UDP's name for the bundle it produces: one UDP header glued in front of one
  chunk of the program's data, sent as a single self-contained unit. It is the transport-layer
  *segment* of the [[network-stack]], specialized to UDP. "Self-contained" is the key adjective:
  each datagram carries its own full destination (host address from the network layer, port from the
  UDP header) and is sent on its own, owing nothing to any datagram before or after it.

- **Connectionless** means no *connection* is set up first. A connection, in the contrasting style,
  is a short opening conversation — a **handshake** — in which the two machines exchange a few
  messages to agree "yes, I am here, I am ready, let us number our bytes from here." UDP skips this
  entirely: the very first thing the receiver ever hears from the sender *is* a datagram of real
  data. There is no state established on either side that says "these two are talking"; each datagram
  stands alone.

- A **checksum** is a small number computed from the datagram's contents and stored in the header,
  so the receiver can recompute it and detect whether the bytes got corrupted in transit. Note what
  this does and does not buy you: it lets the receiver *discard* a mangled datagram, but UDP does not
  then ask for a fresh copy — detection without correction. A corrupted datagram is simply dropped
  and forgotten.

- **Reliable** (the property UDP lacks) is the bundle of promises a transport layer can make on top
  of the dumb network pipe: that every byte arrives (lost ones are **retransmitted**), that they
  arrive in the order sent (out-of-order ones are **reordered**), that duplicates are removed, and
  that a fast sender does not overwhelm a slow receiver or a congested network (**flow control** and
  **congestion control**). UDP makes *none* of these promises.

### What UDP actually does — and the much longer list of what it refuses to do

UDP's entire active job, on the way down through the [[network-stack]], is one step at the transport
layer: take the program's chunk of data, prepend a four-field header — *source port*, *destination
port*, *length*, *checksum* — and hand the resulting **datagram** to the network (IP) layer below,
which routes it to the destination host exactly as the [[network-stack]] node described. At the far
end, the transport layer reads the *destination port*, finds the program listening there, and
delivers the data. That mirrors the receive walk-up of the [[network-stack]] — with one telling
difference: where the [[network-stack]] node said the transport layer, "if this is TCP, also puts
any out-of-order pieces back in order and acknowledges receipt," the UDP transport layer does
*neither*. It verifies the checksum, and if the datagram is intact it hands the bytes up; otherwise
it drops them. Nothing more.

Everything else a transport layer *could* do, UDP declines:

- **No handshake.** Being connectionless, it never sets up a connection, so it pays none of the
  round-trips a setup conversation would cost.
- **No acknowledgment.** The receiver never tells the sender "I got it," so the sender never learns
  whether a datagram arrived.
- **No retransmission.** A lost datagram stays lost; UDP does not resend it, because — having no
  acknowledgments — it cannot even tell that it was lost.
- **No ordering.** Two datagrams may take different routes through the [[network-stack]] and arrive
  in the wrong order; UDP delivers them in whatever order they show up.
- **No deduplication.** If the network delivers the same datagram twice, the application sees it
  twice.
- **No flow or congestion control.** UDP never slows down for a struggling receiver or a clogged
  network; it sends as fast as the program asks it to.

So a UDP datagram may be **lost, duplicated, or reordered, and UDP will not notice.** This is not a
bug — it is the definition.

### The WHY: absence is the feature

The non-obvious, "why would anyone want this?" step is to see that UDP's missing features are
themselves the reason to choose it. Each guarantee a reliable transport adds has a cost, and UDP's
value is dodging those costs:

1. **No setup latency.** A handshake costs *round-trips* — messages that must travel all the way to
   the other machine and back *before any real data moves*. For a tiny one-shot exchange, that
   setup can dwarf the actual payload. UDP's first packet is already the data, so a request can
   complete in a single round-trip total.

2. **Tiny per-packet overhead.** UDP's header is four small fields; it keeps no per-connection state
   on either machine (no record of "byte 5000 was acknowledged, byte 5001 was not"). Less header,
   less bookkeeping, less memory, less CPU.

3. **No head-of-line waiting.** A reliable, ordered stream must *hold back* later data until an
   earlier lost piece is retransmitted — everything stalls waiting for the straggler. For some
   applications that wait is worse than the loss itself: in a live video or audio call, a frame that
   arrives late is *useless* (the moment it depicts has already passed on screen), so it is better
   to drop it and move on than to freeze the picture waiting for it. UDP's refusal to reorder or
   retransmit is exactly the behavior such applications want.

The flip side, which the [[network-stack]] node already hinted at, is that the application is then on
its own for reliability. That is fine in two situations: either the application genuinely does not
*need* reliability (a dropped audio packet is unnoticeable; a lost game position update is replaced
by the next one a moment later), or the application implements *its own* reliability tailored to its
needs, getting UDP's low overhead plus only the guarantees it actually wants. This is exactly why
newer protocols layered on top of UDP can build custom, application-aware reliability without paying
for the one-size-fits-all version baked into the stack.

### A worked instance: one DNS lookup as a single round-trip

Take the most characteristic UDP use, a DNS query — the lookup that turns a name like
`example.com` into a host address. Suppose a program wants the address for `example.com` and sends
its question to a DNS server (a program that listens on **port 53**, the well-known DNS port). Walk
it through the [[network-stack]] in UDP's connectionless style:

1. **One datagram out.** The resolver builds a small query — "what is the address of
   `example.com`?" — and hands it to UDP. UDP prepends its header: *destination port 53*, a
   *source port* (say `49152`, picked for this query so the reply can find its way back), the
   *length*, and a *checksum*. That single **datagram** descends the rest of the [[network-stack]]:
   the network layer wraps it in a packet addressed to the DNS server's host, the link layer hops it
   along, the wire carries it. Crucially, **no handshake preceded this** — the datagram with the
   real question is the very first thing the DNS server hears.

2. **One datagram back.** The DNS server's transport layer reads *destination port 53*, hands the
   query up to the DNS program, which looks up the answer and sends *one* reply datagram back,
   *destination port 49152* (the resolver's source port from step 1). It climbs the resolver's
   [[network-stack]], the transport layer matches port `49152` to the waiting program, and the
   answer — the host address — is delivered.

That is the entire exchange: **one datagram out, one datagram back** — a single round-trip, with no
connection to establish beforehand and none to tear down afterward. Now the payoff is visible by
contrast. A reliable, connection-oriented transport would first spend a handshake — extra messages
crossing to the server and back *before* the question could even be asked — and then acknowledge the
data, adding still more round-trips to a transaction whose real content is two tiny messages. For a
lookup that happens constantly and must feel instant, that setup overhead would be most of the cost.

And the missing reliability is handled trivially by the application: if the reply never comes back
(the query datagram or the answer datagram was lost, and recall UDP will not notice or retransmit),
the resolver simply waits a short timeout and **asks again** — re-sending the one small datagram. A
fresh question is cheap precisely *because* each datagram is self-contained and connectionless;
there is no broken connection to recover, nothing to renegotiate, just another independent datagram.
This instance is non-degenerate on purpose: it exercises both directions, the port-matching that
lets the reply find the right program, and the case where loss actually happens and the
application's own one-line "just re-ask" recovery stands in for everything UDP refuses to do.

### Contrast with TCP, in a sentence

TCP is the other transport choice on the *same* [[network-stack]]: a connection-oriented protocol
that, after a setup handshake, presents the application with a **reliable, ordered byte stream** —
retransmitting losses, reordering, deduplicating, and pacing the sender — at the price of that setup
latency and per-connection bookkeeping; UDP and TCP ride the identical network (IP) and link layers
of the [[network-stack]] and differ *only* in the transport-level guarantees they choose to make,
UDP making the fewest possible and TCP making the most.

## Prerequisites

- [[network-stack]]

## Sources

- `linux-internals-complete.html` — the "TCP — reliable delivery"
  section and especially its "What about UDP?" Q&A ("UDP skips all of that. No reliability, no
  ordering, no flow control. Your program sends a packet and hopes it arrives. If it doesn't — your
  problem. That's why UDP is faster (no overhead) but unreliable. Used for DNS lookups, video
  streaming, gaming — situations where speed matters more than perfection."), which is the basis for
  the connectionless/unreliable definition and the "absence is the feature" reasoning; the same
  section's enumeration of what TCP handles (reliability via retransmission, ordering, flow control,
  congestion control, deduplication) read as the foil — the list UDP refuses — and as the basis for
  the closing TCP contrast and the note that TCP's `connect` is a handshake; and the DNS resolution
  Q&A ("it sends a UDP packet to a DNS server … The DNS server responds … DNS is just regular
  networking — a UDP packet out, a UDP packet back. No special kernel magic."), which is the basis
  for the worked one-datagram-out, one-datagram-back DNS instance on port 53.
