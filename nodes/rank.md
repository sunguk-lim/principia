---
id: rank
title: Rank
summary: A rank is the integer id that a communicator assigns to each of its member processes — 0, 1, …, n-1 for a group of n.
type: concept
tags: [parallel-computing]
prereqs: [communicator]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Rank

## Summary

A **rank** is the **integer id** that a [[communicator]] assigns to each of its
member processes — `0, 1, …, n-1` for a group of `n`. It is how a process is
*addressed*: within the communicator, "rank 2" unambiguously names one specific
process. A process can also ask "what is my rank?" to find out which member of the
group it is.

## Grounded explanation

A [[communicator]] fixes a group of processes and numbers them. That number is the
rank, and it does two jobs:

1. **It is an address.** To send to a particular process you name its rank; to
   single one out (e.g. as a root) you give its rank. Ranks turn an abstract "the
   other process" into a concrete target.
2. **It is an identity.** Because every member runs the *same* program, a process
   uses its own rank to decide what to do — "if my rank is 0, I am the source;
   otherwise I am a receiver." The rank is how otherwise-identical processes
   specialise their behaviour.

Ranks are only meaningful **relative to a [[communicator]]**: the same physical
process can have different ranks in different communicators. Within one, the ranks
`0 … n-1` are exactly the set "all processes," which is what lets a collective act
on the whole group by referring to every rank.

This node closes against [[communicator]] → message-passing → parallel-process, so
no part of it is left unexplained.

## Prerequisites

- [[communicator]]

## Sources

_none_
