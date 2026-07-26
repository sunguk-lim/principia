---
id: transaction-isolation
title: Transaction Isolation
summary: Isolation is the "I" of ACID — the degree to which concurrent [[transaction]]s are shielded from each other's uncommitted, in-progress effects, the strictest level (Serializable) making them appear to run one-at-a-time; the four standard levels form a ladder defined by which of three read anomalies (dirty read, non-repeatable read, phantom read) each one forbids, trading concurrency for correctness.
type: concept
tags: [databases/transactions]
prereqs: [transaction]
sources:
  - "https://www.postgresql.org/docs/current/transaction-iso.html — PostgreSQL: Transaction Isolation"
  - "Berenson, Bernstein, Gray, Melton, O'Neil & O'Neil, \"A Critique of ANSI SQL Isolation Levels\" (SIGMOD 1995)"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Transaction Isolation

## Summary

**Isolation** is the **I** of ACID — the property that governs what concurrently-running
[[transaction]]s are allowed to see of **each other's in-progress, not-yet-committed work**. A
single [[transaction]] running alone is already safe by Atomicity; the danger appears the instant
**two or more run at the same time** and one peeks at the half-finished state of another. The ideal
Isolation gives is **serializability**: even though transactions overlap in real time, the database
makes the result come out *as if* they had each run **completely, one after another, in some serial
order** — no transaction ever observes another's intermediate state. Perfect isolation is expensive,
though, because forcing transactions to stop overlapping throttles throughput. So real databases
offer a **ladder of weaker levels**, each defined by which **read anomalies** it is willing to
tolerate in exchange for more concurrency. The three classic anomalies, from least to most subtle,
are the **dirty read** (you read a write that later gets rolled back, so you saw data that never
existed), the **non-repeatable read** (you read a row twice in one transaction and get two different
values because someone committed an update between your reads), and the **phantom read** (you run a
range query twice and a *new* row appears the second time because someone committed an insert). The
four standard levels — **Read Uncommitted, Read Committed, Repeatable Read, Serializable** — forbid
progressively more of these, so choosing a level is a tunable trade-off: stricter means more correct
but less concurrent.

## Grounded explanation

### What the concept *is* — the fourth ACID property is about *other* transactions

The [[transaction]] node established that a transaction is an **all-or-nothing unit** of work and
named three of its four ACID guarantees — Atomicity, Consistency, Durability — while deferring the
fourth, **Isolation**, to here. The key thing to see is that the first three are properties of a
[[transaction]] **considered on its own**: Atomicity says *this* bundle commits or rolls back as a
whole, Durability says *this* commit survives a crash. None of them mentions a *second*
transaction. Isolation is the one ACID property that exists **only because transactions run
concurrently**. If a database executed [[transaction]]s strictly one at a time — each finishing
completely before the next began — Isolation would be free and there would be nothing to define.

But running one-at-a-time wastes the machine: while one transaction waits on a slow disk, others
could be doing useful work. So databases **interleave** the steps of many [[transaction]]s. The
moment they do, a transaction can **read a row in the middle of another transaction's edits** —
seeing a state the other transaction has not yet committed and may never commit. Isolation is the
guarantee that **bounds how much of that mid-flight state a transaction is exposed to**. Its strongest
form, **serializability**, restores the illusion of one-at-a-time execution: the *outcome* is
identical to *some* serial order of the transactions, even though they physically overlapped. That
illusion — "concurrent in fact, serial in effect" — is the spine of the concept.

### The three read anomalies, each as a two-transaction interleaving

What goes wrong without enough isolation is catalogued as three named **read anomalies**. Each is a
specific bad interleaving of two transactions, T1 and T2. Throughout, "T2 commits" means T2's writes
become permanent and visible per the rules of [[transaction]]; "T2 rolls back" means they are undone
as if T2 never ran. Notation: `R1(x)` = T1 reads row `x`; `W2(x)` = T2 writes row `x`; `C` =
commit, `A` = abort/rollback. Time runs left to right.

**(1) Dirty read** — *reading a write that never becomes real.* T2 reads a row that **T1 has written
but not committed**, and then **T1 rolls back**. T2 has now made a decision based on a value that, in
the committed history of the database, **never existed**:

```
T1:  W1(balance := 150) ............................. A1   (T1 rolls back)
T2:  ................. R2(balance) → 150 ... (acts on 150) ...
```

T2 read `150`, but after T1's rollback the balance is whatever it was before T1 ever touched it.
T2 consumed phantom data. This is the crudest anomaly because the value T2 saw was never committed
by anyone.

**(2) Non-repeatable read** — *the same row changes value under you.* T1 reads a row, gets a value,
and **later in the same transaction reads the same row again** — but between the two reads T2 has
**committed an update** to that row. T1's two reads of one row disagree, so a calculation that
assumed the row was stable is now inconsistent:

```
T1:  R1(balance) → 100 ........................ R1(balance) → 150  ...
T2:  ............. W2(balance := 150) ... C2 ..
```

T1 read `100`, then `150`, for *the same row*, inside *one* transaction. The row was committed-real
both times (unlike a dirty read), but it **did not stay put** across T1's lifetime.

**(3) Phantom read** — *a new row appears in a repeated range query.* T1 runs a query over a **range
or predicate** (e.g. "all accounts with balance > 1000"), getting a set of rows. T2 then **commits a
NEW row** that satisfies that predicate. T1 re-runs the **same** query and a row it never saw before
— a "phantom" — is now in the result set:

```
T1:  Q1(balance > 1000) → {A, B} ....................... Q1(balance > 1000) → {A, B, C}  ...
T2:  ............. INSERT account C (balance = 2000) ... C2 ..
```

