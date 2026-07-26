---
id: socket
title: Socket
summary: A socket is a communication endpoint for the network that the kernel hands to a program as a file-descriptor — the same small per-process integer, and the same coat-check ticket…
type: concept
tags: [networking]
prereqs: [vfs, file-descriptor, system-call]
sources: ["linux-internals-complete.html — 'Sockets — network file descriptors', 'The journey of a packet — send', 'Receiving a packet — the reverse'"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Socket

## Summary

A **socket** is a communication endpoint for the network that the kernel hands to a
program as a **[[file-descriptor]]** — the same small per-process integer, and the same
coat-check ticket, that a program gets when it opens a file. Because the endpoint *is* a
descriptor, the program talks to a machine on the far side of the network using the very
same descriptor-based interface it already uses for files: `read` and `write` (or their
network-flavored aliases `send` and `recv`) on that integer. This is the
[[vfs]] slogan "everything is a file" extended to the network. A program creates the
endpoint with the `socket()` [[system-call]] (getting back, say, descriptor `4`); a client then
`connect()`s it to a remote address and exchanges bytes; a server instead `bind()`s it to
a local address, `listen()`s, and `accept()`s incoming connections. When the program
operates on that descriptor, [[vfs]] routes the call not to a disk filesystem but to the
kernel's networking code, which moves the bytes across the network. The reason for making
the endpoint a descriptor is the whole point: every piece of machinery that already works
on file descriptors — the same system calls, readiness-waiting, descriptor inheritance —
works on a network connection unchanged.

## Grounded explanation

### The defining idea: the network endpoint is a file descriptor

Recall the central mechanism of [[vfs]]. A program never holds the thing it opened; it
holds a **[[file-descriptor]]** — a small per-process integer (the kernel hands back `3` for
the first thing a program opens, since `0`, `1`, `2` are taken by standard input, output,
and error). The descriptor is a ticket: the program keeps the number, the kernel keeps the
real object behind it, and every operation — `read`, `write`, `close` — names that ticket.
[[vfs]] also defines a fixed checklist of operation slots (a slot for "read bytes," a slot
for "write bytes," and so on) that each *backend* fills with its own routines, and one of
the backends [[vfs]] can route a descriptor to is the kernel's **networking** code.

A **socket** is exactly this: a descriptor whose backend is that networking code. The
concept of this node is **not** networking itself, and **not** the descriptor mechanism
(that is the [[vfs]] prerequisite). The concept is the **endpoint** — the object that gives
a program one end of a network conversation and dresses it as a descriptor so that the
program can speak to the network with the same vocabulary it uses for files. The source
states it plainly: "A socket is the same thing [as a file descriptor] — an integer (fd)
that represents an open connection... same interface as files, but the data goes to the
network instead of the disk."

To make a socket usable a program goes through a small sequence of calls, each defined here
before it is used:

- **`socket()`** creates the endpoint and returns a fresh descriptor. It takes arguments
  saying what *kind* of endpoint you want (see stream vs. datagram below). At this moment
  the descriptor exists but is not yet attached to anyone.
- A **client** — the side that initiates contact — calls **`connect()`**, naming the
  remote machine's **address** (which host) and **port** (which service on that host, a
  number such as `80` for a web server). After `connect()` succeeds, the two ends are
  joined and bytes can flow.
- A **server** — the side that waits to be contacted — instead calls **`bind()`** to claim
  a local address and port (so clients know where to reach it), then **`listen()`** to mark
  the socket as accepting incoming connections, then **`accept()`**, which blocks until a
  client connects and then returns *a new descriptor* representing that one client's
  connection. The original listening socket stays open to accept the next client.
- Once joined, either side moves bytes with **`send()`** / **`recv()`** (or plain `write` /
  `read` — they are the same operations on the descriptor), and **`close()`** tears the
  endpoint down.

The asymmetry is only in setup: a client reaches out (`connect`), a server waits to be
reached (`bind` / `listen` / `accept`). Once a connection exists, both ends are symmetric —
each just reads and writes its descriptor.

### Two kinds of endpoint: stream and datagram

The argument to `socket()` chooses one of two behaviors, and they differ in what a `read`
or `write` means. A **stream socket** gives a *reliable, ordered byte stream*: bytes you
send arrive in the same order with none missing or duplicated, and the boundaries between
your individual `send` calls are not preserved — it is one continuous flow, like a pipe
stretched across the network. (On the internet this reliability is provided by the
transport protocol called **TCP**, a separate concept.) A **datagram socket** instead sends
*individual self-contained messages*: each `send` is one packet that arrives whole or not at
all, with no guarantee of order or delivery and no automatic resending. (This corresponds to
the protocol called **UDP**, again a separate concept.) The choice is the trade-off between
"I want a dependable conversation, hide the packet details from me" (stream) and "I want to
fire off discrete messages cheaply and handle loss myself" (datagram).

### Why make the endpoint a descriptor — the real payoff

The non-obvious design decision is: *why route the network through a file descriptor at
all, instead of giving programs a separate, network-specific interface?* The justification
is that an enormous amount of kernel machinery already exists for file descriptors, and
making a socket a descriptor lets every bit of it apply to the network **for free**, with no
new code:

