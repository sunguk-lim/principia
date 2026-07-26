---
name: lock
description: >
  Settle the brain into a coherent, non-redundant, well-grounded state — the `lock` pass. A RE-INDEX:
  it re-derives each node's correct prereq set, ADDING and REMOVING edges (plus merge & demote) via one
  declarative `reindex` per node — not add-only. A FOLDED pass: it reads only the metadata sync emits
  (the review: feedback + one-line node summaries) and never unfolds a body — the LLM judges, brain.py
  executes. Run periodically, after a burst of installs, or before sharing/pushing.
---

# lock — settle the graph (launcher + invariants)

This skill is the **entry point and operating principles**. The full `sync`/`lock` protocol is
canonical in `brain/protocols/EXPLAIN.md` → *"The two authoring passes"*; the tools it drives are
`brain.py` commands. Do not duplicate the protocol here.

> **`lock` is an EXPLICIT procedure, not a vibe.** Every step is either a named `brain.py` command
> (the mechanical part) or a named LLM judgment (the irreducible part). `brain.py` *screens and
> executes*; the LLM *decides*. Nothing reshapes the graph without a reviewable diff gated by
> `audit`. "Explicit" ≠ "deterministic": the judgment stays LLM, but it is invoked at defined points
> on a deterministic worklist.

> **`lock` is FOLDED — it reads metadata, not prose.** A node's body is unfolded only by `sync`, which
> authors it and leaves two artifacts: a one-line `summary:` and `review:` feedback. `lock` reasons
> over the **folded view** — `{title, tags, prereqs, summary}` + feedback — and **exploits progressive
> disclosure**: decide on the **title**; escalate to the **`summary`** when a title is too generic
> (`stack` vs the network stack); open a **body** only for the few cases a summary still can't settle.
> Re-reading every body is the exact anti-pattern this forbids.

> **`lock` is a RE-INDEX — bidirectional, not add-only.** It reconciles each node's *declared* edges
> with what its content actually needs: **add** missing edges, **prune** wrong ones (a homonym like
> `heap → container`), **merge** dupes, **demote** stranded axioms. The LLM declares a node's
> **complete correct prereq set** and issues **one `reindex` call** — `brain.py` diffs it (add + remove
> internally). There are no separate add/remove verbs at the LLM level; re-indexing a node *is*
> declaring its true set.

## When to invoke

"settle / lock / consolidate / dedup / review the graph", after a burst of installs, or before a push.

## The procedure

**1. Gather the worklist — deterministic (`brain.py`), all metadata:**
- `uv run python brain.py feedback` — **primary**: the `review:` notes `sync` left while it had the
  body open. This is where missing/wrong structure was already *seen*; `lock` mostly just applies it.
- `uv run python brain.py dupes [--tag T]` — redundancy candidates over the skeleton + summaries;
  confirm a merge by comparing the two **summaries** (progressive disclosure), not by re-reading bodies.
- `uv run python brain.py audit` — closed-world gate + unlinked-prereq hints.
- `uv run python brain.py reground [--all]` — the **add** direction: missing-edge candidates (prose
  leans on an undeclared node). Mostly residual now that `add` grounds on insertion; matches bare names,
  so confirm each by `summary`.
- `uv run python brain.py reground --prune` — the **remove** direction: suspect *declared* edges
  (declared-but-unlinked, or homonym — cross-field + generic name, like `heap → container`). Confirm
  each by `summary`; a wrong one is dropped simply by re-indexing the node without it.

**2. Judge & act — LLM decides → `brain.py` executes; every change `audit`-gated:**
For each flagged node, determine its **complete correct prereq set** — from its current prereqs + the
add-candidates (`reground`), the prune-suspects (`reground --prune`), the `review:` feedback, and the
`summary`s (folded) — then apply it with **one declarative call**:
- **`brain.py reindex <id> <the full correct set>`** — `brain.py` diffs vs current: **adds** the
  missing, **removes** the wrong (a homonym, an `unused-prereq`, a `mislink`), and strips dropped
  `[[links]]`. This single call subsumes the old add / drop / relink edits.
- **`missing-prereq=X` where X isn't a node yet** → `brain.py add X …` then `sync` X (scaffold the new
  child — the recursion); X then gets `reindex`ed like any node.
- **`overlaps=Y` / a `dupes` hit** → JUDGE by the two summaries; if truly one concept,
  `brain.py merge <from> <into>`.
- **stranded axiom** (a `reground` hit on an axiom) → `brain.py reindex <axiom> <its foundation> --demote`
  (flips `axiom → concept`), then re-`sync` its body.
- Clear each resolved note: `brain.py review <id> --clear`.

**3. Re-gate & converge:**
- After every structural change, `brain.py audit` must pass (closed world, body links ⊆ prereqs).
- Repeat 1–2 until **no feedback is pending and no new merges happen** — the graph is *settled*.
- **Confirm the re-index:** `brain.py diff <base>` — the **`restructured`** block should show exactly the
  edges you added/pruned on each rewired node (and nothing else); `graph --diff <base>` shows it visually.
  This is the check that a `lock` interleave/prune did what you intended, no more.
- Then `brain.py manifest` + `brain.py graph`, and commit (ke-commit conventions).

## Invariants

- **Folded — never unfold a body.** Reason over the folded view (title + summary + edges + feedback)
  with progressive disclosure; a body peek is a last resort on one flagged pair, never a graph-wide
  re-read. Reading prose and emitting feedback are `sync`'s job, not `lock`'s.
- **LLM judges, `brain.py` executes — through ONE edge interface.** Screens only *screen*; the LLM's
  edits to a node's prerequisites go through a **single declarative `reindex`** (it diffs add + remove
  internally) — never separate add/remove verbs. Other commands: `add` (new node), `merge` (dedup),
  `review`. Never hand-mangle a file when a command exists.
- **Screens are candidates, not verdicts.** `dupes` flags name-similar, structurally-similar pairs;
  most are distinct siblings. Confirm each by reading the two nodes; expect to reject most.
- **Never silent.** Every structural change is a reviewable diff and must clear `audit` before commit.
- **Closed-world preserved.** `merge` redirects edges + body links; a drop must not orphan a
  load-bearing link; scaffolding recurses to axioms (per `EXPLAIN.md`).
- **An axiom is provisional.** A floor holds only while nothing beneath it exists; archiving a new
  field can *un-axiom* an older node. `reground` is the re-ascent check that pairs with the descent's
  stop-at-axiom condition — without it, axioms strand wherever field-order left them.
- **Convergence, not one-shot.** `lock` loops with `sync` — a scaffold re-enters `sync`, which may
  emit new feedback. Stop only when settled.

**Definition of done:** `feedback` empty, no confirmed duplicates remain, `reground --prune` surfaces
no wrong edge, `audit` clean, `manifest` + `graph` regenerated, committed. The *rules* live in `protocols/EXPLAIN.md`; this skill says **when to
run `lock` and the order of its explicit steps**.
