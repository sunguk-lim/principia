# Principia Documentation

Principia separates its product overview from its operational reference. Start with the guide that
matches what you are trying to do.

## Start Here

| Goal | Guide |
|---|---|
| Run Principia and inspect the graph | [Getting started](getting-started.md) |
| Understand the system design | [Architecture](architecture.md) |
| Author or validate a concept node | [Node model](node-model.md) |
| Use `brain.py` | [CLI reference](cli-reference.md) |
| Contribute code or documentation | [Repository guidelines](../AGENTS.md) |

## Canonical Sources

Some repository documents are executable policy rather than general product documentation:

| Path | Owns |
|---|---|
| [`protocols/EXPLAIN.md`](../protocols/EXPLAIN.md) | Closed-world authoring, decomposition, depth, and settle rules |
| [`protocols/VISUAL_PROTOCOLS.md`](../protocols/VISUAL_PROTOCOLS.md) | Figure composition and animation rules |
| [`.claude/skills/install-concept/`](../.claude/skills/install-concept/) | The end-to-end concept installation workflow |
| [`.claude/skills/lock/`](../.claude/skills/lock/) | Structural reconciliation workflow |
| [`.claude/skills/draw-brain-figure/`](../.claude/skills/draw-brain-figure/) | Figure-production workflow |
| [`specs/`](../specs/) | Persistent figure specifications and training examples |

## Source and Generated Content

`nodes/` is the knowledge source of truth. `MANIFEST.md` and `web/graph.html` are generated views;
rebuild them with `brain.py manifest` and `brain.py graph` rather than editing them manually.
