"""Graph dashboard rendering for the learning brain.

Projects the concept graph into a `{nodes, edges}` payload and injects it into
`graph.template.html` to produce a self-contained `graph.html` (or a head/body-less
fragment for embedding, e.g. a claude.ai Artifact).

The graph-walking helpers (`parse_list`, `split_tag`) and the node store are owned
by `brain.py`; they are passed in rather than imported, so this module has no
dependency back on the engine (no circular import, no `__main__` duplicate module).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "graph.template.html"
TITLE = "Principia — Concept Graph"
DOC_BASE_FALLBACK = "https://github.com/sunguk-lim/principia/blob/main/nodes"


def doc_base() -> str:
    """GitHub blob base for node docs: ``<repo web URL>/blob/main/nodes``.

    Derived from the ``origin`` remote so a fork links to its own copy; falls back to
    the canonical repo when git is unavailable. Node docs live one dir up, in nodes/,
    so the graph links there rather than to the (Pages-only) web/ artifact.
    """
    try:
        url = subprocess.run(
            ["git", "-C", str(HERE.parent), "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return DOC_BASE_FALLBACK
    if url.startswith("git@"):                 # git@github.com:owner/repo.git
        slug = url.split(":", 1)[1]
    elif "github.com/" in url:                 # https://github.com/owner/repo.git
        slug = url.split("github.com/", 1)[1]
    else:
        return DOC_BASE_FALLBACK
    slug = slug.removesuffix(".git").strip("/")
    return f"https://github.com/{slug}/blob/main/nodes"


def build_graph_data(nodes: dict, parse_list, split_tag) -> dict:
    """Project the node graph into {nodes, edges} for the visualization.

    Each node carries its title/type/status, its first tag + the tag's root, the
    counts of prerequisites (out) and dependents (in), and a topological `level`
    = the longest prerequisite chain beneath it (axioms/leaves = 0). Edges point
    from a node to each prerequisite it depends on (within the closed world).

    `nodes` is the id -> frontmatter dict from brain.all_nodes(); `parse_list` and
    `split_tag` are brain's helpers, injected to keep this module engine-agnostic.
    """
    ids = set(nodes)
    prereqs = {i: [p for p in parse_list(m.get("prereqs", "")) if p in ids]
               for i, m in nodes.items()}
    dependents = {i: 0 for i in ids}
    for i, ps in prereqs.items():
        for p in ps:
            dependents[p] += 1

    level: dict[str, int] = {}

    def lvl(i: str, stack: frozenset) -> int:
        if i in level:
            return level[i]
        if i in stack:          # cycle guard (audit forbids cycles, but be safe)
            return 0
        ps = prereqs[i]
        level[i] = 0 if not ps else 1 + max(lvl(p, stack | {i}) for p in ps)
        return level[i]

    for i in ids:
        lvl(i, frozenset())

    node_list = []
    for i, m in nodes.items():
        tags = parse_list(m.get("tags", ""))
        tag = tags[0] if tags else ""
        node_list.append({
            "id": i,
            "title": m.get("title", i),
            "summary": m.get("summary", ""),
            "type": m.get("type", "concept"),
            "status": m.get("status", "stub"),
            "tag": tag,
            "root": split_tag(tag)[0] if tag else "untagged",
            "deps": len(prereqs[i]),
            "dependents": dependents[i],
            "level": level[i],
        })
    node_list.sort(key=lambda n: n["id"])
    edge_list = [{"s": i, "t": p} for i in sorted(prereqs) for p in prereqs[i]]
    return {"nodes": node_list, "edges": edge_list, "docBase": doc_base()}


def build_diff_graph_data(before: dict, after: dict, diff: dict, parse_list, split_tag) -> dict:
    """Graph payload for the VISUAL diff: the `after` graph plus any removed nodes/edges, with
    every node and edge tagged `diff` ∈ {added, removed, restructured, unchanged} for the dashboard
    to colour. Layout/levels come from the after graph; removed items are appended (level 0).

    `diff` is brain.compute_diff(before, after). The dashboard defaults to the affected subgraph
    (changed nodes + 1-hop) — the full payload is present but scoped in the UI.
    """
    data = build_graph_data(after, parse_list, split_tag)
    added_n = {x["id"] for x in diff["nodesAdded"]}
    restr_n = {x["id"] for x in diff["restructured"]}
    for n in data["nodes"]:
        n["diff"] = ("added" if n["id"] in added_n
                     else "restructured" if n["id"] in restr_n else "unchanged")
    for x in diff["nodesRemoved"]:                       # removed nodes come from the before snapshot
        m = before.get(x["id"], {})
        tags = parse_list(m.get("tags", ""))
        tag = tags[0] if tags else ""
        data["nodes"].append({
            "id": x["id"], "title": m.get("title", x["id"]), "summary": m.get("summary", ""),
            "type": m.get("type", "concept"), "status": m.get("status", "stub"),
            "tag": tag, "root": (split_tag(tag)[0] if tag else "untagged"),
            "deps": 0, "dependents": 0, "level": 0, "diff": "removed",
        })
    data["nodes"].sort(key=lambda n: n["id"])
    added_e = {(e["s"], e["t"]) for e in diff["edgesAdded"]}
    removed_e = {(e["s"], e["t"]) for e in diff["edgesRemoved"]}
    after_e = {(e["s"], e["t"]) for e in data["edges"]}
    # the just-installed root concept(s): added nodes that no OTHER added node depends on (top of the added subgraph)
    installed_roots = added_n - {t for (s, t) in after_e if s in added_n and t in added_n}
    for n in data["nodes"]:
        n["diffRoot"] = n["id"] in installed_roots
    data["edges"] = [
        {"s": s, "t": t,
         "diff": "added" if (s, t) in added_e else "removed" if (s, t) in removed_e else "unchanged"}
        for (s, t) in sorted(after_e | removed_e)
    ]
    data["diffMode"] = True
    data["diffCounts"] = diff["counts"]
    return data


def render_html(data: dict, fragment: bool = False) -> str:
    """Inject the graph data into the template; wrap as a full document unless fragment."""
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Missing template: {TEMPLATE}")
    core = TEMPLATE.read_text(encoding="utf-8").replace(
        "__DATA__", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    if fragment:                      # head/body-less, for embedding (e.g. an Artifact)
        return f"<title>{TITLE}</title>\n{core}"
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{TITLE}</title>\n</head>\n<body>\n{core}\n</body>\n</html>\n')


def write_graph(nodes: dict, parse_list, split_tag, out: Path,
                fragment: bool = False, data: dict | None = None) -> tuple[int, int]:
    """Build + render + write to `out`; return (node_count, edge_count).

    `data` may be a precomputed payload (e.g. build_diff_graph_data's) — when given, `nodes`
    is ignored and the payload is rendered as-is.
    """
    if data is None:
        data = build_graph_data(nodes, parse_list, split_tag)
    Path(out).write_text(render_html(data, fragment), encoding="utf-8")
    return len(data["nodes"]), len(data["edges"])
