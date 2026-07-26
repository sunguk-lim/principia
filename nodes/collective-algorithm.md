---
id: collective-algorithm
title: Collective Algorithm (Ring vs Tree)
summary: A single collective-operation — say, "broadcast this array from one process to all the others" — names what must happen to the data, but it does not say how the underlying…
type: concept
tags: [parallel-computing]
prereqs: [collective-operation]
sources: []
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Collective Algorithm (Ring vs Tree)

## Summary

A single [[collective-operation]] — say, "broadcast this array from one process to
all the others" — names *what* must happen to the data, but it does **not** say
*how* the underlying one-to-one messages are wired together to make it happen. A
**collective algorithm** is one such wiring: a concrete schedule of point-to-point
sends and receives that realizes the operation. The same logical broadcast can be
built as a slow sequential **chain**, as a latency-cheap **tree**, or as a
bandwidth-cheap **ring** — and these cost very differently. Because the right
choice depends on how big the message is, a good library does not commit to one
algorithm; it picks per call. This node is about that choice and why it matters.

## Grounded explanation

Recall that a [[collective-operation]] involves a group of `n` processes, numbered
`0, 1, … , n-1`, and is itself nothing but many ordinary one-to-one messages
arranged in a pattern. The operation fixes the *goal* (e.g. every process ends up
holding the same array); it leaves the *pattern* open. A **collective algorithm**
fixes that pattern. We measure an algorithm two ways at once.

First, its **steps** (also called *rounds*): a step is one batch of sends that all
happen at the same time, so the next batch cannot begin until this one lands. Fewer
steps means the operation finishes after fewer back-and-forth delays.

Second, the **data each process must push**: even if two algorithms take the same
number of steps, one may force a single process to send the whole array many times
(so the wire out of that one process is the bottleneck), while another spreads the
sending evenly so every link carries roughly an equal, small share.

These two costs are captured by a simple **cost model**:

> time ≈ α · (number of steps) + β · (bytes sent per step)

Here **α** (alpha) is the **latency** — a fixed start-up delay paid *once per
message* no matter how small, the cost of "reaching out" at all. **β** (beta) is
the **per-byte time** — the inverse of **bandwidth**, the cost of actually pushing
each byte down the wire. The two terms pull in opposite directions: cutting steps
shrinks the `α` term; spreading bytes thinly and keeping every link busy shrinks
the `β` term. No single algorithm minimizes both, so the best one depends on which
term dominates — and that, in turn, depends on message size.

**Chain (sequential).** The simplest wiring: the source process sends to peer 1,
then to peer 2, then to peer 3, and so on, one after another. With `n` processes
this is `n-1` sends done in sequence, so it takes about `n` steps — the `α` term
grows with the group. It is easy to reason about but slow, because every other
process waits idle while the source dribbles the data out one peer at a time. The
chain is the baseline the other two algorithms beat.

**Tree (recursive doubling).** The key idea: a peer that has *already received* the
data can help hand it onward, instead of leaving all the work to the source. The
set of processes that hold the data **doubles every step**. So in step 1 the source
sends to one peer (2 processes now hold it); in step 2 those 2 each send to a fresh
peer (4 hold it); in step 3 those 4 each send (8 hold it). After `k` steps, `2^k`
processes are covered, so reaching `n` processes takes only about `log₂ n` steps.
This is **latency-optimal**: it spends the fewest possible rounds, so it minimizes
the `α · steps` term. Its weakness is the `β` term — near the end, many processes
are each shipping a full-size message in the same step, so the algorithm is
demanding on bandwidth right when the most data is in flight.

**Ring.** Arrange the processes in a circle: each process has one *successor* (the
neighbor it sends to) and one *predecessor* (the neighbor it receives from). Data
flows around the circle one hop at a time, so completing a lap also takes about `n`
steps — no better than the chain on the `α` term. But here is the payoff: because
every process is sending to its successor *at the same time* as it receives from
its predecessor, **every link in the ring is busy in every step**. The total
sending is shared evenly — over the whole operation each process sends only about
one message's worth of data — so no single wire is the bottleneck. The ring is
therefore **bandwidth-optimal**: it minimizes the `β` term and the congestion that
comes from one process trying to push everything.

**The trade-off, and why libraries choose per message size.** Put the two
extremes side by side through the cost model:

- A **small** message makes the `β · bytes` term tiny; almost all the time is the
  `α · steps` start-up cost. So you want the **fewest steps** → use the **tree**
  (`log₂ n` rounds instead of `n`).
- A **large** message makes the `β · bytes` term dominate; the start-up cost is
  negligible by comparison. So you want to **avoid any single link being a
  bottleneck** and keep all wires full → use the **ring**.

This is exactly why a mature message-passing library does not hard-code one
algorithm: it looks at the byte count of each [[collective-operation]] call and
switches between tree-style and ring-style wiring on the fly. The *operation* the
programmer wrote is unchanged; only the hidden schedule of sends differs.

**Worked instance — broadcast to 8 processes (`n = 8`).** The goal: the array held
by process 0 must end up on all of 0–7.

- *Chain:* process 0 sends to 1, then 2, then 3, …, then 7. That is `7` sequential
  sends → about `7` steps. Slow, and process 0's outgoing link does all the work.
- *Binomial tree:* `⌈log₂ 8⌉ = 3` steps, the set of holders doubling each round:
  - **Round 1:** `0 → 4`. Holders: {0, 4} (2 of them).
  - **Round 2:** `0 → 2`, `4 → 6`. Holders: {0, 2, 4, 6} (4 of them).
  - **Round 3:** `0 → 1`, `2 → 3`, `4 → 5`, `6 → 7`. Holders: all 8.

  Three rounds instead of seven — the `log₂` saving is real and grows with `n`.
  Note round 3 fires four sends at once, each carrying the full array: that
  simultaneous load is the bandwidth pressure the tree trades latency for. This is
  the algorithm to use for a *small* broadcast.
- *Ring (for the bandwidth-bound case):* if instead the array were huge — picture a
  combine-and-share operation where every process contributes a big chunk and all
  must end up with the combined result — you would lay the 8 processes in a circle
  `0 → 1 → 2 → … → 7 → 0` and pass chunks hop-by-hop around it. It still takes on
  the order of `n` steps, but with all 8 links carrying a chunk in every step the
  bandwidth is used to the full and no process's wire is the lone bottleneck.

The two extremes — `3` steps with heavy per-step load (tree) versus `~8` steps with
perfectly balanced load (ring) — are the two ends of the same cost model, selected
by which of `α` and `β` dominates for the message at hand.

## Prerequisites

- [[collective-operation]]

## Sources

_none_
