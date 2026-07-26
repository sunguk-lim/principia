---
id: mvcc
title: Multi-Version Concurrency Control
summary: MVCC is the multi-version member of concurrency control's optimistic family (PostgreSQL's signature scheme) — an UPDATE never overwrites a row in place but writes a NEW version while keeping the old, each version stamped with the id of the transaction that created it (xmin) and the one that superseded it (xmax); a transaction reads against a snapshot of who-had-committed-at-its-start and a version is visible iff its xmin is committed-and-in-snapshot and its xmax is empty-or-not-in-snapshot, so readers never block writers and writers never block readers — delivering snapshot/repeatable-read isolation without read locks, at the cost of dead tuples that a background vacuum must reclaim.
type: concept
tags: [databases/transactions]
prereqs: [concurrency-control, transaction-isolation]
sources:
  - "https://www.postgresql.org/docs/current/mvcc.html — PostgreSQL: Concurrency Control (MVCC)"
  - "Bernstein & Goodman, \"Multiversion Concurrency Control — Theory and Algorithms\" (ACM TODS, 1983)"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Multi-Version Concurrency Control

## Summary

**MVCC** is the **multi-version** member of [[concurrency-control]]'s **optimistic
family** — the scheme PostgreSQL is built on. Its one defining idea is that an
`UPDATE` **never overwrites a row in place**: it writes a **new version** of the
row and leaves the **old version intact**. Each row version carries two
transaction-id stamps — **`xmin`**, the id of the transaction that **created** this
version, and **`xmax`**, the id of the transaction that **deleted or superseded**
it (empty while the version is still live). Every transaction runs against a
**snapshot** — the set of transactions that had **committed as of the moment it
began** — and a version is **visible** to that transaction *iff* its `xmin` is
**committed-and-in-snapshot** *and* its `xmax` is **empty-or-not-in-snapshot**. The
payoff is the whole reason the scheme exists: because a reader keeps seeing the old
version while a writer concurrently creates the new one, **readers never block
writers and writers never block readers** — which is exactly how MVCC delivers the
snapshot / repeatable-read isolation that [[transaction-isolation]] defined,
**without the read locks** [[concurrency-control]]'s pessimistic family would need.
The cost is **bookkeeping**: every superseded version becomes a **dead tuple** that
accumulates as bloat until a background process (**vacuum**) reclaims it, and
write-write conflicts still need a first-updater-wins abort.

## Grounded explanation

### What the concept *is* — versioning instead of overwriting

[[concurrency-control]] laid out two families for running many transactions at once
while keeping the result serial-equivalent. The **pessimistic / locking** family
makes conflicting transactions **wait** — its shared/exclusive lock rules mean an
exclusive (write) lock conflicts with a shared (read) lock, so **a reader can block
a writer and a writer can block a reader.** The **optimistic / multi-version**
family refuses that waiting; **MVCC is its version-keeping branch**, and it is what
[[concurrency-control]] deferred to this node by name. MVCC's spine is a single
structural decision about how a write is stored:

> An `UPDATE` does **not** overwrite the row's bytes in place. It appends a **new
> version** of the row and **leaves the old version sitting in the table**. A
> `DELETE` likewise does not erase the row — it just marks the existing version as
> deleted. So at any instant a single logical row may exist as **several physical
> versions**, and "the current value" is whichever version a given transaction is
> entitled to see.

This is the concept itself — not snapshots, not locks, but **keeping old versions
alive so a write never destroys what a concurrent reader is looking at.** Everything
else (the stamps, the snapshot test, the payoff, the cost) follows from this one
move.

### The two stamps — `xmin` and `xmax`

If multiple versions of a row coexist, each version must carry enough information to
decide *which transactions may see it*. MVCC attaches **two transaction-id stamps**
to every row version (a transaction id is a monotonically increasing integer handed
out when a transaction starts):

- **`xmin`** — the id of the transaction that **created** this version (the
  `INSERT` or `UPDATE` that wrote it). It answers *"since when does this version
  exist?"*
