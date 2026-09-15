---
id: pgai
title: pgai
summary: "pgai is a suite of PostgreSQL extensions that turns the database itself into an AI-application platform — defined not by one feature but by how it composes three: [[pgvector]] stores and similarity-searches embeddings in a column, the [[pgai-vectorizer]] keeps those embeddings automatically in sync with the source table, and [[llm-from-sql]] calls generative and embedding models as SQL functions; assembled, they let the full retrieve-then-generate loop of [[retrieval-augmented-generation]] run inside one database — no separate vector store, no external embedding pipeline, no application-side model orchestration."
type: concept
tags: [databases/vector]
prereqs: [pgvector, pgai-vectorizer, llm-from-sql, retrieval-augmented-generation]
sources:
  - "https://github.com/timescale/pgai — pgai: tools to build RAG, semantic search, and other AI applications with PostgreSQL"
  - "https://github.com/timescale/pgai/blob/main/docs/vectorizer/overview.md — pgai Vectorizer overview"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# pgai

## Summary

**pgai** is a suite of extensions (from Timescale) that turns PostgreSQL into a
platform for building AI applications — chiefly **retrieval-augmented generation** and
**semantic search** — *inside the database*. As with a database engine itself, the point
of a "pgai" node is not any single feature; each is already a prerequisite below. The
point is the **composition**: pgai bundles three capabilities so they reinforce one
another. [[pgvector]] gives the database a `vector` column type, distance operators, and an
ANN index, so embeddings live beside relational data and are searched by meaning in
SQL. The [[pgai-vectorizer]] keeps those embeddings **automatically in sync** with the
source rows, so the searchable vectors never drift from the text they represent.
[[llm-from-sql]] exposes generative and embedding **models as SQL functions**, so inference
runs in a query rather than an external service. Put together, they let the entire
retrieve-then-generate loop of [[retrieval-augmented-generation]] execute within one
PostgreSQL instance — no separate vector database to synchronize, no bespoke embedding
pipeline, no application-side orchestration of model calls.

## Grounded explanation

### Why pgai is its own node and not just the sum of its parts

Each prerequisite already stands on its own: [[pgvector]] is vector storage and search;
the [[pgai-vectorizer]] is an auto-embedding pipeline; [[llm-from-sql]] is model inference
as SQL functions; [[retrieval-augmented-generation]] is the retrieve-then-generate
architecture. So what does a "pgai" node teach that those four do not? **The integration** —
that these particular pieces, assembled in one database, collapse a system that is normally
spread across three or four separate services into a single PostgreSQL deployment.
The conventional RAG stack is: a relational database for the source data, a *separate*
vector database for the embeddings, a *separate* embedding pipeline to keep the two in sync,
and *application code* to orchestrate retrieval and the model call. pgai's contribution is
that every one of those becomes a feature of Postgres: the vectors sit in the same tables
([[pgvector]]), the sync is a declared, self-maintaining pipeline ([[pgai-vectorizer]]), and
both the embedding and the generation calls are SQL ([[llm-from-sql]]). The value is in how
the parts lock together — the [[pgai-vectorizer]] produces exactly the embeddings that
[[pgvector]] indexes, and [[llm-from-sql]]'s generative call consumes exactly the neighbors
[[pgvector]] returns — so [[retrieval-augmented-generation]] needs nothing outside the
database.

### The pieces, and the role each plays

- **Vector storage & search — [[pgvector]].** The substrate. It adds the `vector` column
  type so an embedding is stored in the row, the distance operators so similarity is a
  SQL comparison, and the ANN index so nearest-neighbor retrieval is fast. This is *where
  the vectors live and how they are searched*.

- **Keeping vectors current — the [[pgai-vectorizer]].** The maintenance layer. Declaring a
  vectorizer on a text column means its [[pgvector]] embeddings are created and re-created
  automatically as rows change — a trigger captures every change transactionally and a
  background worker re-embeds out of band. This is *what stops the searchable vectors from
  going stale*, and it is why pgai is usable without hand-writing an embedding pipeline.

