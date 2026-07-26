---
id: garbage-collection
title: Garbage Collection
summary: Garbage collection automatically reclaims the memory of objects a program can no longer reach, freeing the programmer from manual deallocation; the collector periodically finds which objects are still reachable from the roots and treats everything else as garbage.
type: concept
tags: [languages/runtime]
prereqs: [graph]
sources: [jones-gc-handbook]
status: explained
created: 2026-07-07
updated: 2026-07-07
---

# Garbage Collection

## Summary

Garbage collection (GC) is automatic memory management: instead of the programmer explicitly releasing each object when done with it, the language runtime periodically figures out which objects are still *reachable* and reclaims the memory of the rest. The key insight is that an object is still needed only if the running program can still get to it by following references — so the runtime models all live objects and the references between them as a directed [[graph]], and asks which nodes are reachable from the **roots** (the global variables and the local variables of the functions currently executing). Whatever the traversal cannot reach can never be named again, so freeing it is provably safe. This removes an entire class of bugs — leaks, double frees, dangling references — at the cost of the runtime spending time tracing the object [[graph]] and of the collection pauses that tracing can introduce.

## Grounded explanation

**The problem GC solves.** Programs allocate objects as they run and must eventually release the memory, or it fills up. Doing this by hand is notoriously error-prone: free too late (or never) and you leak memory; free too early and later use is a *dangling reference*; free twice and you corrupt the allocator. Garbage collection makes the runtime responsible instead. It rests on a single observation about *need*: the program can only ever use an object it can still **reach** — arrive at by starting from a root and following a chain of references. An object nothing can reach is inert; no future instruction could ever mention it, so reclaiming it changes nothing the program can observe. Correctness of GC is exactly this argument.

**Reachability is a [[graph]] traversal.** Model the situation as a directed [[graph]]: each live object is a node, and an edge goes from object *A* to object *B* whenever *A* holds a reference to *B*. The **roots** are the entry points the program can access directly right now — global variables and the local variables of currently running functions. "Which objects are still needed?" becomes the classic [[graph]] question "which nodes are reachable from the roots?", answered by a traversal that follows edges from the roots and visits everything it can. The **mark-and-sweep** collector does exactly this in two phases: (1) *mark* — traverse the object [[graph]] from the roots, flagging every node it reaches; (2) *sweep* — walk the full set of allocated objects and free every one that was **not** marked. Marked = reachable = keep; unmarked = unreachable = garbage.

**A concrete worked instance.** Suppose there are four objects `A, B, C, D`, and a single root variable that references `A`. The references are `A → B`, `B → C`, and `D` references nothing and is referenced by nothing (its last incoming reference was just dropped).

- **Mark** from the root: visit `A` (mark), follow `A → B` (mark `B`), follow `B → C` (mark `C`). `D` is never reached.
- **Sweep**: `A`, `B`, `C` are marked → kept; `D` is unmarked → freed.

Now suppose the program overwrites `A`'s reference so the edge `A → B` disappears, and the collector runs again:

- **Mark** from the root: visit `A` only. `B` and `C` are no longer reachable — *even though the edge `B → C` still exists*, nothing reaches `B` anymore, so the whole `B → C` cluster is dead.
- **Sweep**: `A` kept; `B` and `C` freed.

The second round is the non-degenerate part: it shows that an internal reference (`B → C`) does **not** keep an object alive if nothing reaches the cluster from the roots — reachability, not mere "is referenced by something," is what counts. (A simpler scheme, *reference counting*, keeps a per-object count of incoming references and frees at zero; it is cheaper but cannot reclaim a cycle of objects that reference each other yet are unreachable from the roots — precisely the case tracing collection handles.)

## Prerequisites

- [[graph]]

## Sources

- jones-gc-handbook
