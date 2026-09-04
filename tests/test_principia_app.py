from __future__ import annotations

import hashlib
import importlib
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


class PrincipiaAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        os.environ["PRINCIPIA_STATUS_DB"] = str(Path(cls.tmp.name) / "status.sqlite3")
        import principia_app.server as server
        cls.server = importlib.reload(server)
        cls.client = TestClient(cls.server.app)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_node_list_is_searchable_and_home_is_graph_first(self):
        response = self.client.get("/api/nodes", params={"q": "quantization"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(n["slug"] == "post-training-quantization" for n in response.json()))
        home = self.client.get("/")
        self.assertIn('src="/graph"', home.text)
        self.assertIn("Interactive Principia knowledge graph", home.text)

    def test_integrated_graph_bridges_selection_and_shows_roadmap_status(self):
        self.client.put(
            "/api/status/post-training-quantization",
            json={"status": "in_progress", "custom_label": "", "note": "Study next"},
        )
        response = self.client.get("/graph")
        self.assertEqual(response.status_code, 200)
        self.assertIn('id="cv"', response.text)
        self.assertIn("principia-node-selected", response.text)
        self.assertIn("principia-status-updated", response.text)
        self.assertIn('const docBase = "/nodes";', response.text)
        self.assertIn('"post-training-quantization": {"slug": "post-training-quantization", "status": "in_progress"', response.text)
        self.assertIn("privateStatusLabel(id)", response.text)
        self.assertIn("study-status", response.text)

    def test_node_content_renders_markdown_and_wikilinks(self):
        response = self.client.get("/api/nodes/post-training-quantization")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("<h2>Summary</h2>", body["html"])
        self.assertIn('/nodes/quantization', body["html"])
        illustrated = self.client.get("/api/nodes/flash-attention").json()
        self.assertIn('/node-assets/flash-attention.svg', illustrated["html"])
        self.assertEqual(self.client.get("/nodes/post-training-quantization").status_code, 200)

    def test_status_round_trip_uses_sqlite(self):
        response = self.client.put("/api/status/post-training-quantization", json={
            "status": "in_progress", "custom_label": "", "note": "Review calibration examples"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "in_progress")
        saved = self.client.get("/api/status/post-training-quantization").json()
        self.assertEqual(saved["note"], "Review calibration examples")
        with sqlite3.connect(self.server.DB_PATH) as conn:
            self.assertEqual(conn.execute("select count(*) from node_status").fetchone()[0], 1)

    def test_static_mirror_is_byte_identical(self):
        expected = (self.server.ROOT / "web" / "graph.html").read_bytes()
        response = self.client.get("/static-mirror")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(hashlib.sha256(response.content).digest(), hashlib.sha256(expected).digest())


if __name__ == "__main__":
    unittest.main()
