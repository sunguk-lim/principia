---
id: file-descriptor
title: File Descriptor
summary: A file descriptor (fd) is a small non-negative integer that a program uses to name one open resource — a file, a network socket, a pipe, a device, anything the kernel can hand it.
type: concept
tags: [os/kernel]
prereqs: [system-call]
sources: ["linux-internals-complete.html — 'file descriptor' / 'coat check ticket' (the open() trace, step 4), 'What is a file descriptor, more precisely?' (fd 0/1/2, everything gets an fd), 'The complete I/O chain' (open→read(3)→write(1)→close(3)), 'Everything is a file'"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# File Descriptor

## Summary

A **file descriptor** (fd) is a small non-negative integer that a program uses to name
one open resource — a file, a network socket, a pipe, a device, anything the kernel can
hand it. The program never holds the resource itself; it holds only the number. The kernel
keeps, for each process, a **file-descriptor table**: an array that maps each fd to the real
**open-file object** living in kernel memory (which tracks the underlying file, the current
read/write position, and the access flags). A resource-opening [[system-call]] — `open`,
`socket`, `pipe` — returns a fresh fd (the lowest integer not already in use), and from then
on the program passes that fd back into `read`, `write`, `close`, and the rest. By long Unix
convention the first three are reserved: fd **0** is standard input, fd **1** is standard
output, fd **2** is standard error. The point of using a bare integer is twofold. It is a
token the program cannot forge into a reach *into* kernel memory — the real object stays on
the trusted side of the boundary the [[system-call]] guards. And because the resource is
named by a number rather than by its kind, the *same* `read`/`write` calls work on a file, a
socket, or a pipe alike.

## Grounded explanation

### What a file descriptor actually is

From [[system-call]] we already know the shape of every privileged request: the program never
enters the kernel's room and never touches a real kernel object; it slides a note under the
door and gets an answer back. A file descriptor is *the form that answer takes* when the thing
being asked for is a long-lived resource. The kernel opens the resource on its own side, keeps
it there, and hands back to the program only a **ticket** — a small integer. The source's image
is exactly a coat-check ticket: you hand over your coat, you get back a numbered stub, and from
then on you say "number 3" instead of carrying the coat around. The cloakroom (the kernel) holds
the coat; you hold only the claim on it.

So the fd is **not** the open file, and it is **not** the bytes on disk. It is a *name* — and a
deliberately impoverished one. It is a non-negative integer (0, 1, 2, 3, …), nothing more. Two
different fds can name two different open resources, and — though we will not need this case
below — two fds can even name the *same* underlying open-file object.

The thing the integer names is what we will call the **open-file object**: a small record the
kernel creates when it opens the resource. That record holds the information that has to persist
across many calls — *which* underlying file or socket this is (the kernel finds it through its
own virtual-file-system layer, which we treat here as plain machinery that locates the resource),
the **current position** (after you have read the first 12 bytes, the next `read` must continue
from byte 12, so the position has to be remembered *somewhere*, and that somewhere is this
object, not the program), and the **access flags** (was it opened read-only? for writing?). The
program sees none of this. It sees only its fd.

### Where the mapping lives: the per-process fd table

The link from "the integer 3" to "this particular open-file object" cannot live in the program's
own memory, because the program is untrusted and the open-file object is a kernel structure. So
the kernel keeps the mapping on *its* side, one per process: the **file-descriptor table**. Think
of it as an array indexed by the fd. Slot 0 points at the open-file object for standard input,
slot 1 at standard output, slot 2 at standard error, slot 3 at whatever you opened next, and so
on. The table is **per-process**: my fd 3 and your fd 3 are entirely unrelated, each indexing a
different process's own array.

This is the whole machine. When the program later issues `read(3, …)`, the kernel takes the `3`,
indexes *this* process's fd table at slot 3, follows the pointer to the open-file object, and from
there reaches the real resource. The integer the program holds is just an index into a kernel-side
array it can never see.

### Why an integer, and why this is the right design

Two pressures, established by [[system-call]], force exactly this shape.

First, **isolation must survive hostile code.** The whole reason the kernel keeps resources behind
the [[system-call]] door is that user code must never get a usable reference *into* kernel memory —
hand it a raw pointer to the open-file object and it could read or corrupt kernel state. An integer
solves this perfectly: `3` means nothing on its own. It is not an address; following it leads
nowhere. It is meaningful *only* as an index the kernel itself looks up in a table it itself owns.
The program cannot forge it into access — at most it can hand back a number the kernel will validate
against its own table (and reject if nothing is open there). The real object stays untouchably on
the trusted side.

Second, **one interface should serve every kind of resource.** If a program had to call
`read_file` for files, `recv_socket` for sockets, and `read_pipe` for pipes, every tool would need
to know what it was talking to. Instead the resource is named by an fd, and the *same* `read` and
`write` [[system-call]]s take that fd whatever sits behind it. The kernel, on its side, routes the
call to the right handler. This is precisely why Unix can say "everything is a file": `cat`, `grep`,
and `echo` do not care whether fd 3 leads to a file on disk, a socket on the network, or a device —
they just call `read`/`write` on the number, and the kernel does the rest. A socket, in fact, is
literally described as "a file descriptor for the network": you get it from the `socket`
[[system-call]] instead of `open`, but you then `read`, `write`, and `close` it identically.

### A worked instance: open → read → close

Run one real, non-degenerate sequence and derive each number from the last.

A freshly started program already has three fds in use before it opens anything: by convention the
shell wired up **0 = stdin, 1 = stdout, 2 = stderr**. The fd table therefore has slots 0, 1, 2
occupied and slot 3 free.

1. **Open.** The program issues the `open` [[system-call]] for `/etc/hostname`, read-only. The
   kernel locates the file, checks permissions, creates an open-file object for it, and must now
   choose an fd. The rule is *lowest unused integer*: 0, 1, 2 are taken, so it picks **3**. It
   writes "slot 3 → this open-file object" into the process's fd table and returns `3`. This is
   the non-degenerate part: the answer is `3`, not `0`, *because* three slots are already in use —
   the lowest-unused rule is actually exercised, not collapsed.

2. **Read.** The program calls `read(3, buf, 100)` — "from the resource named 3, copy up to 100
   bytes into my buffer." The kernel indexes the fd table at 3, follows the pointer to the
   open-file object, reads from the underlying file starting at the object's current position
   (0, the start), copies (say) 12 bytes into the program's buffer, and **advances the position
   in the open-file object to 12**. The program got its bytes; it never saw the file, only fd 3.
   A second `read(3, …)` would resume at byte 12 — proof that the position lives in the kernel's
   object, not in the integer the program holds.

3. **Close.** The program calls `close(3)`. The kernel releases the open-file object and clears
   slot 3 in the fd table. The integer 3 is now free again; the *next* `open` would hand it back
   out as the lowest unused fd.

Throughout, the program manipulated nothing but the number 3. The coat (the open file, its
position, its flags) never left the cloakroom.

### Redirection: the same program, a different slot 3 — er, slot 1

The payoff of separating "the number a program writes to" from "the object behind it" is
**redirection**, and it explains how `program > file.txt` sends a program's output into a file
without the program knowing. A program that prints does not address a screen; it calls
`write(1, …)` — write to whatever fd 1 names. Normally slot 1 of the fd table points at the
open-file object for the terminal.

To redirect, a separate `dup2` [[system-call]] is used to **overwrite slot 1** so that it points
at the open-file object for `file.txt` instead. Concretely: open `file.txt`, get back (say) fd 4,
then `dup2(4, 1)` makes slot 1 point at the *same* open-file object as slot 4. Now the program runs
exactly as before — it still calls `write(1, …)`, with not one byte of its own code changed — but
fd 1 leads to the file, so its output lands in `file.txt`. The program's name for "my output" stayed
`1`; only the kernel-side mapping behind that name moved. That indirection — a program names a
*number*, the kernel decides what the number points at — is the entire reason the file-descriptor
table exists.

## Prerequisites

- [[system-call]]

## Sources

- `linux-internals-complete.html` — the `open("/etc/hostname")`
  trace ("assigns a ticket number: 3 … a **file descriptor** — like a coat check ticket. You hold
  the number; the kernel holds the actual file"; "Allocates a file descriptor in the process's fd
  table"); the Q&A "What is a file descriptor, more precisely?" (an integer naming an open
  resource; fd 0 = stdin, 1 = stdout, 2 = stderr; new files get 3, 4, 5…; files, sockets, pipes
  all get an fd — "everything is a file"); "The complete I/O chain" (`open` → `read(3, buf, 4096)`
  → `write(1, buf, 12)` → `close(3)`); "Everything is a file" (same `read`/`write` over any
  resource); the `dup2`-based redirection note in the fork/exec section; "Sockets — network file
  descriptors."
