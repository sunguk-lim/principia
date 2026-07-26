---
id: relational-model
title: Relational Model
summary: The data model in which all data is a set of relations (tables); a relation is a set of tuples (rows) over named, typed attributes (columns), so rows are unordered and never duplicated, a key uniquely identifies each tuple, and a foreign key references another relation's key — the model SQL queries, joins, and indexes are built on.
type: concept
tags: [databases/relational-database]
prereqs: [set]
sources: ["E. F. Codd, \"A Relational Model of Data for Large Shared Data Banks,\" CACM 13(6), 1970", "https://www.postgresql.org/docs/current/ddl.html"]
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Relational Model

## Summary

The **relational model** is the data model in which *all* data is held as
**relations** — what everyday usage calls *tables*. The model's one structural
idea is precise: a relation is a **[[set]] of tuples**. A *tuple* (a row) is a
fixed list of values, one per **attribute** (a named, typed column); a relation
is a set of such tuples, all sharing the same attributes. Because a relation is
a [[set]], two facts fall out for free, not as extra rules: the rows carry **no
order** (a set is unordered, so "the third row" is meaningless), and there are
**no duplicate rows** (a set holds distinct elements, so two identical tuples are
one tuple). On top of this, a **key** is a subset of the attributes whose values
uniquely identify a tuple — the handle by which a row is named — and a **foreign
key** is an attribute in one relation that holds the key value of a tuple in
another, the link that lets separate relations refer to each other. This is the
model that SQL, joins, and indexes are built on, and its whole power comes from
the values being *visible and typed* — the opposite bargain from a key-value
store, where the value is an opaque blob reachable only by its key.

## Grounded explanation

**The one structural commitment: data is a [[set]] of tuples.** Fix a handful of
named, typed columns — call each an **attribute**. A *students* relation might
have attributes `id` (integer), `name` (text), `year` (integer). A **tuple** is
one choice of value for each attribute, in attribute order: `(1, "Ada", 2)` is a
tuple over those three attributes. The relation itself is then a **[[set]]** whose
elements are such tuples. That is the entire model — everything below is a
consequence of "it is a set," which is why [[set]] is the only thing this concept
must assume. A [[set]] is a collection of *distinct* elements with no notion of
position; membership ("is this tuple in the relation?") is the only question it
answers. So when we say a table *is* a set of rows, we are not speaking loosely —
we are choosing the mathematical object whose two built-in properties are exactly
the two properties a relation must have.

**Why "a relation is a [[set]]" forbids duplicate rows.** A [[set]] holds each
element at most once: `{a, b}` and `{a, b, b}` denote the same set. Carry that to
tuples and it says two *identical* rows — same value in every attribute — are not
two rows, they are one. Add the tuple `(1, "Ada", 2)` to a relation that already
contains it and nothing changes; the relation already has that element. This is
not a policy a database administrator opts into; it is what "set" *means*. (Real
SQL engines famously relax this — a table without a declared key can hold true
duplicate rows, making it a *bag/multiset* rather than a pure set — but the model
the engine approximates is the set, and a declared key restores set behavior by
forbidding two rows from agreeing on the key.)

**Why "a relation is a [[set]]" imposes no row order.** A [[set]] is unordered:
`{a, b}` and `{b, a}` are the same set, because membership records *whether* an
element is present, never *where*. So a relation has no first row, no third row,
no "rows in the order I inserted them." Any order you see in query output is one
the *query* asked for (an explicit sort), not a property of the relation. This is
why you address a row by its *values* — "the student whose `id` is 1" — and never
by a position. The model deliberately throws away position so that the only way to
reach data is by what the data *says*, which is what makes declarative,
value-based querying possible.

**A key: the subset of attributes that names a tuple.** Membership alone lets you
ask "is this exact tuple present?", but you usually want "*which* tuple is the one
about student 1?" A **key** is a subset of a relation's attributes such that no
two distinct tuples can share the same values across that subset — so fixing the
key values picks out at most one tuple. In *students*, the single attribute `{id}`
is a key: no two students may share an `id`, so `id = 1` identifies exactly one
row. (A key may be several attributes together when no single one suffices.) One
key is designated the **primary key** — the canonical handle for a tuple. The key
is what makes a relation behave like the set it is supposed to be: it is precisely
the guarantee that there are no two tuples you could confuse, i.e. no duplicates
in the part of the tuple that matters for identity.

