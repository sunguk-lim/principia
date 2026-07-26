---
id: system-call
title: System Call
summary: A system call is the controlled gateway by which a program running in user mode asks the kernel to perform a privileged service on its behalf — opening a file, reading from a…
type: concept
tags: [os/kernel]
prereqs: [user-mode-vs-kernel-mode]
sources: ["linux-internals-complete.html — 'System calls', 'The solution: slide a note under the door', 'What happens when you call open(\"/etc/hostname\")?', 'Every system call follows this pattern'"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# System Call

## Summary

A **system call** is the controlled gateway by which a program running in user mode
asks the kernel to perform a privileged service on its behalf — opening a file, reading
from a disk, sending a network packet. It is the **one sanctioned way** to cross the
[[user-mode-vs-kernel-mode]] boundary. The mechanism is deliberately narrow: the program
loads a small **syscall number** (an integer naming the service it wants) plus a few
**arguments** into the CPU's fastest storage slots, then executes a single special
instruction — `syscall` — that the hardware treats as a request to enter the kernel. That
instruction flips the CPU into kernel mode and jumps to **one fixed address** the kernel
chose in advance. The kernel reads the number, validates the request, does the work, and
returns to user mode with a result. The reason it must work exactly this way is safety:
the program never enters the kernel's room and never runs a single privileged instruction
of its own. It only hands a request through the door, and the kernel — the trusted side —
decides what to do with it.

## Grounded explanation

### The defining idea: a request, not an entry

From [[user-mode-vs-kernel-mode]] we know the hard fact this concept is built on: a program
in **user mode** (Ring 3) physically cannot touch hardware, cannot read the kernel's memory,
and cannot run privileged instructions — the CPU itself refuses. Yet real programs open
files and send packets constantly, all of which *require* those forbidden powers. The system
call is the resolution of that tension.

The concept here is **not** the privilege boundary itself (that is the prerequisite), and it
is **not** the `syscall` instruction alone (that instruction is just the latch on the door).
The concept is the **whole sanctioned protocol** for asking: a fixed, agreed-upon way for
untrusted code to *request* a privileged service and receive a result, without ever wielding
privilege itself.

The cleanest way to picture it is the source's image: **you slide a note under the door.**
The kernel lives in a locked room you may never enter. You cannot walk in and operate its
machinery. What you *can* do is write down exactly what you want — "open this file,
read-only" — on a small form, slide it under the door, and wait. Someone trusted inside picks
it up, does the work, and slides back an answer. You got your result; you never set foot in
the room. That asymmetry — **request crosses the line, you do not** — is the entire idea.

### Why it must be a request, and why it must be narrow

Why can't a program just call a kernel function directly, the way it calls its own functions?
Because of the guarantee established by [[user-mode-vs-kernel-mode]]: isolation is a property
of the silicon, holding even against hostile code. If user code could jump to any address in
the kernel and start running, it would be running privileged instructions of its *own*
choosing — and the whole protection scheme would collapse. A boundary you can step over
freely is no boundary.

So the crossing has to satisfy two demands at once, and the system call is shaped by both:

1. **The user side must surrender control completely.** It does not get to pick *what* runs
   in kernel mode. It can only trigger the transition; the destination is fixed in advance.
2. **The kernel side must be able to vet every request.** Because the kernel receives the
   request as plain data (a number and some arguments) rather than as executable code, it can
   inspect it — check that the file exists, that this process is *allowed* to open it, that
   the arguments are sane — before doing anything. Permission checks live here, on the trusted
   side of the door.

This is why the gateway is so deliberately small. There is exactly **one** entry address for
all system calls (the source calls the kernel's landing function the "receptionist"). The
program announces *which* service it wants not by jumping to different places — that would
mean choosing code to run — but by putting a **number** in a register and letting the kernel
look that number up in its own table. The narrowness is not a limitation; it is the
protection. A single, fixed, kernel-controlled door is auditable; a thousand doors would not
be.

### The mechanism, made precise

Three terms first, each defined before use:

- A **register** is a tiny storage slot inside the CPU — the fastest memory that exists, only
  8 bytes wide on a 64-bit chip. The CPU has a handful of them with fixed names (`rax`, `rdi`,
  `rsi`, `rdx`, and so on).
- The **syscall number** is the integer that names the service. The kernel keeps an array —
  the **system-call table** — whose index *is* that number: entry 0 is `read`, entry 1 is
  `write`, entry 2 is `open`, and so on. "Dispatch" is nothing more exotic than indexing that
  array.
- A **calling convention** is the agreed rule for *which* register holds *which* piece of the
  request, so that both sides look in the same place. On 64-bit Linux: the number goes in
  `rax`, the first argument in `rdi`, the second in `rsi`, the third in `rdx`.

With those in hand, every system call follows one pattern:

1. **The program fills the registers** — syscall number in `rax`, arguments in `rdi`, `rsi`,
   `rdx`. (An argument too big for 8 bytes, like a filename string, is left in memory and the
   register holds the *address* where it starts.)
2. **The program executes `syscall`.** This single instruction is the door. As one
   uninterruptible step it saves where to return to, switches the CPU from Ring 3 to Ring 0
   (the transition the prerequisite calls "a system call — the elevator up"), and jumps to the
   one fixed kernel entry address.
3. **The kernel, now privileged, dispatches and validates.** It reads `rax`, indexes the
   system-call table at that number to find the handler, checks permissions, and runs the
   service — touching the hardware that user mode could not.
4. **The kernel returns.** It puts the result in `rax`, switches back from Ring 0 to Ring 3,
   and jumps to the saved return address. The program resumes in user mode holding its answer.

The convention for the answer is worth stating, because it is how *failure* crosses back: the
kernel returns a non-negative number on success, and a **negative number on error** (for
example, `-2` means "no such file"). The negative value is the error code — conventionally
exposed to programs under the name `errno`. So the same return channel carries both the result
and the reason for failure.

### A worked instance: tracing `open("/etc/hostname")`

Let us run one real call and derive each step from the last. A program wants to open the file
`/etc/hostname` for reading. The string `"/etc/hostname"` already sits somewhere in the
program's own memory — say at address `0x7fff1a20`.

1. **Fill the registers.** The service "open a file" has syscall number **257** on 64-bit
   Linux (this is the `openat` variant that `open()` actually triggers). So:
   - `rax ← 257` — "I want syscall #257."
   - `rdi ← AT_FDCWD` — a flag meaning "resolve the path starting from my current directory."
   - `rsi ← 0x7fff1a20` — the *address* of the string `"/etc/hostname"` (the string itself is
     15 bytes, far too big for an 8-byte register, so the register points at it).
   - `rdx ← 0` — the value meaning "read-only."

2. **Execute `syscall`.** The program's last user-mode act. The CPU saves the return point,
   flips Ring 3 → Ring 0, and lands at the kernel's single entry address. **The program is now
   frozen**, waiting on its side of the door.

3. **The kernel dispatches.** Running in Ring 0, it reads `rax`, sees `257`, and indexes its
   system-call table at 257 to find the handler for opening files. This array lookup *is* the
   dispatch.

4. **The kernel validates and acts.** It follows the pointer in `rsi` to read the path
   `/etc/hostname`, locates the file, and **checks permissions** — is this process allowed to
   read it? Because the request arrived as data, the kernel is free to refuse here. If all is
   well, it goes to the disk (a privileged act the program could never perform itself) and
   opens the file.

5. **The kernel produces a file descriptor.** It records the open file in a per-process table
   and hands back a small integer — a **file descriptor** — that the program will use to name
   this open file from now on. Descriptors 0, 1, and 2 are taken by default (standard input,
   output, and error), so the first file a program opens typically gets **3**. The descriptor
   is like a coat-check ticket: the program holds the number, the kernel holds the actual file.
   The kernel puts `3` into `rax`.

6. **The kernel returns.** It switches Ring 0 → Ring 3 and jumps back. The program unfreezes,
   reads `rax`, and sees `3`. Its `open` call has returned `3`. It can now issue **further**
   system calls naming that descriptor — `read(3, ...)` to pull in the file's bytes,
   `close(3)` when finished — each one another note slid under the same door.

Now the **failure branch**, so the mechanism is shown end to end and not just on its happy
path. Suppose `/etc/hostname` did not exist. Steps 1–3 are identical — the program cannot tell
in advance, so it asks exactly the same way. At step 4 the kernel looks for the file, fails to
find it, and instead of a descriptor it puts a **negative** number in `rax`, namely `-2`
("no such file"). Step 6 returns as before, but now the program sees a negative `rax`, reads
it as the error code "file not found," and reports failure. The crucial point: even when the
request is *wrong*, nothing dangerous happened. The program never touched the disk, never ran
a privileged instruction, never learned anything about the kernel's internals — it slid a note
under the door and got back a polite "no." That is the safety guarantee of
[[user-mode-vs-kernel-mode]] made useful: the boundary is crossed millions of times a second,
always through the same controlled gateway, and never actually breached.

### The same shape for everything

`open` is one of a small family. `read` and `write` move bytes to and from an open
descriptor; `open` gets you the descriptor in the first place; `fork` asks the kernel to
create a new process; `mmap` asks it to map a region of memory. Different numbers, different
arguments, different handlers in the table — but every one of them is the identical protocol:
fill the registers, fire `syscall`, the CPU crosses Ring 3 → Ring 0, the kernel validates and
serves, the result comes back in `rax`. Learn the one pattern and you have learned how *all*
useful work gets done by a program that, on its own, is allowed to do almost nothing.

## Prerequisites

- [[user-mode-vs-kernel-mode]]

## Sources

- `linux-internals-complete.html` — sections "System calls,"
  "The solution: slide a note under the door," "What happens when you call
  open(\"/etc/hostname\")?" (the five-step `open` trace, registers, `sys_call_table[257]`, the
  file-descriptor ticket, the `-errno` failure path), and "Every system call follows this
  pattern."
