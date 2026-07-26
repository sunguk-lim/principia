---
id: container-networking
title: Container Networking
summary: Container networking gives each container — a regular process the system runs in isolation — its own private network world, and then wires that world out to everything else.
type: concept
tags: [networking]
prereqs: [namespace, socket, container, network-stack]
sources:
  - linux-internals-complete.html ("Container networking — built on kernel primitives")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Container Networking

## Summary

**Container networking** gives each container — a regular process the system runs in
isolation — its own private network world, and then wires that world out to everything
else. The private world comes from a **network [[namespace]]**: a kind of [[namespace]]
that hands the container its *own* set of network interfaces, its *own* address on the
network, its *own* routing table (the rules saying where to send each outgoing packet),
and its *own* full range of port numbers. Because of that last point, the container's
[[socket]]s live in a separate world: two different containers can each `bind()` a
[[socket]] to port 80 with no collision, since each port 80 sits in a different network
[[namespace]]. That is the *isolation* half. The *connectivity* half is built from a few
ordinary kernel parts described here in plain prose — a virtual cable joining the
container's namespace to the host, a software switch on the host, and address-rewriting so
the container can reach the wider internet through the host's real address. The whole point
is that this delivers a believable private network plus real reachability **without any
virtualization** — no emulated network card, no second kernel — using only primitives the
kernel already had.

## Grounded explanation

### What the concept is, and what it is not

A **[[container]]**, recall from [[namespace]], is not a new kernel object: it is a name for an
ordinary process placed inside fresh namespaces so it sees private instances of the
machine's global resources. **Container networking** is the networking slice of that
picture — specifically, the answer to two questions about a container: *what network does
it see?* (isolation) and *how do its bytes get anywhere?* (connectivity). The concept here
is **not** the [[namespace]] mechanism itself (that prerequisite already explains how the
kernel filters a global resource per namespace), and **not** the [[socket]] mechanism
itself (that prerequisite already explains the network endpoint dressed as a file
descriptor). The concept is what happens when you put a [[socket]] inside a network
[[namespace]] and then connect that namespace outward: a container that *believes* it owns
a whole network card and the entire port range, yet can still talk to the host, to sibling
containers, and to the internet.

### The isolation half: a [[socket]] living in a network [[namespace]]

Among the [[namespace]] types is the **network namespace**, which isolates the *[[network-stack]]*:
the interfaces (the network "cards," real or virtual, that a machine can send and
receive through), the addresses assigned to them, the routing table, and the space of port
numbers. When a container is launched into a fresh network [[namespace]], the kernel — by
the same "same code, filtered answer" rule that [[namespace]] establishes — reports to it a
brand-new, near-empty network stack. Concretely the container starts with just a
**loopback interface** (the interface a machine uses to talk to itself, conventionally the
address `127.0.0.1`) and *nothing else*: no connection to any real card, no routes leading
off the machine, and a completely fresh, unused set of all 65,535 port numbers.

Now recall from [[socket]] what a server does to wait for connections: it creates an
endpoint with `socket()`, then `bind()`s that endpoint to a local address and port so
clients know where to reach it. The crucial fact is that "port 80" is not a global property
of the machine — it is a slot *in the network stack*, and each network [[namespace]] has
its own stack. So when a [[socket]] inside container A calls `bind()` on port 80, it is
claiming port 80 *in A's network namespace*; container B's [[socket]] calling `bind()` on
port 80 claims port 80 *in B's namespace*. These are two different slots in two different
pools. The `bind()` calls do not see each other and cannot collide — exactly the way two
processes in two PID namespaces can both be PID 1. This is the [[namespace]] insight applied
to the [[socket]] layer: the same `bind(80)` call, run in two namespaces, succeeds twice
because the kernel resolves "port 80" relative to the caller's network namespace.

### The why of isolation, and why it is not virtualization

Why bother giving every container its own network stack instead of just assigning each one a
different port on a shared stack? Because the goal is to let an *unmodified* program run as
if it owned the machine. A standard web server is written to listen on port 80; a database
on its standard port; and so on. If containers shared one port space you would have to
reconfigure every program to pick a unique port and avoid clashes — and they would still be
able to see and disturb each other's connections. Giving each container a private network
[[namespace]] means each program gets the well-known ports it expects, sees only its own
connections, and cannot interfere with a sibling's. The isolation is also why this is *not*
virtualization: there is no emulated network card and no second networking stack
implemented in software for the container to drive. As [[namespace]] explains, the kernel
keeps one small bookkeeping object per network namespace (carrying that namespace's own
interface list, routing table, and port space) and runs the *same* networking code for
everyone, merely consulting which namespace the calling [[socket]] belongs to. That is what
makes a container cheap: it is one ordinary process whose network questions get answered
from a private slice.

### The connectivity half: cabling the namespace out (plain prose)

Isolation alone would leave the container deaf and mute — a private stack with only
loopback can talk to nothing but itself. So the kernel also offers a way to *join* two
network namespaces, and container tooling uses it. The first part is a **virtual ethernet
pair**, usually written **veth**: a pair of virtual interfaces created together and behaving
like the two plugs of a single patch cable — whatever is sent into one plug comes out the
other. The tooling puts one plug *inside* the container's network [[namespace]] (where it
becomes the container's main interface, the thing its routing table points at) and leaves
the other plug in the *host's* network [[namespace]]. Now a packet a [[socket]] inside the
container writes is routed to the container's plug and emerges from the host-side plug — it
has crossed the namespace boundary with no copying of data, just a hand-off inside the
kernel.