**A foreign key: how one relation refers to another's tuples.** Relations do not
nest — a tuple's attribute values are flat, typed scalars, not other tuples. So to
express "this enrollment is about that student," one relation stores, in one of
*its* attributes, the **key value** of a tuple in another relation. That attribute
is a **foreign key**: it *references* the other relation's (primary) key. The
referenced value must actually exist as a key over there — this is *referential
integrity*, the model's promise that a foreign key never points at a missing
tuple. Foreign keys are the entire mechanism by which the model spreads data
across many narrow relations instead of one wide one, and the thing a **join**
later follows to stitch them back together at query time.

**The contrast that defines the model — visible values vs. opaque blobs.** Place
the relational model beside the key-value model. A key-value store maps a unique
key to a *value it never looks inside*: the value is an opaque blob, and the only
access path is the key — you cannot ask "give me every value whose third field is
2." The relational model makes the opposite commitment: every attribute of every
tuple is *visible and typed*, so you can select tuples by any attribute, combine
relations by matching attribute values (a join), and have the engine build an
index on any attribute to make those queries fast. The price is that you give up
the key-value store's easy horizontal partitioning (a query may touch many tuples
across many relations at once); the reward is a rich, declarative query surface —
SQL — over structured data. The relational model is the data model that *earns*
joins and ad-hoc queries by refusing to hide its values.

**Worked instance — two relations, real rows.** Define a tiny schema.

*students* — attributes `id` (int, **primary key**), `name` (text), `year` (int):

```
id │ name    │ year
───┼─────────┼─────
 1 │ Ada     │ 2
 2 │ Linus   │ 3
 3 │ Grace   │ 1
```

*enrollments* — attributes `student_id` (int, **foreign key** → `students.id`),
`course` (text); the pair `{student_id, course}` is the **primary key** (a student
takes a given course at most once):

```
student_id │ course
───────────┼────────
         1 │ CS101
         1 │ MATH200
         2 │ CS101
```

Read these as sets. *students* is the set of three tuples
`{ (1,"Ada",2), (2,"Linus",3), (3,"Grace",1) }`; *enrollments* is the set
`{ (1,"CS101"), (1,"MATH200"), (2,"CS101") }`. Now watch each property bite:

- **No duplicates (it is a [[set]]).** Try to add `(1,"CS101")` to *enrollments*
  again — say a re-submitted form. The tuple is already an element of the set, so
  the set is unchanged; the would-be duplicate enrollment simply does not exist.
  And because `{student_id, course}` is the primary key, even a *near*-duplicate
  agreeing on those two attributes is rejected as a second tuple with the same key.
- **No order (it is a [[set]]).** The students listed `1, 2, 3` and the
  enrollments listed in that sequence carry no meaning — re-print them in any order
  and they are the *same two relations*. "Ada's row comes before Grace's" is not a
  fact the model stores. To get an order you must ask for one (sort by `year`).
- **Key identifies a tuple.** "Who is student 2?" Fix the key `id = 2`; exactly one
  tuple in *students* matches — `(2,"Linus",3)` — because `id` being a key forbids
  any second tuple from sharing it. The lookup is unambiguous by construction.
- **Foreign key references another relation's key.** In *enrollments*, the tuple
  `(1,"CS101")` has `student_id = 1`. That value is *not* a student's data; it is a
  reference — it must equal the `id` (the key) of some tuple in *students*, and it
  does: `(1,"Ada",2)`. Referential integrity forbids an enrollment with
  `student_id = 9`, because no student tuple has key `9`. Following this reference
  from each enrollment back to its student is exactly the join "list each
  enrollment with the student's name," which pairs `(1,"CS101")` with `"Ada"`,
  `(1,"MATH200")` with `"Ada"`, and `(2,"CS101")` with `"Linus"`. None of that is
  possible against a key-value store, where `students`' values would be opaque and
  `student_id` could match nothing inspectable.

That is the whole model in motion: two relations, each a [[set]] of tuples over
named typed attributes (so unordered and duplicate-free); a key naming each tuple;
a foreign key carrying one relation's key value into another so the two can be
joined — and every value visible, which is what SQL, joins, and indexes stand on.

## Prerequisites

- [[set]] — a relation *is* a set of tuples, so the model inherits its two defining
  properties directly from set semantics: distinct elements (no duplicate rows) and
  no inherent order (no row position). The [[set]] node also notes that a key–value
  mapping is exactly a set of ordered pairs; a relation generalizes that to a set of
  *n*-tuples, and membership ("is this tuple present?") is the primitive question a
  relation answers.

## Sources

- E. F. Codd, "A Relational Model of Data for Large Shared Data Banks," *Communications of the ACM* 13(6), 1970 — the paper that defines data as relations (sets of tuples) over typed domains, with keys and the relational operations.
- PostgreSQL documentation, "Data Definition" — https://www.postgresql.org/docs/current/ddl.html (tables/columns, primary keys, and foreign-key referential integrity as realized in a production relational database).
