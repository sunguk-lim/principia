---
id: document-model
title: Document Data Model
summary: "A data model in which each record is a self-contained document — a nested tree of key-value pairs (JSON-like) with no schema enforced across records — so data that belongs together is embedded inside one record and read in one fetch, where the relational model would normalize it into separate tables and reassemble it with joins."
type: concept
tags: [databases/document-database]
prereqs: [key-value, relational-model]
sources:
  - "https://www.mongodb.com/docs/manual/core/document/ — MongoDB Manual: Documents"
  - "https://bsonspec.org — BSON specification (the binary encoding of documents)"
  - "M. Kleppmann, Designing Data-Intensive Applications (O'Reilly, 2017), ch. 2 — Data Models and Query Languages"
status: explained
created: 2026-07-03
updated: 2026-07-03
---

# Document Data Model

## Summary

The **document data model** stores each record as a **document**: a
self-contained, nested tree of key-value pairs, in practice written as JSON.
Two choices define it against the [[relational-model]]. First, **values may be
structured**: where a relational column holds a flat typed value, a document
field may hold another document or an array of them, so a record can *embed*
the data that belongs to it — one-to-many relationships live *inside* the
record instead of in a separate table joined back at read time. Second, the
schema is **per-document, not per-table**: two documents in the same collection
may carry different fields, so the shape of the data is enforced by the
application on read ("schema-on-read"), not by the database on write. The
payoff is **locality and flexibility** — a record and its sub-records arrive in
one fetch, and the shape can evolve without migrating a table. The price is the
mirror image of the relational model's strengths: embedded data is hard to
reach *from the other direction* (many-to-many relationships and cross-record
queries lose the join machinery), and duplicated embedded data must be kept
consistent by the application.

## Grounded explanation

### A document is a tree of key-value pairs

Start from the [[key-value]] mapping: a set of (key, value) pairs with unique
keys, accessed by key content. A **document** is that mapping made
**recursive** — each value may itself be a scalar, an array, *or another
key-value mapping*. So a document is a finite tree: internal nodes are
key-value mappings, leaves are scalars. Written as JSON:

```json
{
  "_id": 7,
  "title": "Why B-trees are wide",
  "author": { "name": "alice", "joined": "2024-01-10" },
  "tags": ["storage", "trees"],
  "comments": [
    { "who": "ada",  "text": "nice worked example" },
    { "who": "alan", "text": "what about LSM trees?" }
  ]
}
```

One top-level key (`_id`) identifies the document, exactly as a key identifies
a pair in a [[key-value]] mapping; everything else hangs off it as nested
structure. The database stores and retrieves *whole documents by key* — the
associative interface of [[key-value]] — while letting the value carry the
entire nested record. (In MongoDB the concrete wire and disk encoding of this
tree is **BSON** — "binary JSON," which adds types like dates and binary blobs
and length-prefixes each element for fast traversal — but the encoding is an
implementation detail; the *model* is the tree.)

### The defining contrast — embedding vs. normalizing

The [[relational-model]] would represent that same blog post as **three
relations**: a `posts` table, an `authors` table, and a `comments` table, each
a set of flat tuples over typed columns, with `comments.post_id` a foreign key
referencing `posts._id`. Rows hold only flat values, so the one-to-many
"post has comments" relationship must live *between* tables, and reading the
post with its comments requires a **join** — the database reassembles at query
time what the application thinks of as one object.

The document model makes the opposite call: the comments are **embedded** in
the post document itself. This is the model's central trade:

- **Locality wins.** "Show the post page" — the dominant access pattern —
  fetches *one* document by `_id`: author snapshot, tags, and comments arrive
  together, no join, no second lookup. The record's tree structure *is* the
  page's structure.
- **The reverse direction loses.** "List every comment `alan` ever wrote,
  across all posts" was a one-table scan (or an indexed lookup) in the
  relational form; in the document form alan's comments are scattered inside
  post documents, so the query must reach *into* every post's `comments`
  array. Many-to-many relationships (a comment author appearing in thousands
  of posts) either duplicate data into each document — copies the application
  must keep consistent, doing by hand what the relational model's foreign keys
  and joins did for it — or fall back to storing references and joining in
  application code.

**Schema flexibility** follows from the same choice. A relation fixes one
column set for *all* its tuples; a collection of documents fixes nothing — the
next post document may add a `"video"` field or omit `"tags"` entirely, and
the database accepts it. That makes evolving the record shape cheap (no table
migration), and moves the burden of "what fields does this record have?" from
the database's schema to the application's reading code.

### When each model fits

The decision rule falls directly out of the trade above. Data that is a
**tree** — a record owning sub-records, read and written together (a post and
its comments, an order and its line items) — fits documents: embedding buys
one-fetch locality and per-record schema freedom. Data that is a **web** —
many-to-many relationships queried from every direction (students × courses,
parts × suppliers) — fits the [[relational-model]]: normalized tables plus
joins answer *any* direction of question without duplicating data. Document
databases exist because a large class of applications is tree-shaped; the
relational model persists because webs never went away.

## Prerequisites

- [[key-value]] — the atom a document is built from: a mapping of unique keys
  to values with associative get/set/delete; a document is this mapping made
  recursive (values may be mappings), and a collection is key-value at the top
  level (`_id` → document).
- [[relational-model]] — the contrast that defines the model: flat typed
  tuples in normalized relations, related across tables by foreign keys and
  reassembled by joins — exactly the machinery embedding trades away for
  locality and schema flexibility.

## Sources

- MongoDB Manual, "Documents" — https://www.mongodb.com/docs/manual/core/document/ (the document/field/embedded-document structure as realized in MongoDB).
- BSON specification — https://bsonspec.org (the binary JSON encoding: extra types, length-prefixed traversal).
- M. Kleppmann, *Designing Data-Intensive Applications* (O'Reilly, 2017), ch. 2 "Data Models and Query Languages" — the document-vs-relational trade: locality, schema-on-read, and where joins win.
