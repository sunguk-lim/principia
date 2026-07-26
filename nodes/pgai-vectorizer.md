---
id: pgai-vectorizer
title: pgai Vectorizer
summary: "The pgai Vectorizer is a declarative auto-embedding pipeline for Postgres: you declare that a source table's text column should be embedded, and it keeps the [[embedding]]s in sync automatically — a [[database-trigger]] on the source table records every INSERT/UPDATE/DELETE into a work queue, and a background worker drains that queue, chunks the text, calls an embedding model, and writes the vectors into a separate destination table with a [[pgvector]] column (exposed through a view joining source and vectors); decoupling embedding from the write means a slow or failing model call never blocks or aborts the original transaction, yet stale rows are always eventually re-embedded."
type: concept
tags: [databases/vector]
prereqs: [database-trigger, embedding, pgvector]
sources:
  - "https://github.com/timescale/pgai/blob/main/docs/vectorizer/overview.md — pgai Vectorizer overview (declarative embeddings, trigger-driven queue, background worker, destination table + view)"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# pgai Vectorizer

## Summary

The **pgai Vectorizer** is a **declarative auto-embedding pipeline** for Postgres. You
declare *once* that a given source table's text column should be embedded — which model,
how to chunk the text — and the Vectorizer then keeps the [[embedding]]s **in sync with
the source data automatically**, forever, without the writing application doing anything.
It is built from two prerequisite pieces working in concert: a [[database-trigger]] on the
source table records every change (INSERT / UPDATE / DELETE) into a **work queue**, and a
**background worker** drains that queue — chunking each changed row's text, calling an
embedding model, and writing the resulting vectors into a separate destination table whose
column is a [[pgvector]] `vector`. The defining idea is **decoupling**: the embedding work
happens *outside* the transaction that changed the row, so a slow, rate-limited, or failing
model call can never block or roll back the user's write — yet because the queue entry was
created transactionally, no change is ever silently missed, and every stale row is
*eventually* re-embedded.

## Grounded explanation

### The problem it solves — embeddings drift out of sync

To search a table by meaning you need each row's text turned into an [[embedding]] and
stored in a [[pgvector]] column. The naïve way is to embed at write time: whenever you
insert or update a row, also call the embedding model and store the vector. This couples
two very different operations. A database write is fast, local, and transactional; an
embedding call is a **slow network request to a model provider** that costs money, is
rate-limited, and can fail. Doing it inline means the model's latency and failures become
*the write's* latency and failures — a timing-out model aborts an ordinary `INSERT`. And if
the row's text is later updated, its stored vector is now **stale**: it describes the old
text, so similarity search silently returns wrong matches. Keeping vectors faithful to a
changing table, without making every write hostage to a model call, is the problem the
Vectorizer exists to solve.

### The mechanism — trigger enqueues, worker embeds

The Vectorizer resolves the tension by splitting the job across its two prerequisites, with
a queue between them:

1. **Capture changes transactionally — the [[database-trigger]].** When you create a
   vectorizer on `documents(body)`, pgai installs a [[database-trigger]] on `documents`.
   On every INSERT/UPDATE/DELETE it inserts a marker — "row *N* needs (re)embedding" — into
   a **queue table**. Because a [[database-trigger]] runs *inside the firing transaction*,
   the queue entry is created **if and only if** the row change commits: a change and its
   "please re-embed me" note are atomic. This is precisely the change-driven work-queue
   pattern [[database-trigger]] describes, and it is what guarantees nothing is missed and
   nothing is enqueued for a change that rolled back.

2. **Do the slow work outside the transaction — the background worker.** A separate
   **worker process** runs on its own schedule (not in the user's transaction). It polls
   the queue, and for each pending row: fetches the text, **chunks** it into passages small
   enough to embed, calls the embedding model to turn each chunk into an [[embedding]], and
   writes those vectors into a **destination table** — a distinct table with a [[pgvector]]
   `vector` column, one row per chunk, linked back to the source row. It then clears the
   queue entry. If a model call fails, the worker simply leaves the entry (or retries
   later); the source table is untouched and the user's write already committed long ago.

3. **Present it as one thing — a view.** pgai also creates a **view** that joins the source
   rows to their chunk-embeddings in the destination table, so queries can read the original
   columns and the vectors together as if they were one table, and run [[pgvector]]
   similarity search over them.

### Why this shape — the load-bearing idea

The architecture is a direct consequence of **decoupling data modification from embedding**:

- **Writes stay fast and reliable.** The only added cost on the write path is one trigger
  insert into a queue — cheap and local. The model's latency and failures live entirely in
  the worker, never on the transaction.
- **Sync is guaranteed but eventual.** Transactional capture (via the [[database-trigger]])
  means every committed change is queued exactly once; the worker means the actual
  re-embedding happens *soon after*, not instantly. So the [[embedding]]s are **eventually
  consistent** with the source — briefly stale right after a change, then corrected — which
  is the right trade for search, where a few seconds of lag is invisible but a blocked write
  is not.
- **Declarative, not hand-wired.** You state the *what* (embed this column with this model,
  chunked this way) once; the trigger, queue, worker, destination table, and view are
  generated and maintained for you. Compare doing it by hand: you would write the trigger,
  the queue, the worker loop, the chunking, the destination schema, and the [[pgvector]]
  index yourself, and keep them correct as the table evolves.

### Worked instance — a document that changes

Declare a vectorizer on `documents(body)` (embedding model + chunking specified once).
Now watch one row's life:

1. A client runs `INSERT INTO documents (body) VALUES ('...long article...')` and commits.
   The [[database-trigger]] fires inside that transaction and writes "doc 42 → pending" to
   the queue. The client's INSERT returns immediately; no model was called on its critical
   path.
2. Moments later the **background worker** wakes, sees "doc 42 pending," reads the article,
   splits it into (say) 6 chunks, calls the embedding model 6 times to get 6 [[embedding]]s,
   and inserts 6 rows into the destination table — each a [[pgvector]] `vector` linked to
   doc 42 — then removes the queue entry. Doc 42 is now searchable by meaning.
3. Later someone edits the article: `UPDATE documents SET body = '...revised...' WHERE id =
   42`. The [[database-trigger]] fires again and re-enqueues doc 42. The worker re-chunks and
   re-embeds, **replacing** doc 42's stale vectors with fresh ones. Similarity search now
   reflects the revised text — automatically, with no application code aware that embeddings
   exist.

That loop — *trigger captures the change transactionally, worker re-embeds it out of band,
[[pgvector]] stores and serves the vectors* — running for every row forever, is the whole
of what the Vectorizer is.

## Prerequisites

- [[database-trigger]] — the sync capture mechanism: a trigger on the source table records
  each committed INSERT/UPDATE/DELETE into a work queue *inside the firing transaction*, so
  changes are enqueued exactly once and never for a rolled-back write.
- [[embedding]] — what the background worker produces from each text chunk and must keep
  current: the dense meaning-vector similarity search depends on, re-computed whenever the
  source text changes.
- [[pgvector]] — where the vectors are stored and searched: the destination table's column
  is a [[pgvector]] `vector`, so the maintained [[embedding]]s are immediately usable by its
  distance operators and ANN index.

## Sources

- pgai Vectorizer overview — https://github.com/timescale/pgai/blob/main/docs/vectorizer/overview.md (declarative vectorizer definition, trigger-driven change capture, background worker, destination table and joining view, eventual sync).
