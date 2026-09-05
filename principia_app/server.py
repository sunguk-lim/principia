from __future__ import annotations

import argparse
import asyncio
import ipaddress
import json
import os
import re
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
NODES_DIR = ROOT / "nodes"
WEB_DIST = ROOT / "web" / "dist"
GRAPH_DATA = WEB_DIST / "data" / "graph.json"
LEGACY_GRAPH = ROOT / "web" / "graph.html"
DEFAULT_DB = Path.home() / ".local" / "share" / "principia" / "status.sqlite3"
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*")
TAILSCALE_NETWORK = ipaddress.ip_network("100.64.0.0/10")


class StatusUpdate(BaseModel):
    status: Literal["not_started", "in_progress", "blocked", "done", "custom"] = "not_started"
    custom_label: str = Field(default="", max_length=80)
    note: str = Field(default="", max_length=4000)


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """CREATE TABLE IF NOT EXISTS node_status (
        slug TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        custom_label TEXT NOT NULL DEFAULT '',
        note TEXT NOT NULL DEFAULT '',
        updated_at TEXT NOT NULL
        )"""
    )
    return connection


def require_node(slug: str) -> None:
    if not SLUG.fullmatch(slug) or not (NODES_DIR / f"{slug}.md").is_file():
        raise HTTPException(404, "Node not found")


def require_private_client(request: Request) -> None:
    host = request.client.host if request.client else ""
    if host == "testclient":
        return
    try:
        address = ipaddress.ip_address(host)
    except ValueError as error:
        raise HTTPException(403, "Codex sessions are available only on this device or Tailscale") from error
    if not (address.is_loopback or address in TAILSCALE_NETWORK):
        raise HTTPException(403, "Codex sessions are available only on this device or Tailscale")


def filter_principia_codex_sessions(catalog: dict[str, object]) -> list[dict[str, object]]:
    sessions = []
    for host in catalog.get("hosts", []):
        if not isinstance(host, dict):
            continue
        for session in host.get("sessions", []):
            if not isinstance(session, dict):
                continue
            cwd = session.get("cwd", "")
            try:
                belongs_to_principia = Path(str(cwd)).expanduser().resolve() == ROOT
            except (OSError, RuntimeError):
                belongs_to_principia = False
            if not belongs_to_principia:
                continue
            sessions.append(
                {
                    "threadId": session.get("threadId", ""),
                    "name": session.get("name") or "Untitled Codex session",
                    "cwd": cwd,
                    "status": session.get("status", "unknown"),
                    "source": session.get("source", "unknown"),
                    "gitBranch": session.get("gitBranch", ""),
                    "updatedAt": session.get("updatedAt"),
                    "canContinue": bool(session.get("canContinue")),
                    "host": host.get("label", "Local Codex"),
                }
            )
    sessions.sort(key=lambda item: item.get("updatedAt") or 0, reverse=True)
    return sessions


async def read_codex_catalog() -> dict[str, object]:
    openclaw = shutil.which("openclaw")
    if not openclaw:
        return {"available": False, "mode": "catalog", "sessions": []}
    process = await asyncio.create_subprocess_exec(
        openclaw,
        "codex",
        "sessions",
        "--agent",
        "main",
        "--limit",
        "20",
        "--json",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=20)
    except TimeoutError as error:
        process.kill()
        await process.communicate()
        raise HTTPException(504, "Codex session catalog timed out") from error
    if process.returncode != 0:
        detail = stderr.decode("utf-8", errors="replace").strip().splitlines()[-1:] or ["catalog unavailable"]
        raise HTTPException(503, f"Codex session catalog unavailable: {detail[0][:240]}")
    try:
        catalog = json.loads(stdout)
    except json.JSONDecodeError as error:
        raise HTTPException(503, "Codex session catalog returned invalid data") from error

    return {"available": True, "mode": "catalog", "sessions": filter_principia_codex_sessions(catalog)}


def create_app(db_path: Path | None = None, web_dist: Path = WEB_DIST) -> FastAPI:
    configured_db = (db_path or Path(os.environ.get("PRINCIPIA_STATUS_DB", DEFAULT_DB))).expanduser().resolve()
    with connect(configured_db):
        pass

    app = FastAPI(title="Principia", docs_url="/api/docs", openapi_url="/api/openapi.json")
    app.state.db_path = configured_db

    def read_status(slug: str) -> dict[str, str]:
        with connect(configured_db) as connection:
            row = connection.execute(
                "SELECT status, custom_label, note, updated_at FROM node_status WHERE slug = ?", (slug,)
            ).fetchone()
        return dict(row) if row else {"status": "not_started", "custom_label": "", "note": "", "updated_at": ""}

    @app.get("/api/health")
    def health() -> dict[str, object]:
        return {
            "ok": True,
            "graph": GRAPH_DATA.is_file(),
            "statusStore": "sqlite",
            "codexCatalog": bool(shutil.which("openclaw")),
        }

    @app.get("/api/graph")
    def graph_data() -> FileResponse:
        return FileResponse(GRAPH_DATA, media_type="application/json")

    @app.get("/api/status")
    def list_statuses() -> dict[str, dict[str, str]]:
        with connect(configured_db) as connection:
            rows = connection.execute(
                "SELECT slug, status, custom_label, note, updated_at FROM node_status ORDER BY slug"
            ).fetchall()
        return {row["slug"]: {key: row[key] for key in ("status", "custom_label", "note", "updated_at")} for row in rows}

    @app.get("/api/status/{slug}")
    def get_status(slug: str) -> dict[str, str]:
        require_node(slug)
        return read_status(slug)

    @app.put("/api/status/{slug}")
    def put_status(slug: str, update: StatusUpdate) -> dict[str, str]:
        require_node(slug)
        custom_label = update.custom_label.strip()
        if update.status == "custom" and not custom_label:
            raise HTTPException(422, "A custom status needs a label")
        if update.status != "custom":
            custom_label = ""
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with connect(configured_db) as connection:
            connection.execute(
                """INSERT INTO node_status(slug, status, custom_label, note, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(slug) DO UPDATE SET status=excluded.status,
                  custom_label=excluded.custom_label, note=excluded.note, updated_at=excluded.updated_at""",
                (slug, update.status, custom_label, update.note.strip(), now),
            )
        return read_status(slug)

    @app.get("/api/codex/sessions")
    async def codex_sessions(request: Request) -> dict[str, object]:
        require_private_client(request)
        return await read_codex_catalog()

    @app.get("/legacy-graph")
    def legacy_graph() -> FileResponse:
        return FileResponse(LEGACY_GRAPH, media_type="text/html")

    app.mount("/", StaticFiles(directory=web_dist, html=True, check_dir=False), name="frontend")
    return app


app = create_app()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Principia local app.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8876)
    args = parser.parse_args()
    uvicorn.run("principia_app.server:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
