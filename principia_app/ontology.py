"""Deterministic identity, relation, and learning-quality checks.

Markdown remains authoritative. ontology/catalog.json adds reviewed identity and
relation metadata; Neo4j and the browser consume the same validated projection.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path

import brain

RELATIONS = {"ALTERNATIVE_TO", "CONTRASTS_WITH", "APPLIES_TO"}


def normalize(label: str) -> str:
    return " ".join(re.findall(r"\w+", unicodedata.normalize("NFKC", label).casefold()))


def catalog(root: Path) -> dict:
    path = root / "ontology" / "catalog.json"
    return json.loads(path.read_text()) if path.exists() else {"concepts": {}, "disambiguations": {}}


def canonical_id(nid: str, nodes: dict, extra: dict) -> str:
    """Return the canonical identity for a preserved source node.

    ``canonicalId`` is deliberately non-destructive: the old article remains in
    Git, but the ontology and learner resolve it to its canonical concept.
    Validation rejects chains, cycles, and unknown targets, so consumers never
    need to guess which identity to use.
    """
    target = extra.get("concepts", {}).get(nid, {}).get("canonicalId", nid)
    return target if isinstance(target, str) and target else nid


def canonical_ids(nodes: dict, extra: dict) -> dict[str, str]:
    return {nid: canonical_id(nid, nodes, extra) for nid in nodes}


def identities(nodes: dict, extra: dict) -> dict[str, list[str]]:
    index: dict[str, set[str]] = {}
    for nid, node in nodes.items():
        canonical = canonical_id(nid, nodes, extra)
        for name in [nid, node.get("title", nid), *extra.get("concepts", {}).get(nid, {}).get("aliases", [])]:
            index.setdefault(normalize(name), set()).add(canonical)
    return {key: sorted(value) for key, value in sorted(index.items())}


def relations(nodes: dict, extra: dict) -> list[dict]:
    result = []
    seen = set()
    for nid, meta in sorted(nodes.items()):
        record = extra.get("concepts", {}).get(nid, {})
        source = canonical_id(nid, nodes, extra)
        for target in brain.parse_list(meta.get("prereqs", "")):
            reason = record.get("prerequisiteReasons", {}).get(target, "")
            edge = {"s": source, "t": canonical_id(target, nodes, extra), "type": "REQUIRES", "reason": reason,
                    "reviewed": bool(reason)}
            key = (edge["s"], edge["t"], edge["type"])
            if edge["s"] != edge["t"] and key not in seen:
                seen.add(key)
                result.append(edge)
        for relation in record.get("relations", []):
            edge = {"s": source, "t": canonical_id(relation["target"], nodes, extra), "type": relation["type"],
                    "reason": relation["reason"], "reviewed": True}
            key = (edge["s"], edge["t"], edge["type"])
            if edge["s"] != edge["t"] and key not in seen:
                seen.add(key)
                result.append(edge)
    return result


def allowed_links(nid: str, nodes: dict, extra: dict) -> set[str]:
    inherited = set()
    pending = list(brain.parse_list(nodes[nid].get("prereqs", "")))
    while pending:
        target = pending.pop()
        if target not in inherited and target in nodes:
            inherited.add(target)
            pending.extend(brain.parse_list(nodes[target].get("prereqs", "")))
    return inherited | {
        item["target"] for item in extra.get("concepts", {}).get(nid, {}).get("relations", [])
    }


def validate(nodes: dict, extra: dict) -> list[str]:
    errors = []
    for nid, record in extra.get("concepts", {}).items():
        if nid not in nodes:
            errors.append(f"Unknown catalog concept: {nid}")
            continue
        canonical = record.get("canonicalId")
        if canonical is not None:
            if not isinstance(canonical, str) or canonical not in nodes or canonical == nid:
                errors.append(f"{nid}: invalid canonical identity")
            elif extra.get("concepts", {}).get(canonical, {}).get("canonicalId"):
                errors.append(f"{nid}: canonical identity must not point to another alias")
        for alias in record.get("aliases", []):
            if not isinstance(alias, str) or not normalize(alias):
                errors.append(f"{nid}: empty or invalid alias")
        for target, reason in record.get("prerequisiteReasons", {}).items():
            if target not in brain.parse_list(nodes[nid].get("prereqs", "")) or not reason.strip():
                errors.append(f"{nid}: invalid prerequisite rationale for {target}")
        seen = set()
        for r in record.get("relations", []):
            key = (r.get("type"), r.get("target"))
            if (key in seen or r.get("type") not in RELATIONS or r.get("target") not in nodes
                    or r.get("target") == nid or not r.get("reason", "").strip()):
                errors.append(f"{nid}: invalid or duplicate relation {key}")
            seen.add(key)
    index = identities(nodes, extra)
    disambiguations = extra.get("disambiguations", {})
    for label, matches in index.items():
        if len(matches) > 1 and sorted(disambiguations.get(label, [])) != matches:
            errors.append(f"Identity collision needs disambiguation: {label}: {matches}")
    for label, matches in disambiguations.items():
        if normalize(label) != label or len(set(matches)) < 2 or sorted(matches) != index.get(label):
            errors.append(f"Invalid disambiguation: {label}")
    # A required-learning cycle has no valid first step. Never silently truncate it.
    visited, active = set(), []
    def visit(nid):
        if nid in active:
            errors.append("Prerequisite cycle: " + " -> ".join(active[active.index(nid):] + [nid]))
            return
        if nid in visited:
            return
        active.append(nid)
        for target in brain.parse_list(nodes[nid].get("prereqs", "")):
            if target not in nodes:
                errors.append(f"{nid}: missing prerequisite {target}")
            else:
                visit(target)
        active.pop()
        visited.add(nid)
    for nid in sorted(nodes):
        visit(nid)
    return sorted(set(errors))


def admission(label: str, nodes: dict, extra: dict) -> dict:
    key = normalize(label)
    index = identities(nodes, extra)
    exact = index.get(key, [])
    candidates = []
    if not exact:
        scores = {}
        for term, ids in index.items():
            score = difflib.SequenceMatcher(None, key, term).ratio()
            if score >= .72:
                for nid in ids:
                    scores[nid] = max(scores.get(nid, 0), score)
        candidates = [{"id": nid, "score": round(score, 3)}
                      for nid, score in sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:8]]
    return {"label": label, "normalized": key, "exact": exact, "candidates": candidates,
            "decision": "resolve" if len(exact) == 1 else "disambiguate" if exact else
                        "review" if candidates else "new-candidate"}


def body(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)


_FINGERPRINT_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "in", "is", "it",
    "of", "on", "or", "that", "the", "this", "to", "with", "you", "your",
}


def content_tokens(nid: str, root: Path) -> set[str]:
    """Read a complete node locally and return durable identity-bearing terms.

    This is deliberately deterministic and local: it is a screening pass over
    every article, not an LLM assertion that two concepts are identical.
    """
    text = body((root / "nodes" / f"{nid}.md").read_text(encoding="utf-8"))
    return {token for token in re.findall(r"[a-z0-9]{3,}", text.casefold())
            if token not in _FINGERPRINT_STOPWORDS}


def identity_candidates(nodes: dict, root: Path, threshold: float = 0.2) -> list[dict]:
    """Rank possible duplicate entities from complete local node content.

    TF-IDF cosine similarity identifies review candidates. It never creates an
    alias, redirect, or merge automatically.
    """
    documents = {nid: content_tokens(nid, root) for nid in nodes}
    document_frequency: dict[str, int] = {}
    for terms in documents.values():
        for term in terms:
            document_frequency[term] = document_frequency.get(term, 0) + 1
    count = len(documents)
    weighted = {
        nid: {term: math.log((count + 1) / (document_frequency[term] + 1)) + 1 for term in terms}
        for nid, terms in documents.items()
    }
    norms = {nid: math.sqrt(sum(weight * weight for weight in weights.values())) for nid, weights in weighted.items()}
    inverted: dict[str, list[str]] = {}
    for nid, terms in documents.items():
        for term in terms:
            inverted.setdefault(term, []).append(nid)
    dot: dict[tuple[str, str], float] = {}
    for term, ids in inverted.items():
        if len(ids) > 80:  # generic terms create noise, not identity evidence.
            continue
        for offset, first in enumerate(ids):
            for second in ids[offset + 1:]:
                key = (first, second) if first < second else (second, first)
                dot[key] = dot.get(key, 0.0) + weighted[first][term] * weighted[second][term]
    candidates = []
    for (first, second), value in dot.items():
        score = value / (norms[first] * norms[second])
        if score >= threshold:
            candidates.append({"first": first, "second": second, "score": round(score, 3)})
    return sorted(candidates, key=lambda item: (-item["score"], item["first"], item["second"]))


def enrich(data: dict, nodes: dict, root: Path) -> dict:
    extra = catalog(root)
    errors = validate(nodes, extra)
    if errors:
        raise ValueError("\n".join(errors))
    data["relations"] = relations(nodes, extra)
    data["identityIndex"] = identities(nodes, extra)
    canonical = canonical_ids(nodes, extra)
    # The source graph stays complete for reference and audit. The learner graph
    # collapses resolved aliases onto their canonical concept, so an alias never
    # becomes an additional roadmap stop.
    seen_edges = set()
    canonical_edges = []
    for edge in data["edges"]:
        source, target = canonical[edge["s"]], canonical[edge["t"]]
        if source != target and (source, target) not in seen_edges:
            seen_edges.add((source, target))
            canonical_edges.append({"s": source, "t": target})
    data["edges"] = canonical_edges
    for node in data["nodes"]:
        nid = node["id"]
        record = extra.get("concepts", {}).get(nid, {})
        node["canonicalId"] = canonical_id(nid, nodes, extra)
        node["isCanonical"] = node["canonicalId"] == nid
        node["aliases"] = record.get("aliases", [])
        node["objective"] = record.get("objective", node.get("summary", ""))
        node["prerequisiteReasons"] = record.get("prerequisiteReasons", {})
        node["relations"] = [r for r in data["relations"] if r["s"] == nid and r["type"] != "REQUIRES"]
        lesson = root / "lessons" / f"{nid}.md"
        node["lesson"] = lesson.read_text() if lesson.exists() else ""
        node["lessonReviewed"] = lesson.exists()
    return data


def report(nodes: dict, root: Path) -> dict:
    extra = catalog(root)
    entries = []
    for nid, node in sorted(nodes.items()):
        text = body((brain.NODES / f"{nid}.md").read_text())
        words = len(text.split())
        prereqs = brain.parse_list(node.get("prereqs", ""))
        reasons = extra.get("concepts", {}).get(nid, {}).get("prerequisiteReasons", {})
        entries.append({"id": nid, "words": words, "needsShortLesson": not (root / "lessons" / f"{nid}.md").exists(),
                        "unreviewedPrerequisites": [p for p in prereqs if p not in reasons]})
    canonical = canonical_ids(nodes, extra)
    return {"sourceConcepts": len(nodes), "canonicalConcepts": len(set(canonical.values())),
            "resolvedEntities": sum(nid != target for nid, target in canonical.items()), "errors": validate(nodes, extra),
            "reviewedLessons": sum(not e["needsShortLesson"] for e in entries),
            "longArticles": sum(e["words"] > 500 for e in entries), "concepts": entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["audit", "report", "resolve", "candidates", "export"])
    parser.add_argument("label", nargs="?")
    parser.add_argument("--workspace", default="")
    args = parser.parse_args()
    brain.configure_workspace(args.workspace)
    nodes, extra = brain.all_nodes(), catalog(brain.ROOT)
    if args.command == "resolve":
        if not args.label:
            parser.error("resolve requires a label")
        result = admission(args.label, nodes, extra)
    elif args.command == "candidates":
        result = {"method": "local complete-node TF-IDF screening; editorial review required",
                  "candidates": identity_candidates(nodes, brain.ROOT)}
    elif args.command == "export":
        errors = validate(nodes, extra)
        if errors:
            raise SystemExit("\n".join(errors))
        result = {"concepts": [{"id": i, "canonicalId": canonical_id(i, nodes, extra), "title": n.get("title", i), "summary": n.get("summary", ""),
                                 "domain": brain.parse_list(n.get("tags", ""))[0],
                                 "aliases": extra.get("concepts", {}).get(i, {}).get("aliases", [])}
                                for i, n in sorted(nodes.items())], "relations": relations(nodes, extra)}
        result["digest"] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    else:
        result = report(nodes, brain.ROOT)
        if args.command == "audit":
            result.pop("concepts")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("errors"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
