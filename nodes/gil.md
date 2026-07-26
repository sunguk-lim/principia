---
id: gil
title: Global Interpreter Lock
summary: The Global Interpreter Lock (GIL) is a single lock inside the standard Python interpreter (the common implementation called CPython) that may be held by only one thread at a time…
type: concept
tags: [os/process]
prereqs: [thread]
sources:
  - linux-internals-complete.html ("The GIL — why Python threads don't run in parallel"; "One lock, and everything else follows from it")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Global Interpreter Lock

## Summary

The **Global Interpreter Lock (GIL)** is a single lock inside the standard Python
interpreter (the common implementation called **CPython**) that may be held by only one
[[thread]] at a time, and which a [[thread]] **must** hold in order to run Python code.
The blunt consequence: even on a machine with many CPU cores, only **one** [[thread]] is
ever running Python code at any instant. The other [[thread]]s of the program are real,
they share one memory just as [[thread]]s do, but they are stopped — waiting their turn for
the one lock. So if your work is pure Python arithmetic spread across several [[thread]]s,
you get **no speedup** from extra cores: the [[thread]]s take turns rather than running side
by side (concurrency by interleaving, not true parallelism). The GIL exists for one reason —
to keep the interpreter's internal bookkeeping (specifically, per-object **reference counts**,
defined below) safe with a single coarse lock instead of a swarm of tiny ones. The escape
hatches: a [[thread]] **releases** the GIL while it is merely waiting on input/output, and
many heavy numerical libraries release it while crunching in their own non-Python code — so
input/output-heavy and library-offloaded work *does* benefit from [[thread]]s.

## Grounded explanation

### What the lock actually guards

Recall the lock idea from [[thread]]: when several [[thread]]s share one memory and could
trample each other's updates, you put a **lock** in front of the shared thing — a coordination
object a [[thread]] must *acquire* before touching it and *release* afterward, with the rule
that only one [[thread]] may hold it at a time; anyone else who wants it waits. The GIL is
exactly such a lock, but with an unusually broad job: the single shared thing it guards is
**the act of running Python code itself**.

To be precise about "running Python code," we need one term. When Python runs your program it
does not execute your source text directly; it first compiles it into a lower-level list of
simple instructions called **bytecode** — steps like "load a variable," "add two numbers,"
"store the result." The interpreter is the loop that reads this bytecode one instruction at a
time and carries each one out. Now connect this to what a [[thread]] is. Recall from
[[thread]] that every flow of execution carries a private **program counter** — the marker of
which instruction it is about to run next. In a multithreaded Python program the bytecode is
shared, read-only data that all [[thread]]s can see (one copy, no copying — just as [[thread]]s
share all memory), but each [[thread]] has its own program counter pointing into that shared
bytecode. Two [[thread]]s can even sit in the same function at different instructions, each
with its own program counter.

The GIL's rule is then simply this: **to advance its program counter through the bytecode — to
run even one instruction — a [[thread]] must be holding the GIL.** Since only one [[thread]]
can hold it, only one [[thread]] advances at a time. The bytecode is shared and could in
principle be read by all of them at once; the GIL deliberately serializes *which [[thread]] is
allowed to step forward*. That is the entire mechanism.

### Why a global lock and not many small ones — the reference counts

Here is the "why," and it is the hinge of the whole concept. Python has to know when an object
(a list, a string, a number) is no longer needed so it can reclaim that memory. It tracks this
with a **reference count**: every object carries a small integer counting how many places
currently refer to it. When a new name points at the object the count goes up (an operation
called **increment**); when a name stops pointing at it the count goes down (**decrement**);
when the count hits zero, nothing refers to the object and its memory is freed.

These increments and decrements happen constantly — astonishingly often. Even just *reading* an
object touches its count. And crucially, an increment or decrement is itself not a single
indivisible step: just like the `counter = counter + 1` example in [[thread]], it is really
*read the count, change it, write it back*. So picture two [[thread]]s — which, being
[[thread]]s, share all memory and therefore share these objects and their counts — both
incrementing the same object's count at the same time. This is precisely the lost-update race
from [[thread]]: both read the old count, both write back the same "+1," and one increment
**vanishes**. A lost increment means the object's count is too low, so its memory gets freed
while something still points at it — a crash. A lost decrement leaks memory forever. The
interpreter's own internal bookkeeping would corrupt.

The interpreter must prevent that. There are two ways. One is fine-grained: put a *separate*
tiny lock on *every* object's count and acquire it around each update — correct, but it means
constant lock-acquiring on the busiest operation in the language, which is slow, and a program
with one [[thread]] (the common case) pays that cost for nothing. The other way is coarse: take
*one* lock — the GIL — that a [[thread]] must hold to run any bytecode at all. Because no two
[[thread]]s ever run bytecode simultaneously, no two ever touch a reference count
simultaneously, so **every** count update is automatically safe with no per-object locking. The
single-threaded program pays almost nothing (it just holds one lock the whole time), and the
implementation stays simple and fast. That trade — give up multicore Python parallelism, gain a
simple and fast single-threaded interpreter — is the design choice the GIL *is*. As the source
puts it: one lock, and everything else follows from it.

### How the turns are taken, and where the GIL is let go