- **`xmax`** — the id of the transaction that **superseded or deleted** this version
  (the later `UPDATE` that replaced it, or the `DELETE` that removed it). It is
  **empty** while the version is still the live one, and answers *"until when did
  this version exist?"*

An `UPDATE` therefore touches **two versions at once**: it **sets the old version's
`xmax`** to its own id (marking *"I ended this one"*) and **writes a new version
with `xmin`** = its own id (marking *"I began this one"*). A version's life is thus
the half-open interval `[xmin, xmax)` measured in transaction ids.

### The visibility test — reading against a snapshot

A transaction must not simply read "the newest version," because a newer version may
belong to a transaction that started *after* it, or that has not committed. So when
a transaction begins it takes a **snapshot**: the set of transactions that had
**already committed** at that instant. Reading a row then means scanning that row's
versions and applying one rule to each:

> A version is **visible** to transaction `T` **iff**
> 1. its **`xmin` is committed and in `T`'s snapshot** — the version was created by a
>    transaction that finished before `T` started (so the version genuinely exists
>    for `T`); **and**
> 2. its **`xmax` is empty, or not in `T`'s snapshot** — nobody had yet committed a
>    deletion/supersession of this version as of `T`'s start (so the version is still
>    current *from `T`'s point of view*).

Condition (1) hides versions written by transactions that are still in flight or
started later; condition (2) keeps showing a version even after a *concurrent* writer
has stamped its `xmax`, as long as that writer had not committed when `T` began.
Together they pick out **exactly one** version of each row for `T` — a single
**consistent snapshot** of the whole database frozen at `T`'s start.

### The why — readers don't block writers, and that *is* the isolation

Now the payoff, which is the central reason to pay MVCC's bookkeeping cost. Because
a writer **creates a new version rather than mutating the one a reader holds**, the
reader's chosen version is **never disturbed**. A reader therefore needs **no lock**
and **never waits** for a writer; symmetrically a writer is never stalled by a
reader. This is the property [[concurrency-control]] named — **readers don't block
writers, writers don't block readers** — and it is precisely the gap left by the
locking family, where an exclusive lock would have stalled the reader.

And it lands exactly on [[transaction-isolation]]'s ladder for free. That node
defined the **non-repeatable read** (a row you read twice changes underneath you) and
showed that **Repeatable Read** forbids it by promising any row you have read keeps
its first-read value for your whole transaction. MVCC's snapshot **is** that promise,
mechanized: `T` reads from a snapshot fixed at its start, so a re-read of any row
re-applies the *same* visibility test against the *same* snapshot and returns the
*same* version — the second read cannot drift. Where [[transaction-isolation]] left
the enforcement mechanism as deliberately-unspecified prose ("a consistent snapshot
fixed at its start, or a read lock"), MVCC supplies the *snapshot* half concretely,
**without any read lock at all.**

### The cost — dead tuples and vacuum

Keeping old versions alive is not free. Once **no live snapshot can still see** a
superseded version — every transaction old enough to have it in-snapshot has
finished — that version is a **dead tuple**: occupying table and index space, slowing
scans, but visible to no one. Dead tuples **accumulate** (this is called **bloat**),
so MVCC requires a **background reclaimer** — PostgreSQL's **vacuum** — that walks the
table, finds versions older than the oldest live snapshot, and frees their space for
reuse. This is the "**bookkeeping**" side of the trade [[concurrency-control]] framed
as *waiting vs. bookkeeping*: locking pays in stalls and deadlocks; MVCC pays in extra
versions plus the housekeeping to collect them. One thing MVCC does **not** get for
free is the **write-write** conflict: two transactions updating the *same* row both
try to stamp the same version's `xmax`, and that genuinely conflicts. MVCC resolves it
**first-updater-wins** — the first updater proceeds; the second blocks on that row
until the first commits or aborts, then either **aborts** (under snapshot/repeatable-read
it sees the row changed under it) or re-evaluates. Reads scale beautifully; concurrent
writers to one row still serialize.

### Worked instance — one account row, three transactions

Take a single logical row in table `accounts`: `(id = 1, balance = 100)`. It was
created by some past transaction, so it exists as one version:

```
version  balance  xmin  xmax      meaning
v1        100      10    (empty)   created by txn 10; still live (no xmax)
```

Now transaction **T20** runs `UPDATE accounts SET balance = 150 WHERE id = 1`. Per
the versioning rule it does **not** overwrite v1; it appends **v2** and stamps v1's
`xmax`:

```
version  balance  xmin  xmax      meaning
v1        100      10    20        T20 ended this version (xmax := 20)
v2        150      20    (empty)   T20 created this version (xmin := 20); now live
```

**The concurrent reader, mid-write.** A reader transaction **T15** is already
running; its **snapshot was taken before T20 committed**, so T20 (id 20) is **not in
T15's snapshot** (and T20 hasn't committed anyway). T15 reads row `id=1`, scanning its
versions and applying the visibility test with these exact numbers:

