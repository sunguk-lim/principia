# CLI Reference

Run commands from a Principia workspace or any directory beneath it:

```bash
uv run principia <command> [options]
```

The CLI discovers the nearest `principia.toml`. To target a different graph, use
`uv run principia --workspace /path/to/graph <command>`. Run
`uv run principia <command> --help` for the complete option list.

## Inspect

| Command | Purpose |
|---|---|
| `show <id>` | Print one node |
| `tree <id>` | Print its recursive prerequisite tree |
| `list [--type T] [--status S] [--tag P]` | Filter nodes by metadata or taxonomy prefix |
| `missing` | List unresolved prerequisite IDs |
| `feedback` | List pending structural review notes |
| `diff <base> [<head>]` | Show nodes, edges, and structures changed between graph states |

Useful examples:

```bash
uv run principia show onnx-runtime
uv run principia tree onnx-runtime
uv run principia list --tag observability
uv run principia diff HEAD~1 --context
```

## Create and Update

| Command | Purpose |
|---|---|
| `add <id>` | Scaffold a concept, paper, or axiom; `new` is an alias |
| `summary <id> <text>` | Set the folded one-line summary |
| `review <id>` | Add or clear typed structural feedback |
| `reindex <id> [prereq ...]` | Set the complete direct-prerequisite set |
| `merge <from> <into>` | Redirect references and fold a duplicate node |
| `remove <id>` | Remove an unreferenced node and its companions |

Example scaffold:

```bash
uv run principia add onnx-runtime \
  --title "ONNX Runtime" \
  --requires onnx,graph-optimization,execution-provider,graph \
  --tags ml/model-portability \
  --sources https://onnxruntime.ai/docs/ \
  --explained
```

`add` records arguments supplied by the caller. It does not choose the concept boundary,
prerequisites, sources, or prose. Use `/install-concept <new-concept>` for the complete agent-driven
workflow.

Destructive or structural commands deserve a graph diff before commit. `remove --force` bypasses the
dependent-node safeguard; use it only when intentionally repairing all affected references.

## Validate and Derive

| Command | Purpose |
|---|---|
| `sync` | Legacy closed-world dependency check |
| `audit` | Validate schema, tags, links, and graph closure |
| `manifest` | Regenerate `MANIFEST.md` |
| `graph` | Regenerate `web/graph.html` |

`audit` is the required correctness gate:

```bash
uv run principia audit
uv run principia manifest
uv run principia graph
```

`graph --diff <base>` renders a visual structural comparison. `--fragment` emits embeddable markup,
and `--out <path>` selects a different output file.

## Structural Maintenance

| Command | Purpose |
|---|---|
| `dupes [--tag P]` | Screen for structurally similar nodes |
| `reground [<id>]` | Find nodes that may need new, removed, or more precise prerequisites |
| `backfill-summaries` | Derive empty summaries from existing bodies |

These commands identify candidates; the agent still judges semantic identity and correct grounding.
`backfill-summaries --force` overwrites existing summaries and should be reviewed carefully.

## Standard Change Sequence

```bash
uv run principia audit
uv run principia manifest
uv run principia graph
uv run principia diff <base>
```

See [Getting started](getting-started.md) for the first-use workflow and
[Architecture](architecture.md) for the agent/engine responsibility boundary.
