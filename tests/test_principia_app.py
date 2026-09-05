from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from principia_app.server import GRAPH_DATA, LEGACY_GRAPH, ROOT, create_app, filter_principia_codex_sessions


class PrincipiaAppTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "status.sqlite3"
        self.client = TestClient(create_app(self.db_path))

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_generated_graph_is_the_shared_source_for_frontend_and_server(self) -> None:
        generated = json.loads(GRAPH_DATA.read_text())
        served = self.client.get("/api/graph")
        self.assertEqual(served.status_code, 200)
        self.assertEqual(served.content, GRAPH_DATA.read_bytes())
        self.assertEqual(generated["schemaVersion"], 1)
        self.assertGreater(len(generated["nodes"]), 300)
        self.assertGreater(len(generated["edges"]), 600)
        node = next(item for item in generated["nodes"] if item["id"] == "post-training-quantization")
        self.assertIn("Post-training quantization", node["body"])
        self.assertIn("quantization", node["prereqs"])

    def test_home_is_the_compiled_react_app(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('<div id="root"></div>', response.text)
        self.assertIn('./assets/app.js', response.text)
        self.assertEqual(self.client.get("/assets/app.js").status_code, 200)

    def test_private_status_round_trip_and_list(self) -> None:
        payload = {"status": "custom", "custom_label": "Review equations", "note": "Work the example"}
        saved = self.client.put("/api/status/post-training-quantization", json=payload)
        self.assertEqual(saved.status_code, 200)
        self.assertEqual(saved.json()["custom_label"], "Review equations")
        self.assertEqual(self.client.get("/api/status").json()["post-training-quantization"], saved.json())
        with sqlite3.connect(self.db_path) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM node_status").fetchone()[0], 1)

    def test_invalid_status_and_node_are_rejected(self) -> None:
        self.assertEqual(self.client.put("/api/status/missing-node", json={"status": "done"}).status_code, 404)
        self.assertEqual(self.client.put("/api/status/quantization", json={"status": "custom"}).status_code, 422)

    def test_codex_catalog_only_exposes_principia_sessions(self) -> None:
        catalog = {
            "hosts": [{
                "label": "Local Codex",
                "sessions": [
                    {
                        "threadId": "principia-thread",
                        "name": "principia",
                        "cwd": str(ROOT),
                        "status": "notLoaded",
                        "source": "cli",
                        "gitBranch": "main",
                        "updatedAt": 20,
                        "canContinue": True,
                        "sessionKey": "must-not-leak",
                    },
                    {"threadId": "other-thread", "name": "other", "cwd": str(ROOT.parent), "updatedAt": 30},
                ],
            }]
        }
        sessions = filter_principia_codex_sessions(catalog)
        self.assertEqual([session["threadId"] for session in sessions], ["principia-thread"])
        self.assertNotIn("sessionKey", sessions[0])
        self.assertEqual(sessions[0]["host"], "Local Codex")

    def test_legacy_graph_remains_byte_identical(self) -> None:
        response = self.client.get("/legacy-graph")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(hashlib.sha256(response.content).digest(), hashlib.sha256(LEGACY_GRAPH.read_bytes()).digest())


if __name__ == "__main__":
    unittest.main()
