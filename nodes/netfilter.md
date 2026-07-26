---
id: netfilter
title: Netfilter (iptables/NAT)
summary: Netfilter is the part of the kernel that lets you intercept and act on packets while they move through the network-stack.
type: concept
tags: [networking]
prereqs: [network-stack]
sources: ["linux-internals-complete.html — 'The journey of a packet — send' (the netfilter step: ACCEPT/DROP and NAT rewriting), 'Receiving a packet — the reverse' (netfilter on the incoming direction), 'Container networking — built on kernel primitives' (iptables NAT source-rewriting and the -p 8080:80 DNAT port-mapping rule), glossary entry 'netfilter' (the five hooks PREROUTING/INPUT/FORWARD/OUTPUT/POSTROUTING and that iptables/nftables/conntrack attach here)"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Netfilter (iptables/NAT)

## Summary

**Netfilter** is the part of the kernel that lets you *intercept and act on packets while they
move through the* [[network-stack]]. Recall that a packet, on its way in or out, climbs or
descends a fixed ladder of layers; netfilter plants a handful of **hooks** — checkpoints — at
fixed points on that ladder, and at each checkpoint the packet is paused and run past a list of
**rules** you have configured. A rule looks at the packet (its addresses, its port, whether it
belongs to a connection already seen) and, if it matches, fires an **action**. The two actions
that matter are: **filter** the packet — let it through (`ACCEPT`) or throw it away (`DROP`) —
which is what a **firewall** is; and **rewrite** the packet's source or destination address/port
— which is **NAT** (Network Address Translation). Filtering is how a machine blocks unwanted
traffic (e.g. "drop everything aimed at port 23"). NAT is how a whole private network of machines
shares one public address (rewrite each outgoing packet's source to the gateway's address, and
secretly reverse the rewrite on the replies), and how a container's published port works
(`host:8080` rewritten to `container:80`). The single idea is: by putting programmable
inspect-and-rewrite stations at fixed points in the packet's path, you get firewalling, address
sharing, and port forwarding **without touching a single application** — the programs sending and
receiving never know a rule examined or altered their packets.

## Grounded explanation

### Where this picks up: the stack carries packets; netfilter intercepts them mid-journey

The [[network-stack]] told the story of a packet as an unbroken slide: on the way out, the
program's bytes get wrapped in a transport header (which program — a *port*), then a network
header (which host — an *address*), then a link header, and onto the wire; on the way in, each
layer peels its own header and hands the rest up until the bytes surface at the receiving program.
In that telling the slide had no interruptions — every packet that entered one end came out the
other.

Netfilter is what happens when you cut openings into that slide. It is a kernel framework that
places **hooks** — fixed interception points — at specific spots along the packet's path, and at
each hook the kernel pauses the packet and consults a list of **rules** before letting it continue.
This node's concept is *not* the network stack (that is the prerequisite — the road), and *not*
any one rule or tool. The concept is **the hook-and-rule framework itself**: the idea that a small
set of well-chosen checkpoints in the packet path, plus user-configurable rules at each, is enough
to express firewalling, address translation, and routing tricks as data rather than as code.

### Terms, before we use them

- A **hook** is a fixed point in the packet's journey through the stack where the kernel stops and
  asks "should I do anything to this packet?" There are exactly five, named for *where on the path*
  they sit (defined precisely in the next section). A hook is a *place*, not an action.
- A **rule** is a single line of the form *match → action*: a condition on the packet (its source
  or destination address, its port, whether it is part of a known connection) and, if the condition
  holds, what to do. Rules are installed by a person or program from outside the kernel; the kernel
  only stores and runs them.
- The **action** (sometimes called the *target*) is the verdict a matching rule returns. The ones
  that carry this node are `ACCEPT` (let the packet continue along the stack), `DROP` (delete the
  packet silently — the sender never hears back), `REJECT` (delete it but send back an error so the
  sender learns it was refused), and the NAT actions that **rewrite** an address or port in the
  packet's headers.
- **iptables** and its successor **nftables** are the userspace command-line tools you type rules
  into; they are how a human or a program (such as container tooling) tells netfilter what rules to
  install. They are *reference detail* — interchangeable front-ends to the same kernel framework —
  not the concept itself. The concept is netfilter; iptables is one keyboard for it.

### The five hooks: cut openings into the packet path by *where the packet is going*

The genius of netfilter's placement is that the five hooks are not arbitrary — each sits at a point
in the [[network-stack]]'s path where the kernel has just learned something decisive about *where
the packet is headed*, so that a rule at that hook can act with exactly the knowledge it needs. As
a packet moves through the kernel, the network layer makes a routing decision — "is this packet for
*me* (this machine), or is it merely passing *through* me on its way somewhere else?" The hooks
straddle that decision:

1. **prerouting** — the moment a packet *arrives* from the wire, before the kernel has decided
   whether it is local or just passing through. Everything inbound hits this hook first. (This is
   where destination-rewriting NAT happens, because you must rewrite the destination *before* the
   routing decision reads it.)
2. **input** — a packet that the routing decision found is **destined for this machine**, just
   before it is handed up to a local program's [[network-stack]] endpoint. This is the hook a host
   uses to defend *itself* ("don't let anything reach my port 23").
3. **forward** — a packet that the routing decision found is **not for this machine** but is to be
   relayed onward to another machine. Only a machine acting as a router/gateway sees traffic here.
   This is the hook used to police traffic *passing between* networks.
4. **output** — a packet that a **local program just generated** and is sending out, as it begins
   its descent down the stack toward the wire. This is the hook a host uses to control its *own*
   outbound traffic.
5. **postrouting** — the last moment *before a packet leaves* on the wire, after the routing
   decision has chosen which interface it exits by. Both forwarded traffic and locally-generated
   traffic converge here on the way out. (This is where source-rewriting NAT happens, because you
   want to rewrite the source *after* routing has settled which interface — and therefore which
   source address — applies.)

So the inbound life of a packet is: **prerouting**, then the routing decision splits it — either to
**input** (it is for me) or to **forward** then **postrouting** (it is passing through). The
outbound life of a locally-generated packet is: **output**, then **postrouting**, then the wire.
Every packet therefore passes through a *predictable, small* set of hooks, and which ones tell you
its role — local-bound, locally-sourced, or in transit. A rule placed at the right hook sees
exactly the packets it cares about.

### Job one: firewalling — `ACCEPT`, `DROP`, `REJECT` by address, port, or connection state

The first thing rules do at a hook is **filter**: decide whether a packet may proceed. Each hook
holds an ordered list of rules; the packet is tested against them top to bottom, and the **first**
rule whose match condition holds fires its action and the verdict is settled. `ACCEPT` releases the
packet to continue along the stack; `DROP` deletes it on the spot and tells the sender nothing (the
sender just times out, never learning the machine even exists on that port); `REJECT` also deletes
it but sends back an explicit refusal. A match condition can test the packet's destination port
("port 22"), its source address ("anything from 10.0.0.0/8"), the interface it arrived on, and so
on.

The load-bearing refinement is **connection state**, supplied by a netfilter sub-system called
*connection tracking* (conntrack). The kernel remembers the connections it has already seen, so a
rule can match not just on raw header fields but on *whether this packet belongs to a connection
already established*. That is what lets a firewall express the natural policy "block strangers from
starting conversations with me, but let replies to conversations *I* started come back in" — the
outbound first packet creates a tracked connection; inbound packets that match an existing tracked
connection are accepted, while inbound packets that would *start* a new connection are dropped.
Without connection state you could only filter each packet in isolation and could not tell a
solicited reply from an unsolicited intrusion.

A firewall, then, is nothing more than a well-chosen set of filter rules sitting at the hooks. The
word "firewall" names the *use*; netfilter's hooks-and-rules is the *mechanism*.

### Job two: NAT — rewriting source or destination so addresses can be shared and forwarded

The second thing a rule can do is **rewrite** part of the packet rather than merely pass or drop
it. Recall from the [[network-stack]] that the network header carries a *source address* (who sent
it) and a *destination address* (where it is going), and the transport header carries a *source
port* and *destination port* (which program at each end). **NAT** is a rule whose action edits
these fields in flight. There are two directions, and they sit at the two hooks chosen above for a
reason:

- **Source-NAT** rewrites the *source* address (and often port) of an *outbound* packet, at the
  **postrouting** hook (the last stop before the wire, after routing has fixed which interface and
  thus which legitimate source address applies). Its purpose: let many machines share **one** public
  address. A private machine's packet leaves with its own private source address; the gateway
  rewrites that source to the gateway's single public address before it hits the internet, so to the
  outside world all the private machines look like one. The connection-tracking table records the
  rewrite, so when a **reply** arrives addressed to the public address, netfilter looks up the
  tracked connection and **reverses** the rewrite — restoring the original private address as the
  destination — so the reply lands back on the machine that actually sent the request. The reversal
  is automatic and invisible; neither the private machine nor the remote server ever sees the other
  half of the trick.

- **Destination-NAT** rewrites the *destination* address/port of an *inbound* packet, at the
  **prerouting** hook (the first stop on arrival, *before* the routing decision reads the
  destination — which is exactly why it must go here: change where the packet is "for" before the
  kernel decides where to send it). Its purpose: **port forwarding** — make a service reachable at
  one public address/port actually live somewhere else. A packet arriving at the gateway addressed
  to `host:8080` has its destination rewritten to `inner-machine:80`, and routing then carries it to
  that inner machine. Replies are reversed by connection tracking just as with source-NAT.

The "magic-looking" step worth justifying is the *automatic reversal*. It is not magic: it is the
direct consequence of connection tracking remembering each rewrite as part of a tracked connection.
A rewrite in one direction is only safe because the matching un-rewrite in the other direction is
guaranteed — otherwise the reply would arrive at the gateway's public address with no idea which
private machine it belonged to and would be undeliverable. NAT works *because* the firewall's
connection-tracking machinery underwrites it.

### Why hooks-and-rules — the one insight to take away

The non-obvious design choice is: *why express all of this — firewalling, address sharing, port
forwarding — as configurable rules at a few fixed points in the kernel, instead of building each
feature into the programs that need it?* The answer is that the packet path is the **one place
every packet must pass regardless of which application sent or will receive it**, and it is *below*
the applications. Putting programmable inspect-and-rewrite stations there means a single rule
protects or redirects traffic for *every* program at once, and the programs need no awareness of it:
a web server does not have to be rewritten to be reachable through a port-forward, and a private
machine does not have to be reconfigured to share a public address. Inspection and rewriting become
**data** (rules you can add and remove at runtime) rather than **code** (logic compiled into each
app). That is the whole payoff: one neutral, application-agnostic layer where policy lives, exactly
because it sits at the chokepoint the [[network-stack]] already forces every packet through.

### A worked instance: a DROP at input, a source-NAT at postrouting, a DNAT for a container port

Run three concrete rules through the machinery, each exercising a different hook and action, so no
single case hides part of the mechanism.

**(1) A firewall DROP at the input hook.** Install one rule: *match destination port 23 (telnet) →
`DROP`*. A packet arrives from the wire and hits **prerouting**; the routing decision finds it is
addressed to this very machine, so it heads for the **input** hook. There the rule list is walked
top to bottom; the packet's destination port is 23, the condition matches, and the verdict is
`DROP`. The packet is deleted immediately — it never reaches a local program's
[[network-stack]] endpoint, and the sender hears nothing back and eventually times out, unable to
even tell whether the machine exists. (Had no rule matched, the packet would have continued up to
the listening program as in the bare [[network-stack]] story.)

**(2) A source-NAT rewrite at the postrouting hook.** A private machine with source address
`10.0.0.5` sends a packet to some server on the internet. The packet leaves `10.0.0.5`, reaches the
gateway, and — because the gateway is not its final destination — is found by routing to be in
transit: it traverses **forward**, then arrives at **postrouting** on its way out the gateway's
public interface. Here a source-NAT rule fires: rewrite the source address from `10.0.0.5` to the
gateway's single public address. Connection tracking records the pairing `(public addr, that remote
server) ⇄ 10.0.0.5`. The packet hits the wire looking as though the gateway itself sent it. When
the server's **reply** comes back — addressed to the public address — it enters at **prerouting**,
connection tracking recognizes it as belonging to the tracked connection, and *reverses* the
rewrite: it sets the destination back to `10.0.0.5`. Routing then delivers it to the original
private machine. Many private machines can do this at once, all sharing the one public address,
each kept distinct by its own tracked connection.

**(3) A destination-NAT rule for a published container port.** A container — an isolated program
with its own private address on a host-internal virtual network — runs a web server listening on
port 80, and you want it reachable from outside at the host's `8080`. The tooling that launched the
container installs one rule: *match destination = host address, port 8080 → rewrite destination to
`container-addr:80`*. A request arriving at `host:8080` enters at **prerouting**; the rule matches
and rewrites the destination to the container's address and port 80 *before* the routing decision
reads it, so routing now carries the packet onto the host-internal network to the container, where
its web server's [[network-stack]] receives it on port 80 exactly as if the request had been
addressed there all along. The container's reply is reversed by connection tracking back to the
original requester. The port-mapping that looks like a container feature is, underneath, a single
destination-NAT rule at one netfilter hook — the same mechanism case (2) used in the other
direction.

Across the three: a filter (`DROP`) at **input**, a source-rewrite at **postrouting** with an
automatic reverse at **prerouting**, and a destination-rewrite at **prerouting** with its own
reverse — together they touch four of the five hooks, both actions (filter and rewrite), both NAT
directions, and the connection-tracking reversal that ties replies back to their requests. None of
the three required changing the programs whose packets were filtered or rewritten — the point of the
whole framework.

## Prerequisites

- [[network-stack]]

## Sources

- `linux-internals-complete.html` — the "journey of a packet — send"
  diagram places **Netfilter (iptables/nftables)** as an explicit step between the IP layer and the
  device driver, annotated "firewall rules checked here / ACCEPT? → continue. DROP? → packet is
  silently discarded / NAT? → source/dest addresses rewritten here" (the basis for the two jobs,
  filter and rewrite); the "Receiving a packet — the reverse" diagram shows netfilter again on the
  incoming direction after the driver strips the Ethernet header (the basis for hooks sitting on
  both the inbound and outbound paths); the glossary entry **netfilter** — "the kernel framework
  that processes packets at hooks (PREROUTING, INPUT, FORWARD, OUTPUT, POSTROUTING); iptables,
  nftables, and conntrack all attach here" (the basis for the five hooks and connection tracking);
  the "Container networking" section, which shows **iptables NAT** rewriting a container's source IP
  to the host's public IP outbound and reversing it on the response (the source-NAT worked
  instance), and its Q&A "When you run `docker run -p 8080:80`, Docker adds an iptables DNAT rule:
  any packet arriving at host port 8080 → rewrite destination to container's IP port 80" (the
  destination-NAT / port-mapping worked instance); and the experiments section, which lists the
  `iptables` chains INPUT/OUTPUT/FORWARD as "the netfilter rules that every packet passes through"
  (corroborating the per-hook rule lists).
