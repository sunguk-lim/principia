from __future__ import annotations

import argparse
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException
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
        return {"ok": True, "graph": GRAPH_DATA.is_file(), "statusStore": "sqlite"}

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
