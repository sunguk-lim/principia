---
id: dns
title: DNS
summary: DNS (the Domain Name System) is the distributed directory that turns a human-readable name — like example.com — into the numeric IP address — like 93.184.216.34 — that the network…
type: concept
tags: [networking]
prereqs: [socket, udp]
sources: ["linux-internals-complete.html — 'DNS — how names become IP addresses'"]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# DNS

## Summary

**DNS** (the **Domain Name System**) is the distributed directory that turns a
human-readable **name** — like `example.com` — into the numeric **IP address** — like
`93.184.216.34` — that the network actually needs to deliver packets. People remember
names; the network routes only to numbers, so before a program can open a [[socket]] to a
remote machine it must first *resolve* the name into an address. DNS does this by having a
program call a **resolver**, which sends a small query over a [[socket]] (normally a
datagram socket to UDP port `53`) to a **recursive resolver**. That resolver walks a
**hierarchy** of name servers on the program's behalf — a **root** server points it to the
server for `.com`, which points it to the server that is **authoritative** for
`example.com`, which finally returns the address. The answer is then **cached** for a
stated lifetime (its **TTL**, time-to-live), so a repeat lookup of the same name is instant
and the hierarchy is not re-walked. The point of all this machinery is that one global
table of every name would be impossible to scale and to administer; a cached hierarchy
instead lets each organization control its own slice of the name space and spreads the
lookup load across thousands of independent servers. DNS is therefore the **prerequisite
step** before any named connection: you resolve the name to an address, *then* you open the
[[socket]].

## Grounded explanation

### The problem DNS exists to solve

A program that wants to talk to a machine across the network opens a [[socket]] and, as a
client, calls `connect()` naming the remote machine's **address** and **port**. As the
[[socket]] node showed, that address is a number — in the worked example there,
`connect(4, address = 93.184.216.34, port = 80)`. The network's delivery machinery (the
layer that actually routes packets, kept here as plain background) understands only such
numeric **IP addresses**: an *IP address* is the numeric identifier of a network interface,
the thing packets are routed toward, written for the common version as four numbers
`0`–`255` separated by dots, e.g. `93.184.216.34`.

But no human types `93.184.216.34`. People type **names** — `example.com`, `google.com` — a
*name* being a readable label for a service. So there is a gap: the user supplies a name,
the [[socket]] layer demands a number. **DNS is the directory that closes that gap.** Its
defining contribution is the *translation from name to address*, performed not by a lookup
in one giant local table but by a query out onto the network. The source states the shape
plainly: when you run `curl google.com`, "your program doesn't know Google's IP address...
it sends a UDP packet to a DNS server asking 'what's the IP for google.com?' The DNS server
responds with an IP address, and *then* the TCP connection starts."

Two terms used above, defined before going on. **UDP** ([[udp]]) is the network's *datagram* style of
communication — fire one self-contained message, no guarantee it arrives, no automatic
resend — which in the [[socket]] node was the behavior of a **datagram socket**; DNS rides
on it because a query and its reply are each a single tiny message, and the cost of a lost
one (just ask again) is cheaper than maintaining a reliable connection. **Port `53`** is the
agreed-upon port number where name servers listen for these queries, the way port `80` is
where web servers listen.

### DNS is a step *before* the connection, not part of it

The crucial structural fact: **resolving a name is a separate, earlier act than the
connection it enables.** It is itself an ordinary use of a [[socket]]. The source is
emphatic — "DNS is just regular networking — a UDP packet out, a UDP packet back. No special
kernel magic." There is no secret "name" feature inside the kernel's networking code; the
resolver is just a program (or library routine) that opens its own datagram [[socket]],
`send()`s a question to a name server, `recv()`s the answer, and reads the address out of
it. Only *after* that does the real client open the [[socket]] it actually wanted and
`connect()` to the address that came back.

Concretely, fetching a web page is two phases:

1. **Resolve.** The program calls a resolver routine with the name `example.com`. The
   resolver checks a small local override file first (on Linux, `/etc/hosts`, a hand-edited
   list of name-to-address entries), and if the name is not there, opens a datagram
   [[socket]] and sends a UDP query to its configured name server on port `53`. The reply
   carries `93.184.216.34`.
2. **Connect.** *Now* the program does exactly what the [[socket]] node described: open a
   stream [[socket]], `connect(fd, address = 93.184.216.34, port = 80)`, `send()` the
   request, `recv()` the page. The address fed to `connect()` is the one DNS just produced.

So DNS does not move your page's bytes and is not part of the conversation with the web
server; it is the lookup that supplies the destination number for that conversation.

### Why a hierarchy instead of one big table

The non-obvious design — the part worth justifying — is *how* the resolver gets the answer.
The naive picture is a single master table mapping every name on earth to its address, kept
somewhere and consulted on each lookup. That cannot work, for two independent reasons:

- **Scale.** There are billions of names and an enormous rate of lookups worldwide. One
  table on one server (or even a fixed set of servers) could neither hold the load nor stay
  current; updating it would funnel through one administrator.
- **Administration.** Whoever owns `example.com` must be able to change *their* addresses
  without asking a central authority, and without being able to alter anyone else's names.

DNS solves both by making the name space a **hierarchy** and **delegating** authority down
it. A name like `example.com` is read *right to left* as a path in a tree:

- the **root**, written as the empty top (the trailing dot in `example.com.`), which knows
  nothing but *where to find* each top-level zone;
- a **TLD** (top-level domain) such as **`.com`**, whose servers know where to find each
  registered domain under it;
