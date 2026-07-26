---
id: query-planning
title: Query Planning & Optimization
summary: The engine step that turns a declarative [[sql]] query into a concrete execution plan by enumerating physically-different ways to compute the same result relation and choosing the one of least estimated cost — deciding per table an access path (sequential scan vs index scan, chosen by predicate selectivity), per join a method (nested-loop / hash / merge), and the order to join 3+ tables, where estimated cost ≈ estimated rows × per-operation cost summed over the plan tree.
type: concept
tags: [databases/relational-database]
prereqs: [sql, database-index, b-tree]
sources: ["P. Selinger et al., \"Access Path Selection in a Relational Database Management System\", SIGMOD 1979", "https://www.postgresql.org/docs/current/planner-optimizer.html", "A. Silberschatz, H. Korth, S. Sudarshan, Database System Concepts, ch. 16 (Query Optimization)"]
status: explained
created: 2026-06-30
updated: 2026-06-30
---

# Query Planning & Optimization

## Summary

**Query planning** (query *optimization*) is the engine step that turns a
declarative [[sql]] query into a concrete **execution plan** — a specific
procedure for computing the answer. Because [[sql]] says **what** result you
want and not **how** to compute it, there are *many* physically-different
procedures that all return the same relation, and the planner's job is to
**enumerate** the plausible ones and **choose the one of least estimated cost**.
Three decisions dominate. (1) **Access path** per table: read the whole table
(**sequential scan**) or use a [[database-index]] / [[b-tree]] (**index scan**)?
The planner picks by **selectivity** — how few rows the predicate keeps; a highly
selective filter favors the index, a low-selectivity one favors the seq-scan,
because many random index→row fetches cost more than one streaming pass. (2)
**Join method**: **nested-loop** (good when one side is tiny or indexed), **hash
join** (good for large unsorted equijoins), **merge join** (good when both inputs
arrive sorted, e.g. by a [[b-tree]] order). (3) **Join order**: which of 3+ tables
to join first, since that changes intermediate result sizes enormously. The glue
is a **cost model**: estimated cost ≈ estimated rows (the *cardinality*, derived
from selectivity estimates) × per-operation cost, summed over the plan tree. "Pick
the cheapest" is what makes the same [[sql]] run fast on one data distribution and
choose a *different* plan when the distribution changes.

## Grounded explanation

### Why planning exists at all — declarativeness hands the engine a choice

[[sql]] is **declarative**: a query like

```sql
SELECT c.name, COUNT(*)
FROM   customers c JOIN orders o ON c.id = o.customer_id
WHERE  c.country = 'KR'
GROUP BY c.id, c.name;
```

names *what* relation it wants — the matched, filtered, grouped tuples — and says
nothing about *how* to compute it: no scan order, no "use this index," no choice of
join algorithm. That refusal is the whole point of [[sql]], and it has a direct
consequence: **many physically distinct procedures return the identical result
relation.** The engine could read every order and look up each customer; or read
every customer matching `KR` and probe an index on orders; or sort both sides and
merge them. Each yields the same answer; they differ only in *cost*, sometimes by
orders of magnitude.

