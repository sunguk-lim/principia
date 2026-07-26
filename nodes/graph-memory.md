---
id: graph-memory
title: Graph Memory
summary: Graph memory is agent long-term memory whose store is a knowledge graph — entities and typed relations extracted from the agent's history — so recall is a multi-hop, time-aware traversal over connected facts instead of a flat similarity lookup of independent text chunks.
type: concept
tags: [ml/agents]
prereqs: [agent-memory, knowledge-graph]
sources:
  - arxiv:2404.16130
  - arxiv:2501.13956
status: explained
created: 2026-06-25
updated: 2026-06-25
---

# Graph Memory

## Summary

**Graph memory** is a form of [[agent-memory]] in which the agent's long-term store is not a flat pile
of text snippets but a [[knowledge-graph]]: as the agent converses and acts, it **extracts entities and
typed relations** from what it sees and accumulates them as triples — `(User, worksAt, Acme)`,
`(Acme, locatedIn, Seoul)` — into one growing graph of its own experience. Recall then becomes **graph
traversal**: instead of fetching the handful of past snippets that look most similar to the current
question, the agent locates the relevant entities and **walks the labeled edges** around them, returning
a connected neighborhood of facts. This buys three things ordinary [[agent-memory]] struggles with —
**multi-hop relational** recall (answers that require chaining several facts), **deduplication and
update** (because the same real-world thing is one node, repeated mentions merge and corrections
overwrite rather than accumulate), and **temporal reasoning** (edges can be time-stamped, so the store
knows what *was* true versus what is true *now*). It is the architecture behind systems like Microsoft's
GraphRAG and Zep/Graphiti.

## Grounded explanation

**Start from ordinary agent memory and its blind spot.** By [[agent-memory]], a long-horizon agent keeps
a two-tier memory: a small live working set (the short-term tier) plus an external long-term store it
**writes** salient items to and later **recalls** from by embedding the current situation and pulling
back the stored items whose vectors are most *similar* — retrieval-augmented generation pointed at the
agent's own past. That design has a structural blind spot: the long-term store is **flat**. Each saved
item is an independent chunk; the store records *that* "the user said they work at Acme" and *that* "Acme
is in Seoul" as two unrelated entries, but nothing connecting them. Three problems follow. (1) A question
whose answer spans several facts — "what city do I work in?" — has no single chunk that is similar to it,
so similarity search may miss the chain. (2) The same entity mentioned across many sessions produces many
near-duplicate chunks, and there is no notion that they are *about the same thing*. (3) When a fact
changes ("I switched jobs"), the old chunk still sits in the store, equally retrievable, so stale and
current statements compete.

**The shift: make the long-term store a knowledge graph.** Graph memory replaces the flat store with a
[[knowledge-graph]]. The two operations of [[agent-memory]] are re-expressed over it:

- **Write = extract and merge triples.** As the agent works, an extraction step (typically the language
  model itself) reads each new stretch of interaction and emits *facts as triples* — `(subject,
  predicate, object)` over typed entities, exactly the [[knowledge-graph]] data model. Crucially, the
  upsert **merges on entity identity**: the `User` node from session 1 is the *same* node updated in
  session 12, so a new fact about the user attaches to the existing vertex instead of creating a
  duplicate. This is the deduplication the flat store lacked — it falls out for free from the
  [[knowledge-graph]]'s rule that one real-world thing is one vertex.
- **Read = find entry points, then traverse.** To recall, the agent first locates the **entry entities**
  relevant to the current turn — by name match or by the same embedding-similarity search
  [[agent-memory]] already uses, now applied to *find nodes* rather than to fetch chunks — and then
  **walks the labeled edges** out from them, gathering a connected sub-graph. The retrieved sub-graph
  (as triples, or linearized into a few sentences) is injected back into the live window, the short-term
  tier of [[agent-memory]], before the model answers. Because traversal follows *relation labels*, it
  assembles exactly the chain a multi-hop question needs — the `O(V + E)` walk from [[knowledge-graph]],
  not a similarity guess.

**Adding time — the temporal knowledge graph.** The update problem is solved by letting edges carry
**validity time**. Instead of deleting the old fact when the user changes jobs, graph memory records the
new edge `(User, worksAt, Globex)` as valid *from now* and marks the old `(User, worksAt, Acme)` edge as
having *ended* at that moment. The graph thus stores history: a query for "where do I work **now**?"
follows only currently-valid edges and reaches Globex, while "where did I work **before**?" can still
recover Acme. This is the temporal-knowledge-graph idea Zep/Graphiti builds on — the flat store, with no
structure to attach a time interval to a *relationship*, cannot make this distinction cleanly.

**Worked instance — across two sessions.** *Session 1.* The user says, "I work at Acme, and Acme is in
Seoul." Extraction emits two triples and merges them into the graph:
`(User, worksAt, Acme)[valid from S1]` and `(Acme, locatedIn, Seoul)`. *Session 2*, much later (the raw
text of session 1 has long since scrolled out of the window, per [[agent-memory]]). The user says, "I've
moved to Globex." Extraction emits `(User, worksAt, Globex)[valid from S2]` and, finding the `User`
vertex already present, **attaches** the new edge to it while marking the prior `worksAt → Acme` edge
**ended at S2**. Now the user asks, **"what city do I work in now?"** Graph memory finds the `User` entry
node, walks the *currently-valid* `worksAt` edge to `Globex`, then `Globex`'s `locatedIn` edge — a clean
two-hop answer (and if `Globex --locatedIn--> Busan` is known, the answer is *Busan*). Contrast the flat
[[agent-memory]] store: it would hold "I work at Acme," "Acme is in Seoul," and "I've moved to Globex" as
three independent chunks; a similarity search for "what city do I work in" has no chunk that states the
city directly, may surface the **stale** Acme/Seoul pair, and has no mechanism to know Globex superseded
Acme. The graph answers correctly because *identity* merged the user's facts and *time* ordered them.

**Why, and the cost.** Graph memory trades a heavier write path for a sharper read path. The write cost
is real: turning free-form interaction into clean triples is an extra, error-prone LLM step, and
mis-extracted or mis-merged entities corrupt the graph in ways a flat store's independent chunks cannot.
What you buy is recall that is *relational* (multi-hop answers by traversal), *consolidated* (one node
per thing, so memory does not bloat with duplicates), and *temporally honest* (current vs. historical
facts kept distinct) — precisely the capabilities long-running, multi-session agents need and flat
vector recall cannot provide. Real systems differ in emphasis: GraphRAG builds an entity
[[knowledge-graph]] over a document corpus and pre-summarizes its clusters to answer global,
corpus-spanning questions; Zep/Graphiti maintains a *temporal* [[knowledge-graph]] as a live memory layer
for an agent's accumulating conversation and business data.

One closing parallel: this very brain is a [[knowledge-graph]] of concepts that an assistant writes to
and traverses across sessions — a graph-structured instance of the long-term [[agent-memory]] described
here.

## Prerequisites

- [[agent-memory]]
- [[knowledge-graph]]

## Sources

- `arxiv:2404.16130` — Edge, Trinh, Cheng, Bradley, et al., "From Local to Global: A Graph RAG Approach
  to Query-Focused Summarization": constructing an entity knowledge graph from a corpus and summarizing
  its communities to answer global questions (GraphRAG).
- `arxiv:2501.13956` — Rasmussen, Paliychuk, Beauvais, Ryan, Chalef, "Zep: A Temporal Knowledge Graph
  Architecture for Agent Memory": the Graphiti engine maintaining a temporally-aware knowledge graph as
  an agent memory layer.
