---
id: fork-exec
title: Fork and Exec
summary: Fork and exec is how Unix creates a new program and starts it running — and the surprising thing is that it takes two separate system-calls, not one.
type: concept
tags: [os/process]
prereqs: [process, system-call, file-descriptor]
sources: ['linux-internals-complete.html — fork/exec sections (the two-step dance, the ls /tmp walkthrough, fork without exec)']
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Fork and Exec

## Summary

**Fork and exec** is how Unix creates a new program and starts it running — and the
surprising thing is that it takes *two* separate [[system-call]]s, not one. **`fork()`**
**duplicates** the calling [[process]]: the kernel makes a near-identical copy — same
code, same memory contents, copies of the same open [[file-descriptor]]s — but gives it a brand
new PID. **`exec()`** does the opposite kind of work: it **replaces** the calling process's
program with a different executable loaded from disk, keeping the same process (same PID)
but throwing away its old code and memory and starting the new program from scratch. Used
together — `fork()` then, in the copy, `exec()` — they create a process running a *different*
program. The reason Unix splits the job in two, rather than offering a single "run this
program" call, is the small gap it opens up: between the `fork()` and the `exec()`, the copy
is briefly still running the *parent's* code, and in that window it can adjust the
environment the new program will inherit — redirect its output, close descriptors it should
not have — before the new program ever begins. That clean seam is the whole point.

## Grounded explanation

### Two calls, because there are two distinct jobs

Recall from [[process]] the central facts this builds on. A *process* is a running instance
of a program: the kernel has loaded a program file into a private region of memory and
is executing it, while tracking that one execution's live state. Each process owns a private
address space, a set of **file descriptors** (small integers naming things it has opened — a
file, the terminal, a network connection), a unique **PID** (the number that names it), and
a slot in the kernel's process table. And recall that the *only* way a new process is born
is for an existing one to ask the kernel to make it: parent creates child.

Recall too from [[system-call]] *how* a process asks the kernel for anything privileged —
creating a process certainly qualifies. It loads a number naming the service it wants into a
CPU register, executes the `syscall` instruction, and the kernel — on its trusted side of
the boundary — validates and performs the work. `fork` and `exec` are two such requests,
each a number in the kernel's system-call table.

Now the concept itself. Creating-and-launching a program is really *two* logically separate
acts, and Unix gives each its own [[system-call]]:

- **`fork()` — make a new process.** This produces the new [[process]] but runs *no new
  program*; the new process is a copy of the one that asked.
- **`exec()` — load a program into a process.** This loads a *different* program into a
  process that already exists; it makes *no new process*.

Neither call does the other's job. To "run `ls`," the shell needs both — first a new process,
then a different program loaded into it — which is why the pair is the fundamental Unix idiom.
The rest of this node explains each call, then the *why* of keeping them separate.

### `fork()`: duplicate the caller, and the call that returns twice

`fork()` asks the kernel to **duplicate the calling process**. After it completes, two
processes exist where there was one. The child is a near-identical copy of the parent: the
same program code, the same *contents* of memory (the same variables holding the same
values), and copies of the same open file descriptors — so if the parent had a descriptor
pointing at the terminal, the child has its own descriptor pointing at the same terminal.
What the child does *not* share is identity: the kernel gives it a fresh, unique **PID** and
records the forking process as its parent, exactly the parent-child link [[process]]
describes. Think of it as photocopying yourself: for a moment there are two of you with the
same memories, differing only in name.

(An aside the curious will wonder about: copying a whole address space sounds ruinously
expensive. In practice the kernel cheats — it does not physically duplicate the memory at
`fork()` time but lets parent and child share the same physical pages until one of them
writes, copying a page only then. This trick is called *copy-on-write*, and it is its own
topic; here it is enough to know that the duplication is logical and cheap, not a literal
byte-for-byte copy up front.)

Here is the genuinely strange part, the one "magic-looking" step that needs justifying:
**`fork()` returns twice.** A normal [[system-call]] is asked by one process and returns once,
to that process. But `fork()` ends with *two* processes, both poised at the instruction right
after the `fork()` call, both about to read its return value. So the kernel makes the single
call yield a *different* answer in each:

