---
id: concurrency-control
title: Concurrency Control
summary: Concurrency control is the protocol layer that lets many [[transaction]]s run at once yet produces a result equivalent to SOME serial order (serializability), lifting [[atomic-operation]]'s single-cell lost-update guarantee to whole multi-row transactions; its two families are pessimistic locking (two-phase locking — acquire shared/exclusive row locks, hold to commit, make conflictors wait, risk deadlock and abort a victim) and optimistic/multi-version (proceed without blocking and detect conflicts at commit, or keep multiple row versions so readers never block writers — MVCC), trading waiting for bookkeeping.
type: concept
tags: [databases/transactions]
prereqs: [transaction, atomic-operation]
sources:
  - "Bernstein, Hadzilacos & Goodman, Concurrency Control and Recovery in Database Systems (1987) — serializability, two-phase locking, multiversion concurrency control"
  - "Gray & Reuter, Transaction Processing: Concepts and Techniques (1993) — locking, deadlock detection, isolation"
  - "https://www.postgresql.org/docs/current/mvcc.html — PostgreSQL: Concurrency Control (MVCC)"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Concurrency Control

## Summary

**Concurrency control** is the set of mechanisms a database uses to run **many
[[transaction]]s at the same time** while guaranteeing the outcome is the same as
if they had run **one after another in some order** — a property called
**serializability**. The prerequisite [[atomic-operation]] node solved the
lost-update race for **one memory cell** with a single hardware-indivisible
read-modify-write; a transaction, however, touches **many rows across many
statements**, so no single hardware atomic can cover it. Concurrency control is
the **protocol** that supplies the missing indivisibility at that coarser grain.
It comes in two families. **Pessimistic / locking** — chiefly **two-phase locking
(2PL)** — has each transaction take a **shared (read)** or **exclusive (write)**
lock on every row it touches and **hold those locks until it commits**; a
transaction that wants a conflicting lock must **wait**. Waiting can form a cycle
(T1 waits for T2 while T2 waits for T1) — a **deadlock** — which the database
breaks by **aborting one transaction as a victim**. **Optimistic / multi-version**
instead lets transactions **proceed without blocking** and either **checks for
conflicts at commit time** (aborting a loser) or keeps **multiple versions of each
row** so a reader always sees a consistent old snapshot and **never blocks a
writer** — this version-keeping approach is **MVCC**. The central trade: locking
serializes by making conflicting transactions **wait** (a reader can block a
writer); versioning avoids that wait at the cost of **bookkeeping** — extra row
versions and conflict checks.

## Grounded explanation

### What the concept *is* — supplying indivisibility for a whole transaction

The [[atomic-operation]] node established indivisibility at the **smallest** scale:
a read-modify-write on **one memory location** that hardware refuses to let another
thread interrupt. The lost-update race it cured was two threads both reading `5`,
both adding `1`, both writing `6` — one increment vanishing in the gap between a
read and its write — and the cure was to **fuse** read, modify and write into one
uninterruptible event so nobody could slip into the gap.

The [[transaction]] node then lifted *all-or-nothing* from one cell to a whole
**sequence of statements**: a transaction either `COMMIT`s every write or
`ROLLBACK`s them all. But that node deliberately left one ACID letter for later —
**Isolation**, the question of what *concurrent* transactions may see of each
other's not-yet-committed work. **Concurrency control is the machinery that
delivers Isolation.** And here is the catch that forces a new mechanism: a hardware
atomic protects exactly **one address**. A transaction reads and writes **many
rows over many statements**, with think-time and round-trips in between, so you
**cannot** wrap it in a single hardware atomic. You need a **protocol** layered over
the rows — a set of rules every transaction follows — that makes the *whole
multi-row sequence* behave as if it had the cell-level indivisibility, even though
it is physically spread out in time and space.

That is the concept's spine: **concurrency control is the protocol that makes
concurrently-executing, multi-row transactions produce a correct, serial-equivalent
result.** It is the bridge from one indivisible cell up to one indivisible
transaction.

### The correctness target — serializability

What does "correct" mean when transactions overlap? The accepted definition is
**serializability**:

> An interleaved execution of a set of transactions is **serializable** if it
> produces the **same final database state and the same values returned to each
> transaction** as *some* execution in which the transactions ran **one at a time,
> with no overlap** (a **serial schedule**).

