import unittest

from pathlib import Path
from tempfile import TemporaryDirectory

from principia_app.ontology import admission, allowed_links, identities, identity_candidates, prerequisite_evidence, relations, validate


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


if __name__ == "__main__":
    unittest.main()
