---
id: communicator
title: Communicator
summary: A communicator is a named, fixed group of processes that are allowed to exchange messages with one another, together with an addressing scheme that gives each member a rank — an…
type: concept
tags: [parallel-computing]
prereqs: [message-passing]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Communicator

## Summary

A **communicator** is a **named, fixed group of processes** that are allowed to
exchange messages with one another, together with an addressing scheme that gives
each member a **rank** — an integer `0, 1, …, n-1`. It is the "who" that any
communication acts over: a process never sends into the void, it sends *within a
communicator*. In MPI it is the `comm` argument that appears in every operation's
signature.

## Grounded explanation

Plain [[message-passing]] lets one process send a message to another, but to name
"another" you need a stable way to refer to processes and to know which ones form
a group. A communicator supplies exactly that:

1. **Membership** — it fixes *which* processes belong to the group. Communication
   is only defined between members of the same communicator; it draws the boundary
   of the world a message can travel in.
2. **Ranks** — within the communicator each member is assigned a unique integer id
   (its **rank**), `0` to `n-1`. A sender names its target by rank ("send to rank
   2"), so ranks are the addresses that make [[message-passing]] concrete.
3. **Size** — the count `n` of members is known to everyone, so an operation can be
   defined over "all `n` ranks" without anyone enumerating them by hand.

This is what lets communication scale past pairs: because the group and its ranks
are named once, an operation can say "every rank in this communicator" and be
unambiguous. That named "everyone" is precisely what a collective acts on — the
`comm` argument is how a collective is told which group to run over.

`message-passing` is on the frontier; once archived, this node closes against it
down to the parallel-process floor.

## Prerequisites

- [[message-passing]]

## Sources

_none_
