---
id: materialized-view
title: Materialized View
summary: A materialized view stores the result of a declared query and refreshes it separately, trading cheaper repeated reads for storage, refresh work and explicitly bounded staleness.
type: concept
tags: [databases/relational-database]
prereqs: [sql]
sources: [https://www.postgresql.org/docs/current/rules-materializedviews.html, https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html]
status: explained
created: 2026-11-03
updated: 2026-11-03
---

# Materialized View

## Meaning

A materialized view persists the result of a declared query. Readers use those stored rows instead of recomputing the entire derivation each time. Unlike an ordinary logical view that evaluates its defining query when used, the stored result can become stale until a refresh. It is a computation-versus-freshness trade-off, not simply another name for a live query.

## Mechanism

Define the result with [[sql]], populate it from source data, then refresh according to a separate policy. PostgreSQL stores both the result and its defining query; REFRESH MATERIALIZED VIEW replaces the stored contents by executing that query again. The implementation determines locking and concurrent-reader behavior. Incremental maintenance is a separate capability and must not be inferred from the word materialized.

Keeping a stored result can reduce repeated aggregation or remote reads. The cost is storage, refresh computation and a period during which source changes are absent. A refresh success timestamp is not the same as source-event completeness: late events or upstream failures can leave even a newly refreshed result incomplete. Track source cutoff, refresh completion and consumer-visible version separately.

## Worked example

Suppose a query sums completed sales by store and day. Before refresh, store A's stored total is $120. A new qualifying $30 sale enters the source table; querying the stored result still returns $120. Refreshing after that sale commits changes the result to $150. A logical view over the source might instead include the sale immediately under its query snapshot. The materialized result avoided repeating aggregation on every read, but the old number was a deliberate stale snapshot, not evidence that the sale did not occur.

For operational decisions, a batch-derived price table can use the same stored-result pattern. Computing a candidate table does not automatically activate physical labels or checkout values. Stage, validate and publish a version under an explicit consumer contract; physical acknowledgments remain separate. A daily cadence is one possible policy, not a universal requirement or a feature supplied automatically by a database view.

## Boundaries and validation

Compare the result with the defining query at a known source snapshot. Test empty inputs, duplicate source rows, late corrections and refresh failure. Measure read cost, refresh duration, blocking, storage and staleness tails. PostgreSQL's concurrent refresh permits reads but has eligibility requirements, including an already populated view and a qualifying unique index; it is not unconditional nonblocking replacement. Request explicit output ordering when needed because refresh does not promise to preserve a query's prior physical row order.

## Prerequisites

- [[sql]]

## Sources

- <https://www.postgresql.org/docs/current/rules-materializedviews.html>
- <https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html>
