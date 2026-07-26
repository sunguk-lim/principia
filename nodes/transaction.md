---
id: transaction
title: Transaction (ACID)
summary: A transaction is an all-or-nothing unit of database work — a sequence of statements that either COMMITs (every effect takes hold) or ROLLBACKs/ABORTs (no effect takes hold), lifting the indivisibility of [[atomic-operation]] from one memory cell to a whole multi-row sequence; ACID names its guarantees — Atomicity (the indivisible commit-or-rollback unit), Consistency (each transaction carries the database from one constraint-honoring state to another), Durability (a committed effect survives a crash, because the write was forced to stable storage), and Isolation (covered separately).
type: concept
tags: [databases/transactions]
prereqs: [atomic-operation]
sources:
  - "https://www.postgresql.org/docs/current/tutorial-transactions.html — PostgreSQL: Transactions"
  - "Gray & Reuter, Transaction Processing: Concepts and Techniques (1993) — the ACID transaction concept"
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Transaction (ACID)

## Summary

A **transaction** is a **unit of database work** that the system promises to treat as
**all-or-nothing**. You group several statements — reads and writes that together
accomplish one logical change — and the database guarantees that either **all** of their
effects take hold (the transaction **COMMITs**) or **none** of them do (it **ROLLBACKs**,
also called **ABORTs**); there is no surviving in-between where some writes landed and
others didn't. This is the idea of [[atomic-operation]] — an indivisible read-modify-write
on one memory location — **lifted up a level**: where [[atomic-operation]] makes a single
cell's update uninterruptible against other threads, a transaction makes a whole *sequence*
of statements across many rows behave as one indivisible step against crashes and other
transactions. Its guarantees are named by the acronym **ACID**: **A**tomicity (the
commit-or-rollback indivisibility just described), **C**onsistency (the transaction moves
the database from one valid state — one honoring all its declared constraints — to another
valid state), **D**urability (once `COMMIT` returns, the effects survive even a power
loss, because the database forced the write to stable storage first), and **I**solation
(how concurrent transactions are kept from seeing each other's half-done work — its own
concept, covered separately).

## Grounded explanation

### What the concept *is* — promoting indivisibility from a cell to a sequence

The prerequisite [[atomic-operation]] node established indivisibility at the smallest
scale: a read-modify-write on **one memory location** that the hardware refuses to let any
other thread interrupt. The lost-update race it cured was two threads both reading `5`,
both adding `1`, both writing `6` — one increment silently vanishing in the gap between a
read and its write. The cure was to fuse read, modify, and write into a single
uninterruptible event, so no one could slip into the gap.

A **transaction** is that exact insight raised to a coarser, more useful grain. The unit of
indivisibility is no longer one cell touched by one instruction — it is a **whole sequence
of database statements** that may read and write **many different rows**, possibly across
several tables. The transaction says: *treat this entire sequence as one step.* Either the
database carries out every statement and makes the bundle permanent (`COMMIT`), or it acts
as if **not one** of the statements ever ran (`ROLLBACK` / `ABORT`). The "gap" that the
single-cell atomic closed is, at this level, the dangerous window *between two writes of one
logical change* — and the transaction's job is to guarantee no one (no crash, no other
transaction) can ever observe the database stuck in that window.

That is the concept's spine: **a transaction is the unit of work the database treats as
indivisible.** Everything in ACID is a property of that unit.

### Why it must exist — the multi-write change that cannot be done one statement at a time

Many logical changes are *not* a single write; they are several writes that are only correct
**together**. The canonical one is moving money. To transfer funds from account A to account
B you must do two writes — decrease A's balance and increase B's — and the two are only
meaningful as a pair. A database without transactions can still execute each write, but it
offers no promise that the two happen as a unit. If something interrupts the program *after*
the first write and *before* the second, the database is left in a state that is internally
**false**: money has left A but not arrived at B. No single-statement atomicity helps here,
because the danger spans **two** statements. We need indivisibility around the *whole pair* —
which is precisely what a transaction provides and a sequence of independent statements does
not.

### The three properties, named

- **Atomicity (A).** The bundle is the indivisible unit. At `COMMIT`, all its writes become
  visible together; on `ROLLBACK` (whether you ask for it, or a crash or error forces it),
  every write the transaction had made so far is undone, returning the database to exactly the
  state it held before the transaction began. There is no partial application. This is the
  direct lift of [[atomic-operation]]'s "all-at-once, like a light switch — no observable
  in-between state," from one location to one sequence.

