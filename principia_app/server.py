from __future__ import annotations

import argparse
import json
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


@app.get("/graph", response_class=HTMLResponse)
def integrated_graph() -> HTMLResponse:
    source = STATIC_MIRROR.read_text(encoding="utf-8")
    with _db() as conn:
        rows = conn.execute(
            "SELECT slug, status, custom_label, note, updated_at FROM node_status"
        ).fetchall()
    private_status = {row["slug"]: dict(row) for row in rows}

    select_line = "    selId = (id && byId.has(id)) ? id : null;"
    bridge = (
        select_line
        + "\n    window.parent.postMessage({type: 'principia-node-selected', slug: selId}, window.location.origin);"
    )
    if select_line not in source:
        raise HTTPException(500, "Graph integration marker not found")
    source = source.replace(select_line, bridge, 1)

    doc_base = 'const docBase = DATA.docBase || "";'
    status_script = f"""const docBase = "/nodes";
  const PRIVATE_STATUS = {json.dumps(private_status, ensure_ascii=False).replace("</", "<\\/")};
  const privateStatusLabel = id => {{
    const record = PRIVATE_STATUS[id];
    if (!record) return "Not started";
    if (record.status === "custom") return record.custom_label || "Custom";
    return ({{not_started:"Not started",in_progress:"In progress",blocked:"Blocked",done:"Done"}})[record.status] || "Not started";
  }};
  const privateStatusClass = id => "study-" + ((PRIVATE_STATUS[id] || {{status:"not_started"}}).status || "not_started");"""
    if doc_base not in source:
        raise HTTPException(500, "Graph document-link marker not found")
    source = source.replace(doc_base, status_script, 1)

    roadmap_title = '<span class="rtitle" data-go="${id}">${nn.title}${tgt ? " — current" : ""}</span>` +'
    roadmap_status = roadmap_title + '\n              `<span class="study-status ${privateStatusClass(id)}">${privateStatusLabel(id)}</span>` +'
    if roadmap_title not in source:
        raise HTTPException(500, "Graph roadmap marker not found")
    source = source.replace(roadmap_title, roadmap_status, 1)

    css_marker = "  .rstep.tgt { background: #243056; font-weight: 600; }"
    css = css_marker + """
  .study-status { flex-shrink:0;padding:2px 6px;border-radius:999px;border:1px solid #566278;color:#cbd5e1;font-size:10px;line-height:1.25;white-space:nowrap; }
  .study-in_progress { border-color:#e6a417;color:#ffd166;background:#6b4f142e; }
  .study-blocked { border-color:#e5484d;color:#ff8e95;background:#6b1b1f35; }
  .study-done { border-color:#2fbf87;color:#65e6b3;background:#164c3938; }
  .study-custom { border-color:#8b9cff;color:#bcc5ff;background:#32396b45; }"""
    if css_marker not in source:
        raise HTTPException(500, "Graph roadmap-style marker not found")
    source = source.replace(css_marker, css, 1)

    end_marker = "})();\n</script>"
    listener = """  window.addEventListener("message", event => {
    if (event.origin !== window.location.origin || event.data?.type !== "principia-status-updated") return;
    PRIVATE_STATUS[event.data.slug] = event.data.status;
    if (selId) renderDetails();
  });
})();
</script>"""
    if end_marker not in source:
        raise HTTPException(500, "Graph script marker not found")
    source = source.replace(end_marker, listener, 1)
    return HTMLResponse(source)


@app.get("/static-mirror")
def static_mirror() -> FileResponse:
    return FileResponse(STATIC_MIRROR, media_type="text/html")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the private Principia local app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8876)
    args = parser.parse_args()
    uvicorn.run("principia_app.server:app", host=args.host, port=args.port)