- In the **parent**, `fork()` returns the **child's PID** (a positive number).
- In the **child**, `fork()` returns **0**.

Why this asymmetry, rather than returning the same thing to both? Because immediately after
`fork()` the two processes are running *identical code* and are otherwise indistinguishable —
same variables, same position in the program. They need *some* way to tell which copy they
are, or they would both do the parent's job and nobody would do the child's. The return value
is that way. The code reads it and branches: "if I got 0, I am the child — do the child's
work; otherwise I am the parent, and the number I got is my child's PID, which I can use to
wait for it later." The kernel hands the child's PID to the parent precisely because the
parent will need that PID to refer to the child afterward (to wait on it), while the child
needs no PID to identify its parent, so 0 — a value no real PID ever takes — is a clean
"you are the child" signal. One call, two returns, is how each copy learns who it is.

### `exec()`: replace the program, keep the process

`exec()` is the mirror image. It does **not** create a process. It takes the *calling*
process and **replaces the program running inside it** with a different executable named by a
path — `exec("/usr/bin/ls", ...)`. The kernel reads the new program file from disk, throws
away the calling process's current code and memory contents entirely, lays out a fresh
address space for the new program (its code, its data, a clean stack), and jumps to the new
program's starting point. From that instant the process is running `ls`; not one instruction
of the old program remains.

What *survives* is exactly the process's identity and the parts [[process]] said the kernel
tracks per-process rather than per-program: the **PID** is unchanged, the process-table slot
is the same one, the parent link is intact, and the open [[file-descriptor]]s stay open
(unless explicitly marked otherwise). The picture: same sheet of paper, same page number —
but the old text is erased and a new document is printed on it. The "soul" of the process is
swapped; its name and its connections to the outside world are kept.

That descriptors survive `exec()` is not an incidental detail — it is the hinge the next
section turns on. The new program inherits whatever descriptors the process held at the moment
of `exec()`, and it simply uses them by their numbers, knowing nothing about how they were set
up.

### The why: the gap between fork and exec

Now the central question. If the goal is almost always "run a different program in a new
process," why force two calls? Why not a single `run("/usr/bin/ls")` that does it all at once?

Because of the **window the split creates.** After `fork()` but before `exec()`, the child is
a fully real process that is *still running the parent's code*. It has not yet been replaced
by the new program. In that window the child can run ordinary instructions to **arrange the
environment the new program will inherit** — and because file descriptors survive `exec()`,
any descriptor the child rearranges *now* is the descriptor the new program will find *then*.

This is what makes the two everyday features of a shell possible:

- **Redirection.** To run `ls /tmp > out.txt`, the shell forks; in the child it opens
  `out.txt`, then makes the child's "standard output" descriptor point at that file instead
  of the terminal, and only *then* calls `exec()` on `ls`. The `ls` program is written to
  print to standard output with no idea where that goes; it inherits a descriptor already
  aimed at the file, so its output lands in `out.txt`. `ls` needed no redirection feature of
  its own — the seam between fork and exec supplied it.

- **Pipes.** `ls | grep foo` works the same way: the shell sets up a connection, forks twice,
  and in each child rewires the appropriate descriptor to that connection *before* `exec()`,
  so one program's output becomes the other's input. Again the programs themselves are
  oblivious.

A single combined call would slam this window shut. There would be no moment at which the
process exists but the new program has not yet taken over — no place to stand and adjust
things. So Unix splits *creating* a process from *loading* a program into it deliberately: the
gap is a feature. Each program can be written to do its one job and read/write its standard
descriptors, while the *caller* composes programs together by arranging those descriptors in
the fork-to-exec window. That is the design insight the two-step dance encodes.

### Worked instance: the shell running `ls /tmp`

Trace the canonical case end to end, deriving each step from the last. You type `ls /tmp` at a
shell whose PID is **100**.

1. **`fork()`.** The shell (PID 100) issues the `fork` [[system-call]] — a note slid under the
   door asking the kernel to "copy me." The kernel allocates a new process-table slot,
   assigns a fresh PID — say **101** — records PID 100 as its parent, and gives the child a
   logical copy of the shell's memory and copies of its file descriptors. Now two processes
   exist, both `bash`, both sitting just after the `fork()` call.

