---
id: pgvector
title: pgvector
summary: "pgvector is a PostgreSQL extension that adds a first-class vector column type plus distance operators and an approximate-nearest-neighbor index, turning an ordinary [[postgresql]] table into a store for [[embedding]]s: you keep each row's meaning-vector in a column beside its relational data and run [[nearest-neighbor-search]] as a plain ORDER BY ... LIMIT k query scored by a distance operator (cosine distance = 1 − [[cosine-similarity]]), accelerated by an ANN [[database-index]] the planner can use — so vector search lives inside the same engine, transactions, and joins as the rest of the data."
type: concept
tags: [databases/vector]
prereqs: [postgresql, embedding, nearest-neighbor-search, cosine-similarity, database-index]
sources:
  - "https://github.com/pgvector/pgvector — pgvector: open-source vector similarity search for Postgres (README: types, operators, IVFFlat/HNSW indexes)"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# pgvector

## Summary

**pgvector** is an extension for [[postgresql]] that teaches it to store and search
**vectors**. It adds three things to the database: a first-class `vector` **column
type** (a fixed-length list of real numbers), a set of **distance operators** that
score how close two vectors are, and **approximate-nearest-neighbor (ANN) index**
types built on those operators. Together these turn an ordinary relational table into
a vector store: you keep each row's [[embedding]] in a `vector` column *beside* its
normal columns, and you run [[nearest-neighbor-search]] as a plain SQL query —
`ORDER BY embedding <distance> $query LIMIT k`. The whole point of doing this inside
[[postgresql]], rather than in a separate specialized store, is that the vectors then
share the engine's transactions, joins, and filters: one query can combine a `WHERE`
on relational columns with a similarity ordering on the vector column, and a vector is
inserted, updated, and rolled back atomically with the row it belongs to.

## Grounded explanation

### The three things pgvector adds

Recall the retrieval stack this builds on. An [[embedding]] is a dense vector whose
*position* encodes meaning; [[cosine-similarity]] scores how nearly two such vectors
point the same way; and [[nearest-neighbor-search]] is the operation *"given a query
vector, return the `k` stored vectors most similar to it,"* made fast at scale by an
**ANN index** that prunes most of the collection instead of scoring every vector. A
purpose-built vector database is a store dedicated to doing exactly this. pgvector's
contribution is to provide that same capability **as an extension to a general-purpose
relational database** — so you do not need a separate system. It installs three pieces:

1. **A `vector` column type.** `CREATE TABLE documents (id bigserial, body text,
   embedding vector(1536))` declares a column holding a 1536-dimensional
   [[embedding]]. The dimension is fixed per column, and the vector sits in the row
   like any other value — stored, transacted, and backed up by [[postgresql]] exactly
   as `id` and `body` are.

2. **Distance operators.** pgvector adds infix operators that take two vectors and
   return a distance (smaller = closer): `<=>` for **cosine distance**, `<->` for
   Euclidean (L2) distance, and `<#>` for (negative) inner product. Cosine distance is
   the direct expression of the prerequisite: it is defined as `1 − `[[cosine-similarity]],
   so *most similar* (cosine similarity near `+1`) means *smallest cosine distance*
   (near `0`). This is what lets similarity ranking be written as an ordinary SQL
   `ORDER BY`.

3. **ANN index types.** pgvector supplies index types — **HNSW** (a navigable-graph
   index) and **IVFFlat** (a clustering index) — that are pgvector's realization of the
   two ANN families [[nearest-neighbor-search]] describes. Each is a specialized
   [[database-index]]: like a B-tree index it is an auxiliary structure the engine
   maintains so a query avoids scanning the whole table, but instead of ordering rows
   by a scalar key it organizes vectors by their layout in space so a query can prune
   to a few candidates. Crucially it plugs into [[postgresql]]'s existing index
   machinery, so cost-based query planning can *choose* to use it, exactly as it would
   choose a B-tree.

### Why keep the vectors inside the relational engine — the load-bearing idea