So the freedom [[sql]] *creates* (you didn't pin a procedure) becomes an obligation
the engine must *discharge*: **somebody has to pick a procedure, and it is the
planner.** The planner is the component that consumes the declarative query, builds
the set of equivalent candidate plans (an **execution plan** is a tree of physical
operators — scans at the leaves, joins and aggregates above), **estimates each
plan's cost**, and emits the cheapest for the executor to run. This node is about
that *selection* — access path, join method, join order — not about the executor
that later runs the chosen plan, nor about the statistics machinery that feeds the
estimates (both stay prose here).

### Decision 1 — access path: sequential scan vs index scan, chosen by selectivity

For each table the query touches, the planner first decides **how to get the rows
out of it**. Two access paths:

- **Sequential scan** — read **every** page of the table top to bottom, testing the
  predicate on each row. Cost is `O(N)` for `N` rows, but the reads are
  **sequential** (consecutive pages), the cheapest kind of disk I/O.
- **Index scan** — use a [[database-index]] (in practice a [[b-tree]] index) on the
  filtered column: descend the [[b-tree]] to the matching key(s) — `O(log N)`, a few
  reads — and for each, do a **random** fetch of that row from the table by its row
  location.

Which wins is **not** fixed; it depends on **selectivity** — the fraction of rows the
predicate keeps. The [[database-index]] node frames the single-row extreme (`WHERE
email = 'x'` → ~3–4 reads vs ~1,000,000); planning generalizes it to *any*
selectivity. Reason it through:

- A **highly selective** predicate (few matching rows) favors the **index scan**:
  you pay one cheap [[b-tree]] descent per match and a handful of random row fetches,
  versus reading the whole table. Few matches → few random fetches → index wins.
- A **low-selectivity** predicate (many matching rows) flips it. If the filter keeps,
  say, 60% of the table, the index scan would do ~0.6·N **random** row fetches —
  and a random fetch is far more expensive per row than a sequential one. One
  streaming `O(N)` **sequential scan** beats 0.6·N scattered random reads. So
  **many matches → seq-scan wins**, even though it reads *more* rows, because it
  reads them the cheap way and skips the index machinery entirely.

This crossover — index when selective, seq-scan when not — is the first place
"cost-based" becomes concrete, and it is *why* the planner must estimate **how many
rows** a predicate keeps before it can choose.

### Decision 2 — join method

When a query joins two relations (following the foreign-key bridge [[sql]] describes),
the planner picks **how** to perform the match:

- **Nested-loop join** — for each tuple of the outer relation, find its matches in the
  inner relation. This is cheap **only** when the outer side is tiny *or* the inner
  side is indexed: with a [[b-tree]] index on the inner join column, each outer tuple's
  matches are an `O(log N)` index probe rather than a scan. (An un-indexed nested loop
  over two large tables is the `O(N·M)` disaster.)
- **Hash join** — build an in-memory hash table on the smaller relation's join key, then
  stream the larger relation through it, probing the hash for matches. Each side is read
  **once**; no order or index required. This is the workhorse for **large, unsorted
  equijoins**.
- **Merge join** — if both inputs are already **sorted** on the join key (e.g. each
  arrives in [[b-tree]] key order, or from an `ORDER BY`), advance two cursors in lockstep
  and emit matches — one linear pass over each, no hash table. Best precisely when the
  sort comes for free.

### Decision 3 — join order

With three or more tables, the planner also chooses the **order** to join them, because
the order changes the size of the **intermediate** results that flow up the plan tree.
Joining a 1-row result against a 1,000,000-row table produces a small intermediate;
joining two 1,000,000-row tables first produces a huge one that every later operator must
then chew through. Since cost is driven by how many rows flow through each operator (next
section), getting the small intermediates *early* can change total cost by orders of
magnitude — so join order is a first-class search dimension, not an afterthought.

### The cost model — rows × per-operation cost, summed over the tree

The planner ranks candidate plans with a **cost model**. For each operator it estimates
two things and multiplies them:

> **estimated cost of an operator ≈ estimated rows it processes (its *cardinality*) ×
> per-operation cost (per row / per page)**

The **cardinality** comes from **selectivity estimates** — e.g. "`country = 'KR'` keeps
1% of `customers`." (How those estimates are produced — histograms, distinct-value counts,
the table statistics the engine samples — is internal machinery left as prose.) The
**per-operation cost** encodes the substrate: a *sequential* page read is cheap, a *random*
row fetch is dear, a hash-table build costs per row, and so on. The planner then **sums these
costs over the whole plan tree** — leaf scans feeding joins feeding the aggregate — to get one
number per candidate plan, and keeps the **minimum**. Everything above (which access path,
which join method, which join order) is *driven* by this single comparison: the planner is
choosing the tree whose summed estimate is smallest.

### Worked instance — the same join, two selectivities, two winning plans

Two tables: **`orders`** (1,000,000 rows) and **`customers`** (50,000 rows), joined on the
foreign key `orders.customer_id` → `customers.id`. There is a [[b-tree]] index on
`orders.customer_id` and a [[b-tree]] index on `customers.country`. On average each customer
has `1,000,000 / 50,000 = 20` orders. The query:

```sql
SELECT c.name, COUNT(*)
FROM   customers c JOIN orders o ON c.id = o.customer_id
WHERE  c.country = 'KR'
GROUP BY c.id, c.name;
```

Two genuinely different plans return the identical result relation:

