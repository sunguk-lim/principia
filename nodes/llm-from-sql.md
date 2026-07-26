---
id: llm-from-sql
title: Calling LLMs from SQL
summary: "Calling LLMs from SQL exposes model inference as ordinary [[sql]] functions — a generative call like ai.openai_chat_complete(model, prompt) and an [[embedding]] call like ai.openai_embed(model, text) — so a language model runs per row inside a query: the same SELECT/UPDATE that reads a table can classify, summarize, or embed its rows, and because retrieval is also just [[sql]], the whole retrieve-then-generate loop of [[retrieval-augmented-generation]] can be assembled in one statement instead of an external application pipeline."
type: concept
tags: [databases/vector]
prereqs: [sql, retrieval-augmented-generation, embedding]
sources:
  - "https://github.com/timescale/pgai — pgai: call LLM and embedding models (OpenAI, Ollama, Cohere, …) directly from SQL"
  - "https://github.com/timescale/pgai/blob/main/docs/model_calling/openai.md — pgai model-calling functions (chat completion, embeddings) as SQL"
status: explained
created: 2026-07-01
updated: 2026-07-01
---

# Calling LLMs from SQL

## Summary

**Calling LLMs from SQL** means exposing model inference as ordinary [[sql]]
**functions** you can invoke inside a query. Instead of a language model living behind
a separate application service, the database offers functions such as
`ai.openai_chat_complete(model, prompt)` — a **generative** call that sends a prompt to
a large language model and returns its text answer — and `ai.openai_embed(model, text)`
— a call that returns the text's [[embedding]]. Because these are just [[sql]]
functions, they compose with everything [[sql]] already does: a single `SELECT` or
`UPDATE` can run a model **once per row**, so the same statement that reads a table can
classify, summarize, translate, or embed its rows. And since the *retrieval* half of
[[retrieval-augmented-generation]] is itself a [[sql]] query, the entire
retrieve-then-generate loop can be written in one statement — the model call moves *into*
the query rather than sitting in an external pipeline that shuttles rows out to a service
and back.

## Grounded explanation

### What "a model as a SQL function" means

A language model, in the sense [[retrieval-augmented-generation]] uses, is a function
from a text prompt to generated text: you hand it a prompt and it produces a reply,
grounded in whatever context the prompt contains. Normally that function is reached over
the network by application code. **Calling LLMs from SQL** relocates the *call site*: the
database registers functions that, when evaluated, reach out to a model provider (OpenAI,
Ollama running locally, Cohere, …) and return the result as a [[sql]] value. Two families
matter, corresponding to the two model outputs the retrieval stack needs:

- **Generation** — `ai.openai_chat_complete(model, prompt)` returns the model's text
  completion. This is the generative language model of [[retrieval-augmented-generation]],
  now callable in a query.
- **Embedding** — `ai.openai_embed(model, text)` returns an [[embedding]]: the dense
  meaning-vector of the input text. This is the *same* operation that must turn documents
  and questions into vectors before any similarity search.

Because a [[sql]] function is evaluated **per row** in the rows a query touches, wrapping
one of these calls in a `SELECT` list or an `UPDATE ... SET` applies the model across a
whole table with no loop written by hand — the [[sql]] engine does the iterating.

### Why move the model call into the query — the load-bearing idea

The point is not novelty of syntax; it is **eliminating the round-trip pipeline**. The
usual way to enrich rows with a model is: application code `SELECT`s the rows, ships each
one to a model service, waits, and writes the answers back with an `UPDATE`. That pipeline
is extra code, an extra failure surface, and it drags every row across the process
boundary twice. Making the model a [[sql]] function collapses it:

- **Data locality.** The rows never leave the database to be processed; the query that
  already has them in hand also invokes the model on them. Enrichment becomes a property
  of the data layer, expressible in the same [[sql]] as everything else.
- **Composability with [[sql]].** A model call is an expression, so it slots into
  `WHERE`, `SELECT`, `UPDATE`, joins, and aggregates. You can classify only the rows a
  filter selects, or write generated text straight into a column.
- **RAG in one place.** [[retrieval-augmented-generation]] is *retrieve the top-`k`
  relevant chunks, then generate an answer conditioned on them.* When retrieval is a
  [[sql]] similarity query and generation is a [[sql]] function, both halves live in the
  database: one statement can select the nearest chunks, concatenate them into a prompt,
  and pass that prompt to the generative call — the whole loop [[retrieval-augmented-generation]]
  describes, without an external orchestrator.

The costs are real and worth stating: each call is a **network request to a model
provider** (slow and rate-limited relative to normal [[sql]]), it usually costs money per
token, and it can fail or time out — so running one over a million-row table inside a
single transaction is often the wrong shape (this is exactly the pressure that motivates
doing bulk embedding as a managed background job rather than inline).

### Worked instance — one query does the enrichment

Classify the sentiment of every review, in place, with no application code:

```sql
SELECT id,
       ai.openai_chat_complete(
         'gpt-4o-mini',
         'Reply with POSITIVE or NEGATIVE only. Review: ' || body
       ) AS sentiment
FROM reviews
WHERE created_at > now() - interval '1 day';
```

Trace it. The `FROM reviews WHERE ...` is ordinary [[sql]] — it selects yesterday's rows.
For **each** selected row, the [[sql]] engine evaluates the `SELECT`-list expression,
which builds a prompt by concatenating a fixed instruction with that row's `body` and
passes it to the generative model call; the function returns the model's text
(`POSITIVE`/`NEGATIVE`), which becomes the row's `sentiment` value. One statement, one
model invocation per matching row, results as a normal result set — no export, no
write-back script.

The embedding side is the same shape, writing vectors into a column:

```sql
UPDATE documents
SET embedding = ai.openai_embed('text-embedding-3-small', body)
WHERE embedding IS NULL;             -- embed only rows not yet embedded
```

Here the model call returns an [[embedding]] and the `UPDATE` stores it in a `vector`
column, so the very rows a similarity search will later rank are populated by a [[sql]]
statement. Put the two together — an inner query that retrieves the nearest chunks by
[[embedding]] similarity, an outer generative call fed those chunks as its prompt — and
[[retrieval-augmented-generation]] is expressed as a single [[sql]] query. That collapse
of the retrieve-then-generate pipeline into the query itself is what "calling LLMs from
SQL" contributes.

## Prerequisites

- [[sql]] — the interface and the composition medium: model inference is exposed as
  [[sql]] functions that evaluate per row, so they slot into `SELECT`/`UPDATE`/`WHERE`
  and the engine applies the model across a table without hand-written iteration.
- [[retrieval-augmented-generation]] — supplies the generative language model (prompt →
  text) that the chat-completion call invokes, and the flagship reason to want model
  calls in [[sql]]: its retrieve-then-generate loop becomes a single in-database query
  when both halves are [[sql]].
- [[embedding]] — the output of the embed-model calls (`ai.*_embed`): the dense
  meaning-vector the same statement can compute and store, feeding similarity search.

## Sources

- pgai — https://github.com/timescale/pgai (LLM and embedding model calling from SQL across OpenAI, Ollama, Cohere, and others).
- pgai model-calling docs — https://github.com/timescale/pgai/blob/main/docs/model_calling/openai.md (`ai.openai_chat_complete`, `ai.openai_embed`, and related SQL functions).