A [[thread]] holding the GIL does not run forever. It runs a short burst of bytecode, then the
interpreter checks (by default very frequently — on the order of every few milliseconds)
whether it should hand the GIL off so another waiting [[thread]] can run. A hand-off can only
happen *between* two bytecode instructions, never in the middle of one — which is what makes a
single bytecode instruction effectively all-or-nothing.

But notice the GIL only needs to be held to run *Python bytecode*. A [[thread]] that is not
running bytecode has no reason to hold it — and is made to give it up. Two situations matter:

- **Waiting on input/output.** When a [[thread]] asks to read from a network connection or a
  disk and must wait for the data, it is doing no Python work meanwhile — so it **releases** the
  GIL and lets a sibling run, then re-acquires it once the data arrives. So a program with many
  [[thread]]s each waiting on a slow network can have all of them waiting *at once*: the waiting
  overlaps, the program finishes far sooner. Here [[thread]]s genuinely help.
- **Heavy work inside a non-Python library.** Some libraries do their number-crunching not in
  Python bytecode but in fast compiled code underneath (large numerical libraries are the classic
  case). Such a library can deliberately **release** the GIL while it does that compiled work,
  because that work touches no Python reference counts. So if the expensive part of a
  CPU-bound job lives inside such a library, several [[thread]]s really can crunch on several
  cores at once.

So the honest rule is not "[[thread]]s never help with CPU work." It is: [[thread]]s do not help
CPU work that is expressed as **pure Python bytecode**, because that is exactly the work the GIL
serializes. Work that is input/output-bound, or that escapes into GIL-releasing compiled code,
is freed to run in parallel.

One more caution that follows directly from [[thread]]: the GIL keeps the *interpreter's own*
internals safe, but it does **not** make *your* multi-step operations safe. The
`counter = counter + 1` race from [[thread]] still happens in Python — it compiles to several
bytecode instructions, and a hand-off can land in the gap between reading and storing, losing an
update. The GIL guarantees each *single* bytecode instruction completes uninterrupted; it does
not glue *several* of them together. So a multi-step update across [[thread]]s still needs its
own explicit lock, exactly as [[thread]] taught.

### Worked instance: four CPU-bound threads versus four processes

Take a concrete CPU-bound job: sum the squares of the first 100 million integers — pure Python
arithmetic, nothing else. Suppose doing it in a single [[thread]] takes **8 seconds** on one
core, and the machine has **4 cores** sitting idle. The obvious idea: split the range into four
equal chunks of 25 million numbers and run each chunk in its own [[thread]], hoping for ~2
seconds (four cores working at once).

Trace what the GIL actually allows. All four [[thread]]s are pure-Python loops, so every one of
them needs the GIL to run a single instruction, and no library ever releases it. At any instant
exactly one [[thread]] holds the GIL and runs; the other three are stopped, waiting. The
interpreter hands the GIL around every few milliseconds, so the four [[thread]]s take rapid
turns — but turns are all they take. Add up the actual computing done: it is still the same
~8 seconds' worth of arithmetic, now sliced into little time-shares on **one** core's worth of
throughput at a time. Total wall-clock time: still about **8 seconds** — *no* speedup from the
three extra cores. In fact it is often slightly **worse** than the single-[[thread]] version,
because handing the one lock back and forth thousands of times per second is itself work that
the single-[[thread]] run never had to do. Four [[thread]]s, four cores, and you bought yourself
a small *loss*. This is the GIL's signature surprise, and it falls straight out of the rule: one
holder, serialized turns.

Now change one thing. Instead of four [[thread]]s of one program, run **four separate
processes** — recall from [[thread]] that a separate process is a flow with its *own* private
memory, sharing nothing with the others. Each process is a *separate running copy of the
interpreter*, and therefore has its **own** GIL. The four GILs are unrelated locks; nobody waits
on anybody. Each process churns its 25-million chunk on its own core in full parallel, in about
**2 seconds**, and a parent collects the four partial sums and adds them. Roughly a **4×**
speedup — the very thing the [[thread]]s could not deliver. (The Python tool that runs work this
way is named `multiprocessing`; the cost it pays is that the processes share no memory, so the
chunks and the partial sums must be copied between them rather than read for free.)

The contrast is the whole lesson. The GIL is per-interpreter, and [[thread]]s share one
interpreter, so [[thread]]s share one GIL and serialize. Separate processes are separate
interpreters with separate GILs, so they run in true parallel. If the job had instead been
input/output-bound, or had spent its time inside a GIL-releasing numerical library, the four
[[thread]]s *would* have sped up — for the same single reason, read the other way: in those
cases the GIL is released, so the turns stop being mutually exclusive.

## Prerequisites

- [[thread]]

## Sources

- `linux-internals-complete.html` — sections "The GIL — why Python threads don't run in
  parallel" and "One lock, and everything else follows from it": in standard CPython a single
  lock must be held to run Python bytecode, so only one thread runs bytecode at a time even on a
  many-core machine; it exists to make reference-count updates safe with one coarse lock instead
  of fine-grained per-object locks; a thread releases it while blocked on I/O and inside C
  extensions that opt to release it, which is why threading helps I/O-bound and C-offloaded work
  but not pure-Python CPU work; and the GIL guards the interpreter's internals, not your own
  multi-step operations, which still race.
