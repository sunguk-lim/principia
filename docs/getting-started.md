# Getting Started

Principia stores technical knowledge as a prerequisite graph of Markdown files. The deterministic
CLI reads, validates, and renders that graph; an agent authors the concepts and their relationships.

## Requirements

- Python 3
- [`uv`](https://docs.astral.sh/uv/) to run Python commands
- Git for versioning and graph diffs
- A browser for the self-contained dashboard
- Claude Code when using the bundled concept-installation skill

The runtime uses only the Python standard library. No database server or web server is required.

## Inspect the Existing Brain

Run commands from the repository root:

```bash
uv run principia audit
uv run principia tree onnx-runtime
uv run principia show onnx-runtime
uv run principia list --tag ml/model-portability
```

`audit` is the required correctness gate. `tree` follows a concept toward its prerequisites, while
`list --tag` cuts the graph by taxonomy prefix.

## Install a Concept

In Claude Code, invoke the bundled workflow:

```text
/install-concept <new-concept>
```

For example:

```text
/install-concept ONNX Runtime
```

The skill composes the missing prerequisite subgraph, reuses concepts already present, authors the
new nodes, validates the closed world, and regenerates derived views. The slash command is an agent
command, not a shell command.

`principia add` is a lower-level scaffold operation. It records metadata and edges supplied by the
agent but does not decide prerequisites or write a grounded explanation by itself.

## Build the Local Views

```bash
uv run principia manifest
uv run principia graph
```

Open `web/graph.html` directly in a browser. It contains its data, styles, and scripts inline and
makes no runtime network requests.

## Finish a Change

After changing `nodes/`:

```bash
uv run principia audit
uv run principia manifest
uv run principia graph
uv run principia diff HEAD
```

Review both the concept files and regenerated outputs before committing. See the
[CLI reference](cli-reference.md) for command details and [repository guidelines](../AGENTS.md) for
contribution rules.
