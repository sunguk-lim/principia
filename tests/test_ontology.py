import json
import unittest
from unittest.mock import patch

from pathlib import Path
from tempfile import TemporaryDirectory

from principia_app.ontology import admission, allowed_links, enrich, identities, identity_candidates, prerequisite_evidence, relations, validate
from principia_app.neo4j import learning_subgraph, semantic_audit, semantic_sections, snapshot


class OntologyTests(unittest.TestCase):
    def setUp(self):
        self.nodes = {
            "a": {"title": "Alpha", "prereqs": "[]"},
            "b": {"title": "Beta", "prereqs": "[a]"},
            "c": {"title": "Gamma", "prereqs": "[]"},
        }

    def test_alias_resolves_to_existing_concept(self):
        extra = {"concepts": {"a": {"aliases": ["First concept"]}}}
        self.assertEqual(admission("FIRST CONCEPT", self.nodes, extra)["exact"], ["a"])

    def test_collision_requires_explicit_disambiguation(self):
        extra = {"concepts": {"a": {"aliases": ["Beta"]}}}
        self.assertTrue(validate(self.nodes, extra))
        extra["disambiguations"] = {"beta": ["a", "b"]}
        self.assertEqual(validate(self.nodes, extra), [])

    def test_optional_link_does_not_become_prerequisite(self):
        extra = {"concepts": {"b": {"relations": [
            {"type": "CONTRASTS_WITH", "target": "c", "reason": "Different mechanism"}
        ]}}}
        self.assertEqual(validate(self.nodes, extra), [])
        self.assertEqual(allowed_links("b", self.nodes, extra), {"a", "c"})
        required = [r["t"] for r in relations(self.nodes, extra) if r["type"] == "REQUIRES"]
        self.assertEqual(required, ["a"])

    def test_contrast_relation_preserves_distinct_concepts(self):
        extra = {"concepts": {"a": {"relations": [
            {"type": "CONTRASTS_WITH", "target": "c", "reason": "Same problem, different mechanism."}
        ]}}}
        self.assertEqual(validate(self.nodes, extra), [])
        contrast = [r for r in relations(self.nodes, extra) if r["type"] == "CONTRASTS_WITH"]
        self.assertEqual(contrast, [{"s": "a", "t": "c", "type": "CONTRASTS_WITH",
                                     "reason": "Same problem, different mechanism.", "reviewed": True}])

    def test_unsupported_relation_is_rejected(self):
        extra = {"concepts": {"a": {"relations": [
            {"type": "USES", "target": "c", "reason": "Uses the target's cost model."}
        ]}}}
        self.assertTrue(any("invalid" in error for error in validate(self.nodes, extra)))

    def test_direct_requirements_are_preserved_for_goal_retrieval(self):
        self.nodes["c"]["prereqs"] = "[a, b]"
        required = {(r["s"], r["t"]) for r in relations(self.nodes, {}) if r["type"] == "REQUIRES"}
        self.assertEqual(required, {("b", "a"), ("c", "a"), ("c", "b")})

    def test_enriched_reader_graph_is_an_overview_not_a_goal_roadmap(self):
        self.nodes["c"]["prereqs"] = "[a, b]"
        data = {"nodes": [{"id": nid} for nid in self.nodes], "edges": []}
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "lessons").mkdir()
            enrich(data, self.nodes, root)
        by_id = {node["id"]: node for node in data["nodes"]}
        self.assertEqual(by_id["c"]["prereqs"], ["a", "b"])
        self.assertEqual({(edge["s"], edge["t"]) for edge in data["edges"]}, {("b", "a"), ("c", "a"), ("c", "b")})

    def test_legacy_source_id_resolves_to_first_semantic_entity_for_roadmap(self):
        with patch("principia_app.neo4j.query", side_effect=[
            [["ent-goal"]], [["ent-prerequisite"], ["ent-goal"]],
            [["ent-goal", "ent-prerequisite", "Required mechanism"]],
        ]) as mocked:
            result = learning_subgraph("legacy-source")
        self.assertEqual(result["target"], "legacy-source")
        self.assertEqual(result["requiredIds"], ["ent-prerequisite", "ent-goal"])
        self.assertEqual(result["requiredEdges"][0]["reason"], "Required mechanism")
        self.assertEqual(mocked.call_args_list[0].kwargs["reference"], "legacy-source")

    def test_cycle_is_rejected(self):
        self.nodes["a"]["prereqs"] = "[b]"
        self.assertTrue(any("Prerequisite cycle" in e for e in validate(self.nodes, {})))

    def test_missing_prerequisite_is_rejected(self):
        self.nodes["a"]["prereqs"] = "[missing]"
        self.assertTrue(any("missing prerequisite" in e for e in validate(self.nodes, {})))

    def test_preserved_duplicate_resolves_to_one_canonical_identity(self):
        self.nodes["b"]["title"] = "Alpha theorem"
        extra = {"concepts": {"a": {"aliases": ["Alpha theorem"]}, "b": {"canonicalId": "a"}}}
        self.assertEqual(validate(self.nodes, extra), [])
        self.assertEqual(identities(self.nodes, extra)["alpha theorem"], ["a"])
        self.assertEqual([edge for edge in relations(self.nodes, extra) if edge["s"] == "a" and edge["t"] == "a"], [])

    def test_canonical_identity_cannot_chain(self):
        extra = {"concepts": {"a": {"canonicalId": "b"}, "b": {"canonicalId": "c"}}}
        self.assertTrue(any("must not point" in e for e in validate(self.nodes, extra)))

    def test_content_candidates_read_complete_node_bodies(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "nodes").mkdir()
            (root / "nodes" / "a.md").write_text("Shared unique mechanism evidence", encoding="utf-8")
            (root / "nodes" / "b.md").write_text("Shared unique mechanism evidence", encoding="utf-8")
            (root / "nodes" / "c.md").write_text("Different unrelated topic", encoding="utf-8")
            pairs = identity_candidates(self.nodes, root, threshold=0.1)
        self.assertEqual(pairs[0]["first"], "a")
        self.assertEqual(pairs[0]["second"], "b")

    def test_prerequisite_evidence_reads_only_node_body(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "nodes").mkdir()
            (root / "nodes" / "a.md").write_text("---\nprereqs: []\n---\n", encoding="utf-8")
            (root / "nodes" / "b.md").write_text("---\nprereqs: [a]\n---\nUses [[a]] in the explanation.", encoding="utf-8")
            evidence = prerequisite_evidence({"a": self.nodes["a"], "b": self.nodes["b"]}, root)
        self.assertEqual(evidence, [{"concept": "b", "prerequisite": "a", "bodyLink": True, "reviewedReason": False}])

    def test_legacy_uses_relation_is_not_accepted(self):
        nodes = {
            "curl": {"title": "Curl", "prereqs": "[]"},
            "gradient": {"title": "Gradient", "prereqs": "[]"},
            "identity": {"title": "Curl of a gradient", "prereqs": "[curl, gradient]"},
            "overview": {"title": "Differential operators", "prereqs": "[curl]"},
        }
        extra = {"concepts": {"identity": {"relations": [{
            "type": "USES", "target": "overview", "reason": "Contextual family overview."
        }]}}}
        self.assertTrue(any("invalid" in error for error in validate(nodes, extra)))

    def test_semantic_sections_use_authored_boundaries_not_word_count(self):
        long_mechanism = " ".join(["mechanism"] * 500)
        body = """# Example

## Summary

The overview.

## Grounded explanation

**1 — The mechanism.** First semantic unit.

{long_mechanism}

**Why it matters.** Second semantic unit.

## Prerequisites

- [[a]]

## Sources

- A source
""".format(long_mechanism=long_mechanism)
        sections = semantic_sections("example", body)
        self.assertEqual([section["heading"] for section in sections], [
            "Overview", "1 — The mechanism", "Why it matters",
        ])
        self.assertGreater(sections[1]["wordCount"], 280)
        self.assertNotIn("[[a]]", "\n".join(section["content"] for section in sections))
        self.assertNotIn("A source", "\n".join(section["content"] for section in sections))

    def test_structural_explanation_headings_do_not_duplicate_overview_candidates(self):
        body = """# Example

## Summary

The short framing.

## Grounded explanation

The complete explanation.

**Mechanism.** A distinct mechanism.
"""
        sections = semantic_sections("example", body)
        self.assertEqual([section["heading"] for section in sections], ["Overview", "Mechanism"])
        self.assertIn("short framing", sections[0]["content"])
        self.assertIn("complete explanation", sections[0]["content"])

    def test_semantic_audit_candidates_carry_traceability_but_no_entity_identity(self):
        # Candidate extraction may identify a review target, but resolving its
        # identity is an explicit editorial decision.
        body = "# Example\n\n## Grounded explanation\n\n**Mechanism.** An explanation."
        section = semantic_sections("example", body)[0]
        self.assertTrue(section["candidateKey"].startswith("cand-"))
        self.assertNotIn("entityId", section)
        self.assertTrue(section["contentHash"])

    def test_sync_refuses_an_incomplete_semantic_review(self):
        with patch("principia_app.neo4j.semantic_audit", return_value={"complete": False, "resolvedCandidates": 1, "semanticCandidates": 2}), patch("principia_app.neo4j.snapshot") as snapshot:
            with self.assertRaisesRegex(ValueError, "Semantic review incomplete: 1/2"):
                __import__("principia_app.neo4j", fromlist=["sync"]).sync(self.nodes, {})
        snapshot.assert_not_called()

    def test_semantic_audit_rejects_stale_editorial_resolution(self):
        body = "# Example\n\n## Grounded explanation\n\n**Mechanism.** An explanation."
        nodes = {"example": {"title": "Example", "type": "concept", "tags": "[math/example]", "prereqs": "[]"}}
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            nodes_dir = root / "nodes"; nodes_dir.mkdir()
            ontology_dir = root / "ontology"; ontology_dir.mkdir()
            (nodes_dir / "example.md").write_text(body, encoding="utf-8")
            (ontology_dir / "semantic-resolutions.json").write_text(json.dumps({
                "schemaVersion": 1,
                "decisions": [{"candidateKey": "cand-stale", "decision": "retain"}],
            }), encoding="utf-8")
            with patch("principia_app.neo4j.brain.NODES", nodes_dir), patch("principia_app.neo4j.brain.ROOT", root):
                with self.assertRaisesRegex(ValueError, "Invalid semantic resolution decision"):
                    semantic_audit(nodes, {})

    def test_snapshot_does_not_turn_authored_sections_into_entities(self):
        body = """# Example

## Grounded explanation

**1 — First mechanism.** An explanation.

**2 — Second mechanism.** Another explanation.
"""
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            nodes_dir = root / "nodes"
            nodes_dir.mkdir()
            (nodes_dir / "example.md").write_text(body, encoding="utf-8")
            nodes = {"example": {"title": "Example", "type": "concept", "tags": "[math/example]", "prereqs": "[]", "summary": "One concept."}}
            with patch("principia_app.neo4j.brain.NODES", nodes_dir):
                data = snapshot(nodes, {})
        self.assertEqual(len(data["entities"]), 1)
        self.assertEqual(data["entities"][0]["canonicalName"], "Example")
        self.assertEqual(data["entities"][0]["segmentCount"], 1)
        self.assertEqual(data["relations"], [])



if __name__ == "__main__":
    unittest.main()
