---
id: vfs
title: Virtual File System
summary: The Virtual File System (VFS) is a layer inside the kernel that presents one uniform interface — the file system-calls open, read, write, close, lseek, all acting on a small…
type: concept
tags: [os/filesystem]
prereqs: [system-call, file-descriptor]
sources: ["linux-internals-complete.html — 'VFS — the uniform interface', 'Inodes and dentries — how files are tracked', '\"Everything is a file\" — now you understand why'"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Virtual File System

## Summary

The **Virtual File System (VFS)** is a layer inside the kernel that presents **one
uniform interface** — the file [[system-call]]s `open`, `read`, `write`, `close`,
`lseek`, all acting on a small integer handle — over **many different underlying
implementations**. Behind that single interface can sit a disk filesystem (ext4, xfs),
a network filesystem, an in-memory pseudo-filesystem like `/proc`, a device such as a
keyboard or a random-number source, a pipe, or a network socket. The reason VFS exists
is that a program should not have to know, or care, *which* of these it is talking to.
When the program issues `read` on a handle, VFS looks up which backend owns that handle
and forwards the call to *that* backend's own read routine. Because the same call is
routed to the right place every time, a single piece of code — `read(fd, buf, n)` — works
identically whether the bytes come off a spinning disk, a network server, the kernel's
own internal tables, or a stream of random numbers. That routing is what makes the famous
Unix slogan **"everything is a file"** literally true.

## Grounded explanation

### The defining idea: one interface, many backends, a dispatcher between them

Recall from [[system-call]] what a program actually has in hand after it opens a file.
It does not hold the file itself; it holds a **[[file-descriptor]]** — a small per-process
integer (the kernel hands back `3` for the first file a program opens, since `0`, `1`, `2`
are taken by standard input, output, and error). The descriptor is a coat-check ticket:
the program keeps the number, the kernel keeps the real thing the number refers to. Every
later operation — `read`, `write`, `close` — is another note slid under the same door,
naming that ticket.

The concept of this node is **not** the system call (that is the prerequisite — the
protocol for asking the kernel to do something), and it is **not** any one filesystem like
ext4. The concept is the **dispatcher** that sits just inside the door: the kernel layer
that receives a file system call, decides *which* underlying implementation that descriptor
belongs to, and forwards the request to that implementation's own routine. VFS is that
layer. The source's own image is apt: VFS is "the receptionist that looks up which actual
filesystem to talk to and forwards your request."

Here is the structure that makes this work. VFS defines a fixed list of operations that
every backend must supply — think of it as a checklist of named slots: a slot for "open a
file," a slot for "read bytes," a slot for "write bytes," a slot for "list a directory,"
and so on. Each backend fills in those slots with its *own* routines. The ext4 disk
filesystem fills the "read" slot with a routine that pulls bytes off the disk. A network
filesystem fills the same slot with a routine that fetches bytes from a remote server. The
`/proc` pseudo-filesystem fills it with a routine that *manufactures* bytes out of the
kernel's internal data structures — there is no file on any disk at all. The slots have the
same names everywhere; what is plugged into them differs completely.

### Why it must be built this way

Why not let the program call ext4 directly, or the network code directly, depending on what
it wants? Two reasons, and they are the whole justification for the layer.

First, **the program cannot know in advance which backend it will get.** A path like
`/data/report.txt` might today live on a local disk and tomorrow live on a mounted network
share, with no change to the program. If the program had to pick the right backend itself,
every program would need code for every filesystem that exists — and would break the moment
a new one appeared. VFS removes that knowledge from the program entirely: the program names
a path or a descriptor, and VFS alone decides where it routes.

Second, **uniformity is what lets one tool work on everything.** Because the operations have
the same names and the same shapes for every backend, the kernel can dress up things that are
not stored files at all — a device, a kernel data table, a pipe between two programs, a
network connection — and expose each of them *through the same slots*. A program reading from
one of these issues the very same `read` it would issue on a disk file. This is the deep
payoff, and we return to it below.

The key invariant VFS maintains is therefore: **the interface seen by the program is fixed
and backend-independent; the implementation behind it is chosen by the kernel, per descriptor,
at the moment of the call.** Nothing the program does can leak the identity of the backend
into its own code.

### Naming the real file: inode and dentry

To route correctly, VFS needs a precise notion of *what a file is* — and a filename turns out
to be the wrong answer. Two terms, each defined before use.

An **inode** is the kernel object that holds a file's real identity: its metadata (type,
permissions, owner, size, timestamps) plus the pointers to where its data actually lives. The
inode is the file. Crucially, **the filename is not stored in the inode.** A name like
`hostname` lives elsewhere; the inode is a nameless record, identified only by an inode number.
This separation is deliberate and load-bearing: because the name is detached from the file, one
file (one inode) can have *several* names pointing at it (these are hard links), and the data
survives until the last name is removed. Name and identity are different things.

