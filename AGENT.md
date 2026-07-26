# AGENT.md — orienting a session in this repo

> **Audience: AI coding agents, not humans.** This file briefs an agent session operating on the repo
> — what lives where, the workflow, and how to finish a change. It assumes you'll *run* commands and
> *land* changes. **Humans → [`README.md`](README.md)** for the prose overview.

`aicp-connectome` is a **learning brain**: a closed-world concept graph. This file orients a fresh
session and **points** to the canonical docs (it does not duplicate them). Expect it to grow — add
sections as the repo does.

## What it is
A second brain for technical concepts. One concept = one node (`nodes/<id>.md`); a `[[link]]` in a
body **is** a graph edge; the world stays **closed** — every prerequisite resolves, recursively, down
to axioms. `nodes/` is the **source of truth**; `MANIFEST.md` and `web/graph.html` are **generated**.

## Composition — what lives where
| Path | Role |
|------|------|
| `nodes/` | **source of truth** — one `.md` per concept (+ `<id>.ko.md` Korean body, optional `<id>.svg` figure) |
| `brain.py` | the **deterministic engine** + CLI (Python stdlib only; `uv run python brain.py …`) |
| `README.md` | reference — the pieces: data model, node schema, taxonomy, command list |
| `protocols/EXPLAIN.md` | **authoring rules** — closed-world law, Depth, decomposition, the `sync`/`lock` passes |
| `protocols/VISUAL_PROTOCOLS.md` | figure-drawing rules |
| `.claude/skills/install-concept/` | the **install workflow** (add / explain a concept) |
| `.claude/skills/lock/` | the `lock` settle pass |
| `.claude/skills/draw-brain-figure/` | the figure-drawing workflow |
| `MANIFEST.md` | **generated** catalog (stats + frontier + node list) |
| `web/graph.html` | **generated** dashboard — **deployed to GitHub Pages** |
| `web/graph.template.html` | the dashboard template `graph.html` is rendered from |

## Two layers
- **`brain.py`** — deterministic: stores / validates (`audit`) / indexes (`manifest`) / renders (`graph`). It **never reasons**.
- **You (the LLM)** — author: choose concepts, edges (`prereqs` / `[[links]]`), tags; write prose. `audit` is the one correctness check that does **not** depend on your judgment.

## The workflow
To add or explain a concept, invoke the **`install-concept`** skill. In brief: **compose** the
add-queue (decide the whole sub-graph) → **scaffold** (create the queued nodes) → **sync** (author the
bodies) → rare **ground-check** / **lock** (settle). The procedure lives in the skill; the rules in
`protocols/EXPLAIN.md`.

## The epilogue — finish every change
Generated files and the live site do **not** update themselves:
- Changed `nodes/`? → `brain.py audit` (the gate — must pass) → `brain.py manifest` → `brain.py graph`.
- Changed `web/graph.template.html`? → `brain.py graph` (regenerates the deployed `graph.html`).
- **Review the delta**: `brain.py diff <base>` (e.g. `brain.py diff HEAD~1`) — see which nodes/edges the change **adds/removes**, and which existing nodes were **restructured** (the interleave/prune signal). `brain.py graph --diff <base>` renders the same delta visually.
- Then **branch → PR → merge to `main`** (land the PR as a **merge commit** — `gh pr merge <n> --merge` — **never squash**), which **auto-deploys GitHub Pages** (`web/graph.html` is the live dashboard). Never land an audit-failing state on `main`. On the PR, the **`graph-gate.yml`** workflow (report-only) posts the text delta to the Checks **Summary** and attaches a visual **`graph-diff`** artifact.
- **After the merge, prune the branch.** PRs land by **merge commit** (never squash), so the branch is a real ancestor of `main` and `git branch -d` recognizes it as merged; GitHub deletes the remote branch on merge — clean up the leftover local branch, its stale `gone` remote-tracking ref, and any worktree: `git branch -d <branch>` → `git fetch --prune` (→ `git worktree remove <path>` if one was used).

## Conventions
- **ke-commit**: Conventional Commit + Korean What/Why + the AI footer; **stage files individually**; no `--amend`, no `--no-verify`; never commit scratch (`tmp.py`, …).
- **Merge commits, never squash**: land every PR with a merge commit (`gh pr merge <n> --merge`), **not** `--squash` — preserves the branch's individual commits and keeps it a real ancestor of `main` (so `git branch -d` detects the merge).
- **Branch-first**: never edit or commit on `main` directly.
- **Keep the lifecycle in sync**: it is depicted in the skill's ASCII diagram **and** the Pages `(?)` overlay (`web/graph.template.html`) — change both. Canonical stage names: `compose → scaffold → sync → audit → manifest → graph → diff → commit` (with `ground-check` / `lock` as the rare settle-loop).

## Command quick-ref
```bash
uv run python brain.py add <id> --title "…" --requires a,b --tags <path>   # create a node
uv run python brain.py audit        # the commit gate — must pass
uv run python brain.py missing      # the recursion frontier
uv run python brain.py manifest     # regenerate MANIFEST.md
uv run python brain.py graph        # regenerate web/graph.html (the deployed dashboard)
uv run python brain.py diff <base> [<head>]   # structural delta (nodes/edges +/-, restructured); `graph --diff <base>` = visual
uv run python brain.py dupes | reground | reindex | merge | list | show | tree
```