APP_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Principia Local</title><style>
:root{color-scheme:dark;--bg:#0a0d12;--panel:#111722;--line:#273142;--text:#edf2f8;--muted:#9ba9bb;--accent:#8b9cff;--green:#58d39b}*{box-sizing:border-box}html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);color:var(--text);font:15px/1.5 Inter,ui-sans-serif,system-ui,sans-serif}.app{display:grid;grid-template-columns:300px minmax(0,1fr);height:100%}.sidebar{border-right:1px solid var(--line);background:#0d121a;display:flex;flex-direction:column;min-height:0}.brand{padding:17px 18px 9px;display:flex;align-items:center;justify-content:space-between}.brand h1{margin:0;font-size:21px}.graph-button{border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:8px;padding:7px 10px;cursor:pointer}.toolbar{padding:8px 13px 12px}.toolbar input{width:100%;background:var(--panel);border:1px solid var(--line);border-radius:9px;color:var(--text);padding:10px 11px;font:inherit}.count{color:var(--muted);font-size:12px;margin-top:7px}.nodes{overflow:auto;padding:0 7px 15px}.node{display:block;width:100%;text-align:left;border:0;border-bottom:1px solid #1b2330;background:transparent;color:inherit;padding:11px 10px;cursor:pointer}.node:hover,.node.active{background:#171e2a;border-radius:8px}.node strong,.node span{display:block}.node span{color:var(--muted);font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.workspace{position:relative;min-width:0;height:100%}.graph-frame{display:block;width:100%;height:100%;border:0;background:#0b0f17}.inspector{position:absolute;z-index:5;top:0;right:0;width:min(520px,48vw);height:100%;overflow:auto;background:rgba(10,13,18,.97);border-left:1px solid var(--line);box-shadow:-18px 0 40px #0008;padding:22px 24px 60px}.inspector[hidden]{display:none}.close{position:sticky;float:right;top:0;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:50%;width:34px;height:34px;font-size:20px;cursor:pointer}.slug{color:var(--muted);font:12px ui-monospace,monospace}.inspector h2{font-size:26px;margin:5px 42px 5px 0}.summary{color:#c4cfdd}.status-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:13px;margin:18px 0}.status-card label{display:block;color:var(--muted);font-size:12px;margin:8px 0 4px}.status-card select,.status-card input,.status-card textarea{width:100%;background:#0c1119;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:8px;font:inherit}.status-card textarea{height:68px;resize:vertical}.status-card button{margin-top:10px;background:var(--accent);color:#081022;border:0;border-radius:8px;padding:8px 13px;font-weight:700;cursor:pointer}.saved{color:var(--green);font-size:12px;margin-left:8px}.content h1:first-child{display:none}.content h2{margin-top:1.8em}.content a{color:#aeb9ff}.content pre,.content code{background:#151c28;border-radius:5px}.content pre{padding:12px;overflow:auto}.content img{max-width:100%}.content blockquote{border-left:3px solid var(--accent);margin-left:0;padding-left:15px;color:#c5cfdd}@media(max-width:800px){.app{grid-template-columns:1fr}.sidebar{position:absolute;z-index:4;left:8px;top:56px;width:min(82vw,310px);height:calc(100% - 70px);border:1px solid var(--line);border-radius:12px;box-shadow:0 15px 40px #000b;transform:translateX(calc(-100% - 18px));transition:transform .18s}.sidebar.open{transform:none}.mobile-bar{display:flex!important;position:absolute;z-index:6;left:10px;top:10px;gap:8px}.inspector{width:100%;padding-top:58px}.graph-frame{height:100%}}.mobile-bar{display:none}.mobile-bar button{border:1px solid #46546a;background:#111a27dd;color:white;border-radius:9px;padding:9px 12px;font-weight:700}
</style></head><body><div class="app"><aside class="sidebar" id="sidebar"><div class="brand"><h1>Principia</h1><button class="graph-button" id="graphBtn">Graph</button></div><div class="toolbar"><input id="search" placeholder="Search concepts…"><div class="count" id="count"></div></div><div class="nodes" id="nodes"></div></aside><section class="workspace"><iframe class="graph-frame" id="graph" src="/graph" title="Interactive Principia knowledge graph"></iframe><aside class="inspector" id="inspector" hidden></aside><div class="mobile-bar"><button id="menuBtn">Concepts</button><button id="mobileGraphBtn">Graph</button></div></section></div><script>
const nodesEl=document.querySelector('#nodes'),search=document.querySelector('#search'),inspector=document.querySelector('#inspector'),sidebar=document.querySelector('#sidebar');let current='';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function loadList(q=''){const data=await fetch('/api/nodes?q='+encodeURIComponent(q)).then(r=>r.json());document.querySelector('#count').textContent=data.length+' concepts';nodesEl.innerHTML=data.map(n=>`<button class="node ${n.slug===current?'active':''}" data-slug="${n.slug}"><strong>${esc(n.title)}</strong><span>${esc(n.summary)}</span></button>`).join('');nodesEl.querySelectorAll('.node').forEach(b=>b.onclick=()=>openNode(b.dataset.slug));}
async function openNode(slug){current=slug;const n=await fetch('/api/nodes/'+slug).then(r=>r.json());const s=n.status;inspector.hidden=false;inspector.innerHTML=`<button class="close" id="closeInspector" aria-label="Close">×</button><div class="slug">${esc(n.slug)}</div><h2>${esc(n.title)}</h2><p class="summary">${esc(n.summary)}</p><div class="status-card"><strong>Private progress</strong><label>Status</label><select id="status"><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select><div id="customWrap"><label>Custom label</label><input id="custom" maxlength="80" value="${esc(s.custom_label)}"></div><label>Private note</label><textarea id="note" maxlength="4000">${esc(s.note)}</textarea><button id="save">Save</button><span class="saved" id="saved"></span><div class="count" id="updated">${s.updated_at?'Updated '+esc(s.updated_at):'Not updated yet'}</div></div><article class="content">${n.html}</article>`;document.querySelector('#status').value=s.status;toggleCustom();document.querySelector('#status').onchange=toggleCustom;document.querySelector('#save').onclick=saveStatus;document.querySelector('#closeInspector').onclick=showGraph;sidebar.classList.remove('open');await loadList(search.value);history.replaceState(null,'','/nodes/'+slug);}
function showGraph(){inspector.hidden=true;current='';sidebar.classList.remove('open');history.replaceState(null,'','/');loadList(search.value);}
function toggleCustom(){document.querySelector('#customWrap').style.display=document.querySelector('#status').value==='custom'?'block':'none';}
async function saveStatus(){const payload={status:document.querySelector('#status').value,custom_label:document.querySelector('#custom').value,note:document.querySelector('#note').value};const r=await fetch('/api/status/'+current,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok){document.querySelector('#saved').textContent='Could not save';return}const s=await r.json();document.querySelector('#graph').contentWindow.postMessage({type:'principia-status-updated',slug:current,status:s},location.origin);document.querySelector('#saved').textContent='Saved';document.querySelector('#updated').textContent='Updated '+s.updated_at;setTimeout(()=>document.querySelector('#saved').textContent='',1800);}
window.addEventListener('message',e=>{if(e.origin===location.origin&&e.data?.type==='principia-node-selected'&&e.data.slug)openNode(e.data.slug)});
let timer;search.oninput=()=>{clearTimeout(timer);timer=setTimeout(()=>loadList(search.value),120)};document.querySelector('#graphBtn').onclick=showGraph;document.querySelector('#mobileGraphBtn').onclick=showGraph;document.querySelector('#menuBtn').onclick=()=>sidebar.classList.toggle('open');loadList();const linked=location.pathname.match(/^\/nodes\/([a-z0-9][a-z0-9-]*)$/);if(linked)openNode(linked[1]);
</script></body></html>'''