- **Plan A — seq-scan + hash join.** Sequential-scan `customers` (50,000 rows, filter
  `country='KR'`), build a hash table on the survivors' `id`, then **sequential-scan all of
  `orders`** (1,000,000 rows) and probe the hash for each. Cost is dominated by the
  **~1,000,000 sequential order reads** — paid in full *regardless* of how selective the
  filter is, because Plan A reads the whole `orders` table no matter what.
- **Plan B — index-scan + nested-loop.** Index-scan `customers` on the `country`
  [[b-tree]] to get just the matching customers, then for **each** matched customer do a
  nested-loop probe into the `orders.customer_id` [[b-tree]] index to fetch that customer's
  orders. Cost ≈ (matched customers) × (one [[b-tree]] descent ≈ 3–4 reads + its ~20 order
  rows fetched).

**Selective case — `country = 'KR'` matches 500 customers** (1% of 50,000).

- *Plan B:* `500 × (≈4 index reads + 20 row fetches) ≈ 500 × 24 ≈ ~12,000` reads.
- *Plan A:* `~1,000,000` order reads (+ 50,000 customer reads) ≈ **~1,000,000+**.

Plan B is ~80× cheaper, so **the planner picks Plan B (index + nested-loop).** Few matching
customers → few index probes → the index path dominates.

**Now flip the selectivity — `country = 'US'` matches 30,000 customers** (60% of 50,000).
The *query text is unchanged*; only the data distribution differs.

- *Plan B:* `30,000 × (≈4 + 20) ≈ 30,000 × 24 ≈ ~720,000` reads — and crucially these are
  **random** index→row fetches, the expensive kind, scattered across `orders`.
- *Plan A:* still `~1,000,000` order reads, but **sequential** (cheap per page), one streaming
  pass, hash built once over the 30,000 matched customers.

Now Plan B's ~720,000 *random* fetches cost **more** than Plan A's ~1,000,000 *sequential*
reads (and Plan A never pays a per-customer index descent), so **the planner now picks Plan A
(seq-scan + hash join).** The selectivity flip moved the crossover: many matching customers →
the index's random-fetch tax exceeds one clean sequential sweep, exactly the access-path
crossover from Decision 1, now playing out at the join level.

That flip is the whole meaning of **cost-based**: the planner did not memorize "use the index
on this query." It **estimated each plan's cost from the estimated row counts** and chose the
cheaper — and when the row counts changed (500 → 30,000 matches), the cheaper plan changed
with them, *without one character of the [[sql]] changing.* The declarative query stated only
the result; planning is what re-derives the best procedure for it as the data shifts.

## Prerequisites

- [[sql]] — the reason planning exists. Because [[sql]] is *declarative* (it states the
  result relation, not a procedure), one query admits many equivalent physical plans; the
  planner is the component that exploits that freedom by choosing the cheapest. Without
  [[sql]]'s "what, not how" stance there would be nothing to plan — the procedure would already
  be written.
- [[database-index]] — supplies the central access-path choice. "Index scan vs sequential
  scan" is *the* per-table decision the planner makes, and the index node establishes both the
  `O(log N)`-vs-`O(N)` win and the value→location lookup the planner is costing. Planning
  generalizes the index node's single-row case to arbitrary selectivity and decides *when the
  index is actually worth using*.
- [[b-tree]] — the concrete structure behind every index access path here: the index scan is a
  [[b-tree]] descent, the indexed nested-loop join probes a [[b-tree]] per outer row, and merge
  join is attractive precisely when inputs already arrive in [[b-tree]] key order. The
  3–4-reads-per-descent cost the planner plugs into its model is the [[b-tree]]'s.

## Sources

- P. Selinger, M. Astrahan, D. Chamberlin, R. Lorie, T. Price, "Access Path Selection in a
  Relational Database Management System," ACM SIGMOD 1979 — the foundational paper on
  cost-based query optimization: access-path selection by estimated cost, join-method and
  join-order enumeration, and the cardinality/selectivity cost model this node teaches.
- PostgreSQL documentation — "Planner/Optimizer":
  https://www.postgresql.org/docs/current/planner-optimizer.html — a production cost-based
  planner choosing access paths (seq scan vs index scan), join methods (nested-loop, hash,
  merge), and join order from estimated costs.
- A. Silberschatz, H. F. Korth, S. Sudarshan, *Database System Concepts*, ch. 16 ("Query
  Optimization") — textbook treatment of equivalent plan enumeration, cost estimation from
  statistics, and join-order/method selection.
