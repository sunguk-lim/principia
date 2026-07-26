# Repository Guidelines

## Project Structure & Module Organization

This repository is a closed-world concept graph. `nodes/` is the source of truth: each concept uses `nodes/<id>.md`, with an optional Korean companion (`<id>.ko.md`) and SVG figure (`<id>.svg`). `brain.py` provides the standard-library-only graph CLI. Authoring and visual rules live in `protocols/`; specifications live in `specs/`. The dashboard template and renderer are in `web/`. Treat `MANIFEST.md` and `web/graph.html` as generated outputs, not hand-edited sources.

## Build, Test, and Development Commands

Run commands from the repository root with Python 3 through `uv`:

```bash
uv run python brain.py audit       # validate schemas, links, and graph closure
uv run python brain.py missing     # show unresolved prerequisites
uv run python brain.py manifest    # rebuild MANIFEST.md
uv run python brain.py graph       # rebuild web/graph.html
uv run python brain.py tree <id>   # inspect a concept's dependency tree
```

After changing `nodes/`, run `audit`, then regenerate both derived files. After changing `web/graph.template.html`, regenerate the graph. Open `web/graph.html` directly in a browser; it is self-contained and requires no server.

## Coding Style & Naming Conventions

Use four-space indentation and standard Python conventions in `.py` files. Keep the runtime dependency-free unless a change clearly requires otherwise. Name concept IDs and files in lowercase kebab-case, such as `page-cache.md`. Node frontmatter must match the schema documented in `README.md`; declare one hierarchical tag and ensure every body `[[wikilink]]` appears in `prereqs`. Follow `protocols/EXPLAIN.md` for prose and `protocols/VISUAL_PROTOCOLS.md` for figures.

## Testing Guidelines

There is no separate unit-test suite in this checkout. `uv run python brain.py audit` is the required correctness gate and must pass before submission. For graph changes, also inspect `uv run python brain.py diff <base>` and the regenerated dashboard. Verify generated files are committed whenever their sources change.

## Commit & Pull Request Guidelines

Git history is unavailable in this checkout; the repository documentation specifies Conventional Commit subjects with a concise What/Why description. Work on a branch, stage files individually, and never bypass checks. Pull requests should explain the conceptual change, list added or restructured nodes/edges, and include screenshots for dashboard or figure changes. Link relevant issues and use a merge commit rather than squash-merging.

## Security & Generated Content

Do not add secrets or external network dependencies. Generated pages are designed to work offline. Avoid manually modifying generated artifacts because regeneration will overwrite those edits.
