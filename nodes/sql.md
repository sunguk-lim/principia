---
id: sql
title: SQL (Structured Query Language)
summary: The declarative query language over the [[relational-model]] — you state WHAT result relation you want (which columns, from which relations joined on which keys, filtered and aggregated how) and the engine derives HOW to compute it; a query's input and output are both relations (closure), and the same SELECT can be executed many ways, freeing the planner to optimize.
type: concept
tags: [databases/relational-database]
prereqs: [relational-model]
sources: ["ISO/IEC 9075 (the SQL standard)", "https://www.postgresql.org/docs/current/sql.html", "A. Silberschatz, H. Korth, S. Sudarshan, Database System Concepts, ch. 3 (Introduction to SQL)"]
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# SQL (Structured Query Language)

## Summary

**SQL** is the **declarative query language** over the [[relational-model]]. Its
defining commitment is in the word *declarative*: you write down **what** result
you want — which columns, drawn from which relations, joined on which key, kept by
which filter, summarized by which aggregate — and you do **not** write the
procedure that computes it. There is no loop, no "open this relation, scan it row
by row, look up that one in an index." You describe the answer; the database's
*query planner* decides the steps. The core query is
`SELECT … FROM … WHERE …`: `FROM` names the relation(s), `WHERE` keeps the tuples
matching a condition (**selection**), `SELECT` keeps the attributes you asked for
(**projection**). `JOIN` combines tuples from two relations wherever a value in
one matches a value in the other — almost always a **foreign key** matching the
**primary key** it references, the exact link the [[relational-model]] defines.
`GROUP BY` with an aggregate (`COUNT`, `SUM`) collapses many tuples into one
summary tuple per group. And the result of every query is **itself a relation** —
a set of tuples over named attributes — which is the *closure* property that lets
a query feed another query. The reward of being declarative is that one `SELECT`
can be executed many different ways with the same answer, so the engine is free to
pick the fastest.

## Grounded explanation

**The central idea: say what, not how.** The [[relational-model]] gives us data as
**relations** — sets of tuples over named, typed attributes, with a **key**
naming each tuple and a **foreign key** carrying one relation's key value into
another. SQL is the language that *asks questions of* such relations. The one idea
that makes SQL what it is, and is easy to miss because it sounds like a mere
convenience, is that an SQL query is **declarative**: it is a *description of the
result*, not a *recipe for producing it*. Contrast the two stances on a single
task — "list the students in year 2":

- **Imperative** (how): *"Allocate an empty list. Open the students relation. For
  each tuple, read its `year` attribute; if it equals 2, append the tuple's `name`
  to the list. Return the list."* Every step — the iteration, the order, the
  comparison, the accumulation — is spelled out by you.
- **Declarative** (what): `SELECT name FROM students WHERE year = 2`. You name the
  relation (`FROM students`), the condition the tuples must satisfy
  (`WHERE year = 2`), and the attribute you want back (`SELECT name`). You never
  say *scan*, never say *in what order*, never allocate anything.

Both return the same answer. The difference is **who chooses the procedure.** In
the imperative version *you* did; in the declarative version you handed that choice
to the engine. That hand-off is the whole point, and the payoff appears at the end:
because you only described the result, the engine may compute it by any procedure
that yields that result — and it picks the cheapest one available, which can differ
by orders of magnitude (a full scan vs. an index lookup). You get to ignore the
how; the engine gets to optimize it.

**The three pieces of the core query, against a relation.** `SELECT … FROM …
WHERE …` maps directly onto two operations on a single [[relational-model]]
relation:

- **`FROM r`** names the relation `r` whose tuples are the raw material.
- **`WHERE condition`** is **selection**: keep only the tuples for which the
  condition is true — a filter on *rows*. The result is a sub-set of `r`'s tuples.
  Because a relation is a set, "keep the tuples where `year = 2`" is well-defined
  with no reference to position or order.
- **`SELECT a, b`** is **projection**: keep only attributes `a, b` — a filter on
  *columns*. From each surviving tuple, drop every attribute not named.

So `SELECT name FROM students WHERE year = 2` reads as: take `students`, *select*
the tuples with `year = 2`, then *project* onto the single attribute `name`.

**`JOIN` — combining two relations on a key match.** A single relation only
answers questions about itself. To answer "which *course* is each *student*
enrolled in, **by name**," you must combine two relations — and the
[[relational-model]] already built the bridge: a **foreign key** in one relation
holds the **key value** of a tuple in another. A `JOIN` is the operation that
*follows that bridge*. `students JOIN enrollments ON students.id =
enrollments.student_id` pairs a `students` tuple with an `enrollments` tuple
**exactly when** the student's primary key `id` equals the enrollment's foreign
key `student_id`. Each such matching pair becomes one wider tuple carrying both
relations' attributes. This is not a new idea bolted onto SQL — it is the
[[relational-model]]'s foreign-key reference *traversed*: the model spreads data
across narrow relations linked by keys precisely so a join can stitch them back
together at query time. The join condition is almost always *this* key/foreign-key
equality, because that is the relationship the schema was designed to express.

**`GROUP BY` + aggregates — collapsing tuples into summaries.** Selection and
projection return individual tuples; often the question is about *groups* of them:
"how many enrollments does each student have?" `GROUP BY student_id` partitions the
joined tuples into one group per distinct `student_id`, and an **aggregate** —
`COUNT(*)` counts the tuples in each group, `SUM(x)` adds up an attribute across
them — collapses each group into a *single* summary tuple. The output has one row
per group, not one per input tuple. A `HAVING` clause then filters those *group*
summaries (e.g. keep only groups whose count exceeds 1), the way `WHERE` filters
individual tuples.

