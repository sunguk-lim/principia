---
id: postgresql
title: PostgreSQL
summary: PostgreSQL is an open-source relational database management system defined not by any one part but by how it composes them — tables under the [[relational-model]] queried in [[sql]], work grouped into ACID [[transaction]]s, concurrent isolation supplied by [[mvcc]] (its signature choice — readers never block writers) rather than by the read-locking branch of [[concurrency-control]], durability by [[write-ahead-logging]] (commit fsyncs the WAL, data pages flush lazily), data stored in heap tables reached through [[b-tree]] indexes, and each query turned into an execution plan by cost-based [[query-planning]].
type: concept
tags: [databases/relational-database]
prereqs: [relational-model, sql, transaction, mvcc, write-ahead-logging, b-tree, query-planning, concurrency-control]
sources:
  - "https://www.postgresql.org/docs/current/ — PostgreSQL documentation (overview)"
  - "https://www.postgresql.org/docs/current/tutorial-arch.html — PostgreSQL: Architectural Fundamentals"
  - "https://www.postgresql.org/docs/current/internals.html — PostgreSQL: Internals (storage, MVCC, WAL, planner)"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# PostgreSQL

## Summary

**PostgreSQL** is an open-source **relational database management system**
(RDBMS) — but the point of treating it as its own concept is not any single
subsystem, all of which already exist as the prerequisite nodes below. The point
is the **composition**: a specific, battle-tested set of choices that fit
together into one coherent production database. It stores data as tables under
the [[relational-model]] and is queried in [[sql]]. Work happens inside ACID
[[transaction]]s. Its **signature choice** is that isolation between concurrent
transactions is provided by [[mvcc]] — an `UPDATE` writes a *new* row version and
keeps the old one — rather than by the read-locking branch of
[[concurrency-control]], so in PostgreSQL **readers never block writers**; the
price is *dead tuples* that a background **VACUUM** must reclaim. Durability and
crash recovery come from [[write-ahead-logging]]: `COMMIT` forces the WAL to
stable storage with `fsync`, while the modified data pages are flushed **lazily**.
Data itself lives in **heap tables**, and access to it is sped by [[b-tree]]
indexes (PostgreSQL's default index type). Between the declarative query and the
heap sits a cost-based [[query-planning]] step that turns each [[sql]] statement
into an execution plan — sequential scan vs. [[b-tree]]-index scan, which join
method, which join order. None of these is novel to PostgreSQL; what is
PostgreSQL is *this particular bundle* — MVCC for isolation, WAL for durability,
heap + B-tree storage, a cost-based planner, a process-per-connection model, and
deep extensibility — assembled so the parts reinforce one another.

## Grounded explanation

### Why PostgreSQL is its own node and not just the sum of its parts

Each prerequisite below is a *general* concept that many databases share. The
[[relational-model]], [[sql]], ACID [[transaction]]s, [[mvcc]],
[[write-ahead-logging]], the [[b-tree]], and cost-based [[query-planning]] are
not PostgreSQL's inventions; they are the standard ingredients of a relational
engine. So what does a "PostgreSQL" node teach that those seven do not? **The
integration** — the specific, mutually-reinforcing set of choices that turns a
pile of mechanisms into one production system. A different RDBMS makes different
choices from the same menu (overwrite-in-place with undo logs and read locks
instead of MVCC, say), and is therefore a *different* composition. PostgreSQL is
*this* composition, and the value is in how the pieces lock together: MVCC's
"readers don't block writers" only pays off because the WAL already makes commits
cheap and durable; the planner's seq-scan-vs-index choice only matters because the
heap-plus-B-tree storage layout offers exactly those two access paths. Below, each
subsystem is given its role — linking the prerequisite that *defines* it — and
then one transaction is traced through all of them at once.

### The pieces, and the role each plays

- **Data model — [[relational-model]].** Data in PostgreSQL is a set of **tables**:
  each table is a relation, a set of typed, named-column tuples, with primary keys
  and foreign keys exactly as the [[relational-model]] defines. The values are
  *visible* (not opaque blobs), which is the whole precondition for everything
  else — you can filter, join, and index on any column.

- **Query language — [[sql]].** You talk to PostgreSQL **declaratively** in
  [[sql]]: you state *what* relation you want, never *how* to compute it. This is
  what hands the engine the freedom that [[query-planning]] then exploits.

- **Unit of work — [[transaction]].** Every statement runs inside an ACID
  [[transaction]] (a lone statement is an implicit one-statement transaction). The
  bundle is all-or-nothing: `COMMIT` makes every effect take hold, `ROLLBACK`/abort
  makes none of them. Atomicity, Consistency, and Durability come from this node;
  Isolation is delegated to the next two.

- **Isolation — [[mvcc]] (the signature choice).** [[concurrency-control]] lays out
  two families: pessimistic *locking* (readers and writers block each other through
  shared/exclusive row locks) and optimistic *multi-version*. PostgreSQL's defining
  decision is to take the multi-version branch — [[mvcc]]. An `UPDATE` does **not**
  overwrite the row in place; it writes a **new version** stamped with the
  transaction's id (in PostgreSQL the stamps are called **xmin**/**xmax**) and
  leaves the old version in the table. Each transaction reads against a **snapshot**
  fixed at its start, so it keeps seeing the version that was current then. The
  consequence — and the reason this is *the* PostgreSQL fact people quote — is that
  **readers never block writers and writers never block readers**: PostgreSQL pays
  none of the read-locking cost of [[concurrency-control]]'s pessimistic family for
  read/write conflicts. The cost it pays *instead* is **bookkeeping**: every
  superseded version is a **dead tuple** that occupies space until the background
  **VACUUM** process reclaims it. (Write–write conflicts on the *same* row still
  serialize — first-updater-wins.)

- **Durability — [[write-ahead-logging]].** [[transaction]] promises that a committed
  change survives a crash, but PostgreSQL does **not** flush the changed data pages
  at commit — that would be many slow random disk writes. Instead it follows
  [[write-ahead-logging]]'s write-ahead invariant: each change is first appended as a
  record to a **sequential WAL**, and at `COMMIT` only the *WAL* is forced to stable
  storage with `fsync` and waited on — one cheap contiguous write. The modified heap
  and index pages stay dirty in memory and are flushed **lazily** by background
  writeback (or reconstructed by **replaying the WAL** after a crash). This is what
  makes MVCC affordable: commits are fast *and* durable, so keeping extra versions
  around is the only real overhead.

- **Storage + access — heap tables and [[b-tree]] indexes.** A table's tuples live in
  a **heap** — unordered data pages, where MVCC's multiple versions of a row
  physically coexist. To find rows without scanning the whole heap, PostgreSQL builds
  indexes, and the **default** index type is the [[b-tree]]: a high-fan-out balanced
  tree, each node one disk page, so a lookup over millions of rows is 3–4 page reads
  instead of a full-table scan. The index maps a column value to the heap location of
  the matching tuple(s).

- **Planning — cost-based [[query-planning]].** Because [[sql]] is declarative, one
  query admits many equivalent procedures. PostgreSQL's [[query-planning]] step
  enumerates them and picks the **least estimated cost**: per table, a **sequential
  scan** of the heap vs. a **[[b-tree]]-index scan** (chosen by how selective the
  predicate is); per join, the method (nested-loop / hash / merge); and the order to
  join three or more tables. The same [[sql]] text can therefore run via different
  plans as the data distribution changes.

### Worked instance — one transaction, end to end through every piece

Take a table `accounts` under the [[relational-model]] — columns `id` (integer,
primary key) and `balance` (integer) — with a [[b-tree]] index on `id`. One row
currently reads `(id = 1, balance = 500)`, and a long-running **reporting query
R** has already begun (its snapshot was taken a moment ago). Now a client runs:

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```

Follow the *same* statement through the composed subsystems, watching the value
`500 → 400`:

1. **[[sql]] → a request.** The declarative statement says *what* to do (subtract
   100 from row `id = 1`), not *how* to find or store it. PostgreSQL parses it into
   a query tree. Nothing about scanning or locking is in the text — that is the
   engine's to decide.

2. **[[query-planning]] picks the access path.** The planner must locate the row
   matching `id = 1`. Because `id = 1` is **highly selective** (one row out of
   however many), a cost-based comparison favors a **[[b-tree]]-index scan** on `id`
   — a 3–4-read descent — over a **sequential scan** of the whole `accounts` heap.
   The chosen plan: index-scan to the row, then update it.

3. **Inside the [[transaction]], [[mvcc]] writes a new version.** The `UPDATE` runs
   within the ACID [[transaction]] opened by `BEGIN`. Per [[mvcc]], PostgreSQL does
   **not** overwrite the existing tuple. It marks the old version
   `(balance = 500)` as superseded by stamping its **xmax** with this
   transaction's id, and appends a **new heap tuple** `(balance = 400)` stamped with
   this transaction's **xmin**. The [[b-tree]] index on `id` gains a pointer to the
   new tuple's heap location.
   - **The payoff, made concrete:** the reporting query **R**, whose snapshot
     predates this transaction's commit, still applies its visibility test and sees
     the **old** version — `balance = 500`. R is **not blocked**, does **not wait**,
     and is not disturbed by the in-flight write. This is "readers don't block
     writers" in literal numbers: under [[concurrency-control]]'s pessimistic locking
     family, the writer's exclusive lock would have stalled R; under PostgreSQL's
     MVCC it sails through on the old version.

4. **[[write-ahead-logging]] makes the commit durable.** As the change is made,
   PostgreSQL appends a **WAL record** ("txn T: row id=1, page P, 500 → 400") to the
   sequential log. The modified heap page (and the index page) are dirtied **in
   memory only** — not yet written to their scattered disk locations. At `COMMIT`,
   PostgreSQL appends a commit record and **`fsync`s the WAL** — one fast sequential
   write — and only *then* returns "committed" to the client. The data pages are
   **not** forced; they will be flushed lazily by background writeback later.

5. **COMMIT returns durable; later VACUUM cleans up.** The client now has a durable
   commit: if the machine crashes one second later with the `(balance = 400)` heap
   page still unflushed, restart **replays the WAL** and re-applies `500 → 400`, so
   the committed value is never lost. Meanwhile the **old** `(balance = 500)` version
   left behind by step 3 becomes a **dead tuple** once no live snapshot can still see
   it (i.e. once R and every transaction older than this commit have finished). The
   background **VACUUM** process later walks the heap, finds that superseded version,
   and frees its space for reuse — paying off the bookkeeping cost MVCC chose in
   exchange for never locking the reader in step 3.

**Coordinating the levels of this one example.** The **structure** is the
relational row `(id=1, balance)` and its chain of MVCC versions (old 500, new 400)
in the heap, reachable through the [[b-tree]] index. The **algorithm** is
*parse [[sql]] → [[query-planning]] picks the index scan → [[transaction]] wraps it
→ [[mvcc]] versions the row → [[write-ahead-logging]] logs and fsyncs at commit →
VACUUM reclaims*. The **substrate** is disk and memory: heap pages and index pages
dirty in the buffer, the WAL forced to stable storage at commit, the old version
sitting on its page until VACUUM frees it. That single traced statement — every
component doing exactly its one job, in concert — *is* the node: PostgreSQL is the
integration, not any one of the parts.

## Prerequisites

- [[relational-model]] — PostgreSQL's data model: data is tables (relations) of
  typed, named-column tuples with primary/foreign keys; values are visible, which is
  what makes filtering, joins, and indexing possible.
- [[sql]] — the declarative query language clients use to talk to PostgreSQL; stating
  *what*, not *how*, is what gives the planner room to optimize.
- [[transaction]] — the ACID unit of work every statement runs inside; supplies
  Atomicity, Consistency, and Durability, and defers Isolation to the concurrency
  machinery below.
- [[mvcc]] — PostgreSQL's **signature** isolation mechanism: write a new row version,
  keep the old, read against a snapshot — so readers never block writers; the cost is
  dead tuples reclaimed by VACUUM.
- [[concurrency-control]] — the framing that situates that choice: PostgreSQL takes the
  *optimistic / multi-version* branch (MVCC) rather than the *pessimistic / read-locking*
  branch, which is why it avoids reader-writer blocking.
- [[write-ahead-logging]] — how PostgreSQL realizes Durability: `COMMIT` fsyncs the
  sequential WAL (cheap), while scattered data pages flush lazily and a crash is
  recovered by replaying the log.
- [[b-tree]] — PostgreSQL's default index type over its heap tables: a high-fan-out
  balanced tree giving 3–4-read lookups, and the structure the planner's index-scan
  access path descends.
- [[query-planning]] — the cost-based step that compiles each declarative [[sql]] query
  into an execution plan: sequential scan vs. [[b-tree]]-index scan, join method, join
  order — chosen by least estimated cost.

## Sources

- PostgreSQL documentation (overview) — https://www.postgresql.org/docs/current/
- PostgreSQL documentation, "Architectural Fundamentals" — https://www.postgresql.org/docs/current/tutorial-arch.html (the process-per-connection model and the overall structure of a running PostgreSQL server).
- PostgreSQL documentation, "Internals" — https://www.postgresql.org/docs/current/internals.html (heap storage, MVCC/visibility, WAL, and the planner/optimizer as realized in the engine).
