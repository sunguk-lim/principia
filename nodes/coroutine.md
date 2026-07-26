---
id: coroutine
title: Coroutine
summary: A coroutine is a routine that can pause itself mid-execution with a yield and later be resumed from exactly that point, keeping its own call stack of local state in between — a form of cooperative multitasking in which routines hand control to one another voluntarily rather than being preempted from outside.
type: concept
tags: [languages/semantics]
prereqs: [stack]
sources: [de-moura-coroutines, lua-5.0-impl]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Coroutine

## Summary

An ordinary function runs from start to finish on the shared call [[stack]]: it is called, it runs, it returns, and when it returns its frame and all its locals are gone. A **coroutine** relaxes this. It has its *own* private call [[stack]], and it can **yield** — suspend itself partway through, saving that [[stack]] and the exact spot it had reached — handing control back to whoever ran it. Later a **resume** restores the saved [[stack]] and continues from just after the yield, with all local state intact. So a coroutine is a routine with *multiple* entry and exit points and memory of where it was between them. Control passes only at explicit yields and resumes — this is **cooperative** multitasking, as opposed to preemptive, where the running code is preempted from outside at unpredictable points. Coroutines let you write producers, generators, and state machines as ordinary straight-line code, because the suspended [[stack]] remembers "where I was" for you.

## Grounded explanation

**The central object, against the baseline of a normal call.** A normal function participates in the single, shared call [[stack]]: calling it pushes a frame holding its locals and its return position; returning pops that frame, discarding the locals for good. Control is strictly nested — a callee always returns to its caller — and a function has exactly one entry (its start) and one exit (its return). A coroutine breaks both restrictions. It is given its **own** call [[stack]], independent of the caller's, and two new operations act on it. **Yield** suspends the coroutine: it freezes the coroutine's private [[stack]] as-is and records the precise instruction where it paused, then transfers control back to whoever resumed it. **Resume** does the reverse: it reinstates that frozen [[stack]] and jumps back to the saved spot, so execution continues as if it had never stopped. Because the [[stack]] is preserved between a yield and the next resume, every local variable and the whole chain of in-progress calls survive the pause — that persistence is the coroutine's defining capability.

**Why this is useful — cooperative control.** The switch between a coroutine and its caller happens *only* at an explicit `yield` or `resume`. Nothing external preempts a coroutine mid-statement. This is **cooperative** multitasking: the participants voluntarily hand control back and forth at points they choose, in contrast to **preemptive** multitasking, where the system can suspend running code at any instant without its cooperation. The cooperative style means that between two yield points a coroutine has the shared world entirely to itself, so there are no surprise interleavings to guard against. The practical win is expressiveness: a producer that must emit a long series of values, or a parser that must pause when input runs out, can be written as plain sequential code that simply `yield`s each time it has a result — the suspended [[stack]] plays the role that a hand-built state object would otherwise have to, remembering the position in the loop across pauses.

**A concrete worked instance.** A producer coroutine that emits `1`, then `2`, then `3` on successive resumes:

```
co = coroutine.create(function()
  coroutine.yield(1)   -- run to here, freeze this stack, give back 1
  coroutine.yield(2)
  coroutine.yield(3)
end)

coroutine.resume(co)   -- → 1   (runs to the first yield; its stack is saved)
-- ... the main routine does other work here ...
coroutine.resume(co)   -- → 2   (restores the saved stack, continues to the next yield)
coroutine.resume(co)   -- → 3
coroutine.resume(co)   -- → done (the body reached its end)
```

Follow the coroutine's private [[stack]]: on the first resume it runs up to `yield(1)` and its [[stack]] — the running function's frame, positioned just before the second yield — is frozen and set aside while the main routine runs. On the second resume that exact [[stack]] is restored and execution picks up right after `yield(1)`, advancing to `yield(2)`. The non-degenerate part is that there are *several* yields with the main routine interleaved between them: it shows the [[stack]] persisting across more than one suspension, which a single yield-and-done could not demonstrate. The coroutine "remembers" it had already produced `1` and `2` purely because its call [[stack]] was preserved — no external bookkeeping required.

## Prerequisites

- [[stack]]

## Sources

- de-moura-coroutines
- lua-5.0-impl
