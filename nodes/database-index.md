---
id: database-index
title: Database Index
summary: A secondary access structure on a table column that maps each column value to the storage location(s) of the rows holding it — kept ordered (typically a B+-tree) so a query filtering or sorting by that column does an O(log N) lookup instead of an O(N) full table scan; it speeds reads but costs storage and slows every write, since each INSERT/UPDATE/DELETE must also maintain every index.
type: concept
tags: [databases/storage]
prereqs: [binary-search-tree, key-value-store, b-tree]
sources: ["PostgreSQL documentation — Indexes (https://www.postgresql.org/docs/current/indexes.html); Index Types (https://www.postgresql.org/docs/current/indexes-types.html)"]
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Database Index

## Summary

A **database index** is a *secondary* access structure built on one (or more) columns of a table. The table itself is the primary store — the actual rows, identified by some row location (a row id, or a position in storage). An index is a *separate* structure off to the side that maps **each value of the indexed column → the location(s) of the rows that hold that value**, and is kept **ordered by that value**. Its whole reason to exist is the cost of *not* having it: to answer a query like `WHERE email = 'x'` with no index, the database must read **every** row in the table and test the column — a **full table scan**, `O(N)` for `N` rows. The index turns that into a lookup in an ordered structure — `O(log N)` — exactly the way a [[binary-search-tree]] turns a linear scan into a `log`-depth descent. An **ordered** index (which also serves range queries and `ORDER BY`) is in practice a [[b-tree]] index, because the [[b-tree]] is the structure that stays shallow on disk and lets a range scan walk its leaf chain; a **hash** index instead stores the value→location map as a [[key-value-store]]-style hash and serves only *equality*, not ranges. The catch — and the reason indexes are added selectively, not on every column — is the **write trade-off**: an index is a second copy of the keys that must be kept consistent, so every `INSERT`/`UPDATE`/`DELETE` on the table must also update **every** index on it. An index buys fast reads by paying storage and slower writes.

## Grounded explanation

### The problem: a query with no index is a full scan

A table is a collection of rows. Internally each row sits at some **location** — call it a *row id* (an opaque handle naming where the row physically lives, e.g. which block and offset). The table is stored roughly in *insertion* order, **not** sorted by any particular column. So consider the query:

```
SELECT * FROM users WHERE email = 'alice@x.com';
```

With nothing but the table, the database has no idea *where* the matching row is, and the table is not ordered by `email`, so there is no shortcut: it must read row 1, check its `email`; read row 2, check; … all the way to row `N`. This is a **full table scan**, and its cost is **`O(N)`** — linear in the number of rows. For a `users` table with `N = 1,000,000` rows, answering one equality query reads **~1,000,000 rows**. This is the same situation [[binary-search-tree]] starts from: a linear search over unordered data is `O(N)`, and the fix is to impose an *ordered* structure so a comparison can discard most of the candidates at once.

### The fix: a separate ordered map from value to row location

An **index** is that ordered structure, built as a *second* object beside the table. Conceptually it is a map:

> **indexed column value → row location(s)**

For an index on `email`, each entry is `(email_value → row_id)`. This is the same value→location association a [[key-value-store]] makes — store a location *keyed* by a value, fetch it back by naming the value — except the index is **kept ordered by the key** (not opaque-and-hashed), which is what lets it answer more than exact-match. Two flavors fall straight out of *which* structure holds the map:

- A **hash index** stores `value → location` as a hash table — the [[key-value-store]] data model exactly: hash the value, jump to its slot, read the location. This is `O(1)` average for **equality** (`= 'x'`) but, because hashing destroys order, it **cannot** answer a range (`BETWEEN`, `<`, `ORDER BY`) — neighboring keys land in unrelated slots.
- An **ordered index** keeps the keys *sorted*, so it answers both equality **and** ranges. In a database this is almost always a [[b-tree]] index (specifically a B+-tree), for the reasons that node establishes: the index is large and lives on **disk**, so the cost that matters is *disk reads*, not comparisons; a [[binary-search-tree]] over a million keys is ~20 levels deep = ~20 disk reads, whereas a [[b-tree]] packs hundreds of keys per disk-block node and is only **3–4 levels** deep = 3–4 disk reads, and its **leaf chain** lets a range scan walk consecutive sorted blocks without re-descending. So the default index is ordered and is a [[b-tree]].

Either way the *win* is the cost model: instead of scanning `N` rows, the database searches the index — `O(log N)` for the ordered case — lands on the matching entry, reads the `row_id` out of it, and then does **one** direct fetch of that row from the table. The index is the layer that converts "where is it?" from a linear hunt into a directed descent.

### Worked instance — `users`, 1,000,000 rows

Let the `users` table have `N = 1,000,000` rows, with columns `id`, `email`, `created_at`, and others. Put a [[b-tree]] index on `email` and a second [[b-tree]] index on `created_at`. (Two indexes deliberately — it makes the write cost below non-degenerate.)

