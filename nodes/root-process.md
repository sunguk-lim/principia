---
id: root-process
title: Root process
summary: The root is the single process singled out to play a special role in a collective that is not symmetric — the one rank that is either the source of the data (it has the value…
type: concept
tags: [parallel-computing]
prereqs: [rank]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Root process

## Summary

The **root** is the single process **singled out to play a special role** in a
collective that is not symmetric — the one [[rank]] that is either the **source** of
the data (it has the value everyone else will get) or the **sink** (it ends up
holding the combined or collected result). It is named by its rank number, the same
on every process, and passed as the `root` argument of the call.

## Grounded explanation

Within a group, every process has a [[rank]] — an integer id `0 … n-1`. Most
collectives treat all ranks alike, but some have an **asymmetric shape** with one
distinguished endpoint. That endpoint is the *root*, and it is specified simply by
giving its rank:

1. **It is just a chosen rank, not a special kind of process.** Any rank can be the
   root; "root" is a *role* assigned for one call, identified by its [[rank]] number
   (often `0`, but it need not be).
2. **Everyone must name the same root.** The root is an argument every participant
   passes, and they must all pass the *same* [[rank]] — otherwise the operation's
   shape is ill-defined (some think rank 2 is the source, others rank 0).
3. **Source or sink, depending on the operation.** As a **source**, the root is the
   one that holds the data to begin with (broadcast sends *from* it, scatter splits
   *from* it). As a **sink**, the root is the one that ends up with the answer
   (gather collects *to* it, reduce stores the combined result *at* it).

So the root is the asymmetry of a collective made concrete: a single [[rank]] picked
out to be the one end that differs from all the others.

`rank` is currently on the frontier; once archived, this node closes against it down
to the parallel-process floor.

## Prerequisites

- [[rank]]

## Sources

_none_
