#!/usr/bin/env python3
"""brain.py — a recursive concept-dependency graph for learning.

The rule of this brain: a concept may only be explained using prerequisite
concepts that already exist as nodes. When a prerequisite is missing, it must
be archived first — recursively — until reaching axioms (e.g. arithmetic),
which are explicitly stored as `type: axiom` and have no prerequisites.

The script is the GRAPH ENGINE (store nodes, walk dependencies, show the
frontier). The reasoning — choosing prerequisites and writing the grounded
explanations — is done by the human/assistant editing the node bodies.

Run with:  uv run python brain.py <command> [args]

A uv-style interface for a "concept package manager":
  add <id> [--type concept|paper|axiom] [--requires a,b,c]
           [--sources s1,s2] [--title T] [--explained]   Install (create) a concept.
  remove <id> [--force]               Uninstall a concept + its figure/spec (refuses if depended on).
  sync                                Check every dependency resolves (closed world).
  audit                               Deep check: body-link discipline, tags, closed world.
  feedback                            List pending structural feedback (review notes) for lock.
  review <id> [--add t=v] [--clear]   Record/clear a node's review notes (sync's feedback channel).
  summary <id> "text"                 Set a node's one-line summary (the folded view lock reads).
  backfill-summaries [--force]        Populate empty summaries from each node's first body paragraph.
  dupes [--tag T] [--threshold N]     Screen for redundancy candidates (structural; for lock).
  merge FROM INTO                     Fold one node into another (redirect edges + body links).
  reindex NODE [PREREQ...]            Set a node's prereq set to EXACTLY this list (declarative; diffs add+remove).
  reground [<id>] [--all] [--prune]   Screen missing edges (add) or, with --prune, suspect declared edges (for lock).
  manifest                            Regenerate the catalog (MANIFEST.md).
  diff <ref1> [<ref2>]                Structural graph delta between two git revisions (nodes/edges +/-).
  tree <id>                           Show the dependency tree.
  list [--type T] [--status S]        List installed concepts.
  show <id>                           Print one concept.

Aliases: `new` = add; `missing` is the unresolved part of `sync`.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NODES = ROOT / "nodes"
SPECS = ROOT / "specs"
MANIFEST = ROOT / "MANIFEST.md"
WEB = ROOT / "web"

TYPES = ["concept", "paper", "axiom"]
STATUSES = ["stub", "explained"]

BODY_TEMPLATE = (
    "## Summary\n\n_One-paragraph, plain explanation._\n\n"
    "## Grounded explanation\n\n"
    "_Explain using ONLY the prerequisite nodes below. Link them as [[id]]._\n\n"
    "## Prerequisites\n\n{prereq_links}\n\n"
    "## Sources\n\n{source_links}\n"
)

AXIOM_TEMPLATE = (
    "## Axiom\n\n_This is a recursion floor — assumed, not explained further._\n\n"
    "## Why stop here\n\n\n"
)

PAPER_TEMPLATE = (
    "## Problem\n\n_What limitation does this paper address?_\n\n"
    "## Key idea\n\n_The core contribution in one paragraph, grounded in the "
    "prerequisite nodes below._\n\n"
    "## Contributions\n\n- \n\n"
    "## Key equations\n\n_Use the visual protocol: symbol table → equation → "
    "ASCII shape._\n\n"
    "## Builds on (papers)\n\n_Prior papers this extends, as [[id]]._\n\n"
    "## Prerequisites\n\n{prereq_links}\n\n"
    "## Sources\n\n{source_links}\n"
)


def today() -> str:
    return _dt.date.today().isoformat()


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s)[:60] or "untitled"


def _quote_scalar(v: str) -> str:
    """Quote a frontmatter scalar so it stays strict-YAML valid. An unquoted ': ' (or a
    trailing ':') is a mapping indicator and breaks real YAML parsers; wrap such values in a
    double-quoted scalar. Flow lists ('[...]'), empty values, and already-quoted values pass through."""
    if not v or v[0] in "'\"[":
        return v
    if ": " in v or v.endswith(":"):
        return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return v


def _unquote_scalar(v: str) -> str:
    """Inverse of _quote_scalar for the lenient reader: unwrap a value enclosed in matching
    single/double quotes (with standard YAML escape handling). Non-quoted values pass through."""
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace("\\\\", "\x00").replace('\\"', '"').replace("\x00", "\\")
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return v


def parse_frontmatter_text(text: str) -> dict:
    """Parse YAML frontmatter from raw file text (the lenient reader).

    Operates on any string — a file's contents or `git show <ref>:<path>` output — so the
    graph can be reconstructed at an arbitrary revision without a checkout.
    """
    meta: dict = {}
    if not text.startswith("---"):
        return meta
    end = text.find("\n---", 3)
    if end == -1:
        return meta
    for line in text[3:end].strip("\n").splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = _unquote_scalar(val.strip())
    return meta


def parse_frontmatter(path: Path) -> dict:
    return parse_frontmatter_text(path.read_text(encoding="utf-8"))


def parse_list(raw: str) -> list[str]:
    """Parse a frontmatter list like '[a, b, c]' into ['a','b','c']."""
    raw = (raw or "").strip().lstrip("[").rstrip("]")
    return [x.strip() for x in raw.split(",") if x.strip()]


def split_tag(tag: str) -> list[str]:
    """Split a hierarchical tag path 'os/memory' -> ['os', 'memory']."""
    return [p for p in tag.split("/") if p]


def tag_rollup(leaf_counts: dict[str, int]) -> dict[str, int]:
    """Sum leaf-tag counts into every ancestor prefix.

    {'os/memory': 12, 'os/kernel': 12} -> {'os': 24, 'os/memory': 12, 'os/kernel': 12}.
    Lets a path-style taxonomy report both the granular leaf and the rolled-up field.
    """
    roll: dict[str, int] = {}
    for tag, c in leaf_counts.items():
        parts = split_tag(tag)
        for i in range(1, len(parts) + 1):
            prefix = "/".join(parts[:i])
            roll[prefix] = roll.get(prefix, 0) + c
    return roll


def node_path(node_id: str) -> Path:
    return NODES / f"{node_id}.md"


def companion_paths(node_id: str) -> tuple[Path, ...]:
    """A node's subsidiary files — the figure, the Korean body, the figure spec.
    Removed/merged with the node, never parsed as nodes."""
    return (NODES / f"{node_id}.svg", NODES / f"{node_id}.ko.md",
            SPECS / f"{node_id}.spec.md")


def all_nodes() -> dict[str, dict]:
    """Map node id -> frontmatter dict."""
    if not NODES.exists():
        return {}
    out = {}
    for p in NODES.glob("*.md"):
        if p.name.endswith(".ko.md"):    # Korean body companion, not a node
            continue
        meta = parse_frontmatter(p)
        out[meta.get("id", p.stem)] = meta
    return out


def _git(*args: str) -> str:
    """Run a read-only git command rooted at ROOT and return stdout (raises on failure)."""
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def nodes_at_ref(ref: str) -> dict[str, dict]:
    """Map node id -> frontmatter at a git revision, WITHOUT a checkout.

    The revision-scoped mirror of all_nodes(): lists nodes/*.md at `ref` (git ls-tree) and
    reads each blob (git show), parsing frontmatter from the string. `.svg` figures and
    `.ko.md` companions are skipped (not graph data).
    """
    try:
        listing = _git("ls-tree", "-r", "--name-only", ref, "nodes/")
    except subprocess.CalledProcessError as e:
        sys.exit(f"git could not read '{ref}': {(e.stderr or '').strip() or e}\n"
                 f"(a shallow clone? in CI use actions/checkout with fetch-depth: 0)")
    out: dict[str, dict] = {}
    for path in listing.splitlines():
        if not path.endswith(".md") or path.endswith(".ko.md"):
            continue
        meta = parse_frontmatter_text(_git("show", f"{ref}:{path}"))
        stem = path.rsplit("/", 1)[-1][:-3]     # nodes/foo.md -> foo
        out[meta.get("id", stem)] = meta
    return out


def graph_edges(nodes: dict[str, dict]) -> set:
    """The directed edge set {(source, prereq)} within the closed world.

    A prereq referencing a non-existent node is dropped — identical to the `if p in ids`
    filter in web/render.build_graph_data (line ~60), so the diff and the rendered
    dashboard always agree on what counts as an edge.
    """
    ids = set(nodes)
    return {(i, p) for i, m in nodes.items()
            for p in parse_list(m.get("prereqs", "")) if p in ids}


def cmd_new(args) -> None:
    if args.type not in TYPES:
        sys.exit(f"Unknown type '{args.type}'. Choose from: {', '.join(TYPES)}")
    node_id = slugify(args.id)
    NODES.mkdir(parents=True, exist_ok=True)
    path = node_path(node_id)
    if path.exists():
        sys.exit(f"Node already exists: {path}")

    title = args.title or args.id
    raw_prereqs = args.prereqs or getattr(args, "requires", "")
    prereqs = parse_list(raw_prereqs) if args.type != "axiom" else []
    sources = parse_list(args.sources)
    tags = parse_list(getattr(args, "tags", ""))
    status = "explained" if args.explained else "stub"
    if args.type == "axiom":
        status = "explained"

    meta_extra = ""
    if args.type == "paper":
        if args.authors:
            meta_extra += f"authors: {args.authors}\n"
        if args.year:
            meta_extra += f"year: {args.year}\n"

    frontmatter = (
        "---\n"
        f"id: {node_id}\n"
        f"title: {title}\n"
        f"summary:\n"
        f"type: {args.type}\n"
        f"tags: [{', '.join(tags)}]\n"
        f"prereqs: [{', '.join(prereqs)}]\n"
        f"sources: [{', '.join(sources)}]\n"
        f"{meta_extra}"
        f"status: {status}\n"
        f"created: {today()}\n"
        f"updated: {today()}\n"
        "---\n\n"
        f"# {title}\n\n"
    )
    prereq_links = "\n".join(f"- [[{p}]]" for p in prereqs) or "_none yet_"
    source_links = "\n".join(f"- {s}" for s in sources) or "_none_"
    if args.type == "axiom":
        body = AXIOM_TEMPLATE
    elif args.type == "paper":
        body = PAPER_TEMPLATE.format(prereq_links=prereq_links,
                                     source_links=source_links)
    else:
        body = BODY_TEMPLATE.format(prereq_links=prereq_links,
                                    source_links=source_links)

    path.write_text(frontmatter + body, encoding="utf-8")
    rebuild_manifest()
    print(f"Created {path}")
    # Surface the new frontier immediately.
    missing = compute_missing()
    fresh = [m for m in (prereqs) if m in missing]
    if fresh:
        print("Next to archive (missing prereqs): " + ", ".join(fresh))


def cmd_show(args) -> None:
    path = node_path(slugify(args.id))
    if not path.exists():
        sys.exit(f"No node '{args.id}'. Missing? run: brain.py missing")
    print(path.read_text(encoding="utf-8"))


def cmd_tree(args) -> None:
    nodes = all_nodes()
    start = slugify(args.id)
    if start not in nodes:
        sys.exit(f"No node '{start}'.")

    def walk(nid: str, prefix: str, visited: set) -> None:
        meta = nodes.get(nid)
        if meta is None:
            print(f"{prefix}{nid}  ⚠️  MISSING (archive me)")
            return
        tag = {"axiom": "  🛑 axiom", "paper": "  📄 paper"}.get(
            meta.get("type", ""), "")
        if meta.get("status") == "stub":
            tag += "  (stub)"
        print(f"{prefix}{nid}{tag}")
        if nid in visited:
            print(f"{prefix}  ↑ (cycle)")
            return
        visited = visited | {nid}
        prereqs = parse_list(meta.get("prereqs", ""))
        for p in prereqs:
            walk(p, prefix + "    ", visited)

    walk(start, "", set())


def compute_missing() -> set[str]:
    nodes = all_nodes()
    referenced: set[str] = set()
    for meta in nodes.values():
        referenced.update(parse_list(meta.get("prereqs", "")))
    return {r for r in referenced if r not in nodes}


def cmd_missing(_args) -> None:
    missing = sorted(compute_missing())
    if not missing:
        print("✅ Frontier empty — every prerequisite is archived "
              "(world is closed).")
        return
    print("Recursion frontier — referenced but not yet archived:")
    for m in missing:
        print(f"  ⚠️  {m}")


def cmd_feedback(_args) -> None:
    """List pending structural feedback — `review:` notes that `sync` emits for `lock` to act on.

    A note is a `type=target` pair in a node's `review:` frontmatter list (e.g.
    `missing-prereq=gpu-memory-spaces`, `overlaps=paged-attention`, `unused-prereq=…`,
    `mislink=…`, `regrounding=self`). `=` (not `: `) keeps notes safe for the frontmatter parser
    and the audit. This is a deterministic worklist, like the frontier: `sync` writes the notes,
    `lock` reflects on them — reconciling structure (merge / relink / **scaffold** missing prereqs)
    — and clears the ones it resolves.
    """
    nodes = all_nodes()
    pending = [(nid, parse_list(nodes[nid].get("review", ""))) for nid in sorted(nodes)]
    pending = [(nid, notes) for nid, notes in pending if notes]
    if not pending:
        print("✅ No pending structural feedback.")
        return
    total = sum(len(n) for _, n in pending)
    print(f"Pending structural feedback — {total} note(s) across {len(pending)} node(s):")
    for nid, notes in pending:
        print(f"  {nid}:")
        for note in notes:
            print(f"    - {note}")
    print("\nResolve with `lock`: reflect, reconcile structure (merge / relink / scaffold), "
          "then clear the notes.")


def cmd_list(args) -> None:
    nodes = all_nodes()
    rows = sorted(nodes.values(), key=lambda m: m.get("id", ""))
    if args.type:
        rows = [m for m in rows if m.get("type") == args.type]
    if args.status:
        rows = [m for m in rows if m.get("status") == args.status]
    if getattr(args, "tag", None):
        q = args.tag
        rows = [m for m in rows if any(t == q or t.startswith(q + "/")
                                       for t in parse_list(m.get("tags", "")))]
    if not rows:
        print("No matching nodes.")
        return
    for m in rows:
        n = len(parse_list(m.get("prereqs", "")))
        print(f"{m.get('type','?'):8} {m.get('status','?'):9} "
              f"{m.get('id',''):30} ({n} prereqs)  {m.get('title','')}")


def rebuild_manifest() -> None:
    nodes = all_nodes()
    missing = compute_missing()
    n_axioms = sum(1 for m in nodes.values() if m.get("type") == "axiom")

    lines = ["# 🧠 Learning Brain — Concept Graph", "",
             f"_Last rebuilt: {today()}_", "",
             f"**{len(nodes)}** nodes · **{n_axioms}** axioms · "
             f"**{len(missing)}** on the frontier", ""]

    if missing:
        lines += ["## ⚠️ Frontier (archive next)", ""]
        lines += [f"- `{m}`" for m in sorted(missing)]
        lines.append("")
    else:
        lines += ["✅ World is closed — no missing prerequisites.", ""]

    referenced = set()
    for m in nodes.values():
        referenced.update(parse_list(m.get("prereqs", "")))
    roots = sorted(i for i in nodes if i not in referenced)
    leaves = sorted(i for i, m in nodes.items()
                    if not parse_list(m.get("prereqs", "")))
    lines += [f"## 🌳 Parent (root) nodes — top-level, required by nothing "
              f"({len(roots)})", ""]
    lines += ([f"- [{nodes[i].get('title', i)}](nodes/{i}.md)" for i in roots]
              or ["_none_"])
    lines += ["", f"## 🍃 Leaf nodes — no prerequisites · the axioms / "
              f"recursion floors ({len(leaves)})", ""]
    lines += ([f"- [{nodes[i].get('title', i)}](nodes/{i}.md)" for i in leaves]
              or ["_none_"])
    lines.append("")

    headings = {"paper": "## 📄 Papers", "concept": "## 🔷 Concepts"}
    for typ, heading in headings.items():
        bucket = sorted([m for m in nodes.values() if m.get("type") == typ],
                        key=lambda m: m.get("id", ""))
        if not bucket:
            continue
        lines += [heading, ""]
        for m in bucket:
            stub = " _(stub)_" if m.get("status") == "stub" else ""
            lines.append(f"- [{m.get('title', m.get('id'))}]"
                         f"(nodes/{m.get('id')}.md){stub}")
        lines.append("")

    tagmap: dict = {}
    for m in nodes.values():
        for t in parse_list(m.get("tags", "")):
            tagmap.setdefault(t, []).append(m)
    if tagmap:
        roll = tag_rollup({t: len(ms) for t, ms in tagmap.items()})
        tops = sorted({split_tag(t)[0] for t in tagmap})
        lines += [f"## 🏷️ By field (cut the graph) — {len(tops)} top-level / "
                  f"{len(tagmap)} leaf fields", ""]

        def render(ms):
            ms = sorted(ms, key=lambda m: m.get("id", ""))
            return ", ".join(f"[{m.get('title', m.get('id'))}]"
                             f"(nodes/{m.get('id')}.md)" for m in ms)

        for top in tops:
            leaves = sorted(t for t in tagmap if split_tag(t)[0] == top)
            if leaves == [top]:                      # top-level leaf, no children
                lines += [f"### {top} ({roll[top]})", "", render(tagmap[top]), ""]
                continue
            lines += [f"### {top} ({roll[top]})", ""]
            for t in leaves:                         # show the leaf's path, indented
                depth = len(split_tag(t)) - 1
                lines += [f"{'  ' * depth}- **{t}** ({len(tagmap[t])}) — "
                          f"{render(tagmap[t])}", ""]

    MANIFEST.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_manifest(_args) -> None:
    """Regenerate the catalog MANIFEST.md from the nodes (the deterministic 'lock' job)."""
    rebuild_manifest()
    print(f"Wrote manifest: {len(all_nodes())} nodes -> {MANIFEST}")


def cmd_remove(args) -> None:
    """Uninstall a node — refuse if other nodes still depend on it (uv-style)."""
    nid = slugify(args.id)
    path = node_path(nid)
    if not path.exists():
        sys.exit(f"No node '{nid}' to remove.")
    dependents = sorted(i for i, m in all_nodes().items()
                        if nid in parse_list(m.get("prereqs", "")))
    if dependents and not args.force:
        sys.exit(f"Cannot remove '{nid}' — required by: {', '.join(dependents)}.\n"
                 f"Use --force to remove anyway (they would become unresolved).")
    path.unlink()
    # Companions are subsidiary to the node — remove the figure, Korean body, and spec with it.
    removed_companions = []
    for comp in companion_paths(nid):
        if comp.exists():
            comp.unlink()
            removed_companions.append(comp.relative_to(ROOT).as_posix())
    rebuild_manifest()
    print(f"Removed {nid}")
    if removed_companions:
        print("Also removed companions: " + ", ".join(removed_companions))
    if dependents:
        print("Now-unresolved dependents: " + ", ".join(dependents))


def _set_review(nid: str, notes: list[str]) -> None:
    """Write (or remove) the `review:` frontmatter list of a node, in place."""
    path = node_path(nid)
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    if not text.startswith("---") or end == -1:
        sys.exit(f"{nid}: no frontmatter to edit.")
    head, fm, tail = text[:4], text[4:end], text[end:]   # '---\n' , fm body , '\n---...'
    out, found = [], False
    new_line = f"review: [{', '.join(notes)}]" if notes else None
    for ln in fm.split("\n"):
        if ln.startswith("review:"):
            found = True
            if new_line is not None:
                out.append(new_line)
        else:
            out.append(ln)
    if not found and new_line is not None:
        idx = next((i for i, l in enumerate(out) if l.startswith("status:")), len(out))
        out.insert(idx, new_line)
    path.write_text(head + "\n".join(out) + tail, encoding="utf-8")


def cmd_review(args) -> None:
    """Record/clear a node's structural feedback (the `review:` notes `sync` emits for `lock`).

    The LLM decides WHAT to flag; this command only *stores* it as validated `type=target` notes.
    """
    nid = slugify(args.id)
    if not node_path(nid).exists():
        sys.exit(f"No node '{nid}'.")
    notes = parse_list(all_nodes()[nid].get("review", ""))
    if args.clear:
        notes = []
    for n in (args.add or []):
        n = n.strip()
        if "=" not in n or ": " in n:
            sys.exit(f"Bad note '{n}'. Use type=target (e.g. missing-prereq=foo); no ': '.")
        if n not in notes:
            notes.append(n)
    _set_review(nid, notes)
    rebuild_manifest()
    print(f"{nid}: review = [{', '.join(notes) or '∅'}]")


def _tokens(s: str) -> set:
    return {t for t in re.split(r"[-_\s]+", s.lower()) if t}


def _jaccard(a: set, b: set) -> float:
    u = a | b
    return len(a & b) / len(u) if u else 0.0


def cmd_dupes(args) -> None:
    """Deterministic redundancy SCREEN — candidate duplicate pairs by structure (no LLM, no embeddings).

    Score = prereq-set overlap + id/title token overlap, compared only WITHIN a tag root (where
    real duplicates live). It only *flags* candidates; the merge decision is `lock`'s LLM judgment.
    """
    nodes = all_nodes()
    thr = args.threshold
    pre = {i: set(parse_list(m.get("prereqs", ""))) for i, m in nodes.items()}
    tok = {i: _tokens(i) | _tokens(m.get("title", "")) for i, m in nodes.items()}
    summ = {i: (m.get("summary", "") or "").strip() for i, m in nodes.items()}
    root = {i: ((parse_list(m.get("tags", "")) or [""])[0].split("/")[0]) for i, m in nodes.items()}
    ids = sorted(nodes)
    if args.tag:
        ids = [i for i in ids if any(t == args.tag or t.startswith(args.tag + "/")
                                     for t in parse_list(nodes[i].get("tags", "")))]
    pairs = []
    for x in range(len(ids)):
        for y in range(x + 1, len(ids)):
            a, b = ids[x], ids[y]
            if root[a] != root[b]:
                continue
            tj = _jaccard(tok[a], tok[b])
            if tj <= 0:                # real duplicates share name tokens; pure prereq overlap is noise
                continue
            pj = _jaccard(pre[a], pre[b])
            score = 0.6 * tj + 0.4 * pj
            if score >= thr:
                pairs.append((score, pj, tj, a, b))
    pairs.sort(reverse=True)
    if not pairs:
        print(f"✅ No redundancy candidates at score ≥ {thr:.2f}.")
        return
    print(f"Redundancy candidates (score ≥ {thr:.2f}) — for `lock` to judge by COMPARING SUMMARIES:")
    for score, pj, tj, a, b in pairs:
        print(f"  {score:.2f}  {a}  ~  {b}   (prereq {pj:.2f} · title {tj:.2f})")
        print(f"          {a}: {summ.get(a) or '—'}")
        print(f"          {b}: {summ.get(b) or '—'}")
    print("\nSummaries differ in kind → not duplicates. If truly the same:  brain.py merge <from> <into>")


def cmd_merge(args) -> None:
    """Execute an LLM-decided merge: fold <from> into <into>, atomically and closed-world-safe.

    Redirects every prereq edge and every body `[[from]]` link to <into>, then removes <from>.
    The LLM decides the merge; this performs it mechanically.
    """
    a, b = slugify(args.from_id), slugify(args.into_id)
    if a == b:
        sys.exit("Cannot merge a node into itself.")
    nodes = all_nodes()
    if a not in nodes:
        sys.exit(f"No node '{a}' (from).")
    if b not in nodes:
        sys.exit(f"No node '{b}' (into).")
    link_re = re.compile(r"\[\[" + re.escape(a) + r"\]\]")
    changed = []
    for nid in nodes:
        if nid == a:
            continue
        path = node_path(nid)
        text = path.read_text(encoding="utf-8")
        orig = text
        end = text.find("\n---", 3)
        if text.startswith("---") and end != -1:
            head, fm, tail = text[:4], text[4:end], text[end:]
            out = []
            for ln in fm.split("\n"):
                if ln.startswith("prereqs:"):
                    ps = [b if p == a else p for p in parse_list(ln.split(":", 1)[1])]
                    ps = [p for p in dict.fromkeys(ps) if p != nid]   # dedup, drop self-loop
                    out.append(f"prereqs: [{', '.join(ps)}]")
                else:
                    out.append(ln)
            text = head + "\n".join(out) + tail
        text = link_re.sub(f"[[{b}]]", text)              # body links [[a]] -> [[b]]
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed.append(nid)
    for kp in NODES.glob("*.ko.md"):                      # Korean bodies carry the same links
        if kp.name == f"{a}.ko.md":
            continue                                      # deleted with the node below
        ktext = kp.read_text(encoding="utf-8")
        krew = link_re.sub(f"[[{b}]]", ktext)
        if krew != ktext:
            kp.write_text(krew, encoding="utf-8")
    node_path(a).unlink()
    for comp in companion_paths(a):
        if comp.exists():
            comp.unlink()
    rebuild_manifest()
    print(f"Merged {a} → {b}. Redirected {len(changed)} node(s): {', '.join(changed) or 'none'}")
    print("Next: `brain.py audit`, and check the kept node's body still grounds everything.")


def _rewrite_frontmatter(nid: str, updates: dict) -> None:
    """Set frontmatter fields in place. Existing keys are overwritten; a missing key is INSERTED
    right after the `title:` line (so e.g. `summary:` can be added to a legacy node that lacks it)."""
    path = node_path(nid)
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    if not text.startswith("---") or end == -1:
        sys.exit(f"{nid}: no frontmatter to edit.")
    head, fm, tail = text[:4], text[4:end], text[end:]
    out, seen, after_title = [], set(), None
    for ln in fm.split("\n"):
        key = ln.split(":", 1)[0].strip() if ":" in ln else ""
        if key in updates:
            out.append(f"{key}: {_quote_scalar(str(updates[key]))}")
            seen.add(key)
        else:
            out.append(ln)
        if key == "title":
            after_title = len(out)
    for k in (k for k in updates if k not in seen):     # insert any missing keys after title (or end)
        pos = after_title if after_title is not None else len(out)
        out.insert(pos, f"{k}: {_quote_scalar(str(updates[k]))}")
        after_title = pos + 1
    path.write_text(head + "\n".join(out) + tail, encoding="utf-8")


def _first_sentence(text: str, limit: int = 180) -> str:
    """The first sentence of `text`, or a clean truncation to ~limit chars with an ellipsis."""
    text = text.strip()
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    s = (m.group(1) if m else text).strip()
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].rstrip(",;: ") + "…"
    return s


def _extract_summary(nid: str) -> str:
    """Deterministically derive a one-line summary from a node's first real body paragraph (no LLM).

    Skips headings, blank lines, list/table/code/equation blocks, and italic template placeholders;
    strips `[[id]]` -> id and basic markdown; returns the first sentence. Empty if the body is still a
    template stub (nothing to extract) — leave those for `sync`.
    """
    para = []
    for raw in _body_text(nid).split("\n"):
        ln = raw.strip()
        if not ln:
            if para:
                break                                   # first paragraph ended
            continue
        if ln.startswith("#"):                          # heading
            if para:
                break
            continue
        if ln.startswith("_") and ln.endswith("_"):     # italic template placeholder
            continue
        if ln.startswith(("- ", "* ", "| ", "```", "$$")):   # list / table / code / equation block
            if para:
                break
            continue
        para.append(ln)
    text = " ".join(para)
    text = re.sub(r"\[\[([a-z0-9-]+)\]\]", r"\1", text)         # [[id]] -> id
    text = re.sub(r"[*`]", "", text)                            # drop bold/code markers
    text = re.sub(r"\s+", " ", text).strip().lstrip("[").strip()
    return _first_sentence(text)


def _set_summary(nid: str, text: str) -> str:
    """Sanitize (one line, no leading '[', collapsed whitespace) and write a node's `summary:`."""
    text = re.sub(r"\s+", " ", (text or "")).strip().lstrip("[").strip()
    _rewrite_frontmatter(nid, {"summary": text})
    return text


def cmd_summary(args) -> None:
    """Set a node's one-line `summary:` — the folded view `lock` reads (sync's job; also used by backfill)."""
    nid = slugify(args.id)
    if not node_path(nid).exists():
        sys.exit(f"No node '{nid}'.")
    text = _set_summary(nid, " ".join(args.text))
    rebuild_manifest()
    print(f"{nid}: summary = {text or '∅'}")


def cmd_backfill_summaries(args) -> None:
    """Populate empty `summary:` fields deterministically from each node's first body paragraph (no LLM)."""
    nodes = all_nodes()
    done, skipped = [], 0
    for nid in sorted(nodes):
        if (nodes[nid].get("summary", "") or "").strip() and not args.force:
            skipped += 1
            continue
        s = _extract_summary(nid)
        if not s:
            skipped += 1
            continue
        _set_summary(nid, s)
        done.append((nid, s))
    rebuild_manifest()
    print(f"Backfilled {len(done)} summaries; skipped {skipped} (already set or no extractable text).")
    for nid, s in done[:8]:
        print(f"  {nid} → {s[:80]}")


def cmd_reindex(args) -> None:
    """Set a node's prerequisite set to EXACTLY the given list — the **single declarative edge interface**.

    The LLM declares a node's complete correct prereq set (kept + new); `brain.py` **diffs** it against
    the current set and reconciles — **adding** new edges and **removing** dropped ones (stripping the
    dropped edge's body `[[link]]`s so `audit` stays green). Added edges' `[[link]]` wiring is the
    deferred `sync` (they show as unlinked-prereq hints); unchanged set → no-op (idempotent). Guards: a
    prereq must already exist (a missing one is a `scaffold` job); a cycle-forming edge is refused; giving
    an `axiom` any prereq requires `--demote` (flips `type: axiom → concept`). Add and remove are the
    internal mechanics — the LLM only ever calls `reindex` (re-indexing a node = declaring its true set).
    """
    nid = slugify(args.node)
    nodes = all_nodes()
    if nid not in nodes:
        sys.exit(f"No node '{nid}'.")
    desired = list(dict.fromkeys(slugify(p) for p in args.prereqs))
    unknown = [p for p in desired if p not in nodes]
    if unknown:
        sys.exit(f"reindex sets EXISTING nodes as prereqs; unknown: {', '.join(unknown)} (scaffold them first).")
    was_axiom = nodes[nid].get("type") == "axiom"
    if was_axiom and desired and not args.demote:
        sys.exit(f"'{nid}' is an axiom; giving it prereqs demotes it. Re-run with --demote (axiom→concept).")
    closure = _prereq_closure(nodes)
    final, cycles = [], []                              # cycle-guard the desired set
    for p in desired:
        (cycles if (p == nid or nid in closure.get(p, set())) else final).append(p)
    finalset = set(final)
    current = parse_list(nodes[nid].get("prereqs", ""))
    added = [p for p in final if p not in set(current)]
    removed = [p for p in current if p not in finalset]
    if not added and not removed:
        print(f"{nid}: already indexed as [{', '.join(final) or '∅'}]"
              + (f" (cycle-refused {cycles})" if cycles else "") + " — no change.")
        return
    updates = {"prereqs": f"[{', '.join(final)}]", "updated": today()}
    if was_axiom and final:
        updates["type"] = "concept"
    _rewrite_frontmatter(nid, updates)
    if removed:                                         # strip each dropped prereq's body link(s)
        for path in (node_path(nid), NODES / f"{nid}.ko.md"):   # the Korean body mirrors the links
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for r in removed:
                text = re.sub(r"(?m)^- \[\[" + re.escape(r) + r"\]\]\s*\n", "", text)   # the prereq-list bullet
                text = re.sub(r"\[\[" + re.escape(r) + r"\]\]", r, text)                 # any inline mention → plain word
            path.write_text(text, encoding="utf-8")
    rebuild_manifest()
    parts = ([f"+{added}"] if added else []) + ([f"−{removed}"] if removed else []) + \
            ([f"cycle-refused {cycles}"] if cycles else [])
    print(f"{nid}{' (demoted axiom→concept)' if (was_axiom and final) else ''}: "
          f"{' · '.join(parts)}  →  [{', '.join(final)}]")
    print("Added edges' [[links]] are the deferred `sync`; dropped edges' links were stripped. Gate with `brain.py audit`.")


def _body_text(nid: str) -> str:
    """Return a node's prose body with the frontmatter stripped."""
    text = node_path(nid).read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def _prereq_closure(nodes: dict) -> dict:
    """Map each node id -> the set of ALL its transitive prerequisites (cycle-safe)."""
    direct = {i: set(parse_list(m.get("prereqs", ""))) for i, m in nodes.items()}
    memo: dict = {}

    def walk(i: str, stack: set) -> set:
        if i in memo:
            return memo[i]
        acc: set = set()
        for p in direct.get(i, ()):            # p may be a frontier id absent from nodes — fine
            if p in stack:
                continue
            acc.add(p)
            acc |= walk(p, stack | {p})
        memo[i] = acc
        return acc

    for i in list(nodes):
        walk(i, {i})
    return memo


_MENTION_SUFFIX = r"(?:e?s|ed|ing)?"        # light morphology: switch -> switch/switches/switching


def _mention_res(meta: dict, nid: str) -> list:
    """Whole-phrase, case-insensitive regexes that detect a node's title or id in prose.

    A node is named either by its title ("Context switch") or its id-as-words ("context switch");
    the last word may carry a light inflection so "context switch" still catches "context switching".
    """
    terms = {(meta.get("title", "") or "").strip().lower(), nid.replace("-", " ").lower()}
    out = []
    for term in terms:
        words = [w for w in term.split() if w]
        if not words:
            continue
        esc = [re.escape(w) for w in words]
        esc[-1] += _MENTION_SUFFIX
        out.append(re.compile(r"\b" + r"\s+".join(esc) + r"\b"))
    return out


def cmd_reground(args) -> None:
    """Surface MIS-POSITIONED nodes — prose-parked edges the grown world can now resolve.

    A node may name, in its prose, a concept that did not yet exist as a node when it was written;
    once that concept is archived, the node sits ABOVE a prerequisite it never declared. This
    deterministic SCREEN flags, per target node A, every existing node B such that: A's prose names B ·
    B is not a declared prereq of A · B does not transitively build on A. The cycle guard is the crux:
    a B that already depends on A sits ABOVE it (like message-passing over parallel-process) and is
    skipped. For an **axiom** a hit means the chosen floor is *stranded* (demote it); for a **concept**
    a hit is a *missing prerequisite edge* (interleave it). It only *flags*; the edits (add the edge,
    or flip `axiom → concept` + re-`sync`) are `lock`'s LLM judgment — the inverse of `dupes`, which
    collapses peers while this deepens position.

    Scope: default = axioms only (the cheap floor check) · `--all` = every node (the re-interleave
    screen, noise accepted) · `<id>` = one node.
    """
    nodes = all_nodes()
    closure = _prereq_closure(nodes)
    if getattr(args, "id", None):
        tid = slugify(args.id)
        if tid not in nodes:
            sys.exit(f"No node '{tid}'.")
        targets = [tid]
    elif getattr(args, "all", False):
        targets = list(nodes)
    else:
        targets = [i for i, m in nodes.items() if m.get("type") == "axiom"]
    res = {i: _mention_res(nodes[i], i) for i in nodes}
    body_lc = {i: _body_text(i).lower() for i in nodes}

    # Corpus document-frequency: in how many node bodies does each candidate's title appear? Computed
    # over the FULL corpus (every node), NOT just `targets` — so a single-node `reground <id>` suppresses
    # the same generic/hub terms (process, stack, kernel, …) as `--all`. Generic-ness is a property of
    # the corpus, not of the scope being screened. (`--max-df` overrides the cap.)
    df = {i: 0 for i in nodes}
    for a in nodes:
        text = body_lc[a]
        for n in nodes:
            if n != a and any(rx.search(text) for rx in res[n]):
                df[n] += 1
    cap = args.max_df if args.max_df is not None else max(12, int(0.08 * len(nodes)))
    generic = sorted((i for i in nodes if df[i] > cap), key=lambda i: (-df[i], i))
    gen_set = set(generic)

    if getattr(args, "prune", False):
        # PRUNE screen — the REMOVE direction: flag SUSPECT *declared* edges A→B for `lock` to validate.
        #   (a) declared-but-unlinked — B is a prereq of A but never [[linked]] in A's body (A doesn't use it);
        #   (b) homonym-suspect — B IS linked but cross-field (A.root≠B.root) AND B's title is generic
        #       (high df), e.g. heap(algorithms)→container(os). The LLM confirms by summary, then `reindex`es.
        link_re = re.compile(r"\[\[([a-z0-9-]+)\]\]")
        root = {i: ((parse_list(m.get("tags", "")) or [""])[0].split("/")[0]) for i, m in nodes.items()}
        scope = targets if getattr(args, "id", None) else list(nodes)
        suspects = []
        for a in sorted(scope):
            links = set(link_re.findall(_body_text(a)))
            for b in parse_list(nodes[a].get("prereqs", "")):
                if b not in nodes:
                    continue
                if b not in links:
                    suspects.append((a, b, "declared-but-unlinked"))
                elif (root.get(a) != root.get(b) and b in gen_set
                      and nodes[b].get("type") != "axiom"):     # an axiom (arithmetic) has one sense — never a homonym
                    suspects.append((a, b, "homonym-suspect (cross-field + generic name)"))
        if getattr(args, "json", False):
            print(json.dumps([{"node": a, "prereq": b, "why": why} for a, b, why in suspects]))
            return
        if not suspects:
            print("✅ No suspect declared edges — every edge is [[linked]], in-field, or a specific name.")
            return
        print(f"Prune candidates — suspect DECLARED edges for `lock` to validate by summary ({len(suspects)}):")
        for a, b, why in suspects:
            print(f"  {a}  →  {b}   [{why}]")
        print("\nIf an edge is wrong, the LLM `reindex`es that node to its correct prereq set (dropping it).")
        return

    # Candidates per target: the target's prose names B, where B is not already a declared prereq, not a
    # suppressed generic, and does not transitively build on the target (cycle guard).
    found = []
    for a in sorted(targets):
        text = body_lc[a]
        declared = set(parse_list(nodes[a].get("prereqs", "")))
        hits = [n for n in nodes
                if n != a and n not in declared and n not in gen_set
                and a not in closure.get(n, set())
                and any(rx.search(text) for rx in res[n])]
        if hits:
            found.append((a, nodes[a].get("type") == "axiom", hits))
    found.sort(key=lambda f: (-len(f[2]), f[0]))
    if getattr(args, "json", False):
        print(json.dumps([{"node": a, "isAxiom": is_ax, "candidates": hits}
                          for a, is_ax, hits in found]))
        return
    if not found:
        print(f"✅ No re-grounding candidates among {len(targets)} node(s) (after suppressing "
              f"{len(generic)} generic/hub term(s)).")
        return
    n_ax = sum(1 for _, is_ax, _ in found if is_ax)
    print(f"Re-grounding candidates — for `lock` to judge ({len(found)} node(s), {n_ax} axiom(s); "
          f"generic terms matched in > {cap} bodies suppressed):")
    for a, is_ax, hits in sorted(found, key=lambda f: (-len(f[2]), f[0])):
        mark = "  🛑 axiom → demote?" if is_ax else ""
        print(f"  {a}{mark}  ⤵ may now rest on: {', '.join(hits)}")
    if generic:
        shown = ", ".join(f"{i}({df[i]})" for i in generic[:24])
        print(f"\nSuppressed {len(generic)} generic/hub term(s) [id(bodies-matched)]: {shown}"
              + (" …" if len(generic) > 24 else ""))
    print("\nIf real, `lock`: add the prereq edge(s) (axioms: flip type axiom→concept first), "
          "re-`sync` the affected body, then `audit`.")


def cmd_sync(_args) -> None:
    """Check the whole graph resolves — like `uv sync` against a lockfile."""
    nodes = all_nodes()
    missing = sorted(compute_missing())
    if not missing:
        n_ax = sum(1 for m in nodes.values() if m.get("type") == "axiom")
        print(f"Resolved {len(nodes)} nodes ({n_ax} axioms) · 0 unresolved "
              "— world is closed. ✅")
    else:
        print(f"{len(missing)} unresolved dependencies:")
        for m in missing:
            print(f"  - {m}")
        print("Install each with:  brain add <id> ...")


def cmd_audit(_args) -> None:
    """Whole-graph validation beyond `sync`.

    `sync` only checks that frontmatter `prereqs` resolve. `audit` also reads each
    node BODY and enforces the closed-world law at the symbol level: every `[[link]]`
    in the prose must be a declared prerequisite (no dead links, no "see-also" links
    to non-prerequisites). The Korean companion body (`nodes/<id>.ko.md`) is held to
    the same law; an orphan companion is an error, a missing one only a hint.
    It also flags untagged nodes and prints the tag taxonomy.
    Exits non-zero if anything is wrong, so it can gate commits/CI.
    """
    nodes = all_nodes()
    ids = set(nodes)
    problems = 0

    missing = sorted(compute_missing())
    if missing:
        problems += len(missing)
        print("⚠️  unresolved prerequisites: " + ", ".join(missing))

    link_re = re.compile(r"\[\[([a-z0-9-]+)\]\]")
    unlinked_hints = []
    missing_ko = []
    for nid in sorted(nodes):
        text = node_path(nid).read_text(encoding="utf-8")
        body = text
        if text.startswith("---"):
            end = text.find("\n---", 3)
            if end != -1:
                body = text[end + 4:]
                # Frontmatter sanity: a block-list item that is unquoted yet
                # contains ': ' is invalid YAML (a stray mapping indicator).
                for fl in text[3:end].splitlines():
                    s = fl.strip()
                    if s.startswith("- "):
                        item = s[2:].strip()
                        if item and item[0] not in "'\"[" and ": " in item:
                            problems += 1
                            print(f"  ⚠️  {nid}: invalid frontmatter YAML "
                                  "(unquoted ': ' in a list item — quote it)")
        prereqs = set(parse_list(nodes[nid].get("prereqs", "")))
        links = set(link_re.findall(body))
        dead = sorted(l for l in links if l not in ids)
        leak = sorted(l for l in links if l in ids and l not in prereqs and l != nid)
        if dead:
            problems += len(dead)
            print(f"  ❌ {nid}: dead body links {dead}")
        if leak:
            problems += len(leak)
            print(f"  ⚠️  {nid}: body links not in prereqs {leak}")
        # The Korean companion body obeys the same closed-world law.
        ko = NODES / f"{nid}.ko.md"
        if ko.exists():
            klinks = set(link_re.findall(ko.read_text(encoding="utf-8")))
            kdead = sorted(l for l in klinks if l not in ids)
            kleak = sorted(l for l in klinks if l in ids and l not in prereqs and l != nid)
            if kdead:
                problems += len(kdead)
                print(f"  ❌ {nid}.ko: dead body links {kdead}")
            if kleak:
                problems += len(kleak)
                print(f"  ⚠️  {nid}.ko: body links not in prereqs {kleak}")
        elif nodes[nid].get("status") == "explained":
            missing_ko.append(nid)
        # HINT only (not a problem): a declared prereq never linked in an explained body
        # — either truly unused (drop the edge) or a missed link. The call is the LLM's at sync/lock.
        if nodes[nid].get("status") == "explained":
            unl = sorted(p for p in prereqs if p not in links)
            if unl:
                unlinked_hints.append((nid, unl))

    orphan_ko = sorted(p.name for p in NODES.glob("*.ko.md")
                       if p.name[:-len(".ko.md")] not in ids)
    if orphan_ko:
        problems += len(orphan_ko)
        print(f"  ❌ orphan Korean companions (no matching node): {orphan_ko}")

    if unlinked_hints:
        print(f"  💡 unlinked prereqs (hint for sync/lock — drop or link; {len(unlinked_hints)} node(s)):")
        for nid, unl in unlinked_hints:
            print(f"       {nid}: {unl}")
    if missing_ko:
        print(f"  💡 explained nodes missing a Korean body (hint for sync; {len(missing_ko)}): "
              + ", ".join(missing_ko))

    untagged = sorted(n for n, m in nodes.items() if not parse_list(m.get("tags", "")))
    if untagged:
        problems += len(untagged)
        print(f"  🏷️  untagged ({len(untagged)}): " + ", ".join(untagged))

    tagmap: dict = {}
    for m in nodes.values():
        for t in parse_list(m.get("tags", "")):
            tagmap[t] = tagmap.get(t, 0) + 1
    roots: dict = {}
    for t, c in tagmap.items():
        roots[split_tag(t)[0]] = roots.get(split_tag(t)[0], 0) + c
    print(f"tags ({len(tagmap)} leaves under {len(roots)} roots):")
    for top in sorted(roots, key=lambda k: (-roots[k], k)):
        leaves = sorted((t for t in tagmap if split_tag(t)[0] == top),
                        key=lambda t: (-tagmap[t], t))
        detail = ", ".join(f"{t}({tagmap[t]})" for t in leaves)
        print(f"  {top}({roots[top]}): {detail}")

    if problems:
        print(f"❌ audit: {problems} issue(s) across {len(nodes)} nodes.")
        sys.exit(1)
    print(f"✅ audit clean — {len(nodes)} nodes: closed world, "
          "body links ⊆ prereqs, all tagged.")


def cmd_graph(args) -> None:
    """Render the interactive dashboard. Delegates to web/render.py (the graph frontend).

    The engine stays free of rendering concerns; it only hands the node store and its
    two graph-walking helpers to web.render, which projects the data and writes the HTML.
    """
    try:
        from web import render            # lazy: keeps the engine importable without the web pkg
    except ImportError as e:               # pragma: no cover
        sys.exit(f"Cannot load web/render.py: {e}")
    out = Path(args.out) if args.out else (WEB / "graph.html")
    data = None
    base = getattr(args, "diff", "")
    if base:                                    # visual diff mode: annotate nodes/edges by status
        before = nodes_at_ref(base)
        after = nodes_at_ref(args.head) if getattr(args, "head", "") else all_nodes()
        d = compute_diff(before, after)
        data = render.build_diff_graph_data(before, after, d, parse_list, split_tag)
    try:
        n_nodes, n_edges = render.write_graph(all_nodes(), parse_list, split_tag,
                                              out, fragment=args.fragment, data=data)
    except FileNotFoundError as e:
        sys.exit(str(e))
    print(f"Wrote {out}  ({n_nodes} nodes, {n_edges} edges){' (diff)' if base else ''}")


def _tag_of(nodes: dict, i: str) -> str:
    tags = parse_list(nodes.get(i, {}).get("tags", ""))
    return tags[0] if tags else ""


def compute_diff(before: dict, after: dict, with_context: bool = False) -> dict:
    """Structural delta between two {id: frontmatter} snapshots — DELTA-SCOPED.

    Reports only what changed: nodes added/removed, edges added/removed, and
    `restructured` = nodes present in BOTH snapshots whose edge set changed (the
    interleave/prune signal). Unchanged nodes are never enumerated. With `with_context`,
    attaches each changed node's 1-hop neighborhood (prereqs out / dependents in) in the
    relevant snapshot — a confirm-the-change view, still bounded by the changed set.
    """
    b_ids, a_ids = set(before), set(after)
    added_ids = sorted(a_ids - b_ids)
    removed_ids = sorted(b_ids - a_ids)

    b_edges, a_edges = graph_edges(before), graph_edges(after)
    added_edges = sorted(a_edges - b_edges)
    removed_edges = sorted(b_edges - a_edges)

    touched = {s for s, _ in added_edges} | {s for s, _ in removed_edges}
    restructured = []
    for s in sorted(touched):
        if s in b_ids and s in a_ids:            # in both snapshots = an EXISTING node re-wired
            plus = sorted(t for (x, t) in added_edges if x == s)
            minus = sorted(t for (x, t) in removed_edges if x == s)
            if plus or minus:
                restructured.append({"id": s, "tag": _tag_of(after, s),
                                     "addedPrereqs": plus, "removedPrereqs": minus})

    result = {
        "nodesAdded": [{"id": i, "tag": _tag_of(after, i)} for i in added_ids],
        "nodesRemoved": [{"id": i, "tag": _tag_of(before, i)} for i in removed_ids],
        "edgesAdded": [{"s": s, "t": t} for s, t in added_edges],
        "edgesRemoved": [{"s": s, "t": t} for s, t in removed_edges],
        "restructured": restructured,
        "counts": {"nodesAdded": len(added_ids), "nodesRemoved": len(removed_ids),
                   "edgesAdded": len(added_edges), "edgesRemoved": len(removed_edges),
                   "restructured": len(restructured)},
    }
    if with_context:
        changed = set(added_ids) | set(removed_ids) | {r["id"] for r in restructured}
        changed |= {t for _, t in added_edges} | {t for _, t in removed_edges}   # edge endpoints
        ctx = {}
        for i in sorted(changed):
            edges = a_edges if i in a_ids else b_edges
            ctx[i] = {"prereqs": sorted(t for (s, t) in edges if s == i),
                      "dependents": sorted(s for (s, t) in edges if t == i)}
        result["context"] = ctx
    return result


def _print_diff_human(d: dict, ref1: str, ref2: str) -> None:
    c = d["counts"]
    print(f"graph diff  {ref1}..{ref2}")
    for key, sign, label in (("nodesAdded", "+", "nodes"), ("nodesRemoved", "-", "nodes")):
        if d[key]:
            print(f"\n{sign} {label} ({c[key]})")
            for n in d[key]:
                print(f"    {sign} {n['id']}  [{n['tag']}]")
    for key, sign in (("edgesAdded", "+"), ("edgesRemoved", "-")):
        if d[key]:
            print(f"\n{sign} edges ({c[key]})")
            for e in d[key]:
                print(f"    {e['s']} → {e['t']}")
    if d["restructured"]:
        print(f"\nrestructured existing nodes ({c['restructured']})")
        for r in d["restructured"]:
            plus = "+[" + ", ".join(r["addedPrereqs"]) + "]" if r["addedPrereqs"] else ""
            minus = "−[" + ", ".join(r["removedPrereqs"]) + "]" if r["removedPrereqs"] else ""
            print(f"    {r['id']}  {plus} {minus}".rstrip())
    if "context" in d:
        print("\ncontext (1-hop neighborhood of changed nodes)")
        for i, ctx in d["context"].items():
            print(f"    {i}")
            print(f"        prereqs:    {', '.join(ctx['prereqs']) or '—'}")
            print(f"        dependents: {', '.join(ctx['dependents']) or '—'}")
    if not any(c[k] for k in ("nodesAdded", "nodesRemoved", "edgesAdded", "edgesRemoved")):
        print("\n(no structural change)")
    print(f"\nsummary: +{c['nodesAdded']} nodes, −{c['nodesRemoved']} nodes, "
          f"+{c['edgesAdded']} edges, −{c['edgesRemoved']} edges, "
          f"{c['restructured']} restructured")


def cmd_diff(args) -> None:
    """Structural graph delta between two git revisions (or a revision vs the working tree)."""
    before = nodes_at_ref(args.ref1)
    after = nodes_at_ref(args.ref2) if args.ref2 else all_nodes()
    result = compute_diff(before, after, with_context=args.context)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_diff_human(result, args.ref1, args.ref2 or "(working tree)")
    if args.exit_nonzero_on_change and any(
            result["counts"][k] for k in
            ("nodesAdded", "nodesRemoved", "edgesAdded", "edgesRemoved")):
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="A recursive concept graph.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_node_args(p):
        p.add_argument("id")
        p.add_argument("--title", default="")
        p.add_argument("--type", default="concept", help=", ".join(TYPES))
        p.add_argument("--prereqs", default="", help="comma-separated prerequisite ids")
        p.add_argument("--requires", default="", help="alias for --prereqs (uv-style)")
        p.add_argument("--sources", default="")
        p.add_argument("--tags", default="", help="comma-separated taxonomy fields (cut the graph by these)")
        p.add_argument("--authors", default="")
        p.add_argument("--year", default="")
        p.add_argument("--explained", action="store_true",
                       help="Mark as fully explained (default: stub).")
        p.set_defaults(func=cmd_new)

    # `add` is the primary (uv-style) name; `new` stays as an alias.
    add_node_args(sub.add_parser("add", help="Install (create) a concept node."))
    add_node_args(sub.add_parser("new", help="Alias for add."))

    p_show = sub.add_parser("show", help="Print a node.")
    p_show.add_argument("id")
    p_show.set_defaults(func=cmd_show)

    p_tree = sub.add_parser("tree", help="Print the prerequisite tree.")
    p_tree.add_argument("id")
    p_tree.set_defaults(func=cmd_tree)

    p_missing = sub.add_parser("missing", help="List the recursion frontier.")
    p_missing.set_defaults(func=cmd_missing)

    sub.add_parser("feedback", help="List pending structural feedback (review notes) for lock.") \
        .set_defaults(func=cmd_feedback)

    p_review = sub.add_parser("review", help="Record/clear a node's review notes (sync's feedback).")
    p_review.add_argument("id")
    p_review.add_argument("--add", action="append", metavar="type=target",
                          help="add a note, e.g. missing-prereq=foo (repeatable)")
    p_review.add_argument("--clear", action="store_true", help="clear all notes first")
    p_review.set_defaults(func=cmd_review)

    p_summary = sub.add_parser("summary", help="Set a node's one-line summary (the folded view lock reads).")
    p_summary.add_argument("id")
    p_summary.add_argument("text", nargs="+", help="the summary text")
    p_summary.set_defaults(func=cmd_summary)

    p_backfill = sub.add_parser("backfill-summaries",
                                help="Populate empty summaries deterministically from each node's first paragraph.")
    p_backfill.add_argument("--force", action="store_true", help="overwrite existing summaries too")
    p_backfill.set_defaults(func=cmd_backfill_summaries)

    p_dupes = sub.add_parser("dupes", help="Screen for redundancy candidates (structural; for lock).")
    p_dupes.add_argument("--tag", help="restrict to a tag subtree (prefix match)")
    p_dupes.add_argument("--threshold", type=float, default=0.45, help="min score (default 0.45)")
    p_dupes.set_defaults(func=cmd_dupes)

    p_merge = sub.add_parser("merge", help="Fold one node into another (redirect edges + links).")
    p_merge.add_argument("from_id", metavar="FROM")
    p_merge.add_argument("into_id", metavar="INTO")
    p_merge.set_defaults(func=cmd_merge)

    p_reindex = sub.add_parser("reindex",
                               help="Set a node's prereq set to EXACTLY the given list (the single declarative edge interface).")
    p_reindex.add_argument("node")
    p_reindex.add_argument("prereqs", nargs="*", metavar="PREREQ", help="the complete desired prereq set")
    p_reindex.add_argument("--demote", action="store_true",
                           help="permit demoting an axiom→concept when giving it prereqs")
    p_reindex.set_defaults(func=cmd_reindex)

    p_reground = sub.add_parser("reground",
                                help="Screen for mis-positioned nodes / stranded axioms the grown graph can now ground (for lock).")
    p_reground.add_argument("id", nargs="?", help="check one node (default: screen axioms only)")
    p_reground.add_argument("--all", action="store_true",
                            help="screen every node, not just axioms (the re-interleave screen)")
    p_reground.add_argument("--prune", action="store_true",
                            help="REMOVE direction: flag suspect DECLARED edges (unlinked / homonym) to validate")
    p_reground.add_argument("--max-df", type=int, default=None,
                            help="suppress a title matched in more than N bodies as a generic/hub term "
                                 "(default: max(12, 8%% of nodes))")
    p_reground.add_argument("--json", action="store_true",
                            help="emit candidates as JSON [{node, isAxiom, candidates}] (for tooling)")
    p_reground.set_defaults(func=cmd_reground)

    p_list = sub.add_parser("list", help="List nodes.")
    p_list.add_argument("--type")
    p_list.add_argument("--status")
    p_list.add_argument("--tag", help="filter by taxonomy field (cut the graph)")
    p_list.set_defaults(func=cmd_list)

    p_remove = sub.add_parser("remove", help="Uninstall a concept node.")
    p_remove.add_argument("id")
    p_remove.add_argument("--force", action="store_true",
                          help="Remove even if other nodes depend on it.")
    p_remove.set_defaults(func=cmd_remove)

    sub.add_parser("sync", help="Check all dependencies resolve (closed world).") \
        .set_defaults(func=cmd_sync)
    sub.add_parser("audit", help="Deep check: body-link discipline, tags, closed world.") \
        .set_defaults(func=cmd_audit)
    sub.add_parser("manifest", help="Regenerate the catalog (MANIFEST.md).") \
        .set_defaults(func=cmd_manifest)

    p_graph = sub.add_parser("graph", help="Render the interactive graph dashboard (graph.html).")
    p_graph.add_argument("--out", default="", help="output path (default: graph.html)")
    p_graph.add_argument("--fragment", action="store_true",
                         help="emit a head/body-less fragment (for embedding / an Artifact).")
    p_graph.add_argument("--diff", default="", metavar="BASE",
                         help="render a VISUAL diff vs the BASE revision (colours added/removed/restructured)")
    p_graph.add_argument("--head", default="", metavar="REF",
                         help="head revision for --diff (default: the working tree)")
    p_graph.set_defaults(func=cmd_graph)

    p_diff = sub.add_parser("diff",
        help="Show the structural graph delta between two git revisions (nodes/edges +/-).")
    p_diff.add_argument("ref1", help="base revision (commit/branch/tag; e.g. HEAD~1)")
    p_diff.add_argument("ref2", nargs="?", default="",
                        help="head revision; omit to compare against the working tree")
    p_diff.add_argument("--json", action="store_true",
                        help="emit the delta as JSON (delta-scoped, not the whole graph)")
    p_diff.add_argument("--context", action="store_true",
                        help="also show each changed node's 1-hop neighborhood")
    p_diff.add_argument("--exit-nonzero-on-change", action="store_true",
                        help="exit 1 if anything changed (scripting; the PR gate does NOT use this)")
    p_diff.set_defaults(func=cmd_diff)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