- **The same system calls.** `read`, `write`, and `close` already do exactly what a network
  conversation needs — move bytes in, move bytes out, tear down. Because [[vfs]] dispatches
  per descriptor, calling `read` on a socket descriptor routes to the networking backend's
  read routine instead of a disk one. No new "network read" call had to be invented.
- **Readiness-waiting works unchanged.** A program that must juggle many connections at once
  uses calls like `select`/`poll` that take a set of descriptors and block until at least one
  is *ready* (has data to read, or room to write). Those calls were built for file
  descriptors; because a socket *is* a descriptor, the same call lets a single program watch a
  thousand network connections and a few open files together, in one list, with one
  mechanism.
- **Inheritance across `fork` works unchanged.** When a process forks a copy of itself, the
  child inherits the parent's open descriptors. Since a socket is a descriptor, a server can
  accept a connection and hand the resulting socket descriptor straight to a child process,
  which then serves that client — the classic "one child per connection" design — using the
  ordinary descriptor-inheritance rule, not a special network feature.

The key invariant is the one [[vfs]] establishes: **the interface the program sees is fixed
and backend-independent; the kernel chooses the backend per descriptor at the moment of the
call.** A socket simply makes "the network" one of those backends. Remove the descriptor
framing and every one of the benefits above would need to be reinvented specifically for the
network.

### A worked instance: fetching a web page, byte-for-byte like a file

Run a concrete client conversation — a program asking a web server for a page — and watch
how each step is shaped exactly like a file operation. Suppose the program's descriptors
`0`, `1`, `2` are the standard streams and it has nothing else open, so the next descriptor
the kernel issues is small.

1. `fd = socket(...)` asking for a **stream** endpoint for internet communication. The
   kernel creates the endpoint and returns, say, **`fd = 4`** (it would have been `3`, but
   imagine the program already holds a log file there). The program now has a ticket whose
   backend is the networking code — but it is not yet connected to anyone.
2. `connect(4, address = 93.184.216.34, port = 80)`. This names a specific web server host
   and the port where web servers listen (`80`). The kernel reaches across the network and
   establishes the connection. (For a stream/TCP socket this involves a short setup
   exchange between the two machines, a detail that lives in the TCP concept; from the
   program's side `connect` simply succeeds and the line is now open.)
3. `send(4, "GET / HTTP/1.1\r\n...")`. This writes the request bytes into descriptor `4`.
   Note the shape: it is *identical* to `write(4, "GET / HTTP/1.1\r\n...")` on a file — same
   descriptor in hand, same "here are bytes for this ticket" operation. [[vfs]] sees the
   write on descriptor `4`, looks up that the backend is networking, and calls the networking
   write routine, which copies the bytes into kernel memory and pushes them out onto the
   network toward `93.184.216.34`.
4. `recv(4, buf, 4096)`. This reads up to 4096 bytes from descriptor `4` into the buffer
   `buf` — shape-identical to `read(4, buf, 4096)` on a file. [[vfs]] routes it to the
   networking read routine, which hands back up to 4096 bytes that have arrived from the
   server (the start of the HTTP response — the page). If no bytes have arrived yet, this
   blocks, exactly as a `read` on a slow file would.
5. `close(4)`. Same call that closes a file; here it also tells the kernel to tear down the
   network connection.

This is the entire payoff made concrete. Compare it directly to the [[vfs]] worked example,
where the *same* `read(5, buf, 100)` on a socket descriptor returned bytes that had arrived
over the network — that example showed the kernel-side routing; this one shows the
client-side conversation that put bytes there in the first place. The program code in
steps 3 and 4 is byte-for-byte what file code would be; only the descriptor's backend
differs, and the program neither knows nor cares. The instance is non-degenerate on
purpose: it exercises both directions (a `send` and a `recv`), the full client setup
(`socket` then `connect`), and a real remote service on a real port — not a do-nothing call
that would hide half the mechanism.

The server side of the same picture, in prose: a web server would `socket()` to make an
endpoint, `bind()` it to port `80` so clients can find it, `listen()` to start accepting,
and loop on `accept()` — each `accept()` returning a *new* descriptor for one client's
connection, on which the server then `recv()`s the request and `send()`s the page back,
using the identical read/write shape. The listening socket and each connected socket are
all just descriptors, which is why a server can watch them all with one `select`/`poll` and
hand each connected one to a forked child.

## Prerequisites

- [[vfs]]
- [[file-descriptor]]
- [[system-call]]

## Sources

- `linux-internals-complete.html` — sections "Sockets —
  network file descriptors" (a socket is a file descriptor for network communication;
  `socket()` / `connect()` / `send()` / `recv()` / `close()` on `fd = 3`; the VFS layer
  routes to the network "same interface as files, but the data goes to the network instead
  of the disk"; the worked `connect` to `93.184.216.34:80` then `GET / HTTP/1.1` request and
  the read of the response), and "The journey of a packet — send" / "Receiving a packet —
  the reverse" (the socket layer copies the program's bytes into kernel memory on `send`,
  and on receive deposits arriving bytes into the socket's receive buffer and wakes the
  process blocked in `recv` — the basis for the plain-prose mention that operations on the
  socket descriptor are routed into the network stack).