- **Model inference in the query — [[llm-from-sql]].** The compute layer. It exposes
  embedding calls (used by the vectorizer and for ad-hoc embedding) and generative calls
  (used to produce the final answer) as SQL functions. This is *how a model is invoked*
  without leaving the database.

- **The application shape — [[retrieval-augmented-generation]].** The architecture the other
  three exist to serve: retrieve the few most relevant chunks, then generate an answer
  conditioned on them. pgai does not invent RAG; it makes RAG a thing you assemble from SQL.

### Worked instance — a RAG assistant over a documents table, end to end

Build a question-answering assistant over a `documents` table, entirely in Postgres, and
watch each prerequisite do its one job:

1. **Ingest (handled continuously by the [[pgai-vectorizer]]).** You declared a vectorizer
   on `documents(body)`. As articles are inserted or edited, its trigger enqueues them and
   its worker chunks and embeds each one via an embedding model, writing the chunk
   embeddings into a [[pgvector]]-typed destination table. No ingestion script runs on
   your side; the corpus's vectors simply stay current with its text.

2. **A question arrives.** The user asks *"What is our refund policy?"* First embed the
   question — an embedding call through [[llm-from-sql]] — producing a query vector `$q`.

3. **Retrieve (via [[pgvector]]).** A SQL query ranks the chunk vectors by cosine distance
   to `$q` and takes the top 5:
   `SELECT chunk FROM documents_embeddings ORDER BY embedding <=> $q LIMIT 5`. These are the
   five passages most relevant in meaning — the retrieval half of
   [[retrieval-augmented-generation]], executed as an ANN index scan.

4. **Generate (via [[llm-from-sql]]).** The five retrieved chunks are concatenated into a
   prompt — *"Answer using these passages: … Question: what is our refund policy?"* — and
   passed to a generative model call. The model returns an answer grounded in the retrieved
   text.

5. **The whole is [[retrieval-augmented-generation]].** Steps 2–4 are exactly retrieve then
   generate, and step 1 kept the retrievable set faithful to the source. Every step was a
   SQL statement against one PostgreSQL database: the vectors were maintained by the
   [[pgai-vectorizer]], searched by [[pgvector]], and both embedding and generation were
   [[llm-from-sql]] calls. What would otherwise be four cooperating systems is one.

**Coordinating the levels.** The **structure** is a `documents` table and its companion
[[pgvector]] embeddings, joined by a view. The **algorithm** is *vectorizer keeps embeddings
synced → embed the question → [[pgvector]] nearest-neighbor retrieval → [[llm-from-sql]]
generation* — i.e. [[retrieval-augmented-generation]] with every arrow a SQL call. The
**substrate** is a single Postgres instance: the source rows, the vector column and its ANN
index, the vectorizer's queue and worker, and the model-call functions, all in one engine.
That end-to-end assembly — not any one extension — *is* pgai.

## Prerequisites

- [[pgvector]] — the storage-and-search substrate: the `vector` column type, distance
  operators, and ANN index that let embeddings live in a table and be retrieved by
  meaning in SQL.
- [[pgai-vectorizer]] — the maintenance layer that keeps those [[pgvector]] embeddings
  automatically in sync with the source rows, so pgai works without a hand-built embedding
  pipeline.
- [[llm-from-sql]] — the compute layer: embedding and generative model calls exposed as SQL
  functions, invoked for both indexing and the final answer without leaving the database.
- [[retrieval-augmented-generation]] — the application architecture pgai assembles from the
  other three: retrieve the relevant chunks, then generate an answer conditioned on them,
  here run end-to-end inside PostgreSQL.

## Sources

- pgai — https://github.com/timescale/pgai (a suite for building RAG, semantic search, and other AI applications with PostgreSQL: model calling, and the Vectorizer).
- pgai Vectorizer overview — https://github.com/timescale/pgai/blob/main/docs/vectorizer/overview.md.