**(1) Equality query — `WHERE email = 'alice@x.com'`.**

- *Without the index:* full table scan. Read all **~1,000,000 rows**, comparing each `email`. Cost ≈ `N` row reads.
- *With the `email` [[b-tree]] index:* descend the index. With ~1,000,000 keys and a fan-out of a few hundred per node, the [[b-tree]] is ~3 levels deep, so the descent is **~3 disk reads** (root → internal → leaf), and the leaf entry hands back the `row_id`. Then **1 more read** fetches that row from the table. Total ≈ **3–4 reads** versus ~1,000,000. That ratio — `log N` vs `N` — is the entire point of an index, and it is the [[binary-search-tree]] `log`-depth-vs-linear argument carried onto disk.

**(2) Range query — `WHERE created_at BETWEEN '2026-01-01' AND '2026-01-31'`.**

This is what a hash index *cannot* do and the ordered [[b-tree]] does well. The query wants every row whose `created_at` falls in a contiguous interval. Using the `created_at` [[b-tree]] index:

1. Descend **once** to the leaf holding the low bound `2026-01-01` — ~3 disk reads.
2. Then **walk the leaf chain** rightward — the sequential links the [[b-tree]] (B+-tree) keeps between leaves — reading consecutive, already-sorted leaf blocks and collecting each `row_id` until a key passes the high bound `2026-01-31`. No climbing back up into internal nodes; the chain supplies the next key directly.

The matching `row_id`s come out in `created_at` order, so the same index also satisfies `ORDER BY created_at` for free. Cost ≈ "one descent + one read per leaf in the range" — proportional to the *size of the answer*, not to `N`. A full scan would again be ~1,000,000 row reads plus a sort.

**(3) The write trade-off — one INSERT must maintain both indexes.**

Now make the cost of having indexes concrete. Insert one new user:

```
INSERT INTO users (id, email, created_at) VALUES (1000001, 'zoe@x.com', '2026-02-14');
```

The database does **not** just append the row to the table. It must keep **every** index consistent, or a later indexed query would miss this row. So this *single* logical insert is really **three** structural updates:

1. Write the row into the **table** itself (get its `row_id`).
2. Insert `('zoe@x.com' → row_id)` into the **`email` [[b-tree]]** — descend to the right leaf and splice it in (a [[b-tree]] insert, possibly splitting a node).
3. Insert `('2026-02-14' → row_id)` into the **`created_at` [[b-tree]]** — another descend-and-splice.

With two indexes, one `INSERT` is **1 table write + 2 index maintenances**; with `k` indexes it is `1 + k`. The same multiplication applies to `DELETE` (remove the row's key from every index) and to `UPDATE` of an indexed column (delete the old key and insert the new one in that column's index). This is why indexes are added **selectively**: each one accelerates the reads that filter or sort by its column, but taxes *every* write to the table and consumes extra storage (a whole second [[b-tree]] of the keys). The design decision for each candidate index is exactly this trade — *do the reads it speeds up outweigh the writes it slows down?*

### Why the contrast with the bare tree matters

The cost story is layered. At the *structure* level an index is the [[key-value-store]] idea — fetch a location by a value — made **ordered**. At the *algorithm* level the ordered case is the [[binary-search-tree]] descent: each step discards most of the remaining keys, giving `O(log N)` instead of `O(N)`. At the *substrate* level the index lives on disk, which is why the binary tree's ~20 reads are unacceptable and the index is a shallow, high-fan-out [[b-tree]] whose leaf chain turns range queries into a sequential walk. The index is not a new way to *store* the data (the table still holds the rows); it is a secondary, ordered, value-keyed map *to* the data, paid for in storage and write speed.

## Prerequisites

- [[binary-search-tree]] — supplies the core cost argument the index rests on: an ordered branching structure turns an `O(N)` linear scan into an `O(log N)` descent by discarding most candidates per comparison. An index lookup *is* this descent; without the BST cost model "an index makes the query fast" has no meaning.
- [[key-value-store]] — the index's data model is value→location, the same store-and-fetch-by-key association a key–value store makes. A hash index *is* this model directly (equality only, order destroyed); an ordered index is the same map kept sorted. It frames *what an index entry is*.
- [[b-tree]] — the structure an ordered (range-capable) index actually is on disk. It justifies *why not a plain [[binary-search-tree]]*: disk reads are the scarce resource, so the index is a shallow high-fan-out tree (3–4 reads, not ~20), and its leaf chain is what makes the `BETWEEN`/`ORDER BY` range scan cheap.

## Sources

- PostgreSQL documentation — Indexes: https://www.postgresql.org/docs/current/indexes.html — indexes as a secondary structure that lets the planner avoid a sequential scan, and the explicit note that indexes add overhead to data-modification (write) operations and so should be used judiciously.
- PostgreSQL documentation — Index Types (B-tree, Hash): https://www.postgresql.org/docs/current/indexes-types.html — B-tree as the default index handling equality and range queries (and `ORDER BY`); hash indexes handling only simple equality.
