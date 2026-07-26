---
id: database-trigger
title: Database Trigger
summary: "A database trigger is a procedure the engine runs automatically when a specified [[sql]] data-change event (INSERT / UPDATE / DELETE) occurs on a table — its body executing inside the same [[transaction]] as the statement that fired it, so its effects commit or roll back atomically with that statement; it moves a reaction from application code into the database, where it fires no matter which client caused the change."
type: concept
tags: [databases/relational-database]
prereqs: [sql, transaction]
sources:
  - "https://www.postgresql.org/docs/current/triggers.html — PostgreSQL: Triggers (overview, BEFORE/AFTER, row- vs statement-level)"
  - "https://www.postgresql.org/docs/current/sql-createtrigger.html — PostgreSQL: CREATE TRIGGER"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# Database Trigger

## Summary

A **database trigger** is a procedure the database engine runs **automatically**
when a specified data-change event happens on a table. You register it once with
`CREATE TRIGGER`, naming the event — an `INSERT`, `UPDATE`, or `DELETE` written in
[[sql]] — and from then on the engine fires the procedure every time that event
occurs, **no matter which client or statement caused it**. Two properties define
the concept. First, it is **automatic and centralized**: the reaction lives in the
database next to the data, so it cannot be forgotten or bypassed by one careless
application path. Second, it is **transactional**: the trigger body runs *inside
the same* [[transaction]] as the statement that fired it, so its effects and the
original change are one all-or-nothing unit — either both commit or both roll back.
That second property is what makes a trigger trustworthy rather than merely
convenient: a trigger cannot leave the database in a half-updated state.

## Grounded explanation

### What a trigger is a reaction *to*

Every change to a relational table arrives as one of three [[sql]] data-modification
statements — `INSERT` (add rows), `UPDATE` (change rows), `DELETE` (remove rows).
A trigger is a standing instruction of the form *"whenever event E happens on table
T, run procedure F."* You declare it with `CREATE TRIGGER`, specifying:

- **the event** — `INSERT`, `UPDATE`, or `DELETE` (or a combination);
- **the timing** — `BEFORE` the change is applied (so F can inspect or rewrite the
  incoming row, or reject it) or `AFTER` it is applied (so F can react to the
  committed-shape change);
- **the granularity** — `FOR EACH ROW` (F runs once per affected row, and is handed
  that row's old and new values) or `FOR EACH STATEMENT` (F runs once for the whole
  statement, however many rows it touched).

The body F is itself written in [[sql]] (in PostgreSQL, a `SQL`/PL-pgSQL function).
So a trigger is [[sql]] reacting to [[sql]]: a data-change statement is the stimulus,
and a stored [[sql]] procedure is the response.

### Why it must run inside the firing transaction — the load-bearing idea

The reason a trigger is more than "an event callback" is *where it runs in time*. A
[[transaction]] is the all-or-nothing unit of database work: every statement runs
inside one, and at `COMMIT` all its effects take hold together while at `ROLLBACK`
none do. A trigger's body executes **within that same transaction** — as if its
statements had been written immediately after the firing statement. This yields the
guarantee that matters: **the triggered effect is atomic with the change that caused
it.** If the transaction later aborts, the trigger's writes vanish along with the
original row change; there is no window in which the change happened but the reaction
did not. A `BEFORE` trigger can even veto the change outright (raise an error), which
aborts the whole transaction — the change is refused precisely *because* trigger and
statement share one fate.

Contrast the alternative the trigger displaces: putting the reaction in application
code ("after I insert an order, also insert an audit row"). That is neither automatic
(a second code path that inserts orders might forget the audit write) nor atomic (a
crash between the two application statements leaves the audit row missing). The trigger
fixes both at once by moving the reaction *into* the database and *into* the
transaction.

### Worked instance — keeping an audit log in lock-step

Take a table `accounts(id, balance)` and an `audit(account_id, old_balance,
new_balance, changed_at)` table. Register one trigger:

```sql
CREATE TRIGGER log_balance_change
  AFTER UPDATE ON accounts
  FOR EACH ROW
  EXECUTE FUNCTION log_balance();   -- body: INSERT INTO audit VALUES (OLD.id, OLD.balance, NEW.balance, now());
```

Now a client runs, as one [[transaction]]:

```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;   -- 500 → 400
COMMIT;
```

Trace it:

1. The `UPDATE` matches row `id = 1` and changes `balance` `500 → 400`. Because the
   trigger is `AFTER UPDATE ... FOR EACH ROW`, the engine now runs `log_balance()`
   **once for that row**, handing it two implicit values: `OLD` (the pre-image,
   `balance = 500`) and `NEW` (the post-image, `balance = 400`).
2. The trigger body executes its [[sql]] `INSERT INTO audit VALUES (1, 500, 400,
   now())` — **inside the same transaction** opened by `BEGIN`. The audit row is not
   yet durable; it is part of the pending transaction.
3. At `COMMIT`, the balance change *and* the audit insert become durable **together**.
   Had the client issued `ROLLBACK` instead — or had a constraint failed — *both* the
   balance change and the audit row would disappear. There is never an audit row for a
   balance change that did not happen, nor a balance change with no audit row.

The audit table therefore stays a faithful, gap-free ledger of `accounts` changes,
and it does so no matter which application, admin console, or ad-hoc [[sql]] session
issued the `UPDATE` — the guarantee lives in the database, not in any one caller.

### The general pattern: triggers as a change-driven work queue

Generalize the example: the reaction need not be an audit row — it can be **enqueuing
work to do because a row changed**. An `AFTER INSERT OR UPDATE OR DELETE` trigger that
inserts a marker into a "pending work" table turns any change to the source table into
a durable, transactional to-do item, which some other process can later drain. This
"trigger writes a change into a queue, a worker consumes it" pattern is exactly how
systems keep a *derived* copy of a table in sync with its source without the writing
client having to know about the derived copy — the trigger guarantees the queue entry
is created if and only if the change commits.

## Prerequisites

- [[sql]] — the language of both the stimulus (the `INSERT`/`UPDATE`/`DELETE`
  data-modification statement) and the response (the trigger body is stored [[sql]]);
  a trigger is [[sql]] reacting automatically to [[sql]].
- [[transaction]] — the all-or-nothing unit the trigger body runs *inside*: this is
  what makes the triggered effect atomic with the firing change (both commit or both
  roll back), turning a trigger from a mere callback into a reliable invariant.

## Sources

- PostgreSQL documentation, "Triggers" — https://www.postgresql.org/docs/current/triggers.html (BEFORE/AFTER timing, row- vs statement-level granularity, `OLD`/`NEW` row images).
- PostgreSQL documentation, "CREATE TRIGGER" — https://www.postgresql.org/docs/current/sql-createtrigger.html (the registration syntax used above).