- the **authoritative** server for **`example.com`** — *authoritative* meaning it holds the
  real, owner-maintained records for that domain and gives the definitive answer.

Each level does not store the level below it — it only **delegates**: it hands back a
pointer saying "I don't have the final answer, but the servers for the next level down are
*here*." Authority is thus split per domain: the owner of `example.com` runs (or pays for)
its authoritative server and controls only its own records; `.com`'s operator controls only
the list of which domains exist and where their authoritative servers live; the root
controls only the list of TLDs. No one holds the whole table, so no one is the bottleneck,
and each owner administers exactly their own slice. This delegation *is* the structure of
DNS — the directory's contribution is not just "name → address" but "name → address by a
walk down a delegated tree."

### The recursive resolver and walking the hierarchy

A plain program does not want to perform this multi-step walk itself. So it sends *one*
query to a **recursive resolver** — a name server (run by your network or a public provider)
whose job is to do the whole walk on your behalf and hand back just the final answer.
*Recursive* here means "you ask me once for the complete answer, and I chase down every
referral myself," as opposed to a server that merely answers "I don't know, go ask them."

The walk the recursive resolver performs, when it has nothing cached:

1. Ask a **root** server: "address of `example.com`?" The root does not know it but
   **refers**: "ask the `.com` servers, they are at *these* addresses."
2. Ask a **`.com` (TLD)** server the same question. It refers again: "ask the authoritative
   servers for `example.com`, at *these* addresses."
3. Ask the **authoritative** server for `example.com`. It holds the real record and returns
   the answer: `93.184.216.34`.
4. The recursive resolver returns that single address to the program that asked.

Each of these messages is itself just a UDP query/reply over a [[socket]] on port `53` — the
same mechanism end to end, repeated down the tree.

### Caching and the TTL — why repeats are instant

Walking root → TLD → authoritative for *every* lookup would be slow and would hammer the
upper servers. The fix is **caching**: every DNS answer arrives stamped with a **TTL**
(time-to-live), a number of seconds the answer may be reused before it must be looked up
again. The TTL is set by the domain's owner — it is their lever on the trade-off between
*fast repeat lookups* (long TTL) and *quick propagation of changes* (short TTL, since old
cached answers expire sooner).

The recursive resolver keeps a cache of recent answers. So:

- A **cache miss** (name not cached, or its TTL expired) triggers the full walk above.
- A **cache hit** (name cached, TTL not yet expired) returns the stored address immediately,
  with **no** network walk at all.

This is also why the upper levels survive the world's query load: the root and TLD referrals
themselves get cached with long TTLs, so the recursive resolver rarely has to bother them —
it usually still has "the `.com` servers are *here*" in hand and can jump straight to the
authoritative server, or straight to the cached final answer.

### A worked instance: resolving `example.com` twice

Run it concretely. A fresh recursive resolver, empty cache. A program wants `example.com`.

**First lookup (cold cache — every branch is exercised).** The program opens a datagram
[[socket]] and sends one UDP query to its recursive resolver on port `53`: "address of
`example.com`?"

1. The resolver checks its cache: **miss** (nothing stored). So it must walk.
2. It queries a **root** server. Reply: a **referral** — "for `.com`, ask the TLD servers at
   *these* addresses." (Not the answer — the root never holds it.)
3. It queries a **`.com` TLD** server. Reply: another **referral** — "for `example.com`, ask
   its authoritative servers at *these* addresses."
4. It queries the **authoritative** server for `example.com`. Reply: the real record,
   **`93.184.216.34`**, stamped with a TTL of, say, **`3600`** seconds (one hour).
5. The resolver **caches** `example.com → 93.184.216.34` for `3600` seconds and sends
   `93.184.216.34` back to the program in one UDP reply.

The program now has the address and proceeds to phase two: open a stream [[socket]] and
`connect(fd, address = 93.184.216.34, port = 80)` — the exact `connect()` from the
[[socket]] worked example. DNS's job ended at step 5.

**Second lookup (30 seconds later — cache hit).** Another program (or the same one) again
asks the resolver for `example.com`. The resolver checks its cache: the entry is present and
only 30 of its 3600 seconds have elapsed, so it is still valid — a **hit**. The resolver
returns `93.184.216.34` immediately, with **zero** queries to root, `.com`, or the
authoritative server. The tree is not re-walked.

**Later (after 3600 seconds — the entry expires).** Once the TTL runs out the cached entry
is discarded; the next lookup is a miss again and re-walks the hierarchy, picking up any
address the owner has changed in the meantime. This is the TTL doing its job: it bounds how
stale a cached answer can be.

This instance is non-degenerate on purpose: the cold lookup triggers all three referral
levels (root, TLD, authoritative) rather than collapsing into one, and the second lookup
demonstrates the cache-hit branch that makes DNS fast — the two cases together show both
*how the directory is walked* and *why it does not have to be walked again*.

## Prerequisites

- [[socket]]

## Sources

- `linux-internals-complete.html` — section "DNS — how names
  become IP addresses" (a program calls a resolver, which checks `/etc/hosts` then sends a
  UDP packet to a DNS server on port `53` asking for a name's IP, gets the address back, and
  *then* the connection starts; "DNS is just regular networking — a UDP packet out, a UDP
  packet back. No special kernel magic"; and the adjacent note that UDP is "used for DNS
  lookups" because speed matters more than reliability). The root → TLD → authoritative
  hierarchy, recursive resolution, and TTL caching are the standard DNS mechanism expanding
  on this section.