You *could* run [[nearest-neighbor-search]] in a standalone vector database and keep
your rows in [[postgresql]]. pgvector's reason for being is what you gain by **not**
splitting them:

- **One query, filter + similarity together.** Because the vector is a column, a single
  SQL statement can constrain on relational columns *and* rank by vector distance:
  `SELECT id, body FROM documents WHERE lang = 'en' ORDER BY embedding <=> $q LIMIT 5`.
  In a split system you would either over-fetch neighbors and filter afterward, or
  maintain a fragile filtered mirror; here the planner handles both in one pass.
- **Transactional consistency for free.** The vector is written, updated, and rolled
  back in the same transaction as the row (the ACID guarantee [[postgresql]] already
  gives every row). There is no second store to keep in sync and no window where the
  row exists but its vector does not — the two are literally the same row.
- **Joins.** A neighbor result is just a set of rows, so it can be joined to any other
  table in the schema — authors, permissions, timestamps — with ordinary SQL.

The cost pgvector inherits from [[nearest-neighbor-search]] is the same ANN trade-off:
an approximate index returns *nearly* the true top-`k`, trading a sliver of recall for
sub-linear query time, and it costs build time, extra storage, and per-write index
maintenance (every insert or update of a `vector` must also update the index, just as
any [[database-index]] slows writes).

### Worked instance — semantic search over a documents table

Store a corpus and query it by meaning, entirely in SQL:

```sql
CREATE EXTENSION vector;
CREATE TABLE documents (id bigserial PRIMARY KEY, body text, embedding vector(1536));
-- each row's `embedding` is the 1536-dim vector produced from `body` by some embedding model
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);   -- ANN index on cosine distance

-- query: the 5 documents most similar in meaning to a question vector $q
SELECT id, body
FROM documents
ORDER BY embedding <=> $q      -- cosine distance: smallest = most similar
LIMIT 5;
```

Trace the query. `$q` is the query's [[embedding]]. The `ORDER BY embedding <=> $q`
asks for rows sorted by **cosine distance** to `$q`, i.e. by `1 − `[[cosine-similarity]],
so the row whose vector is most aligned with `$q` sorts first. Without an index this
would be an exact scan — compute the distance for every row, `O(N)`, the slow-but-exact
method. With the HNSW index present, [[postgresql]]'s planner can instead walk the
navigable graph: enter at some node and repeatedly hop toward the vector nearer to `$q`,
touching on the order of `log N` vectors and returning the top 5 approximately — the
same speed-for-recall bargain [[nearest-neighbor-search]] defines, now expressed as a
Postgres index scan. `LIMIT 5` is the `k`. The result is five ordinary rows, so you can
wrap the whole thing in a `WHERE` or `JOIN` to combine meaning-search with any
relational condition. That combination — vector search as *just another operator and
index inside the RDBMS* — is the whole of what pgvector contributes.

## Prerequisites

- [[postgresql]] — the relational engine pgvector extends; the `vector` type is a new
  column type, and the ANN index plugs into Postgres's own index and query-planning
  machinery, so vectors ride the same transactions, storage, and joins as all other data.
- [[embedding]] — what a `vector` column *holds*: the dense meaning-vector of a row's
  content, so that geometric closeness stands for closeness in meaning.
- [[nearest-neighbor-search]] — the operation pgvector makes available in SQL
  (`ORDER BY <distance> LIMIT k`), including the ANN index that makes it sub-linear.
- [[cosine-similarity]] — the similarity the `<=>` operator scores: cosine *distance*
  is `1 −` cosine similarity, which is why "most similar" becomes "smallest distance,"
  orderable by SQL.
- [[database-index]] — the general notion pgvector's HNSW/IVFFlat specialize: an
  auxiliary structure the engine maintains to avoid a full scan (here, to prune the
  vector space), at the cost of storage and slower writes.

## Sources

- pgvector README — https://github.com/pgvector/pgvector (the `vector` type; the `<=>`/`<->`/`<#>` distance operators; the HNSW and IVFFlat index types and their `vector_cosine_ops`/`vector_l2_ops` operator classes).
