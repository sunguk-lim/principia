import unittest

from principia_app.ontology import admission, allowed_links, identities, relations, validate


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


if __name__ == "__main__":
    unittest.main()
