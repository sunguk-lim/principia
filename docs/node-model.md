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

A body reference such as `[[tensor]]` is a graph edge. Every body wikilink must resolve to an existing
node and appear in the owning node's `prereqs` list. `brain.py audit` enforces both conditions.

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
uv run python brain.py list --tag ml/model-portability
```

The generated manifest and dashboard roll these paths up into broader fields.

For prose and decomposition rules, follow [`protocols/EXPLAIN.md`](../protocols/EXPLAIN.md). For
figures, follow [`protocols/VISUAL_PROTOCOLS.md`](../protocols/VISUAL_PROTOCOLS.md).
