# Architecture

Principia is a local, graph-native knowledge system. Each durable concept is a node; each declared
prerequisite is a directed edge. The graph lives in plain files and is versioned with Git.

## Closed-World Grounding

A concept may refer only to prerequisites already declared in its metadata. Missing prerequisites
are installed recursively until the explanation reaches explicit axioms. This creates a reviewable
chain from a new idea to the knowledge that supports it.

Closed-world validation proves structural grounding—not factual truth. Sources and author judgment
still matter.

## Two Layers

| Layer | Responsibility |
|---|---|
| Agent | Chooses concept boundaries, prerequisites, taxonomy, sources, and explanatory prose |
| `brain.py` | Records files, validates invariants, computes diffs, and renders derived views |

The boundary is deliberate: semantic judgment remains explicit and reviewable, while correctness
checks and generated outputs remain deterministic and reproducible.

## Data Flow

```text
request
  ↓
compose prerequisite subgraph        agent judgment
  ↓
scaffold and author nodes            nodes/*.md
  ↓
audit graph invariants               brain.py
  ↓
render catalog and dashboard         MANIFEST.md + web/graph.html
  ↓
review structural diff and version   Git
```

When later requests need the same prerequisite, Principia links to the existing node instead of
restating it. New knowledge therefore expands the shared graph and becomes a foundation for future
concepts.

## Storage Model

`nodes/` is the only knowledge source of truth. A concept is an English Markdown file with YAML-like
frontmatter, a grounded body, and `[[wikilink]]` edges. A node may also have a Korean companion and an
SVG figure; both are subsidiary assets, not independent graph nodes.

There is no database server, daemon, or query index. The graph is small enough to read from disk for
each operation, which keeps it portable and easy to inspect.

## Operational Areas

| Path | Responsibility |
|---|---|
| `nodes/` | Knowledge data and optional node assets |
| `brain.py` | Deterministic graph engine and CLI |
| `protocols/` | Canonical authoring and visual policy |
| `.claude/skills/` | Agent workflows that apply the policy |
| `specs/` | Persistent figure-design specifications |
| `web/` | Dashboard renderer, template, and generated page |
| `docs/` | Human-facing product and reference documentation |

## Generated Views and Distribution

`brain.py manifest` derives `MANIFEST.md`; `brain.py graph` derives the self-contained
`web/graph.html`. Git distributes the complete knowledge base and preserves structural history.
GitHub Pages publishes the contents of `web/` and uses the generated graph as its landing page.

The engine and renderer use the Python standard library. Agent authoring is the primary variable
cost; deterministic validation and rendering run locally without model calls.
