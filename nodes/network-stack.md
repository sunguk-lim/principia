---
id: network-stack
title: Network Stack
summary: The network stack is the layered path that bytes written to a socket travel down, inside the kernel and out the wire, to reach a program on another machine — and the mirror-image…
type: concept
tags: [networking]
prereqs: [socket, device-driver, file-descriptor, interrupt]
sources: ["linux-internals-complete.html — 'The journey of a packet — send', 'Receiving a packet — the reverse', 'The physical layer — what signals actually arrive at the NIC?'"]
status: explained
created: 2026-06-23
updated: 2026-06-25
---

# Network Stack

## Summary

The **network stack** is the layered path that bytes written to a [[socket]] travel down,
inside the kernel and out the wire, to reach a program on another machine — and the mirror-image
path they climb back up at the far end. Going down, the data is wrapped layer by layer: each
layer takes whatever the layer above handed it, prepends a small block of its own bookkeeping (a
**header**) addressed to its own concern, and passes the bigger bundle to the layer below. The
program's bytes become a *transport segment* (a header naming **which program** — a port number)
inside a *network packet* (a header naming **which host** — an address that can be routed across
the world) inside a *link frame* (a header naming **which device on this one cable** — a hardware
address) which the network card finally turns into voltage, light, or radio on the wire. This
nesting of envelope-inside-envelope is called **encapsulation**. At the receiving machine the
same layers run in reverse: each reads and removes (strips) its own header, keeps only the payload
inside, and hands it up — **decapsulation** — until the original bytes surface at the listening
[[socket]], identical to what was sent. The point of doing it in layers at all is that each layer
solves exactly one problem and treats the layer beneath it as a dumb pipe, so the layers can be
swapped and improved independently.

## Grounded explanation

### Where this picks up: the socket is one end; the stack is the road between two ends

Recall from [[socket]] that a program holds a network connection as a **[[file-descriptor]]** — a small
integer ticket — and pushes bytes into it with `send` (or plain `write`) and pulls them out with
`recv` (or `read`), exactly as if it were a file. That node deliberately stopped at the descriptor:
when the program calls `send(4, "hello", 5)`, the kernel "moves the bytes across the network," and
how that happens was left as a black box. **This node is that black box.** The [[socket]] is the
*endpoint* — one mouth of the pipe. The network stack is the **pipe itself**: the machinery that
carries the five bytes from this machine's [[socket]] to the [[socket]] of a program on a different
machine, possibly on the other side of the planet, and brings the reply back.

The concept of this node is **not** any single layer (a port number, an address, a hardware
identifier) and **not** the socket (that is the prerequisite). The concept is the **layered
structure** — the stack of nested envelopes and the discipline that each layer only ever talks to
the one directly above and the one directly below it. That discipline is the whole idea.

### A term, before we use it: a header is a small label glued to the front of the data

Throughout, a **header** means a short, fixed-purpose block of bytes that one layer puts *in front
of* the data it was given. It carries only what that layer needs to do its job — nothing about the
content, which the layer treats as an opaque blob. Wrapping data in a header is like sealing a
letter in an envelope and writing one address on it: the postal worker reads the envelope, never
the letter. **Encapsulation** is the act of doing this wrapping on the way down; **decapsulation**
is reading and discarding the envelope on the way up. Keep one mental picture: an envelope inside a
bigger envelope inside a bigger envelope. The innermost letter is your data; each surrounding
envelope was added by one layer for one purpose.

### Going down: send() to the wire, one envelope per layer

When the program calls `send` on its socket descriptor, the bytes descend through a fixed sequence
of layers. Take the payload to be the five-byte string `"hello"` and follow it down:

1. **The socket layer** is the top, the layer the [[socket]] descriptor opens onto. Its only job
   here is to copy `"hello"` out of the program's own memory into a buffer the kernel owns, so the
   program is free to move on while the kernel works. After this step the kernel holds `"hello"`.

