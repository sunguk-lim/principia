from __future__ import annotations

import argparse
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from markdown_it import MarkdownIt
from pydantic import BaseModel, Field
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
NODES_DIR = ROOT / "nodes"
STATIC_MIRROR = ROOT / "web" / "graph.html"
DEFAULT_DB = Path.home() / ".local" / "share" / "principia" / "status.sqlite3"
DB_PATH = Path(os.environ.get("PRINCIPIA_STATUS_DB", DEFAULT_DB)).expanduser()
MARKDOWN = MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": True})
STATUS_VALUES = {"not_started", "in_progress", "blocked", "done", "custom"}

app = FastAPI(title="Principia Local", docs_url="/docs")


class StatusUpdate(BaseModel):
    status: Literal["not_started", "in_progress", "blocked", "done", "custom"] = "not_started"
    custom_label: str = Field(default="", max_length=80)
    note: str = Field(default="", max_length=4000)


def _db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS node_status (
        slug TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        custom_label TEXT NOT NULL DEFAULT '',
        note TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL
        )"""
    )
    return conn


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _node_path(slug: str) -> Path:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
        raise HTTPException(404, "Node not found")
    path = NODES_DIR / f"{slug}.md"
    if not path.is_file():
        raise HTTPException(404, "Node not found")
    return path


def _node_summary(path: Path) -> dict[str, str]:
    data = _frontmatter(path.read_text(encoding="utf-8"))
    slug = path.stem
    return {
        "slug": slug,
        "title": data.get("title", slug.replace("-", " ").title()),
        "summary": data.get("summary", ""),
        "type": data.get("type", "concept"),
        "tags": data.get("tags", "[]").strip("[]"),
    }


def _render_markdown(source: str) -> str:
    body = source
    if source.startswith("---\n"):
        end = source.find("\n---\n", 4)
        if end >= 0:
            body = source[end + 5 :]
    body = re.sub(
        r"\[\[([a-z0-9][a-z0-9-]*)(?:\|([^\]]+))?\]\]",
        lambda m: f"[{m.group(2) or m.group(1).replace('-', ' ')}](/nodes/{m.group(1)})",
        body,
    )
    rendered = MARKDOWN.render(body)
    return re.sub(
        r'(<img\b[^>]*\bsrc=")(?!(?:https?:)?//|/)([^"]+)',
        r'\1/node-assets/\2',
        rendered,
    )


def _status(slug: str) -> dict[str, str]:
    with _db() as conn:
        row = conn.execute(
            "SELECT status, custom_label, note, updated_at FROM node_status WHERE slug = ?", (slug,)
        ).fetchone()
    if row is None:
        return {"status": "not_started", "custom_label": "", "note": "", "updated_at": ""}
    return dict(row)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return APP_HTML


@app.get("/nodes/{slug}", response_class=HTMLResponse)
def node_page(slug: str) -> str:
    _node_path(slug)
    return APP_HTML


@app.get("/node-assets/{filename}")
def node_asset(filename: str) -> FileResponse:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.svg", filename):
        raise HTTPException(404, "Asset not found")
    path = NODES_DIR / filename
    if not path.is_file():
        raise HTTPException(404, "Asset not found")
    return FileResponse(path, media_type="image/svg+xml")


@app.get("/api/nodes")
def list_nodes(q: str = Query(default="", max_length=200)) -> list[dict[str, str]]:
    needle = q.strip().lower()
    nodes = [_node_summary(path) for path in NODES_DIR.glob("*.md") if not path.name.endswith(".ko.md")]
    if needle:
        nodes = [n for n in nodes if needle in f"{n['title']} {n['slug']} {n['summary']} {n['tags']}".lower()]
    return sorted(nodes, key=lambda n: n["title"].lower())


@app.get("/api/nodes/{slug}")
def get_node(slug: str) -> dict[str, object]:
    path = _node_path(slug)
    source = path.read_text(encoding="utf-8")
    return {**_node_summary(path), "html": _render_markdown(source), "status": _status(slug)}


@app.get("/api/status/{slug}")
def get_status(slug: str) -> dict[str, str]:
    _node_path(slug)
    return _status(slug)


@app.put("/api/status/{slug}")
def put_status(slug: str, update: StatusUpdate) -> dict[str, str]:
    _node_path(slug)
    if update.status == "custom" and not update.custom_label.strip():
        raise HTTPException(422, "A custom status needs a label")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _db() as conn:
        conn.execute(
            """INSERT INTO node_status(slug, status, custom_label, note, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET status=excluded.status,
              custom_label=excluded.custom_label, note=excluded.note, updated_at=excluded.updated_at""",
            (slug, update.status, update.custom_label.strip(), update.note.strip(), now),
        )
    return _status(slug)


@app.get("/static-mirror")
def static_mirror() -> FileResponse:
    return FileResponse(STATIC_MIRROR, media_type="text/html", filename="principia-graph.html")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the private Principia local app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8876)
    args = parser.parse_args()
    uvicorn.run("principia_app.server:app", host=args.host, port=args.port)


APP_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Principia Local</title><style>
:root{color-scheme:dark;--bg:#0a0d12;--panel:#111722;--line:#273142;--text:#edf2f8;--muted:#9ba9bb;--accent:#8b9cff;--green:#58d39b;--red:#ff7d8d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 Inter,ui-sans-serif,system-ui,sans-serif}.app{display:grid;grid-template-columns:minmax(280px,360px) 1fr;height:100vh}.sidebar{border-right:1px solid var(--line);background:#0d121a;display:flex;flex-direction:column;min-height:0}.brand{padding:20px 22px 12px}.brand h1{margin:0;font-size:22px;letter-spacing:.02em}.brand p{margin:3px 0 0;color:var(--muted)}.toolbar{padding:10px 16px 14px}.toolbar input{width:100%;background:var(--panel);border:1px solid var(--line);border-radius:10px;color:var(--text);padding:11px 12px;font:inherit}.mirror{display:inline-block;margin-top:10px;color:var(--accent);text-decoration:none}.count{color:var(--muted);font-size:12px;margin-top:8px}.nodes{overflow:auto;padding:0 10px 18px}.node{display:block;width:100%;text-align:left;border:0;border-bottom:1px solid #1b2330;background:transparent;color:inherit;padding:13px 12px;cursor:pointer}.node:hover,.node.active{background:#171e2a;border-radius:9px}.node strong{display:block}.node span{display:block;color:var(--muted);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.main{overflow:auto;padding:34px clamp(24px,5vw,78px)}.empty{color:var(--muted);margin-top:25vh;text-align:center}.header{display:flex;gap:24px;align-items:flex-start;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:22px}.header h2{font-size:30px;margin:0}.slug{color:var(--muted);font-family:ui-monospace,monospace}.status-card{width:min(320px,100%);background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:14px}.status-card label{display:block;color:var(--muted);font-size:12px;margin:8px 0 4px}.status-card select,.status-card input,.status-card textarea{width:100%;background:#0c1119;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:8px;font:inherit}.status-card textarea{height:72px;resize:vertical}.status-card button{margin-top:10px;background:var(--accent);color:#081022;border:0;border-radius:8px;padding:8px 13px;font-weight:700;cursor:pointer}.saved{color:var(--green);font-size:12px;margin-left:8px}.content{max-width:850px;padding:26px 0 70px}.content h1:first-child{display:none}.content h2{margin-top:2em}.content a{color:#aeb9ff}.content pre,.content code{background:#151c28;border-radius:5px}.content pre{padding:14px;overflow:auto}.content blockquote{border-left:3px solid var(--accent);margin-left:0;padding-left:18px;color:#c5cfdd}@media(max-width:800px){.app{display:block}.sidebar{height:45vh;border-right:0;border-bottom:1px solid var(--line)}.main{height:55vh;padding:22px}.header{display:block}.status-card{margin-top:18px}}
</style></head><body><div class="app"><aside class="sidebar"><div class="brand"><h1>Principia</h1><p>Private local workspace</p></div><div class="toolbar"><input id="search" placeholder="Search concepts…" autofocus><a class="mirror" href="/static-mirror" target="_blank">Open static mirror ↗</a><div class="count" id="count"></div></div><div class="nodes" id="nodes"></div></aside><main class="main" id="main"><div class="empty">Choose a concept to read and track.</div></main></div><script>
const nodesEl=document.querySelector('#nodes'),main=document.querySelector('#main'),search=document.querySelector('#search');let current='';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function loadList(q=''){const data=await fetch('/api/nodes?q='+encodeURIComponent(q)).then(r=>r.json());document.querySelector('#count').textContent=data.length+' concepts';nodesEl.innerHTML=data.map(n=>`<button class="node ${n.slug===current?'active':''}" data-slug="${n.slug}"><strong>${esc(n.title)}</strong><span>${esc(n.summary)}</span></button>`).join('');nodesEl.querySelectorAll('.node').forEach(b=>b.onclick=()=>openNode(b.dataset.slug));}
async function openNode(slug){current=slug;const n=await fetch('/api/nodes/'+slug).then(r=>r.json());const s=n.status;main.innerHTML=`<div class="header"><div><div class="slug">${esc(n.slug)}</div><h2>${esc(n.title)}</h2><p>${esc(n.summary)}</p></div><div class="status-card"><strong>Private progress</strong><label>Status</label><select id="status"><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select><div id="customWrap"><label>Custom label</label><input id="custom" maxlength="80" value="${esc(s.custom_label)}"></div><label>Private note</label><textarea id="note" maxlength="4000">${esc(s.note)}</textarea><button id="save">Save</button><span class="saved" id="saved"></span><div class="count" id="updated">${s.updated_at?'Updated '+esc(s.updated_at):'Not updated yet'}</div></div></div><article class="content">${n.html}</article>`;document.querySelector('#status').value=s.status;toggleCustom();document.querySelector('#status').onchange=toggleCustom;document.querySelector('#save').onclick=saveStatus;await loadList(search.value);}
function toggleCustom(){document.querySelector('#customWrap').style.display=document.querySelector('#status').value==='custom'?'block':'none';}
async function saveStatus(){const payload={status:document.querySelector('#status').value,custom_label:document.querySelector('#custom').value,note:document.querySelector('#note').value};const r=await fetch('/api/status/'+current,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok){document.querySelector('#saved').textContent='Could not save';return}const s=await r.json();document.querySelector('#saved').textContent='Saved';document.querySelector('#updated').textContent='Updated '+s.updated_at;setTimeout(()=>document.querySelector('#saved').textContent='',1800);}
let timer;search.oninput=()=>{clearTimeout(timer);timer=setTimeout(()=>loadList(search.value),120)};loadList();const linked=location.pathname.match(/^\/nodes\/([a-z0-9][a-z0-9-]*)$/);if(linked)openNode(linked[1]);
</script></body></html>'''