**Closure: the answer is itself a relation.** Every SQL query takes relations in
and produces a relation out — a set of tuples over named attributes, obeying the
same [[relational-model]] rules (unordered unless you sort, the named result
columns are its attributes). This is the **closure** property, and it is why SQL
composes: because a query's output is the same kind of object as its input, you can
feed one query into another — a join's output can be grouped, a grouped result can
be joined again, a subquery's result relation can sit in another query's `FROM`.
The model is closed under querying, just as integers are closed under addition.

**Worked instance — JOIN + WHERE + aggregate, with concrete rows.** Reuse the
[[relational-model]]'s schema.

*students* — `id` (int, **primary key**), `name` (text), `year` (int):

```
id │ name    │ year
───┼─────────┼─────
 1 │ Ada     │ 2
 2 │ Linus   │ 3
 3 │ Grace   │ 1
```

*enrollments* — `student_id` (int, **foreign key** → `students.id`), `course`
(text); primary key `{student_id, course}`:

```
student_id │ course
───────────┼────────
         1 │ CS101
         1 │ MATH200
         2 │ CS101
```

Ask a non-degenerate question — *"For each student in year 2 or 3, how many courses
are they enrolled in? List the student's name and the count."* In SQL:

```sql
SELECT   students.name, COUNT(*) AS course_count
FROM     students
JOIN     enrollments ON students.id = enrollments.student_id
WHERE    students.year >= 2
GROUP BY students.id, students.name;
```

Trace it as a description of the result (the order below is *one* reading, not the
procedure the engine must use):

1. **`FROM students JOIN enrollments ON students.id = enrollments.student_id`** —
   follow the foreign key. Each enrollment pairs with the one student whose `id`
   equals its `student_id`:
   - `(1,"CS101")` → student `(1,"Ada",2)` → `(Ada, 2, CS101)`
   - `(1,"MATH200")` → student `(1,"Ada",2)` → `(Ada, 2, MATH200)`
   - `(2,"CS101")` → student `(2,"Linus",3)` → `(Linus, 3, CS101)`

   Note Grace (`id 3`) vanishes: no enrollment's `student_id` is 3, so no pair
   forms. The join produces only matched tuples.
2. **`WHERE students.year >= 2`** — selection on the joined tuples. Ada's `year` is
   2 and Linus's is 3, both pass; all three joined tuples survive. (If we had asked
   `>= 3`, Ada's two rows would drop here — the filter bites *before* the count, so
   "courses for year-3+ students" would count only Linus's.)
3. **`GROUP BY students.id, students.name`** — partition the survivors by student:
   group *Ada* = `{(Ada,2,CS101), (Ada,2,MATH200)}`, group *Linus* =
   `{(Linus,3,CS101)}`.
4. **`SELECT students.name, COUNT(*)`** — projection plus the aggregate. Each group
   collapses to one tuple: count Ada's group = 2, count Linus's group = 1.

The **result relation** — itself a set of tuples over attributes `(name,
course_count)`:

```
name  │ course_count
──────┼─────────────
Ada   │ 2
Linus │ 1
```

That output is a relation in its own right (closure), so it could be filtered,
joined, or grouped again by an enclosing query.

**Why declarative pays off — two procedures, same answer.** Nowhere in the query
did we say *how* to compute it. The engine's planner is free to choose, and at
least two genuinely different procedures yield this exact result relation:

- **Scan-and-filter (nested-loop join).** Read every tuple of `enrollments`; for
  each, scan `students` to find the one whose `id` matches its `student_id`; check
  `year >= 2`; then accumulate counts in a per-student tally. Cost is dominated by
  the repeated scans of `students`.
- **Index lookup (index-nested-loop / hash aggregate).** If `students` has an index
  on its primary key `id` (a sorted or hashed access path from key value to tuple),
  then for each enrollment the engine *looks up* the matching student directly —
  no scan — applies `year >= 2`, and maintains the group counts in a hash table
  keyed by `student_id`. On large relations this is dramatically cheaper.

Both compute the same two-row answer. **Because the SQL only declared the result,
the engine may pick whichever is faster given what indexes exist** — and may
re-decide as the data or indexes change, without the query text changing at all.
That freedom is exactly what the declarative stance buys: by refusing to name a
procedure, SQL hands the engine the latitude to optimize. This is the whole
relationship between the language and the model: the [[relational-model]] makes
every value visible and key-linked so that *selection, projection, join, and
aggregation* are even askable; SQL is the declarative surface for asking them; and
declarativeness is what turns "askable" into "askable *and* fast."

## Prerequisites

- [[relational-model]] — SQL is a query language *over relations*. Every SQL
  construct is an operation on the model's objects: `WHERE`/`SELECT` are selection
  and projection on a relation's tuples and attributes; `JOIN` traverses the
  model's foreign-key → primary-key reference to combine two relations; `GROUP BY`
  partitions a relation's tuples; and the result of any query is *itself* a
  relation (closure). Without the model's relations, keys, and foreign keys, none
  of SQL's constructs would have anything to denote.

## Sources

- ISO/IEC 9075, *Information technology — Database languages — SQL* — the official
  SQL standard defining the language's syntax and semantics.
- PostgreSQL documentation, "SQL" — https://www.postgresql.org/docs/current/sql.html
  (`SELECT`, `FROM`, `WHERE`, joins, `GROUP BY`, and aggregate functions as realized
  in a production relational database).
- A. Silberschatz, H. F. Korth, S. Sudarshan, *Database System Concepts*, ch. 3
  ("Introduction to SQL") — textbook treatment of SQL as a declarative language and
  the relational operations it expresses.
