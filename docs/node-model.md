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

A synonym belongs in `aliases` on the existing concept, not in a new node. Distinct meanings
sharing a label require a disambiguation entry. Similarity is a review hint, never proof of identity.

Only `prereqs` produce `REQUIRES` edges and required roadmap steps. Record a concise reason
for each reviewed prerequisite: what part of the learning objective needs it? Optional types are
`ALTERNATIVE_TO`, `CONTRASTS_WITH`, and `APPLIES_TO`; each record has `type`, `target`, and
an explanatory `reason`. They never expand the required roadmap. Current storage is directed;
reverse relationships are not inserted automatically. No generic `SIMILAR_TO` type is supported.

## Short learning steps

Keep the full reference article in `nodes/<id>.md`. A reviewed core lesson lives in
`lessons/<id>.md`, under the same canonical identity, without frontmatter. Aim for one objective
and 250–500 words (roughly 2–4 minutes), adjusting for mathematical difficulty instead of padding.
Use: Meaning → Mechanism → One example → Check your understanding (with a brief answer).
Keep advanced derivations and implementation detail in the full article. Split only genuinely
independent learning objectives, not synonyms or arbitrary paragraph chunks.

At present, lesson-file presence sets `lessonReviewed`; create these files only after editorial
review. This is a convention, not an independent review-signoff mechanism.

## Legacy command limitations

`merge` does not reconcile catalog metadata or lessons; do not use it for ontology consolidation
until those references are migrated together. `reindex` strips removed prerequisite links even
when they could become optional relations; review both language bodies afterward. `reground`
produces lexical candidates, not proof of a missing prerequisite: comparisons and applications
must not be promoted automatically. After any identity/edge edit, audit the complete projection.