The host-side plug alone only reaches the host. To let *many* containers talk to the host
and to each other, the host-side plugs are all attached to a **bridge** — a software
network switch living in the host's namespace. A switch's job is to forward a packet that
arrives on one of its ports out toward the port where the destination lives, so every
container plugged into the same bridge can reach every other one, and the host can reach
them all, as if they were machines on one small private local network.

That private network still uses private addresses that mean nothing on the public internet.
To reach the outside world the host performs **NAT** (network address translation): as a
container's outbound packet leaves the host toward the internet, the host rewrites the
packet's *source* address from the container's private address to the host's own real,
publicly reachable address, and remembers the swap; when the reply comes back to the host,
the host rewrites the *destination* back to the container's private address and forwards it
in over the veth. The container thus borrows the host's public identity for outbound trips
without ever needing a public address of its own. The reverse direction — letting an
outside client *reach into* a container — is the same trick aimed inward: the host installs
a **port-forwarding** rule that says "any packet arriving at *this* host port, rewrite its
destination to *that* container's private address and port, and send it in over the veth."

The reason to belabor that all of this is veth + bridge + NAT is the concept's punchline:
container networking adds *no new kernel subsystem*. Network namespaces, virtual interface
pairs, software bridges, and address translation each existed and were used independently
for years; a container is just these primitives composed around one [[namespace]]-isolated
process.

### A worked instance: two web servers, both on port 80

Run the canonical case, with real numbers, exercising both the no-collision property and
the outside-reachability path so nothing is hidden.

Two containers, **A** and **B**, each run a web server. Each container is in its own network
[[namespace]], so each has a private address on the host's bridge — give A the address
`172.17.0.2` and B the address `172.17.0.3`, with the host holding `172.17.0.1` on the
bridge and, say, the public address `203.0.113.5` on its real card.

1. **Both bind port 80 — no collision.** The server in A creates a [[socket]] and calls
   `bind()` on port 80; following [[socket]], it then `listen()`s and loops on `accept()`.
   The server in B does the *identical* thing: `bind()` on port 80, `listen()`, `accept()`.
   Both `bind()` calls succeed. There is no clash because A's port 80 is a slot in A's
   network [[namespace]] and B's port 80 is a slot in B's — two separate pools, just as two
   processes can both be PID 1 in separate PID namespaces. Had both servers shared one
   network stack, B's `bind(80)` would have failed with "address already in use"; the
   separate namespaces are exactly what prevent that.

2. **Each container is cabled to the bridge.** A has a veth whose far plug sits on the host
   bridge; B has its own veth to the same bridge. So A and B can already reach each other and
   the host across that private `172.17.0.0` network.

3. **An external client reaches A.** Because A's `172.17.0.2` is private and invisible from
   the internet, the host is given two port-forwarding rules: "host port **8080** → forward
   to `172.17.0.2` port 80" (container A) and "host port **8081** → forward to `172.17.0.3`
   port 80" (container B). Now a browser anywhere on the internet connects a [[socket]] to
   `203.0.113.5` port 8080. The packet arrives at the host; the host rewrites its destination
   to `172.17.0.2:80` and sends it over A's veth, where it pops into A's namespace and lands
   in the [[socket]] A's server has waiting on `accept()`. A's reply retraces the path: out
   the veth, and the host rewrites the source back to `203.0.113.5:8080` so the client sees a
   coherent answer from the address it dialed. A connection to `203.0.113.5:8081` lands in B
   the same way.

The result: two unmodified web servers, both convinced they own port 80, reachable from the
outside on `:8080` and `:8081` respectively — *one* host port mapping disambiguating them on
the public side, while *separate* network namespaces let them share the same port number on
the private side. The example is non-degenerate on purpose: it forces the no-collision case
(two real `bind(80)` calls that both succeed), traverses the veth in both directions, and
exercises both flavors of address translation (outbound source-rewriting and inbound
port-forwarding) rather than a single container that would hide the collision question
entirely.

### Where this sits

Container networking is the network face of the broader container idea from [[namespace]]:
take the *isolation* a network [[namespace]] gives — private interfaces, address, routes,
and port space, so a [[socket]]'s `bind()` is resolved per namespace — and add *connectivity*
by joining that namespace to the host with a virtual cable, switching the cables together on
a software bridge, and translating addresses for the outside. Both halves are assembled from
primitives the kernel already had, which is the whole reason a container can have a complete,
believable, private network at almost no cost and with no virtualization.

## Prerequisites

- [[namespace]]
- [[socket]]
- [[container]]
- [[network-stack]]

## Sources

- `linux-internals-complete.html` — section "Container networking — built on kernel
  primitives": a container has its own network namespace (an isolated stack with only a
  loopback interface); connectivity is built from three pre-existing kernel features — a
  **veth pair** (a virtual ethernet cable with one end in the container's namespace and the
  other on the host), a **bridge** (a virtual switch, e.g. `docker0`, connecting container
  veth ends so they can talk to each other), and **NAT via iptables** (rewriting the source
  address from the container's private IP to the host's public IP outbound, and back on the
  reply); the "under the hood" path of a container's `send()` traveling socket → routing →
  veth → host bridge → NAT → host card → internet; and the port-mapping note that
  `docker run -p 8080:80` installs a destination-rewriting rule "host port 8080 → container
  IP port 80," the basis for the worked instance's `:8080`/`:8081` forwarding.