2. **The transport layer** prepends a header whose job is to say **which program** the bytes are
   for, because a single machine runs many programs at once and they share one network connection
   to the world. It does this with a **port** — a number identifying one program's endpoint on the
   machine (for example, `443` is the port a secure web server listens on). The header carries a
   *source port* (which program here is sending) and a *destination port* (which program there
   should receive). The bundle is now `[transport header] + "hello"`, called a **segment**. (On the
   internet this layer is usually the protocol **TCP**, which also makes the byte stream reliable —
   resending anything lost, reordering anything that arrives scrambled — or sometimes **UDP**, which
   does not. Reliability is its own concept and lives elsewhere; here, all we need is that this
   layer's header names *which program*.)

3. **The network layer** prepends a header whose job is to say **which host** (which machine) the
   bytes are for, and to let the bundle be **routed** — carried from network to network across the
   world toward that machine. It does this with an **address** identifying a host: a *source
   address* (this machine) and a *destination address* (the target machine). The bundle is now
   `[network header] + [transport header] + "hello"`, called a **packet**. (On the internet this
   layer is the **IP** protocol, and the routing decision — which direction to forward toward a
   given address — is its own concept elsewhere. Here, all we need is that this layer's header names
   *which host* and is the address that survives the whole trip end to end.)

4. **The link layer** prepends a header whose job is to deliver the bundle across exactly **one
   physical hop** — the single cable or radio link to the *next* device, which is usually not the
   final machine but a relay (a router) one step closer to it. It addresses the bundle with a
   **hardware address** (a number burned into each network card, identifying one device on this one
   local network — sometimes called a MAC address). The header names *this card* as source and the
   *next device's card* as destination. The bundle is now `[link header] + [network header] +
   [transport header] + "hello"`, called a **frame**.

5. **The physical layer** is the network card (NIC) itself — driven by a [[device-driver]], the
   kernel code that speaks the card's private register dialect — turning the frame's bits into a
   physical signal on the medium: changing **voltage** on copper wires, pulsing **light** in a
   glass fiber, or broadcasting **radio waves** for Wi-Fi. A `1` bit is one voltage level (or
   light on, or one radio symbol), a `0` is another. After this the bytes have left the machine.

Notice the strict nesting. The destination *port* sits innermost, wrapped by the destination
*host address*, wrapped by the *next-hop hardware address* — innermost is the most specific
("which program"), outermost is the most local and immediate ("which device on this wire right
now"). That ordering is not arbitrary: it mirrors *when* each piece of information is needed. The
hardware address is consumed first, at the very next device, and thrown away; the host address is
consumed last, at the final machine; the port is consumed last of all, once the bytes are already
inside the right machine.

### Across the world: the hardware envelope is rewritten at every hop

A packet does not ride one wire from sender to receiver. It **hops** through many relays — your
switch, your router, your internet provider's routers, the destination's routers — and on each hop
it exists only on the one wire between two adjacent devices. Here is the crucial asymmetry between
the two outer envelopes, and the reason there are two of them:

- The **host address** (network layer) names the *final* destination and stays the same for the
  entire journey. It is the answer to "where is this ultimately going?"
- The **hardware address** (link layer) names only the *next* device, and is **rewritten at every
  hop**. When a router receives the frame, it strips the link envelope, reads the unchanged host
  address inside to decide which wire to forward on, then wraps the packet in a *fresh* link
  envelope addressed to the next device's hardware address, and sends it. The packet is effectively
  reborn on each segment.

This is why two addressing schemes exist rather than one. The host address is for getting *across*
networks (global, end-to-end, routed); the hardware address is for getting *across one link*
(local, single-hop, replaced each time). One says "final destination: that server"; the other says
"next step: hand this to my router." Trying to do both jobs with one address would force every
device on Earth to know a single-hop path to every other device — exactly the coupling the layering
avoids.

### Coming up: the wire to recv(), each layer peeling its own envelope

At the receiving machine the signal climbs the same stack in reverse, and each layer undoes exactly
what its counterpart did on the way down — **decapsulation**:

1. **Physical / NIC**: the card senses the voltage, light, or radio; its [[device-driver]]
   reassembles the bits into the frame, and (because the CPU was doing other things) raises an
   **[[interrupt]]** — a hardware nudge meaning "a packet arrived, come handle it."
2. **Link layer**: reads the link header, confirms the frame's destination hardware address is this
   card's, strips that header, and passes up the packet inside.
3. **Network layer**: reads the host address — "is this packet addressed to me?" If yes, it strips
   the network header and passes up the segment. (If no, and this machine is a router, it forwards
   instead — that is the hop-by-hop behavior above.)
4. **Transport layer**: reads the port in the transport header to decide **which program's**
   [[socket]] this belongs to, strips the header, and hands the payload to that socket. (If this is
   TCP, it also puts any out-of-order pieces back in order and acknowledges receipt — separate
   concept.)
5. **Socket layer**: deposits the now-bare payload into the receive buffer of the matching
   [[socket]] and **wakes the process** that was blocked in `recv` on that descriptor. The program's
   `recv` returns, holding `"hello"` — byte-for-byte what was sent, every envelope having been added
   and then removed.

The symmetry is the whole story: layer *n* on the sender speaks only to layer *n* on the receiver,
through the header it wrote and the receiver read. The transport header written in send-step 2 is
the transport header read in receive-step 4, and nothing in between looked inside it.

### Why layer at all — the one insight to take away

The non-obvious design choice is: *why slice this into a stack of layers at all, instead of one
program that does the whole job?* The answer is **separation of concerns enforced by the dumb-pipe
rule**: each layer solves exactly one problem and treats the layer below it as an opaque pipe that
"just moves bytes," never inspecting how. The transport layer worries only about which program and
(for TCP) reliability; it neither knows nor cares whether the layer under it routes over six
networks or zero. The network layer worries only about reaching the right host across networks; it
neither knows nor cares whether the link beneath it is copper, fiber, or Wi-Fi. The link layer
worries only about one hop and one medium.

The payoff of that rule is that **layers compose and evolve independently**. You can replace the
bottom layer — swap a copper Ethernet card for Wi-Fi — and *nothing above it changes*, because all
the upper layers ever asked of it was "carry these bits to the next device," which both still do.
You can replace the transport layer — choose UDP instead of TCP for a video call — and the network
and link layers below are untouched, because all they were ever asked was "carry this packet to that
host." Each layer presents the same simple promise upward and demands the same simple promise
downward, so any one layer can be redesigned in isolation. That is exactly why the same word —
*network stack* — describes Wi-Fi-and-UDP and Ethernet-and-TCP and every combination: the layers
are interchangeable parts, held together only by their narrow contracts. Collapse the layers into
one monolith and every new medium or new transport would force a rewrite of the whole thing.

### A worked instance: tracing "GET /" from a client socket to a server socket

Make it concrete with the [[socket]] node's own example — a program fetching a web page — and
follow one request all the way down, across, and up. The program already has a connected stream
[[socket]] on descriptor `4`, connected to a web server. It calls:

```
send(4, "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n", ...)
```

That string — the payload, call it `"GET /"` for short — is the innermost letter. Watch it travel:

1. **Socket layer (client):** copies `"GET /"` from the program's memory into kernel memory. The
   program's part is done; the kernel now carries the bytes.
2. **Transport layer (client):** wraps it as a segment, prepending a header with *destination port
   `443`* (the secure-web port — which program on the server) and a source port for this program.
   Bundle: `[port 443 …] + "GET /"`.
3. **Network layer (client):** wraps that as a packet, prepending a header with *destination host
   address = the server's address* and *source = this machine's address*. Bundle:
   `[→ server host] + [port 443 …] + "GET /"`. This host address will not change for the rest of
   the trip.
4. **Link layer (client):** wraps that as a frame, prepending a header with *destination hardware
   address = the first-hop router's network card* (not the server — the server is many hops away;
   the router is the next device on this cable). Bundle: `[→ router card] + [→ server host] +
   [port 443 …] + "GET /"`.
5. **Physical (client):** the NIC turns the frame into voltage on the wire and sends it.
6. **Across the world:** the router receives the frame, strips the link envelope, reads the
   unchanged server host address inside, decides the next wire, wraps the packet in a *new* link
   envelope addressed to the *next* device's card, and sends. This repeats at each router. The
   port `443` and the server host address ride along untouched; only the outer hardware envelope is
   replaced at each hop.
7. **Physical / link / network (server):** the server's NIC senses the signal and interrupts; the
   link layer strips the (final) hardware envelope; the network layer reads the host address, sees
   "this is me," and strips the host envelope. Left: `[port 443 …] + "GET /"`.
8. **Transport layer (server):** reads *port `443`*, matches it to the listening web-server
   [[socket]], strips the port envelope. Left: `"GET /"`.
9. **Socket layer (server):** drops `"GET /"` into that socket's receive buffer and wakes the web
   server process blocked in `recv`. Its `recv` returns the exact bytes `"GET / HTTP/1.1\r\n…"`.

The request the client wrote with one `send` arrives at the server's `recv` unchanged, having been
clothed in three nested envelopes (port, host, hardware), carried across many cables — its hardware
envelope swapped at each — and then undressed in the reverse order. The server's reply (the page)
makes the identical trip backward, with the ports and addresses swapped, surfacing at the client's
`recv(4, …)` from the [[socket]] node. The instance is non-degenerate on purpose: it exercises all
three header layers, both directions of the journey, and at least one intermediate hop where the
hardware envelope is genuinely rewritten while the host address is genuinely preserved — the single
fact that justifies having two addressing layers at all. A localhost-to-itself example would
collapse the hop (no rewrite) and hide that distinction.

## Prerequisites

- [[socket]]
- [[file-descriptor]]
- [[device-driver]]

## Sources

- `linux-internals-complete.html` — section "The journey of a
  packet — send" (the send path through five layers, each adding its header to the same `sk_buff`:
  socket layer copies the program's bytes into kernel memory; TCP adds source/dest port; IP adds
  source/dest address and consults the routing table; the device driver adds the Ethernet
  source/dest hardware address; the NIC converts to electrical/optical signals on the wire — the
  "envelope inside an envelope" framing used here for encapsulation), "Receiving a packet — the
  reverse" (the mirror path triggered by a hardware interrupt: driver strips the link header, IP
  asks "is this addressed to me?", TCP matches the connection by port and the socket layer deposits
  the data in the receive buffer and wakes the process in `recv` — the basis for the decapsulation
  walk-up), and "The physical layer — what signals actually arrive at the NIC?" (the bottom layer as
  voltage on copper / light in fiber / radio for Wi-Fi; the hop-by-hop journey in which the packet
  is "reborn" at each router; and the explanation that the hardware address delivers within one
  local link and is rewritten at each hop while the host address stays the same end to end — the
  basis for the two-addresses section).
