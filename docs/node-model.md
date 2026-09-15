# Node Model

Every durable concept is stored as `nodes/<id>.md`. The filename and `id` use lowercase kebab case,
such as `computation-graph.md`.

## Schema

```yaml
---
id: onnx-runtime
title: ONNX Runtime
summary: A cross-platform runtime that validates, optimizes, partitions, and executes ONNX graphs.
type: concept
tags: [ml/model-portability]
prereqs: [onnx, graph-optimization, execution-provider, graph]
sources: [https://onnxruntime.ai/docs/]
status: explained
created: 2026-07-28
updated: 2026-07-28
---
```

| Field | Meaning |
|---|---|
| `id` | Stable graph identifier; must match the filename |
| `title` | Human-readable concept name |
| `summary` | One self-contained sentence used as the folded view |
| `type` | `concept`, `paper`, or `axiom` |
| `tags` | Exactly one hierarchical taxonomy home |
| `prereqs` | Direct prerequisite node IDs |
| `sources` | References that support the explanation |
| `status` | `stub` or `explained` |
| `created`, `updated` | ISO dates |

Paper nodes additionally carry `authors` and `year`. During authoring, a node may temporarily carry
typed `review` notes for the structural settle pass.

## Edges and the Closed World

A body reference such as `[[tensor]]` must resolve to an existing canonical node. It must be in
the owning node's prerequisite closure (direct or inherited), or be an explicit optional relation
in `ontology/catalog.json`. `brain.py audit` enforces this rule. A link alone does not make a
concept required learning.

Declare only direct prerequisites. A node inherits deeper grounding through those prerequisites;
copying transitive dependencies into every node makes the graph noisy and harder to maintain.

## Node Types

- **Concept:** a reusable technical idea grounded in prerequisites.
- **Paper:** a publication represented using the paper template and bibliographic metadata.
- **Axiom:** an explicit recursion floor. An axiom may later be demoted when the graph grows enough
  to explain it through more fundamental nodes.

## Folded and Unfolded Views

The title and `summary` form the folded view used for navigation, deduplication, and structural
review. The Markdown body is the unfolded explanation. Summaries should distinguish similarly named
concepts without requiring readers or agents to open every body.

## Optional Companions

The English node is canonical. `nodes/<id>.ko.md` is an optional Korean translation with no
frontmatter; when present, its wikilinks must obey the same closed-world rules. `nodes/<id>.svg` is
an optional figure referenced from the English body and any translations.

Companions never become graph nodes and never receive separate IDs.

## Taxonomy

Each node has one hierarchical home, for example `os/memory` or `ml/llm/inference`. The tag answers
“where does this concept live?”; prerequisite edges express cross-field relationships.

`brain.py list --tag ml` selects every node beneath the `ml/` root, while a deeper prefix narrows the
view:

```bash
uv run principia list --tag ml/model-portability
```

The generated manifest and dashboard roll these paths up into broader fields.

For prose and decomposition rules, follow [`protocols/EXPLAIN.md`](../protocols/EXPLAIN.md). For
figures, follow [`protocols/VISUAL_PROTOCOLS.md`](../protocols/VISUAL_PROTOCOLS.md).

## Canonical identity and typed relationships

Markdown remains authoritative; `ontology/catalog.json` supplies aliases, objectives,
`prerequisiteReasons`, optional `relations`, and normalized-label `disambiguations`.
Resolve a proposed name before creating a node:

```bash
uv run python -m principia_app.ontology resolve "FlashAttention"
```

`brain.py add` performs the same exact canonical/alias collision check before it
writes a file. A collision is rejected; near-name candidates are printed for
editorial review because spelling resemblance alone cannot prove identity.

A synonym belongs in `aliases` on the existing concept, not in a new node. Distinct meanings
sharing a label require a disambiguation entry. Similarity is a review hint, never proof of identity.