2. **The twin returns split them.** In the **parent** (PID 100), `fork()` returns **101** —
   the child's PID. In the **child** (PID 101), the very same `fork()` returns **0**. The
   shared code reads this value and branches. The parent sees a non-zero number, concludes "I
   am the parent, my child is 101," and takes the parent path. The child sees 0, concludes "I
   am the child," and takes the child path. *This is the only thing that distinguishes the two
   identical copies* — without it they could not divide the labor.

3. **The child arranges the environment (the gap).** Still running `bash` code, the child is
   in the fork-to-exec window. For a plain `ls /tmp` there is nothing to redirect, so it does
   little here — but this is exactly the point where it *would* open a file and re-aim its
   output descriptor for `ls /tmp > out.txt`, or rewire a pipe for `ls | grep`. (Naming this
   step even when it is light keeps the mechanism honest: the window is always present; this
   command just doesn't use it heavily.)

4. **`exec()`.** The child calls `exec("/usr/bin/ls", ["ls", "/tmp"])`. The kernel loads
   `/usr/bin/ls` from disk, discards all the `bash` code and memory that filled PID 101, and
   starts `ls` fresh. **PID 101 is unchanged** — same process, same slot, same parent link,
   same inherited file descriptors (so `ls`'s output still reaches the terminal) — but the
   program inside is now `ls`, not `bash`. `ls` reads the directory `/tmp` and prints the
   names to its standard-output descriptor, which it inherited and which still points at your
   screen.

5. **The parent waits.** Meanwhile the parent (PID 100) took the other branch: it issues a
   `wait` call naming PID 101 — "pause me until child 101 finishes." As [[process]] explains,
   the waiting parent goes to *sleep*, off the CPU, while the child runs.

6. **Exit and reaping.** `ls` finishes and exits with a success status. By the rules in
   [[process]], PID 101's memory and descriptors are reclaimed at once, but its table slot
   lingers as a *zombie* holding the exit status until the parent collects it. The parent's
   `wait` now returns with that status; the parent has *reaped* the child, PID 101 ceases to
   exist (the number 101 may be reused later), and the shell — seeing success — prints its next
   prompt.

Notice how the prerequisites carried every step: `fork` and `exec` were two [[system-call]]s,
each a request validated by the kernel; the new process, its fresh PID, the parent-child link,
the sleeping parent, and the zombie-then-reaped ending were all the [[process]] lifecycle; and
the two return values of `fork()` were the hinge that let one piece of code act as both parent
and child.

### `fork()` without `exec()`: another copy of yourself

The two calls are paired so often that it is easy to think `fork()` always leads to `exec()`.
It does not. Sometimes a program forks *without* ever calling `exec()` — and then the child
keeps running the *same* program as the parent, because no replacement ever happens. The point
is no longer "run a different program" but "have a second copy of *myself* doing work in
parallel, with its own private memory."

This is a common server pattern. A web server can `fork()` a pool of **worker** children up
front; each child is a copy of the server already holding the right code, so each can handle
incoming requests immediately — no `exec()` needed, since the program it should run is the one
it already is. Because each child has its own copy of memory (logically separate, even if
copy-on-write keeps it cheap), a worker that crashes does not take the others down. Here
`fork()` is used purely as the [[process]]-creation half of the pair, on its own, to multiply a
running program into many isolated instances of itself.

## Prerequisites

- [[process]]
- [[system-call]]
- [[file-descriptor]]

## Sources

- `linux-internals-complete.html` — sections "The two-step dance: fork + exec" (`fork()`
  as a near-identical copy returning 0 to the child and the child's PID to the parent;
  `exec()` replacing the program while keeping the PID and surviving file descriptors),
  "Putting it together: what happens when you type \"ls /tmp\"" (the shell `fork()` →
  child `execve("/usr/bin/ls", ...)` → parent `waitpid` → exit/reap sequence; the "why two
  steps" gap enabling redirection and pipes), and "fork() without exec() — copying yourself"
  (prefork web-server workers and other self-copy uses).