- **Consistency (C).** A transaction takes the database from one **valid state to another
  valid state**, where "valid" means *every declared constraint holds* — uniqueness, foreign
  keys, check constraints, and any invariant the schema enforces. The transaction may pass
  through temporarily-illegal intermediate states *inside* itself (after the debit but before
  the credit, the books don't balance), but at the boundaries — before it starts and after it
  commits — all constraints are satisfied. If a statement would commit a state that violates a
  constraint, the database refuses and forces a rollback instead, so an invalid state is never
  made permanent.

- **Durability (D).** Once `COMMIT` returns to the caller, the transaction's effects
  **survive a crash** — a power loss, an OS kill, a process abort. The database achieves this
  by forcing the record of the change out to **stable storage** (disk, or its modern
  equivalent) *before* it reports the commit as successful, so that on restart the committed
  data is still there to recover. (The specific mechanism — appending the change to a
  sequential log and flushing that log to disk before acknowledging the commit — is the
  subject of a later node and is left in plain prose here.) Durability is what makes a commit a
  *promise* and not merely a hope.

- **Isolation (I)** is the fourth ACID property — it governs what *concurrent* transactions
  are allowed to see of each other's not-yet-committed work. It is its own concept, **covered
  separately**, and is named here only for completeness.

### Worked instance — a $100 bank transfer

Let account **A** start with a balance of **500** and account **B** with **200**. We transfer
**$100** from A to B. The transaction is two writes:

```
BEGIN
  W1:  A.balance  =  500 − 100  =  400      (debit A)
  W2:  B.balance  =  200 + 100  =  300      (credit B)
COMMIT
```

The numbers are derived directly: A goes `500 → 400`, B goes `200 → 300`. The **invariant**
the transfer must preserve is that **no money is created or destroyed** — the total across A
and B must stay `500 + 200 = 700` at every commit boundary. Before: `500 + 200 = 700`. After a
successful commit: `400 + 300 = 700`. The invariant holds. That preserved total *is*
**Consistency** in this example.

Now the all-or-nothing point, made concrete. Suppose the machine **crashes after W1 but before
W2** — A has already been debited to **400**, but B has not yet been credited and still holds
**200**. The total at this instant is `400 + 200 = 600`: **$100 has simply vanished**. This is
exactly the multi-write analogue of the lost-update race in [[atomic-operation]], except the
loss now spans *two statements* rather than living in the gap of one. **Atomicity** forbids
this outcome from ever being the final, observed state: because the transaction never reached
`COMMIT`, the database must `ROLLBACK` on restart, undoing W1 and restoring A to **500**. The
recovered state is `500 + 200 = 700` — as if the transfer never started. The database is never
left at `400 + 200`; that state is *transient and private*, never the committed truth.

And the mirror case: if the machine instead crashes **after `COMMIT` returned**, **Durability**
guarantees the opposite — the recovered state is `400 + 300 = 700`, the *completed* transfer,
because the commit was forced to stable storage before it was acknowledged. So every crash
resolves to one of exactly two legal totals — `700` before (rollback) or `700` after (durable
commit) — and **never** the illegal `600` in between.

Tying the levels of this one example together: the **structure** is the indivisible unit (the
two-write bundle A→B); the **algorithm** is `BEGIN … COMMIT`-or-`ROLLBACK`, which decides
atomically whether both writes count or neither does; and the **substrate** is stable storage,
where forcing the committed record to disk before acknowledging is what turns Atomicity's
"both or neither" into Durability's "and it stays that way after a crash."

## Prerequisites

- [[atomic-operation]] — a transaction *is* this concept lifted from one memory cell to a
  multi-statement, multi-row sequence: the indivisible "all-or-nothing, no observable
  in-between state" guarantee, and the lost-update danger it prevents, are exactly the framing
  Atomicity reuses at transaction granularity.

## Sources

- PostgreSQL Documentation — *Transactions* — https://www.postgresql.org/docs/current/tutorial-transactions.html
- Jim Gray & Andreas Reuter, *Transaction Processing: Concepts and Techniques* (Morgan Kaufmann, 1993) — the ACID transaction concept.