When a previously published node is proven to duplicate another node, preserve its article and
set `canonicalId` on that node's catalog record. The duplicate becomes a resolvable historical
source record; its title and aliases resolve to the canonical concept in the ontology projection.
`canonicalId` must point directly to a canonical node (never another alias). Do not use the legacy
`merge` command for this workflow because it deletes the preserved source record.

The closed ontology edge vocabulary is `REQUIRES`, `ALTERNATIVE_TO`, and `CONTRASTS_WITH`.
Only `prereqs` produce `REQUIRES` edges and required roadmap steps. Record a concise reason
for each reviewed prerequisite: what part of the learning objective needs it? The optional types
never expand the required roadmap. Each record has `type`, `target`, and an explanatory `reason`.
Current storage is directed; reverse relationships are not inserted automatically. No generic
`SIMILAR_TO` type is supported.

## Short learning steps

Keep the full reference article in `nodes/<id>.md`. A reviewed core lesson lives in
`lessons/<id>.md`, under the same canonical identity, without frontmatter. Aim for one objective
and 250–500 words (roughly 2–4 minutes), adjusting for mathematical difficulty instead of padding.
Use: Meaning → Mechanism → One example → Check your understanding (with a brief answer).
Keep advanced derivations and implementation detail in the full article. Split only genuinely
independent learning objectives, not synonyms or arbitrary paragraph chunks.

At present, lesson-file presence sets `lessonReviewed`; create these files only after editorial
review. This is a convention, not an independent review-signoff mechanism.

## Semantic extraction and Neo4j projection

Neo4j stores **resolved semantic entities**, not files, headings, paragraphs, or reading pages.
One independently learnable concept has one entity signature. Its source IDs, aliases, source hash,
and content hash are properties used for traceability; none of them is an ontology edge.

The baseline projection resolves every canonical source concept to one entity. A semantic split is
an editorial operation, not an indexing side effect: extract candidate concepts from a source,
resolve each candidate against existing entities, and create a new entity only when it is genuinely
distinct. Every accepted entity needs its own name, learning objective, explanation, and reviewed
placement using the existing closed vocabulary. Similar text, a Markdown heading, and text length
are review signals—not identity evidence.

Use the semantic audit to create an authored review queue:

```bash
uv run python -m principia_app.neo4j semantic-audit
```

The audit reports authored semantic candidates and their source context. It does not create nodes
or relationships; however, projection sync requires a complete, reasoned decision record. There is no fixed word limit: an explanation should be as
concise as its objective permits, while preserving necessary equations, examples, and distinctions.
The entity signature uses canonical name, kind, and domain; the current prose hash is retained
separately for content traceability. Editing an explanation therefore updates the same resolved
entity rather than creating a new concept from a Markdown filename.

### Semantic-review decision record

The audit is a *queue*, not a migration. For every candidate, record one explicit, non-empty
editorial reason with its decision before changing the graph or syncing the projection:

| Decision | Meaning | Graph effect |
| --- | --- | --- |
| `resolve` | The candidate explains an existing entity. | No new entity or edge. |
| `retain` | The candidate is supporting explanation, example, or derivation inside its source entity. | No new entity or edge. |
| `new` | The candidate is a separately learnable concept with its own objective. | Author one new node, resolve its signature, and add only reviewed closed-vocabulary relations. |
| `reject` | The candidate is a heading, repetition, or non-learning material. | No graph effect. |

`new` requires a unique canonical name, objective, independently readable explanation, source
anchors/content hash, identity-collision check, and a reviewed `REQUIRES` placement. It must not
be used merely because a section is long. A source article may resolve entirely to its existing
entity; semantic extraction does not imply a numerical expansion of the graph.

## Legacy command limitations

`merge` does not reconcile catalog metadata or lessons; do not use it for ontology consolidation
until those references are migrated together. `reindex` strips removed prerequisite links even
when they could become optional relations; review both language bodies afterward. `reground`
produces lexical candidates, not proof of a missing prerequisite: comparisons and applications
must not be promoted automatically. After any identity/edge edit, audit the complete projection.
