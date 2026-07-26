---
id: leader-election
title: Leader Election
summary: "The protocol by which a group of replicas agrees on a single new primary after the current one fails — a candidate solicits votes and wins only with a majority (quorum), and because any two majorities of the same group must share a member, at most one leader can win a given term, making failover automatic instead of a human paging exercise."
type: concept
tags: [databases/distributed]
prereqs: [replication]
sources:
  - "D. Ongaro, J. Ousterhout, 'In Search of an Understandable Consensus Algorithm (Raft)', USENIX ATC 2014 — leader election via terms and majority votes"
  - "https://www.mongodb.com/docs/manual/core/replica-set-elections/ — MongoDB Manual: Replica Set Elections"
status: explained
created: 2026-07-03
updated: 2026-07-03
---

# Leader Election

## Summary

Leader-based [[replication]] hinges on there being **exactly one primary**:
one node sequences all writes, and that single sequence is what keeps replicas
identical. So the moment the primary's machine dies, the system faces a
question it must answer *by itself*: **who is the new primary?**
**Leader election** is the protocol that answers it. The remaining replicas
detect the leader's silence, one or more stand as **candidates**, and each
solicits votes from the group; a candidate becomes primary only by collecting
a **majority** of votes (a **quorum**). Majorities are the load-bearing trick:
any two majorities of the same group must **overlap in at least one member**,
and since each member casts one vote per election round, two candidates can
never both reach a majority in the same round — so *at most one* leader can
win, even though no central referee exists. Rounds are numbered by a **term**
that increases with each election, letting every node distinguish the current
leader from a stale one. The result is that failover — detect, vote, promote,
resume — happens in seconds, automatically.

## Grounded explanation

### The problem: replacing the single writer, safely

[[replication]] deliberately funnels all writes through one primary — that is
what manufactures the single write order. The design's weak point is the
primary itself: when it dies, writes stop until *something* appoints a new
one. Waiting for a human defeats the availability that replication exists to
provide. But the naive automatic rule — "whoever notices first takes over" —
is worse than the outage: on a network hiccup, two replicas may *each*
conclude the primary is dead and *both* take over. Two simultaneous primaries
(**split-brain**) each accept writes and append to their own log, producing
two divergent write orders — precisely the disaster the single leader existed
to prevent. So the protocol must guarantee **at most one winner**, using
nothing but messages among the surviving replicas.

### The mechanism: terms, votes, majority

- **Detection.** Every replica expects periodic heartbeats from the primary.
  A replica that hears nothing for a timeout concludes the primary may be
  dead. (It can never *know* — a slow network looks identical to a dead
  machine — which is exactly why the next steps must tolerate false alarms.)
- **Candidacy and terms.** The detecting replica increments the **term**
  number — election rounds are numbered 1, 2, 3, … — votes for itself, and
  asks every member for a vote in that term.
- **One vote per member per term.** Each member grants at most one vote in a
  given term, typically to the first reasonable candidate that asks. ("Reasonable"
  matters in log-replicating systems: a member refuses a candidate whose
  [[replication]] log is *behind* its own, so a stale replica cannot win and
  silently discard acknowledged writes.)
- **Majority wins.** A candidate that collects votes from a **majority** of
  the full membership — at least ⌊N/2⌋+1 of N — becomes primary for that
  term and resumes accepting writes and appending log entries.

**Why a majority — the two-line quorum argument.** Take any two majorities of
the same N members. Each has at least ⌊N/2⌋+1 members, so together they count
at least N+2 > N members — impossible unless they **share at least one
member**. That shared member cast at most one vote this term, so it cannot
have voted for both candidates; hence two candidates cannot both assemble a
majority, and **at most one leader per term** holds unconditionally — no
referee, no shared storage, just counting. The same intersection argument is
why a majority is the smallest safe quorum: with exactly half (or any less),
two disjoint "winning" groups can form, and split-brain returns.

### Worked instance — a 5-member replica set loses its primary

Members **A B C D E**; **A** is primary in **term 7**; all replicate A's log.

1. **A's machine dies.** B–E stop receiving heartbeats. B's timeout fires
   first; C's fires a moment later (timeouts are randomized precisely so that
   *usually* one candidate starts first, but suppose both stand).
2. **B and C both start an election in term 8**, each voting for itself.
   B solicits D and E; C solicits D and E too. D votes B (first to ask it);
   E votes B; by the one-vote-per-term rule neither can also vote C.
3. **Count:** B has {B, D, E} = 3 of 5 — a majority (⌊5/2⌋+1 = 3). C has only
   {C} and cannot reach 3: the members B's majority absorbed are barred from
   voting again, the overlap argument in action. **B is the sole primary of
   term 8** and resumes the write stream at the next log entry.
4. **A's machine reboots** believing it is primary — of term 7. The first
   message stamped *term 8* it receives tells it a newer election has
   happened; it steps down to follower and catches up on B's log by ordinary
   [[replication]] replay. Total unavailability: the detection timeout plus
   one voting round — seconds, no human involved.

Note what did **not** need to happen: nobody consulted a central authority,
and the false-alarm case (A was merely slow, not dead) is handled by the same
term mechanism that handled its real death.

## Prerequisites

- [[replication]] — the setting that creates the problem and the material the
  protocol works with: leader-based replication needs exactly one primary
  sequencing one log, so a dead primary must be replaced — and candidates are
  judged partly by how up-to-date their replicated log is.

## Sources

- D. Ongaro, J. Ousterhout, "In Search of an Understandable Consensus Algorithm (Raft)", USENIX ATC 2014 — terms, randomized timeouts, one-vote-per-term, majority election (the design this node's mechanism follows).
- MongoDB Manual, "Replica Set Elections" — https://www.mongodb.com/docs/manual/core/replica-set-elections/ (the same protocol as deployed in MongoDB replica sets: heartbeats, priority, majority votes).