A **dentry** (directory entry) is the other half: a cached mapping from a **name → inode
number**. A directory, at bottom, is just a list of such pairs. To resolve the path
`/etc/hostname`, the kernel walks the dentries: start at the root directory, look up `etc` in
its list to get an inode number, confirm that inode is itself a directory, then look up
`hostname` in *that* directory's list to get the final file's inode number. The reason dentries
are *cached* — kept in fast memory rather than re-read from disk on every lookup — is that path
resolution happens constantly (every `open` walks a whole path), and re-reading directory data
from disk for each component would be ruinously slow. The dentry cache makes traversal of a path
you have used before nearly free.

So the chain VFS follows is: **name → dentry → inode number → inode → the data (or the backend
routine that produces it).** The name gets you to the identity; the identity tells VFS which
backend owns the file and what its operation slots contain.

### A worked instance: the same `read`, three different worlds

Now the payoff, run concretely. Suppose a single program has opened three things and holds
three descriptors. Each `open` (a [[system-call]]) returned a small integer, and along the way
VFS recorded, for each descriptor, *which backend owns it*:

- `fd = 3` — a regular file `/data/report.txt` on an **ext4 disk filesystem**.
- `fd = 4` — the special device file `/dev/urandom`, a kernel **random-number source** (not a
  file on any disk).
- `fd = 5` — a **TCP network socket** connected to a remote server.

The program now executes the identical line three times, changing only the descriptor:

```
read(3, buf, 100)
read(4, buf, 100)
read(5, buf, 100)
```

These are the *same* system call — same syscall number, same argument shape — fired exactly as
the [[system-call]] node describes: descriptor in the first register, buffer address in the
second, the count `100` in the third, then the `syscall` instruction crosses into the kernel.
The program code is byte-for-byte identical across the three. It does not branch on the kind of
thing it is reading; it cannot, because it does not know.

Inside the kernel, VFS does three *different* things, and this is the entire mechanism:

1. For `fd = 3`, VFS finds that this descriptor belongs to the ext4 backend, so it calls ext4's
   read routine. That routine resolves which disk blocks hold the file's bytes and brings up to
   100 of them into `buf`. (In practice the kernel often satisfies this from a RAM copy of
   recently used file data rather than the physical disk, but that caching is a separate
   optimization layered beneath VFS; the routing decision VFS makes is the same either way.)
2. For `fd = 4`, VFS finds that this descriptor belongs to the random-device backend, so it
   calls *that* backend's read routine. There is no disk lookup at all — the routine generates
   100 fresh random bytes and writes them into `buf`.
3. For `fd = 5`, VFS finds that this descriptor belongs to the socket backend, so it calls the
   networking read routine, which hands back up to 100 bytes that have arrived from the remote
   server over the network.

Three calls, identical from the program's side; three completely different implementations
reached on the kernel's side. The dispatch — "look at which backend this descriptor belongs to,
call that backend's routine for this operation" — *is* VFS, and it is the only thing standing
between the one uniform call and the many possible sources of bytes. Note also that the
worked instance is non-degenerate on purpose: it deliberately picks three backends that behave
differently (disk lookup, on-the-fly generation, network arrival), so the routing is exercised
rather than collapsing to a single trivial case.

### "Everything is a file," now earned

The Unix slogan "everything is a file" is now not a mystery but a direct consequence. Because
every backend implements the same operation slots, the kernel can present *anything* as a file
and let ordinary file system calls work on it:

- `/etc/hostname` — a real file on disk; `read` returns its stored bytes.
- `/proc/cpuinfo` — not a stored file at all; `read` returns CPU information manufactured from
  the kernel's internal tables.
- `/dev/null` — a black hole; `write` always succeeds and the data is discarded.
- `/dev/urandom` — a generator; `read` returns random bytes.
- a pipe or a socket — a stream between programs or across the network; `read` and `write` move
  bytes through it.

A program uses the same `read`/`write` for all of them, and VFS routes each to the right
backend. This is exactly why the everyday tools — `cat`, `grep`, `echo` — work on things that
are not files in any ordinary sense: they only ever call `read` and `write` on a descriptor, and
VFS does the rest. The slogan is true *because* of the dispatcher; remove VFS and "everything is
a file" becomes meaningless, since there would be no single interface for "everything" to share.

(Two further layers commonly sit near VFS but are separate concepts, mentioned here only so they
are not confused with it: a **page cache** that keeps recently used file data in RAM to avoid
slow disk reads, and **OverlayFS**, the layered copy-on-write filesystem container runtimes use
to stack a writable layer over shared read-only image layers. Both live *beneath* the uniform
interface; neither changes the fact that the program above sees only the one set of file system
calls.)

## Prerequisites

- [[system-call]]
- [[file-descriptor]]

## Sources

- `linux-internals-complete.html` — sections "VFS — the uniform
  interface" (the operation-slot table that every filesystem fills in: `.read = ext4_read` /
  `nfs_read` / `proc_read`; the receptionist that forwards the call to the owning filesystem),
  "Inodes and dentries — how files are tracked" (inode as the file's metadata-and-data identity
  distinct from its name; dentry as the cached name→inode mapping; path resolution of
  `/etc/hostname`; hard links), and "\"Everything is a file\" — now you understand why" (the same
  `read` routed to disk files, `/proc`, `/dev/null`, `/dev/random`, and sockets).
