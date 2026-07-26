---
id: replication
title: Replication
summary: "Keeping full copies of the same data on multiple machines so the system survives a machine failure and can serve more reads — in the dominant leader-based form all writes go to one primary, which appends each change to a replication log that follower replicas replay in order, so every replica converges on the same state by the same replay-a-log mechanism a write-ahead log uses to recover from a crash."
type: concept
tags: [databases/distributed]
prereqs: [write-ahead-logging]
sources:
  - "M. Kleppmann, Designing Data-Intensive Applications (O'Reilly, 2017), ch. 5 — Replication"
  - "https://www.mongodb.com/docs/manual/replication/ — MongoDB Manual: Replication"
status: explained
created: 2026-07-03
updated: 2026-07-03
---

# Replication

## Summary

**Replication** keeps a full copy of the same data on several machines
(**replicas**). It exists for two reasons: **availability** — one machine can
die, burn, or reboot and the data is still served — and **read scaling** —
reads can be answered by any replica, multiplying read throughput without
touching the data model. The hard part is not copying data once; it is keeping
the copies *identical while the data keeps changing*. The dominant answer is
**leader-based replication**: exactly one replica (the **primary**, or leader)
accepts writes; it records each change as an entry in an ordered **replication
log**; the other replicas (**followers**, or secondaries) pull that log and
replay the entries *in the same order*. Because each follower applies the same
changes in the same order to the same starting state, every replica converges
on the same data — the same replay-a-log-to-rebuild-state idea that
[[write-ahead-logging]] uses to recover one machine from a crash, generalized
so that *another machine* replays the log too.

## Grounded explanation

### The problem: identical copies of changing data

A static file is trivial to replicate — copy it once. A database is not
static: writes keep arriving, and the copies must stay identical *under a
stream of changes*. Order is the whole difficulty. Suppose `x = 3` everywhere
and two writes are issued concurrently: "set x = 5" and "increment x". A
replica that applies *set, then increment* ends at `6`; a replica that applies
*increment, then set* ends at `5`. Same two writes, different order,
**diverged replicas** — and no machine failed. So the core requirement is a
single agreed **order of writes** that every replica applies.

### Leader-based replication: one writer, one log

Leader-based replication manufactures that single order by construction:

1. **One leader.** All writes go to a single designated replica, the
   **primary**. One node sequences every write, so a total order exists
   trivially — the order the primary applied them.
2. **A replication log.** As the primary applies each write, it appends a
   record of the change to an ordered log — entry #1, #2, #3, … Each entry
   says what changed, exactly as a [[write-ahead-logging]] record does
   ("row r: 500 → 400"). The log *is* the write order, made durable and
   shippable.
3. **Followers replay.** Each follower keeps a cursor into that log ("applied
   up to entry #N"), pulls entries it hasn't seen, and applies them in log
   order. Determinism does the rest: same start state + same entries in the
   same order ⇒ same end state.

The kinship with [[write-ahead-logging]] is exact and worth spelling out. A
WAL makes one machine's state reconstructible: after a crash, replay the log
against the last-flushed state and you re-derive the lost updates. Replication
points the *same log* at a *different machine*: a follower is, permanently,
what a crashed node is momentarily — a machine rebuilding state by replaying
an ordered change log. A follower that was offline for an hour is not a
special case; it re-joins, says "I'm at entry #4,000", and replays forward
until it catches up.

### Synchronous or asynchronous — the one knob

When may the primary acknowledge a write to the client?

- **Asynchronously:** as soon as the write is applied (and logged) locally;
  followers replay later. Fast — the client never waits on the network — but
  if the primary dies *after* acking and *before* any follower pulled that
  entry, the acknowledged write is **lost** on failover.
- **Synchronously (to some):** only after at least one follower — in
  practice, a **majority** of replicas — holds the log entry. The write now
  survives the primary's death (an acked copy exists elsewhere), at the cost
  of one network round-trip per write.

Real systems expose the knob per write (MongoDB calls it the *write concern*:
`w:1` is asynchronous, `w:"majority"` is synchronous-to-a-majority). It trades
latency against durability-under-failover; choosing it per write is routine.

### Worked instance — three replicas, one write, one failure

A replica set has three members: primary **P**, followers **F1** and **F2**.
All hold `x = 3` and have applied the log through entry **#41**.

1. A client writes `x = 5` to **P** with a majority write concern. P applies
   it, appends **entry #42: "set x = 5"** to its replication log, and waits.
2. **F1** pulls entry #42, applies it (`x` becomes 5), and reports its cursor
   is at #42. Two of three replicas — a majority — now hold the entry, so P
   acknowledges the client. **F2** is momentarily behind (cursor #41,
   `x = 3`): replicas *converge*; they are not in lockstep.
3. **F2** pulls #42 a moment later and catches up. All three replicas hold
   `x = 5` — the log made them identical without any replica ever comparing
   full states.
4. Now **P's machine dies.** Nothing acknowledged is lost: F1 holds entry
   #42. The surviving members promote one of themselves to primary (*how*
   they choose — votes, terms, majorities — is its own concept: leader
   election), the new primary continues appending at entry #43, and when P's
   machine returns it re-joins as a follower and replays forward from its
   cursor — the same catch-up walk F2 did in step 3.

Each piece earns its keep in the trace: the **single leader** gave the order,
the **log** carried it, **replay** converged F2 with no special repair path,
and the **majority ack** in step 2 is exactly why step 4 lost nothing.

## Prerequisites

- [[write-ahead-logging]] — the mechanism replication generalizes: an ordered
  log of changes, appended before acknowledgment and replayed to reconstruct
  state — used by a WAL to recover one machine after a crash, and by
  replication to make *other machines* converge on the same state.

## Sources

- M. Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), ch. 5 "Replication" — leader-based replication, replication logs, sync vs. async, failover hazards.
- MongoDB Manual, "Replication" — https://www.mongodb.com/docs/manual/replication/ (replica sets, the oplog as the replication log, write concern as the sync/async knob).