Two things to note. First, it is *some* serial order, **not a specific one** — if
running T1-then-T2 and running T2-then-T1 both leave the books valid, the system may
match either; it only must match **one** of them. Second, serializability is about
the **observable result**, not the physical schedule: the database is free to
interleave operations however it likes **internally**, as long as the result is
indistinguishable from *some* serial run. A schedule that is **not** serializable —
one whose result matches *no* serial order — is exactly where anomalies like the
lost update live. Serializability is therefore the multi-transaction analogue of
[[atomic-operation]]'s "no observable in-between state," now stated over **whole
transactions** instead of one cell.

### Family 1 — pessimistic / locking (two-phase locking)

The **pessimistic** stance assumes conflicts *will* happen, so it prevents them up
front by **locking** each row before touching it. Two lock modes encode the only
asymmetry that matters — reads commute with reads, but a write conflicts with
everything:

- a **shared (S) lock** — taken to **read** a row; many transactions may hold an S
  lock on the same row at once (concurrent reads are safe);
- an **exclusive (X) lock** — taken to **write** a row; it conflicts with **every**
  other lock on that row (no other S or X lock may coexist), so only one writer, and
  no reader, may proceed.

A request for a lock that **conflicts** with one already held makes the requester
**wait** until the holder releases it. Locking alone is not enough, though — *when*
you release matters. **Two-phase locking (2PL)** adds the rule that gives the family
its name and its guarantee: each transaction has a **growing phase** in which it
only **acquires** locks and a **shrinking phase** in which it only **releases** them
— **never a release before the last acquire**. In practice the shrinking phase is
deferred entirely to commit (this stricter form is **strict 2PL**): a transaction
**holds every lock until it COMMITs or ROLLBACKs**, then drops them all at once.

The **why**: the two-phase discipline is exactly what forces serializability. Once
T has released *any* lock it can never take a new one, so no transaction can
"reach back" and conflict with a row T already finished and unlocked while T is
still working elsewhere. The order in which transactions reach their **lock point**
(the moment they hold their last lock) is a valid serial order the execution
provably matches. Holding to commit additionally prevents a second transaction from
reading a value the first one wrote but then rolls back. So the protocol *waits its
way* into a serial-equivalent schedule.

The **cost** is the flip side of waiting. If T1 holds an X lock on row `a` and wants
one on row `b`, while T2 holds X on `b` and wants `a`, **each waits for the other
forever** — a **deadlock**, a *cycle* in the "who-waits-for-whom" graph. The
database cannot satisfy both, so it **detects the cycle** (or times a waiter out),
picks one transaction as the **victim**, and **aborts** it — rolling back its writes
and releasing its locks so the other can proceed; the victim is then retried. Note
the sharp consequence of the S/X rules: an X lock conflicts with an S lock, so under
locking **a reader can block a writer and a writer can block a reader.** That
blocking is precisely what the second family attacks.

### Family 2 — optimistic / multi-version (and MVCC)

The **optimistic** stance assumes conflicts are *rare*, so it refuses to pay for
locks up front and instead lets transactions **run without blocking**, dealing with
trouble only if it actually arises. Two shapes:

- **Optimistic concurrency control (validation).** A transaction reads freely and
  buffers its writes privately. At `COMMIT` it **validates**: did any row it read get
  changed by a transaction that committed in the meantime? If **no**, it installs its
  writes; if **yes**, the conflict means committing would violate serializability, so
  it **aborts and retries.** Conflicts are caught at the **end**, not prevented at the
  start.

- **Multi-version (MVCC).** Instead of overwriting a row in place, each write creates
  a **new version** of the row, tagged with the writing transaction, and **old
  versions are kept**. A reader is handed a **consistent snapshot** — the set of row
  versions that were committed as of the moment its transaction began — and reads from
  that snapshot. The decisive consequence: a reader **never needs a lock and never
  waits for a writer**, because the writer's new version doesn't disturb the old
  version the reader is looking at; **readers don't block writers and writers don't
  block readers.** (MVCC is the approach a separate node covers; named here in plain
  prose, not linked.)

The **central trade**, stated plainly: **locking** achieves serializability by
making conflicting transactions **wait** — simple and always-correct, but a reader
can stall a writer and deadlocks must be hunted and broken. **Versioning** removes
that waiting for the common read-vs-write case, but pays in **bookkeeping**:
multiple row versions consume space and must eventually be garbage-collected, and
write-vs-write conflicts still need detection and an abort. Waiting versus
bookkeeping is the axis the whole field turns on.

### Worked instance — two transactions selling the last seats

Take one row: a concert's `seats_left`, starting at the concrete value **`10`**.
Two transactions each sell **4** tickets with the same read-modify-write logic:

```
T:  r := READ seats_left ;  w := r − 4 ;  WRITE seats_left = w
```