The phantom differs from a non-repeatable read in *what* changed: a non-repeatable read is an
**existing row's value** changing; a phantom is the **set of rows matching a predicate** growing (or
shrinking) because rows were inserted or deleted. Guarding individual rows you already read does not
stop a phantom, because the new row was not one you had read — which is exactly why it needs its own,
stronger defense.

### The four isolation levels — a ladder by which anomalies are forbidden

The SQL standard defines four levels, and the clean way to understand them is **not** by their
implementation but by **which anomalies each one promises cannot happen**. Each rung forbids
everything the rung below it forbids, plus one more:

| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| **Read Uncommitted** | allowed | allowed | allowed |
| **Read Committed** | **forbidden** | allowed | allowed |
| **Repeatable Read** | **forbidden** | **forbidden** | allowed |
| **Serializable** | **forbidden** | **forbidden** | **forbidden** |

- **Read Uncommitted** — the weakest. A transaction may read other transactions' uncommitted writes,
  so all three anomalies are possible. Maximum concurrency, minimum protection.
- **Read Committed** — a transaction only ever reads data that **has been committed** by someone, so
  the dirty read is impossible. But it makes no promise that a value you read **stays** that value, so
  non-repeatable reads and phantoms still occur.
- **Repeatable Read** — additionally guarantees that any **row you have already read** keeps the same
  value for the rest of your transaction, killing the non-repeatable read. Phantoms can still slip in,
  because the guarantee covers rows you *read*, not rows that *appear*.
- **Serializable** — the strongest: also forbids phantoms, delivering the **as-if-serial** outcome.
  The result is guaranteed equivalent to running the transactions in some one-at-a-time order, so no
  anomaly of any kind is observable.

**The why — it is a tunable trade-off.** Each step up the ladder buys correctness by **reducing how
much transactions may overlap**: the database must do more work — holding read data stable, blocking
or aborting conflicting writers, guarding entire predicate ranges (this is what locking and
multi-version schemes implement under the hood) — and that work **lowers throughput and raises the
chance a transaction must wait or be retried**. So the level is a dial. An analytics dashboard that
can tolerate slightly stale numbers runs Read Committed and serves more queries per second; a
ledger that must never miscount runs Serializable and accepts the contention. The point of having
four levels is that *you* choose where on the correctness-vs-concurrency curve a given workload sits.

### Worked instance — a non-repeatable read, and how Repeatable Read forbids it

Take one concrete row: account **A** with a committed `balance = 100`. T1 is computing interest and
needs the balance **twice** — once to compute the interest, once to write the new total — and
between those two reads, T2 deposits `50` and commits.

**Under Read Committed (anomaly occurs).** The schedule, step by step:

```
step 1   T1: BEGIN
step 2   T1: R1(A.balance) → 100         (T1's first read: 100)
step 3   T2: BEGIN
step 4   T2: W2(A.balance := 100 + 50 = 150)
step 5   T2: COMMIT                       (150 is now committed-real)
step 6   T1: R1(A.balance) → 150          (T1's second read: 150)
step 7   T1: COMMIT
```

Every number is derived: T1's first read returns the committed `100` (step 2). T2 computes
`100 + 50 = 150` and commits it (steps 4–5). When T1 reads **the same row again** at step 6, Read
Committed only forbids reading *uncommitted* data — and `150` **is** committed — so T1 dutifully
returns `150`. T1 has now read `100` and then `150` **for one row inside one transaction**: the read
was **not repeatable**. If T1's logic assumed the balance was stable (say it computed interest on
`100` but then based a limit check on `150`), it is now working from two contradictory facts.

**Under Repeatable Read (anomaly forbidden).** Repeatable Read promises that **any row T1 has already
read keeps the value it had at T1's first read, for T1's whole lifetime.** Concretely, T1's first
read at step 2 establishes that, *as far as T1 is concerned*, `A.balance = 100`, and that view is
**frozen** for T1 until it ends:

```
step 1   T1: BEGIN
step 2   T1: R1(A.balance) → 100          (T1 pins its view of A at 100)
step 3   T2: BEGIN
step 4   T2: W2(A.balance := 150)
step 5   T2: COMMIT                        (committed-real for transactions starting after T2)
step 6   T1: R1(A.balance) → 100           (STILL 100 — T1's pinned view is unchanged)
step 7   T1: COMMIT
```

The only line that changes is **step 6**: T1's second read returns `100`, **not** `150`. T2's commit
is real and visible to *new* transactions, but T1 is shielded — its repeated read of a row it had
already read yields the **same value**, so the non-repeatable read is gone. (The mechanism — T1
reading from a consistent snapshot fixed at its start, or holding a read lock on A — is
implementation detail and stays in plain prose; what *defines* the level is the forbidden anomaly,
not how it is enforced.) Note this level still would **not** stop a *phantom*: had T1's query been
"all accounts with balance > 80" and T2 *inserted* a brand-new qualifying account, that new row
could still appear on T1's re-query — which is precisely the gap Serializable closes.

## Prerequisites

- [[transaction]] — Isolation is the fourth ACID guarantee of a [[transaction]], the one that only
  has meaning when [[transaction]]s run concurrently; the anomalies are defined entirely in terms of
  one [[transaction]] reading another's committed-or-not writes, and serializability is the promise
  that the concurrent outcome equals some serial order of [[transaction]]s.

## Sources

- PostgreSQL Documentation — *Transaction Isolation* — https://www.postgresql.org/docs/current/transaction-iso.html
- Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil & Patrick O'Neil, *A Critique
  of ANSI SQL Isolation Levels*, ACM SIGMOD 1995 — the precise definitions of the read phenomena
  (dirty / non-repeatable / phantom) and the level ladder.
