---
id: knowledge-graph
title: Knowledge Graph
summary: A knowledge graph is a graph whose vertices are typed real-world entities and whose edges are labeled, directed relations (subject–predicate–object triples), so the structure stores machine-readable facts you can answer by traversal — not just bare connectivity.
type: concept
tags: [ml/information-retrieval]
prereqs: [graph]
sources:
  - arxiv:2003.02320
status: explained
created: 2026-06-25
updated: 2026-06-25
---

# Knowledge Graph

## Summary

A **knowledge graph** is a [[graph]] put to a particular use: its vertices are *entities* — specific,
identifiable real-world things (the person *Ada Lovelace*, the company *Acme*, the city *Seoul*) — and
its edges are *typed, directed relations* that say **how** two entities are connected (*worksAt*,
*locatedIn*, *bornIn*). Where a plain [[graph]] records only that two things are linked, a knowledge
graph records *what the link means*, so each edge is a stand-alone **fact**. Those facts are written as
**triples** — `(subject, predicate, object)`, e.g. `(Ada, worksAt, Acme)` — and a pile of triples *is*
a directed, edge-labeled graph. Because the relations are machine-readable, you can answer questions by
**walking the edges**: a multi-hop query like "in what city does Ada work?" becomes "follow Ada's
`worksAt` edge to Acme, then Acme's `locatedIn` edge to Seoul." This is the data model behind Google's
Knowledge Graph, Wikidata, and the entity indexes that modern retrieval systems build over a corpus.

## Grounded explanation

**Start from the plain graph — and what it leaves out.** By [[graph]], a graph is a set of *vertices*
(things) and a set of *edges* (pairs of connected things), stored as an adjacency list. That definition
is deliberately bare: an edge `A–B` says only *that* `A` and `B` are connected, never *how* or *what they
are*. For a road map or a friend network that is enough. But if the vertices are a mix of people,
companies, and cities, and the edges mean different things — employment, location, authorship — the
plain graph throws away exactly the information that matters: the **meaning** of each node and each link.
A knowledge graph is the [[graph]] with that meaning added back, under two specializations.

**Specialization 1 — vertices are typed entities.** Each vertex is an *entity*: a particular thing with
a stable **identity** and a **type** (also called its *class*). "Ada Lovelace the person," not the bare
label `A`; "Acme the organization"; "Seoul the city." The identity means the same real-world thing is one
node no matter how many facts mention it (every statement about Ada attaches to the *same* Ada vertex),
and the type (*Person*, *Organization*, *City*) says what *kind* of thing it is. Entities may also carry
*attributes* — literal values that are not themselves entities, like a birth year `1815` — but the heart
of the model is entities joined to other entities.

**Specialization 2 — edges are typed, directed relations.** Each edge carries a **label** naming the
relationship (`worksAt`, `locatedIn`, `authoredBy`) and a **direction**, because relationships are
usually asymmetric: `(Ada, worksAt, Acme)` is true while `(Acme, worksAt, Ada)` is nonsense. This is the
*directed, weighted* extension the [[graph]] node anticipated — except the "weight" on each edge is not a
number but a **relation type**. A labeled directed edge is written as a **triple** `(subject, predicate,
object)`: the *subject* is the entity the edge leaves, the *predicate* is the relation label, the *object*
is the entity the edge enters. `(Ada, worksAt, Acme)` is the edge `Ada --worksAt--> Acme`. Triples are
the universal currency of knowledge graphs: the whole graph is just a *set of triples*, and conversely
any set of triples is a knowledge graph, because each triple is one labeled directed edge between two
vertices.

**The schema (ontology) — optional rules over the types.** On top of the instance-level facts sits an
optional **schema**, or *ontology*: a vocabulary declaring which entity types exist and which relations
are allowed to connect which types — e.g. "a `worksAt` edge goes from a *Person* to an *Organization*,"
"a `City` can be the object of `locatedIn`." The schema does for a knowledge graph what a table's column
definitions do for a spreadsheet: it constrains what is well-formed, lets a machine *validate* new facts,
and lets it *infer* implied ones (if `worksAt` implies the person is `affiliatedWith` that organization,
the inverse or super-relation can be derived without storing it). A knowledge graph can run schema-free
(just accumulate triples) or schema-rich; the more schema, the more a machine can check and reason.

**Why add all this — facts you can query by traversal.** Three payoffs follow, none available from the
bare [[graph]]:

1. *Heterogeneous integration.* Because every fact is a triple over typed entities, data from many
   sources — a personnel database, an org chart, a gazetteer of cities — merges into **one** graph simply
   by sharing entity identities: the same `Acme` vertex that appears in an employment fact also appears in
   a location fact. There is no need to design a joined table in advance.
2. *Multi-hop relational queries.* A question that spans several relationships is answered by **walking a
   path of labeled edges** — exactly the `O(V + E)` traversal the [[graph]] node describes, but now each
   step is chosen *by relation label*. "Which cities employ people Ada knows?" is: from Ada, follow
   `knows` edges to people, from each follow `worksAt` to organizations, from each follow `locatedIn` to
   cities. The graph structure makes the join cheap and the query expressible as a path pattern.
3. *Machine-readable meaning.* Each triple is independently true and interpretable, so a program (or a
   language model) can read a fact, cite it, and combine it with others, instead of re-extracting meaning
   from prose every time.

**Worked instance.** Take five entities and five facts, written as triples:

```
(Ada,  knows,     Bob)
(Ada,  worksAt,   Acme)
(Bob,  worksAt,   Globex)
(Acme, locatedIn, Seoul)
(Globex, locatedIn, Busan)
```

As a [[graph]] this is the adjacency list `{Ada: [Bob, Acme], Bob: [Globex], Acme: [Seoul], Globex:
[Busan]}` — but every edge now also carries its label and points one way. Entities have types: *Ada, Bob*
are `Person`; *Acme, Globex* are `Organization`; *Seoul, Busan* are `City`. Now answer the two-hop query
**"in what city does Ada work?"** purely by traversal: look up `Ada`'s edges, follow the one labeled
`worksAt` to reach `Acme`; look up `Acme`'s edges, follow the one labeled `locatedIn` to reach `Seoul`.
Answer: **Seoul** — obtained by following two labeled edges, never by scanning the other facts. A
three-hop query, **"which cities employ people Ada knows?"**, walks `Ada --knows--> Bob --worksAt-->
Globex --locatedIn--> Busan`, yielding **Busan**. The same bare connectivity a plain [[graph]] would
store could not distinguish "knows" from "works at" from "located in," so it could not answer either
question; the *labels* are what make the path meaningful.

**Where this shows up.** Large public knowledge graphs — Wikidata, DBpedia, Google's Knowledge Graph —
store billions of such triples (the web-standard serialization, RDF, is literally a triple format).
Inside an application, a knowledge graph is the structured backbone for entity search ("show everything
related to this customer"), for combining siloed databases under shared entity identities, and — when the
entities and relations are *extracted from a document corpus or an agent's history* — for retrieval and
memory systems that reason over relationships rather than over isolated text chunks.

## Prerequisites

- [[graph]]

## Sources

- `arxiv:2003.02320` — Hogan, Blomqvist, Cochez, et al., "Knowledge Graphs" (ACM Computing Surveys,
  2021): the graph-based data model (entities as nodes, directed labeled edges), triples, schema/ontology,
  and knowledge-graph creation, enrichment, and applications.
