#!/usr/bin/env python3
"""Build the canonical browser dataset from Principia Markdown nodes."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import brain  # noqa: E402
from web import render  # noqa: E402


def body_from(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    marker = text.find("\n---\n", 4)
    return text[marker + 5 :] if marker >= 0 else text


def main() -> None:
    brain.configure_workspace(str(ROOT))
    metadata = brain.all_nodes()
    data = render.build_graph_data(metadata, brain.parse_list, brain.split_tag, ROOT)
    by_id = {node["id"]: node for node in data["nodes"]}
    for node_id, meta in metadata.items():
        node = by_id[node_id]
        node["prereqs"] = brain.parse_list(meta.get("prereqs", ""))
        node["tags"] = brain.parse_list(meta.get("tags", ""))
        node["body"] = body_from((brain.NODES / f"{node_id}.md").read_text(encoding="utf-8"))
        node["hasFigure"] = (brain.NODES / f"{node_id}.svg").is_file()

    output = ROOT / "web" / "dist"
    data_dir = output / "data"
    assets_dir = output / "node-assets"
    data_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "graph.json").write_text(
        json.dumps({"schemaVersion": 1, **data}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    for svg in brain.NODES.glob("*.svg"):
        shutil.copy2(svg, assets_dir / svg.name)
    shutil.copy2(ROOT / "web" / "graph.html", output / "legacy-graph.html")
    print(f"Wrote {data_dir / 'graph.json'} ({len(data['nodes'])} nodes, {len(data['edges'])} edges)")


if __name__ == "__main__":
    main()
