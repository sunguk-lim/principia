---
id: mac-vs-ip
title: MAC vs IP Addressing
summary: A single message crossing the network-stack is addressed twice, with two completely different kinds of address that answer two different questions, and the gap between them is how…
type: concept
tags: [networking]
prereqs: [network-stack]
sources: ["linux-internals-complete.html — 'How does the signal reach the right machine?', 'How a packet reaches Google — hop by hop' (incl. 'Switch uses MAC addresses, router uses IP addresses — why two?' and the ARP/ARP-spoofing note)"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# MAC vs IP Addressing

## Summary

A single message crossing the [[network-stack]] is addressed **twice**, with two completely
different kinds of address that answer two different questions, and the gap between them is how
packets actually find their way across the world. The **IP address** (the network-layer / host
address) is the **end-to-end logical address**: it names the *ultimate* machine the message is
for — "which host, anywhere on the internet" — and it stays **identical** for the entire journey,
from the first wire to the last. The **MAC address** (the link-layer / hardware address) is the
**physical address of one particular network card** on one local stretch of wire: it answers
"which device on *this* segment right now" and is used only to carry the message across **one
hop** — one cable or radio link to the next device. The defining behavior, and the whole point of
this node, is that as a packet is forwarded hop by hop, its **source and destination IP never
change**, but the surrounding frame's **source and destination MAC are rewritten at every
router** — each hop re-addresses the frame to the *next* device's card. Mapping a next-hop IP to
the MAC that currently holds it, on the local segment, is the job of a small lookup protocol
called **ARP**. Two layers exist because the two jobs are genuinely different: IP gives a global,
hierarchical, *routable* identity that scales to the whole internet and can be reassigned, while
MAC gives concrete *local delivery* on a physical medium with a flat, factory-burned identifier.
Routing decisions are made in IP terms; the actual handing-off of bits happens in MAC terms.

## Grounded explanation

### Where this picks up: the [[network-stack]] already put two addresses on the packet

The [[network-stack]] node established the layered descent of a message: the program's bytes are
wrapped first by the transport layer (a port, naming *which program*), then by the network layer
(a **host address**, naming *which machine*), then by the link layer (a **hardware address**,
naming *which device on this one cable*), and finally turned into a signal on the wire. It also
stated, as a fact to take on faith, the crucial asymmetry: the host address stays the same for the
whole trip, while the hardware address is **rewritten at every hop**. This node is about *that one
pair of addresses* and *that one asymmetry* — it names them by their real-world names (IP and MAC),
explains **why** the two are different in kind, and shows the mechanism that lets the rewrite
happen at all. The concept here is not the layered stack (that is the prerequisite); it is the
**distinction between the two addresses and the division of labor between them**.

So we are zooming in on exactly two of the envelopes the [[network-stack]] described — the
network-layer host address and the link-layer hardware address — and asking: why are there two,
what is each one shaped like, and what makes one constant while the other is replaced over and over?

### Two terms, defined before we lean on them

An **IP address** is the network-layer host address. "IP" is just the name of the internet's
network-layer protocol; for our purposes an IP address is a number that identifies one host
(one machine) on the internet, written in a familiar dotted form like `192.168.1.5` or `8.8.8.8`.
Its essential properties are three. It is **logical**, meaning it is assigned by configuration, not
welded to any piece of hardware — a machine can be given a different IP, and the same IP can later
belong to a different machine. It is **hierarchical**, meaning the number has structure: a leading
portion names a *network* (a whole block of addresses that live together) and the rest names a host
within that network, so a router can decide where to send a packet by looking only at the network
part, the way a postal system routes by city and country without knowing every individual house.
And it is **routable**, meaning that because of this hierarchy, devices anywhere can forward a
packet step by step toward the network that owns the destination address. The IP address answers
**"which machine, anywhere?"**

A **MAC address** is the link-layer hardware address — "MAC" stands for *media access control*,
the part of a network card that governs putting bits onto the physical medium. A MAC address is a
number **burned into the network card (the NIC) at the factory**, written as six bytes like
`aa:bb:cc:dd:ee:ff`. Its essential properties are the opposite of IP's in the ways that matter. It
is **physical**, meaning it identifies one specific piece of hardware, not a configurable role. It
is **flat**, meaning it has no internal structure a router could navigate by — there is no "network
part" of a MAC address, so you cannot look at two MACs and tell whether the devices are near each
other. And consequently it is **local-only**: it is meaningful just on the one network segment the
card is physically attached to (the cable, the switch, the Wi-Fi cell), and it cannot be used to
route across the wider internet, because nothing in the number says which direction to go. The MAC
address answers **"which device on *this* wire?"**

The word **frame** below means, as in the [[network-stack]], the link-layer envelope: the packet
(which carries the two IP addresses inside it) wrapped in a link header that carries the two MAC
addresses on the outside. A **router** is a device that joins two or more networks and forwards
packets between them; a **hop** is the crossing of one such link from one device to the next.

### The why: one address cannot do both jobs

The reason there are two addresses, rather than one, is that "identify the final destination
globally" and "deliver across one physical link" are different problems whose good solutions pull
in opposite directions.

Global routing wants addresses that are **hierarchical and reassignable**. Hierarchy is what makes
the internet tractable: a router does not need a path to every machine on Earth, only a rule of the
form "addresses starting like *this* go out *that* interface." That only works if the address has a
navigable structure — exactly what IP provides and MAC, being flat, cannot. Reassignability matters
too: machines move, networks are renumbered, addresses are leased; a logical address can follow
those changes, a factory-burned one cannot.

Local delivery, by contrast, wants an address that is **concrete and tied to the actual hardware**
present on the segment, so that a switch or a card can answer the only question that matters on a
single wire — "is this particular electrical/optical/radio frame for the card sitting *here*?" —
without any notion of distant networks. A flat, burned-in identifier is ideal for that and useless
for the other job.

Trying to collapse both into one scheme forces a contradiction. If the single address were flat
like MAC, every router on the planet would need a route to every individual device — the routing
tables could not be summarized, and the internet would not scale. If instead the single address
were hierarchical like IP and we threw MAC away, then the moment a packet had to physically cross
one wire we would still need to say *which card on this wire* should grab it — and that is a local,
hardware question the hierarchical address was not built to answer cleanly, especially since
multiple unrelated hosts can share one segment. So the layers keep both: **routing decisions are
made in IP terms, and the physical hand-off is made in MAC terms.** This is precisely why the
[[network-stack]] keeps the host address constant (it is the routing target, fixed for the trip)
yet rewrites the hardware address each hop (it is only ever the answer to "next card, on this
wire").

### The mechanism that makes the rewrite possible: ARP

There is a gap to bridge. When a router (or the original sender) decides, in IP terms, "the next
device toward the destination is the one at IP `X` on my local segment," it still must put a *MAC*
address on the outgoing frame, because the wire only understands MACs. It needs to translate the
next-hop *IP* into the *MAC* of whatever card currently holds that IP, **on this segment**. That
translation is the job of **ARP — the Address Resolution Protocol**.

ARP is deliberately simple, and it works only within one local segment (consistent with MAC being
local-only). When a device knows a next-hop IP but not its MAC, it broadcasts a small question onto
the segment — heard by every card on that wire — of the form "whoever has IP `X`, tell me your
MAC." The one device configured with that IP answers directly with its MAC; everyone else stays
silent. The asker caches the IP-to-MAC pairing for a while (an *ARP cache*) so it need not ask
again for every packet. With that answer in hand, the device can finally fill in the frame's
destination MAC and transmit. (Because the question is a broadcast that anyone on the segment can
answer, a malicious device can lie — claim to own an IP it does not — and so intercept frames; this
is *ARP spoofing*. It is a security consequence of ARP's trust-the-segment design, not part of the
addressing mechanism itself, and is mentioned only to show where the trust boundary sits.)

So the full forwarding step at each hop is: read the unchanged destination **IP**, consult the
routing rules to pick the next-hop **IP** on some local segment, use **ARP** to turn that next-hop
IP into a **MAC**, and emit a fresh frame whose destination MAC is that next device's card — while
the IP addresses inside ride along untouched.

### A worked instance: host A to 8.8.8.8 through a gateway

Make it concrete and non-degenerate by using a real hop, so the rewrite actually happens (a
same-segment example would hide it). Host **A** has IP `192.168.1.5` and a network card with MAC
`aa:aa:aa:aa:aa:aa`. It wants to reach a public server at IP `8.8.8.8`, which is *not* on A's local
network. A's gateway — the router that connects A's home network to the rest of the internet — has
IP `192.168.1.1` and a card with MAC `bb:bb:bb:bb:bb:bb`. Trace the addressing:

1. **A decides the destination, in IP terms.** A's network layer sees destination IP `8.8.8.8`.
   Comparing it against A's own network (`192.168.1.x`), A concludes `8.8.8.8` is not local, so the
   packet must go to A's gateway first. The routing decision yields a *next-hop IP*: `192.168.1.1`.
   Note carefully — the *destination* IP on the packet remains `8.8.8.8`; `192.168.1.1` is only the
   next stepping-stone, not written into the packet's destination field.

2. **A resolves the next-hop MAC with ARP.** A needs the MAC of `192.168.1.1` to address the frame.
   If it is not already cached, A broadcasts on the local segment: "who has `192.168.1.1`?" The
   gateway replies "that's me, `bb:bb:bb:bb:bb:bb`." A caches the pairing
   `192.168.1.1 → bb:bb:bb:bb:bb:bb`.

3. **A emits the first frame.** Its addresses are:
   - source IP `192.168.1.5`, destination IP **`8.8.8.8`** (the ultimate target);
   - source MAC `aa:aa:aa:aa:aa:aa`, destination MAC **`bb:bb:bb:bb:bb:bb`** (the *gateway's* card,
     not the server — the server is many hops away and has no MAC on this wire).

   So even on the very first link, the destination IP and destination MAC point at **different
   machines**: the IP names the far-off server, the MAC names the local gateway. That mismatch *is*
   the two-address idea in one line.

4. **The gateway forwards: same IPs, new MACs.** The gateway's card sees a frame addressed to its
   MAC `bb:bb:bb:bb:bb:bb`, so it accepts it and strips the frame. Inside, it reads the destination
   IP `8.8.8.8`, still unchanged, and consults its own routing rules to pick *its* next hop toward
   `8.8.8.8` — say a router at the internet provider, on a different segment, reachable at some
   next-hop IP whose MAC the gateway resolves by ARP on *that* segment (call that MAC
   `cc:cc:cc:cc:cc:cc`). The gateway then builds a **brand-new frame**:
   - source IP `192.168.1.5`, destination IP **`8.8.8.8`** — *identical to before*;
   - source MAC = the gateway's *outgoing* card, destination MAC **`cc:cc:cc:cc:cc:cc`** — *both
     completely different from step 3*.

5. **Repeat to the end.** Every subsequent router does the same: accept the frame addressed to its
   MAC, read the still-unchanged IPs, ARP-resolve the next card on its outgoing segment, and emit a
   fresh frame with new source/destination MACs. After the last hop, the frame's destination MAC is
   finally the destination server's own card, and only there does the destination MAC and the
   destination IP refer to the *same* machine.

Across the whole path the pair `(192.168.1.5, 8.8.8.8)` of IP addresses is the invariant — written
once by A, read by every router, never altered — while the pair of MAC addresses is replaced at
every single hop, each value valid only on the one wire it was emitted onto. That is the entire
distinction: **IP is the constant, global, routable name of the endpoints; MAC is the disposable,
local, hardware name of the next handoff; ARP is the bridge from a next-hop IP to its MAC; and the
two-layer scheme is what lets routing be global while transmission stays physical and local.**

## Prerequisites

- [[network-stack]]

## Sources

- `linux-internals-complete.html` — section "How does the signal
  reach the right machine?" (a NIC checks each incoming frame's destination MAC — "is this for me?"
  — and a switch learns which MAC sits on which port; the basis for MAC as a flat, per-card, local
  identifier), "How a packet reaches Google — hop by hop" (the packet is "reborn" at each router,
  which reads it into memory, makes a routing decision, and transmits fresh signals on a different
  wire — the basis for the per-hop frame rewrite), its Q&A "Switch uses MAC addresses, router uses
  IP addresses — why two?" (MAC works within one local network and IP works across networks; the
  IP header says "final destination: Google" while the Ethernet header says "next hop: my router's
  MAC," and the Ethernet header is rewritten with the next hop's MAC at each router while the IP
  header stays the same to the end — the central two-address distinction and invariant used here),
  and its Q&A on interception (ARP associating a MAC with an IP, and ARP spoofing — the basis for
  the ARP next-hop-IP-to-MAC resolution and the noted trust boundary).
