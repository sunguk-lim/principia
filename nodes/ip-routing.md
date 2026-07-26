---
id: ip-routing
title: IP Routing
summary: "IP routing is the decision the network layer of the network-stack makes on every outgoing packet: out which interface, and to which next device, do I send this so it gets one step…"
type: concept
tags: [networking]
prereqs: [network-stack]
sources: ["linux-internals-complete.html — 'The journey of a packet — send' (IP layer consults the routing table on every outgoing packet), 'How a packet reaches Google — hop by hop', and the routing-table / two-addresses Q&A boxes"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# IP Routing

## Summary

**IP routing** is the decision the network layer of the [[network-stack]] makes on every
outgoing packet: *out which interface, and to which next device, do I send this so it gets one
step closer to its final host?* The network layer already stamps each packet with a destination
host address; routing is the step that turns that address into a concrete "send it that way."
The decision is driven by a **routing table** — a short list of rules, each pairing a *destination
network* (a whole range of addresses, written as a **prefix**) with a *next-hop* (the address of
the neighbouring router to hand the packet to) and an *outgoing interface* (which network card to
send it from). To route a packet the kernel finds the rule whose prefix matches the destination
most specifically — **longest-prefix match** — and follows it. A catch-all **default route**
matches everything, so a packet that fits no narrower rule still has somewhere to go: the **default
gateway**, your local router. Crucially, routing is **hop-by-hop**: this machine only decides the
*next* device; that device then consults *its own* table and decides the device after it, and so on.
No single machine knows the whole path. That is the whole trick — because each router only needs to
know "for addresses like that, send them this way," the global internet scales without anyone
holding a complete map.

## Grounded explanation

### Where this picks up: the one black box the network-stack node left closed

The [[network-stack]] node walked a packet down five layers and, at the network layer (the IP
layer), said this: that layer "prepends a header whose job is to say which host the bytes are for,
and to let the bundle be routed — carried from network to network across the world toward that
machine," and then it explicitly parked the routing decision — *"which direction to forward toward a
given address — is its own concept elsewhere."* **This node is that elsewhere.** Everything the
[[network-stack]] established still holds: the destination *host address* is stamped into the packet
and stays the same end to end; the *hardware address* in the link envelope names only the next
device and is rewritten at every hop. What was left open is the question that sits exactly between
those two facts: given the unchanging host address, *how does each machine choose the next device* —
and therefore which hardware address to write into the next link envelope? Choosing that next device
is IP routing.

The concept of this node is **not** the host address (that belongs to the [[network-stack]]) and
**not** the hardware rewriting (also already covered). The concept is the **decision procedure and
the table that drives it** — how a destination address is turned into a "send it out *this*
interface, toward *that* neighbour." That procedure, and why it is structured the way it is, is the
whole idea.

### The terms, before we use them

A few words must be pinned down before the mechanism makes sense; each is defined here on first use.

- An **address** is the network-layer identifier of one host, as introduced in the [[network-stack]]
  — for the examples here, written in the familiar four-number dotted form like `192.168.1.5`.
- A **network prefix** is not one address but a *whole contiguous block* of them, written as an
  address followed by a slash and a number, like `192.168.1.0/24`. The number after the slash says
  *how many leading bits are fixed*; the rest are free to vary. `/24` fixes the first 24 bits — here,
  the first three numbers `192.168.1` — so the prefix `192.168.1.0/24` names every address from
  `192.168.1.0` through `192.168.1.255`: "all hosts whose address starts with `192.168.1`." A
  *larger* slash number means *more* bits fixed, hence a *smaller, more specific* block; `/32` fixes
  all 32 bits and so names exactly one host. The extreme other end, `0.0.0.0/0`, fixes *zero* bits
  and so matches **every** address that exists.
- A **next-hop** is the address of the single neighbouring router to which this machine hands the
  packet — one step, not the destination. (It is also called a **gateway**: a gateway is simply a
  router that serves as the doorway out of your local network toward everywhere else.)
- An **interface** is one of this machine's network cards — the physical exit the packet leaves by
  (the link layer of the [[network-stack]] will then wrap it for that specific medium).

### The object: a routing table is a list of (prefix → interface, next-hop) rules

Every host and every router holds a **routing table**: an ordered-by-specificity list in which each
row says *"for any destination address that falls inside this prefix, send the packet out this
interface — and if the destination is not directly attached, hand it to this next-hop router."* A
tiny but complete table for an ordinary home/office machine has just two rows:

```
192.168.1.0/24   dev eth0                  ← my own local network: deliver directly
0.0.0.0/0        via 192.168.1.1  dev eth0 ← everything else: hand to the gateway
```

The two rows embody the two fundamentally different ways a packet can be delivered, and the
difference is the heart of routing:

- **Direct delivery** (the first row). If the destination address falls inside a prefix that names
  *my own attached local network*, then the destination host is sitting on the same wire I am — no
  router is needed. The packet is sent straight to that host. The row has no `via`: there is no
  next-hop, because the next hop *is* the destination.
- **Indirect delivery via a gateway** (the second row). If the destination is somewhere else on
  Earth, I cannot reach it directly — I do not share a wire with it. So I hand the packet to a
  router that is closer to it than I am (the `via` address), trusting that router to continue the
  job. The `0.0.0.0/0` prefix matches *everything*, which is precisely why this row can be the
  fallback for any destination not otherwise named. A `0.0.0.0/0` row is called the **default
  route**, and its next-hop is the **default gateway**.

### The procedure: longest-prefix match

When the network layer of the [[network-stack]] is about to send a packet, it takes the
destination address and scans the table for *every* row whose prefix contains that address — there
can be more than one, because a specific block and the all-matching `0.0.0.0/0` can both contain the
same address. The tie is broken by a single rule: **longest-prefix match** — pick the matching row
whose prefix fixes the *most* bits (the largest slash number), i.e. the most specific one. The
intuition is "the most specific instruction wins": a rule that speaks about a narrow block of
addresses is more knowledgeable about those addresses than a rule that speaks about everything, so
it should be obeyed. The default route, fixing *zero* bits, is by construction the least specific
match and therefore the loser of every tie — which is exactly the behaviour wanted from a catch-all:
it is consulted only when nothing more specific applies.

Once a row is chosen, the rest follows mechanically and rejoins the [[network-stack]]: the packet
leaves by that row's interface, and the link layer wraps it in a fresh link envelope addressed to
the hardware address of the next-hop (for a direct-delivery row, the next-hop *is* the destination
host; for an indirect row, it is the gateway). The packet's *host* address is never touched — only
the choice of next device, and hence the next link envelope, comes out of this procedure.

### Why hop-by-hop, and why it is the point

Here is the non-obvious design choice this node exists to justify: **no machine knows the full path
to the destination — and that is deliberate, not a limitation.** Each machine's table answers only
*one* question — "what is the *next* device toward this prefix?" — and then trusts the next device to
answer the same question again from where *it* stands. The packet is, as the [[network-stack]] put
it, "reborn" at each hop: a router strips the link envelope, reads the unchanged host address,
consults *its own* routing table by the *same* longest-prefix-match procedure, picks *its own*
next-hop, wraps a *new* link envelope, and forwards. The host follows its table to reach its
gateway; the gateway follows *its* table to reach the next router; and so on until some router is
directly attached to the destination's network and delivers it directly.

Why build it this way instead of having each sender compute the whole route? Because a full-path
scheme would force *every* device on Earth to store a route to *every* other device, and to update
all of them whenever anything anywhere changed — the same all-to-all coupling the [[network-stack]]
showed the layering was designed to avoid. The hop-by-hop, prefix-based table replaces that with a
purely *local* duty: a router need only know directions — "for prefixes like *that*, send it *that*
way" — for the handful of neighbours it can reach, summarised as a few prefixes rather than billions
of individual hosts. Correct local decisions, chained, compose into a correct global path that no
one entity ever computes or stores. That decomposition — global reachability from local-only
knowledge — is why the internet's routing scales at all, and it is the real content of "IP routing."

### A worked instance: pinging 8.8.8.8 from 192.168.1.5

Make it concrete. This machine has address `192.168.1.5` and the two-row table shown above. The user
runs `ping 8.8.8.8`, which sends a packet to the destination host address `8.8.8.8` (a public DNS
server, deliberately *not* on the local network — a non-degenerate choice that forces the
interesting branch). Follow the routing decision:

1. **Gather candidate rows.** The kernel scans the table for prefixes containing `8.8.8.8`.
   - Row 1, `192.168.1.0/24`, names addresses starting `192.168.1`. `8.8.8.8` does **not** start
     with `192.168.1`, so this row does **not** match. (This is the branch that matters: the
     destination is *not* local, so direct delivery is impossible.)
   - Row 2, `0.0.0.0/0`, fixes zero bits and matches every address, so it **does** match `8.8.8.8`.
   - Exactly one row matches; longest-prefix match trivially selects it.

2. **Read the chosen row.** Row 2 says `via 192.168.1.1 dev eth0`: send out interface `eth0`, with
   next-hop = the default gateway `192.168.1.1`. So the packet is *not* delivered directly to
   `8.8.8.8`; it is handed to the local router.

3. **Hand off, per the [[network-stack]].** The link layer wraps the packet in a frame whose
   destination *hardware* address is that of `192.168.1.1`'s network card — **not** `8.8.8.8`'s. The
   packet's *host* address stays `8.8.8.8`. The frame goes out `eth0` to the gateway.

4. **The gateway repeats the procedure.** Router `192.168.1.1` receives the frame, strips the link
   envelope, reads the still-unchanged host address `8.8.8.8`, and consults *its own* routing table
   by the same longest-prefix-match rule. `8.8.8.8` is not on the router's local networks either, so
   *its* matching row points at *its* next-hop — its upstream router at the internet provider. It
   wraps a fresh link envelope toward that next device and forwards.

5. **And again, hop by hop.** Each subsequent router does the identical thing: read host address,
   longest-prefix match against its own table, pick its own next-hop, rewrite the link envelope,
   forward. Somewhere along the line a router *is* directly attached to the network containing
   `8.8.8.8` — its table has a specific row for that block with no `via` — and it performs **direct
   delivery** to `8.8.8.8` itself. The reply retraces the same kind of journey back, each router
   independently routing toward `192.168.1.5`.

The instance is non-degenerate on purpose. It exercises a *failed* specific-prefix match (so the
local row is genuinely skipped, not a formality), the default route being selected as the catch-all,
the host-vs-hardware address split inherited from the [[network-stack]] (host address preserved,
hardware address freshly written toward the gateway), and at least one downstream hop where another
router makes its *own* independent decision — the single fact that makes routing "hop-by-hop" rather
than "the sender computes the path." A destination on the local network instead — say `192.168.1.9`
— would have matched row 1, taken the direct-delivery branch with no gateway and no further hops, and
hidden the entire distributed, multi-hop mechanism that is the point of this node.

## Prerequisites

- [[network-stack]]

## Sources

- `linux-internals-complete.html` — the IP-layer step of "The
  journey of a packet — send" (the IP layer, on every outgoing packet, "looks up the routing table:
  'where do I send this?'") and its "What is a routing table?" Q&A ("a list of rules that says 'if
  the destination IP is in this range, send the packet out this network interface to this next-hop
  router' … consults this on every outgoing packet" — the basis for the table-of-(prefix → interface,
  next-hop)-rules object); the "See the routing table" experiment showing `ip route show` output
  `default via 172.17.0.1 dev eth0` ("send everything here") beside `172.17.0.0/16 dev eth0` ("local
  network, send directly") — the concrete two-row table, the default route, and the direct-vs-gateway
  distinction used here; and "How a packet reaches Google — hop by hop" with its "How does each router
  know where to send the packet?" Q&A (each router has its own routing table and forwards toward the
  destination, "every major intersection knows which direction to point") and the "why two addresses?"
  Q&A ("the IP header says 'final destination' … the Ethernet header says 'next hop' … at each router
  the Ethernet header is rewritten with the next hop's MAC, but the IP header stays the same") — the
  basis for the hop-by-hop, each-router-decides-its-own-next-hop mechanism and the host-vs-hardware
  split. Longest-prefix match is the standard reading of "find the rule whose range contains the
  destination, most specific wins" implied by the table having both a `/24`-style specific row and the
  all-matching `0.0.0.0/0` default.