- **v2** — `xmin = 20`. Condition (1) asks: is 20 committed-and-in-T15's-snapshot?
  **No** — 20 is not in the snapshot. → **v2 is INVISIBLE to T15.**
- **v1** — `xmin = 10`: is 10 committed-and-in-snapshot? **Yes** (txn 10 finished long
  ago). Condition (1) passes. Now condition (2): is `xmax = 20` empty-or-not-in-snapshot?
  20 is **not in T15's snapshot** (T20 hadn't committed at T15's start) → condition (2)
  passes. → **v1 is VISIBLE to T15.**

So **T15 reads `balance = 100`** — the old value — **with no lock and no wait**, while
T20 is still mid-write creating v2. This is the readers-don't-block-writers payoff in
literal numbers: under the locking family T20's exclusive lock would have **stalled**
T15; here T15 sails through on v1.

**After T20 commits.** Now a fresh transaction **T25** begins; its snapshot is taken
*after* T20 committed, so **20 is in T25's snapshot**. T25 reads row `id=1`:

- **v2** — `xmin = 20`: committed-and-in-snapshot? **Yes** → condition (1) passes.
  `xmax` empty? **Yes** → condition (2) passes. → **v2 is VISIBLE.** T25 reads
  **`balance = 150`.**
- **v1** — `xmax = 20`, and 20 **is** in T25's snapshot → condition (2) **fails** →
  **v1 is INVISIBLE** to T25.

T25 correctly sees the new value `150`. And v1 is now reachable by **no live snapshot**
(T15 has finished; every newer transaction has 20 in-snapshot and so skips v1): v1 is a
**dead tuple**, taking up space until **vacuum** reclaims it.

**Coordinating the levels of this one example.** The **structure** is the chain of
versions of row `id=1` — v1 then v2, each a `(balance, xmin, xmax)` triple. The
**algorithm** is the visibility test run per version against each transaction's
snapshot — the `xmin`/`xmax` checks worked above for T15 and T25. The **substrate** is
the table itself, where both versions physically coexist as rows on disk/in the page
cache and where vacuum eventually frees the dead v1 — exactly the "bookkeeping" the
trade-off is paid in.

## Prerequisites

- [[concurrency-control]] — MVCC is the **multi-version branch of its optimistic
  family**; this node inherits the framing (serializability, the
  waiting-vs-bookkeeping trade, the "readers don't block writers" property the
  versioning approach uniquely delivers) and fills in the scheme
  [[concurrency-control]] named but deferred. The cost side (dead tuples, write-write
  first-updater-wins abort) is the bookkeeping that node priced.
- [[transaction-isolation]] — MVCC **implements** snapshot-based isolation: its
  per-transaction snapshot is the concrete mechanism that forbids the
  **non-repeatable read** and delivers the **Repeatable Read** guarantee that node
  defined, supplying the "consistent snapshot fixed at its start" that
  [[transaction-isolation]] left as deliberately-unspecified enforcement detail.

## Sources

- PostgreSQL Documentation — *Concurrency Control (MVCC)* — https://www.postgresql.org/docs/current/mvcc.html
- Philip A. Bernstein & Nathan Goodman, *Multiversion Concurrency Control — Theory and Algorithms*, ACM Transactions on Database Systems 8(4), 1983 — the formal model of multiversion schedules, snapshots, and version visibility.