The correct serial result is unambiguous — whichever runs first, the total sold is
`4 + 4 = 8`, so `seats_left` must end at **`10 − 8 = 2`**. Any concurrent schedule
that ends elsewhere is **not serializable**.

**(a) Uncontrolled — the lost update, now at row grain.** Let the two reads and
writes interleave:

```
T1: READ seats_left → 10
T2: READ seats_left → 10        (T1 hasn't written yet — T2 sees the stale 10)
T1: WRITE 10 − 4 = 6
T2: WRITE 10 − 4 = 6
```

`seats_left` ends at **`6`**, recording only **one** sale of 4. **Eight seats were
sold but four were charged against thin air** — the venue oversells by 4. This is
the **exact same lost-update race** as the two-threads-both-read-`5` story in
[[atomic-operation]], lifted from one memory cell to one database row touched by two
transactions: an update computed from a value that went stale in the gap between a
read and its write. The result `6` matches **neither** serial order (both give `2`),
so the schedule is **not serializable**.

**(b) 2PL serializes it.** Now both transactions obey two-phase locking. T1 needs to
write `seats_left`, so it requests an **exclusive (X) lock** and gets it. T2 then
requests an X lock on the **same** row — it **conflicts**, so T2 **waits**:

```
T1: X-lock seats_left (granted) ; READ → 10 ; WRITE 10 − 4 = 6 ; COMMIT ; release lock
T2: X-lock seats_left ........... blocked until T1 commits .................. (granted)
T2: READ → 6  (the value T1 committed, no longer stale) ; WRITE 6 − 4 = 2 ; COMMIT
```

T2's read now returns **`6`**, not `10`, because T1 held its X lock **to commit**, so
T2 could not slip into the gap. Final `seats_left = `**`2`** — exactly the serial
result, and the realized order (T1 before T2) is a valid serial order the execution
matches. Serializability achieved **by waiting**. (Had each transaction instead
locked a *different* row first and then reached for the other's, the two waits would
have formed a cycle — a **deadlock** — and the database would have aborted one as a
**victim** and retried it, still reaching `2`.)

**(c) How a versioned scheme handles it.** Under MVCC neither write overwrites the
other in place — each `WRITE` would create a new version of `seats_left`. The system
must still serialize the two **writers** (write-write on the same row is a genuine
conflict): one transaction commits its version `10 → 6`; the second, on validating
at commit, **sees that the row it read (`10`) was changed underneath it** and so
**aborts and retries**, re-reading the now-committed `6` and writing `6 − 4 = 2`. The
final value is again **`2`** — but it was reached by **detecting the conflict at
commit and retrying**, never by making either transaction block during its work. The
gain shows for *readers*: a third transaction merely *displaying* `seats_left` would
read its snapshot's version with **no lock and no wait**, where 2PL's X lock would
have stalled it.

**Coordinating the levels of this one example.** The **structure** is the
correctness target — a serializable schedule on the row `seats_left`, equivalent to
*some* serial order that lands on `2`. The **algorithm** is the protocol that
enforces it: 2PL's *acquire-conflicting-lock → wait → hold-to-commit*, or MVCC's
*read-a-snapshot → validate-at-commit → abort-and-retry on conflict*. The
**substrate** is the row and its locks/versions in the database's buffer — a single
X lock guarding one row in family 1, or a chain of timestamped row versions in
family 2 — which is exactly where "wait" versus "bookkeeping" is physically paid.

## Prerequisites

- [[transaction]] — concurrency control's unit of work *is* the transaction: it
  schedules and isolates whole multi-statement `COMMIT`/`ROLLBACK` units against one
  another, and the serializability target is defined over transactions. It also
  supplies the Isolation (the "I" of ACID) that [[transaction]] deferred — this node
  is the mechanism that delivers it.
- [[atomic-operation]] — the single-cell, hardware-indivisible read-modify-write and
  its lost-update race are the seed this node generalizes: because a transaction spans
  many rows and statements, one hardware atomic cannot cover it, so concurrency
  control supplies the same "no interleaving into the gap" guarantee by *protocol* at
  row/transaction grain. The worked lost-update is the identical race lifted up a
  level.

## Sources

- Philip A. Bernstein, Vassos Hadzilacos & Nathan Goodman, *Concurrency Control and Recovery in Database Systems* (Addison-Wesley, 1987) — serializability theory, two-phase locking, and multiversion concurrency control.
- Jim Gray & Andreas Reuter, *Transaction Processing: Concepts and Techniques* (Morgan Kaufmann, 1993) — locking modes, deadlock detection and victim selection, isolation.
- PostgreSQL Documentation — *Concurrency Control (MVCC)* — https://www.postgresql.org/docs/current/mvcc.html
