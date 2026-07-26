---
id: message-passing
title: Message passing
summary: Message passing is the communication model in which separate processes, each with its own private memory, share data only by explicitly sending and receiving messages.
type: concept
tags: [parallel-computing]
prereqs: [parallel-process]
sources: []
status: explained
created: 2026-06-19
updated: 2026-06-19
---

# Message passing

## Summary

**Message passing** is the communication model in which separate processes, each
with its **own private memory**, share data only by **explicitly sending and
receiving messages**. One process packages up some data and sends it; another must
post a matching receive to accept it. There is no shared variable they can both
read — moving data is always a deliberate, two-sided act.

## Grounded explanation

A [[parallel-process]] has private memory: no other process can reach into it and
read or write its variables. So if process A computes a value that process B needs,
the value cannot simply "appear" in B — it has to be **transmitted**. Message
passing is the discipline for doing that:

1. **Two sides, both explicit.** Communication is a *send* paired with a *receive*.
   A's `send(data → B)` only completes the transfer when B does a matching
   `receive(from A)`. Neither side can move the data alone; both must participate.
2. **Addressing a peer.** The sender names *who* it is sending to and the receiver
   names *who* it expects data from. (This naming is what a higher group structure
   later makes systematic.)
3. **Copy, not share.** The bytes are copied from A's private memory into B's
   private memory. After the exchange each still owns its own copy — consistent
   with the [[parallel-process]] rule that memory is never shared.

This is the foundation every richer pattern is built on: a group-wide operation is
ultimately just **many of these point-to-point send/receive exchanges** arranged in
some order. Message passing is the smallest unit of "processes talking", and the
axiom [[parallel-process]] is why that talking has to be explicit at all.

## Prerequisites

- [[parallel-process]]

## Sources

_none_
