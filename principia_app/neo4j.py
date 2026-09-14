"""Rebuildable Principia projection: portable entities and closed edges.

Markdown is build input only.  The private application reads its cards,
content units, and goal roadmaps from Neo4j at request time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import brain
from principia_app.ontology import canonical_id, catalog, relations, validate

_lock = threading.Lock()
EDGE_KINDS = ("REQUIRES", "ALTERNATIVE_TO", "CONTRASTS_WITH")
# A portable explanation is a target for editorial review, not a token at which
# the indexer is allowed to cut prose.  The builder must preserve semantic
# boundaries even while reporting an overlong authored unit.
MAX_NODE_WORDS = 280


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _words(value: str) -> int:
    return len(re.findall(r"\S+", value))


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5:].strip()
    return text.strip()


def _entity_signature(title: str, kind: str, domain: str) -> str:
    """Return the source-file-independent identity fingerprint for an entity."""
    return _hash("\x1f".join(("principia-entity-v2", title.strip().casefold(), kind, domain.casefold())))


def _unit(entity_id: str, source_id: str, source_hash: str, ordinal: int, heading: str, content: str) -> dict:
    content_hash = _hash(content)
    return {
        "contentId": "cnt-" + _hash(f"{entity_id}:{source_id}:{ordinal}:{content_hash}")[:20],
        "entityId": entity_id, "sourceId": source_id, "sourcePath": f"nodes/{source_id}.md",
        "sourceHash": source_hash, "contentHash": content_hash, "ordinal": ordinal,
        "heading": heading, "content": content, "wordCount": _words(content),
    }


_NON_EXPLANATION_HEADINGS = {
    "prerequisites", "prerequisite", "sources", "source", "references",
    "visuals", "visual", "further reading", "전제 조건", "선행 개념", "출처",
    "시각 자료",
}
_EXPLANATION_HEADINGS = {
    "summary", "grounded explanation", "explanation", "details", "detail",
    "요약", "상세 설명",
}


def _heading_name(block: str) -> tuple[int, str] | None:
    match = re.fullmatch(r"(#{1,3})\s+(.+?)\s*", block)
    return (len(match.group(1)), match.group(2).strip()) if match else None


def _inline_semantic_label(block: str) -> tuple[str, str] | None:
    """Recognize an author-declared semantic move, never arbitrary emphasis.

    Existing explanations commonly use numbered mechanisms and explicit worked
    examples/consequences inside a single Markdown section.  Those labels are
    authored conceptual boundaries.  A sentence boundary or a word count is
    deliberately not one.
    """
    match = re.match(r"^\*\*((?:\d+\s*[—–:-]\s*[^*]+|Worked (?:example|instance)\.?|Why it matters\.?|Key idea\.?|Mechanism\.?|Consequence\.?|Example\.?))\*\*(?:\s+(.*))?$", block, re.S | re.I)
    if not match:
        return None
    label, remainder = match.group(1).strip().rstrip("."), (match.group(2) or "").strip()
    return label, remainder


def semantic_sections(entity_id: str, source_id: str, body: str) -> list[dict]:
    """Project authored semantic units without length- or sentence-based cuts.

    `###` headings and an explicit, limited set of in-body mechanism labels
    form boundaries.  Metadata sections such as sources and prerequisites are
    omitted.  If an authored unit exceeds ``MAX_NODE_WORDS`` it is retained as
    one unit and marked unreviewed by the caller; shortening it requires an
    editorial rewrite, not automatic fragmentation.
    """
    source_hash = _hash(body)
    sections: list[tuple[str, list[str]]] = []
    heading, blocks, skipping = "Overview", [], False

    def flush() -> None:
        nonlocal blocks
        if blocks:
            sections.append((heading, blocks))
        blocks = []

    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block:
            continue
        header = _heading_name(block)
        if header:
            level, text = header
            normalized = text.casefold()
            if level == 1:
                continue
            flush()
            if normalized in _NON_EXPLANATION_HEADINGS:
                skipping = True
            else:
                skipping = False
                # Structural h2s retain the current overview; authored h3s
                # and non-structural h2s name a new learnable idea.
                if normalized not in _EXPLANATION_HEADINGS:
                    heading = text
            continue
        if skipping:
            continue
        label = _inline_semantic_label(block)
        if label:
            flush()
            heading, remainder = label
            if remainder:
                blocks.append(remainder)
        else:
            blocks.append(block)
    flush()
    if not sections:
        sections = [("Overview", ["No indexed explanation is available yet."])]

    return [
        _unit(entity_id, source_id, source_hash, ordinal, title, "\n\n".join(source_blocks))
        for ordinal, (title, source_blocks) in enumerate(sections, start=1)
    ]


def endpoint() -> str:
    value = os.environ.get("PRINCIPIA_NEO4J_URL", "http://127.0.0.1:17474").rstrip("/")
    parsed = urlparse(value)
    if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path):
        raise ValueError("Neo4j must be a loopback HTTP origin without embedded credentials")
    return value + "/db/neo4j/tx/commit"


def transaction(statements: list[dict]) -> list:
    request = Request(endpoint(), data=json.dumps({"statements": statements}).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("Neo4j rejected transaction: " + "; ".join(item.get("code", "error") for item in result["errors"]))
    return result.get("results", [])


def query(statement: str, **parameters) -> list:
    results = transaction([{ "statement": statement, "parameters": parameters }])
    return [item["row"] for item in results[0]["data"]] if results else []


def snapshot(nodes: dict, extra: dict) -> dict:
    errors = validate(nodes, extra)
    if errors:
        raise ValueError("\n".join(errors))
    canonical_by_source = {sid: canonical_id(sid, nodes, extra) for sid in nodes}
    entities, entities_for_source = [], {}
    for source_id in sorted(set(canonical_by_source.values())):
        node = nodes[source_id]
        kind = node.get("type", "concept")
        domain = brain.parse_list(node.get("tags", ""))[0]
        source_ids = sorted(sid for sid, canonical in canonical_by_source.items() if canonical == source_id)
        source_titles = [nodes[sid].get("title", sid) for sid in source_ids]
        canonical_title = node.get("title", source_id)
        aliases = list(extra.get("concepts", {}).get(source_id, {}).get("aliases", []))
        aliases.extend(title for title in source_titles if title.casefold() != canonical_title.casefold())
        aliases = list(dict.fromkeys(alias.strip() for alias in aliases if alias.strip()))
        sections = semantic_sections(source_id, source_id, _body(brain.NODES / f"{source_id}.md"))
        node_ids = []
        for position, section in enumerate(sections, start=1):
            suffix = "" if len(sections) == 1 else f" — {section['heading']} ({position}/{len(sections)})"
            title = canonical_title + suffix
            # Identity follows the learnable objective, not its current prose.
            # A concise editorial rewrite therefore updates this same entity;
            # ``contentHash`` below remains the distinct-content trace.
            semantic_name = f"{canonical_title} — {section['heading']}"
            signature = _entity_signature(semantic_name, kind, domain)
            entity_id = "ent-" + signature[:20]
            node_ids.append(entity_id)
            entities.append({"entityId": entity_id, "signature": signature, "canonicalName": title,
                             "canonicalSourceId": source_id, "sourceIds": source_ids, "sourceTitles": source_titles,
                             "sourceId": source_id, "sourcePath": f"nodes/{source_id}.md", "sourceHash": section["sourceHash"],
                             "contentHash": section["contentHash"], "explanation": section["content"], "wordCount": section["wordCount"],
                             "ordinal": position, "segmentCount": len(sections), "type": kind, "domain": domain,
                             "summary": node.get("summary", "") if position == 1 else section["heading"],
                             "objective": section["heading"], "aliases": aliases if position == 1 else [], "statusId": source_id,
                             "portable": section["wordCount"] <= MAX_NODE_WORDS, "reviewed": False})
        entities_for_source[source_id] = node_ids
    for source_id, canonical_source in canonical_by_source.items():
        entities_for_source[source_id] = entities_for_source[canonical_source]
    edge_rows, seen = [], set()
    # A split concept is a sequence of actual ontology nodes.  Each later node
    # requires the previous one; provenance remains node properties, not edges.
    for source_id in sorted(set(canonical_by_source.values())):
        chain = entities_for_source[source_id]
        for position in range(1, len(chain)):
            edge_rows.append({"sEntity": chain[position], "tEntity": chain[position - 1], "type": "REQUIRES",
                              "reason": "Semantic explanation sequence", "reviewed": False})
    for edge in relations(nodes, extra):
        source_chain, target_chain = entities_for_source[edge["s"]], entities_for_source[edge["t"]]
        item = {**edge, "sEntity": source_chain[0] if edge["type"] == "REQUIRES" else source_chain[-1],
                "tEntity": target_chain[-1]}
        key = (item["sEntity"], item["tEntity"], item["type"])
        if item["sEntity"] != item["tEntity"] and key not in seen:
            seen.add(key); edge_rows.append(item)
    result = {"entities": entities, "portableNodes": len(entities), "relations": edge_rows}
    result["digest"] = _hash(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return result


def semantic_audit(nodes: dict, extra: dict) -> dict:
    """Report editorial work remaining before a portable-node import.

    This is intentionally an audit, not a fallback that changes boundaries.
    Every listed unit is one authored semantic boundary that needs a concise
    rewrite or an explicit further semantic decomposition.
    """
    errors = validate(nodes, extra)
    if errors:
        raise ValueError("\n".join(errors))
    canonical_by_source = {sid: canonical_id(sid, nodes, extra) for sid in nodes}
    rows = []
    for source_id in sorted(set(canonical_by_source.values())):
        for section in semantic_sections(source_id, source_id, _body(brain.NODES / f"{source_id}.md")):
            rows.append({"sourceId": source_id, "objective": section["heading"],
                         "wordCount": section["wordCount"],
                         "portable": section["wordCount"] <= MAX_NODE_WORDS})
    overlong = [row for row in rows if not row["portable"]]
    return {"canonicalSources": len(set(canonical_by_source.values())),
            "semanticNodes": len(rows), "portableNodes": len(rows) - len(overlong),
            "overlongNodes": len(overlong), "maxWords": max((row["wordCount"] for row in rows), default=0),
            "needsEditorialRewrite": sorted(overlong, key=lambda row: (-row["wordCount"], row["sourceId"], row["objective"]))}


def status() -> dict:
    rows = query("MATCH (p:PrincipiaProjection {id:'current'}) RETURN p.digest, p.entities, p.portableNodes, p.relations")
    return ({"available": True, "digest": rows[0][0], "entities": rows[0][1], "portableNodes": rows[0][2], "relations": rows[0][3]}
            if rows else {"available": False})


def sync(nodes: dict, extra: dict) -> dict:
    audit = semantic_audit(nodes, extra)
    if audit["overlongNodes"]:
        raise ValueError(
            f"Semantic projection blocked: {audit['overlongNodes']} authored units exceed "
            f"{MAX_NODE_WORDS} words; rewrite or explicitly decompose them before sync."
        )
    data = snapshot(nodes, extra)
    digest = data["digest"]
    query("CREATE CONSTRAINT principia_entity_id IF NOT EXISTS FOR (n:PrincipiaEntity) REQUIRE n.entityId IS UNIQUE")
    query("CREATE CONSTRAINT principia_projection_id IF NOT EXISTS FOR (n:PrincipiaProjection) REQUIRE n.id IS UNIQUE")
    transaction([{ "statement": "MATCH (n) WHERE n:PrincipiaConcept OR n:PrincipiaEntity OR n:PrincipiaContentUnit OR n:PrincipiaProjection DETACH DELETE n" }])
    statements = [
        {"statement": "UNWIND $items AS item CREATE (n:PrincipiaEntity {entityId:item.entityId}) SET n += item, n.snapshot=$digest", "parameters": {"items": data["entities"], "digest": digest}},
    ]
    for kind in EDGE_KINDS:
        statements.append({"statement": f"UNWIND $items AS item MATCH (s:PrincipiaEntity {{entityId:item.sEntity}}), (t:PrincipiaEntity {{entityId:item.tEntity}}) CREATE (s)-[r:{kind}]->(t) SET r.reason=item.reason, r.reviewed=item.reviewed, r.snapshot=$digest", "parameters": {"items": [edge for edge in data["relations"] if edge["type"] == kind], "digest": digest}})
    statements.append({"statement": "CREATE (p:PrincipiaProjection {id:'current',digest:$digest,entities:$entities,portableNodes:$portableNodes,relations:$relations})", "parameters": {"digest": digest, "entities": len(data["entities"]), "portableNodes": data["portableNodes"], "relations": len(data["relations"])}})
    transaction(statements)
    return status()


def ensure_current(root: Path) -> dict:
    with _lock:
        brain.configure_workspace(str(root)); nodes, extra = brain.all_nodes(), catalog(brain.ROOT)
        wanted = snapshot(nodes, extra)["digest"]
        return status() if status().get("digest") == wanted else sync(nodes, extra)


def reader_graph() -> dict:
    entities = query("MATCH (p:PrincipiaProjection {id:'current'}), (e:PrincipiaEntity {snapshot:p.digest}) RETURN e.entityId,e.canonicalName,e.summary,e.type,e.domain,e.aliases,e.canonicalSourceId ORDER BY e.canonicalName")
    required = query("MATCH (p:PrincipiaProjection {id:'current'}), (s:PrincipiaEntity {snapshot:p.digest})-[:REQUIRES {snapshot:p.digest}]->(t:PrincipiaEntity {snapshot:p.digest}) RETURN s.entityId,t.entityId")
    optional = query("MATCH (p:PrincipiaProjection {id:'current'}), (s:PrincipiaEntity {snapshot:p.digest})-[r:ALTERNATIVE_TO|CONTRASTS_WITH {snapshot:p.digest}]->(t:PrincipiaEntity {snapshot:p.digest}) RETURN s.entityId,t.entityId,type(r),r.reason")
    prerequisites = {row[0]: [] for row in entities}; contextual = {row[0]: [] for row in entities}
    for source, target in required: prerequisites[source].append(target)
    for source, target, kind, reason in optional: contextual[source].append({"t": target, "type": kind, "reason": reason or ""})
    nodes = [{"id": row[0], "title": row[1], "summary": row[2], "type": row[3], "root": row[4].split("/")[0], "tags": [row[4]], "aliases": row[5] or [], "statusId": row[6], "prereqs": prerequisites[row[0]], "relations": contextual[row[0]], "isCanonical": True, "level": 0, "body": ""} for row in entities]
    return {"schemaVersion": 2, "nodes": nodes, "edges": [{"s": source, "t": target} for source, target in required]}


def entity_content(entity_id: str) -> dict | None:
    entity = query("MATCH (p:PrincipiaProjection {id:'current'}), (e:PrincipiaEntity {entityId:$id,snapshot:p.digest}) RETURN e.entityId,e.canonicalName,e.signature,e.sourceId,e.sourcePath,e.sourceHash,e.contentHash,e.explanation,e.wordCount,e.ordinal,e.segmentCount,e.reviewed", id=entity_id)
    if not entity: return None
    row = entity[0]
    return {"entityId": row[0], "canonicalName": row[1], "signature": row[2], "sourceId": row[3], "sourcePath": row[4], "sourceHash": row[5], "contentHash": row[6], "explanation": row[7], "wordCount": row[8], "ordinal": row[9], "segmentCount": row[10], "reviewed": row[11]}


def learning_subgraph(reference: str) -> dict | None:
    """Retrieve a goal path by opaque entity ID or a legacy source ID.

    The latter keeps the source-oriented API usable while the phone reader uses
    stable semantic entity IDs. A source goal begins at its first semantic unit.
    """
    resolved = query("MATCH (p:PrincipiaProjection {id:'current'}), (e:PrincipiaEntity {snapshot:p.digest}) WHERE e.entityId=$reference OR (e.canonicalSourceId=$reference AND e.ordinal=1) RETURN e.entityId ORDER BY e.entityId LIMIT 1", reference=reference)
    if not resolved: return None
    entity_id = resolved[0][0]
    ids = [row[0] for row in query("MATCH (p:PrincipiaProjection {id:'current'}), (t:PrincipiaEntity {entityId:$id,snapshot:p.digest})-[:REQUIRES*0..]->(n:PrincipiaEntity {snapshot:p.digest}) RETURN DISTINCT n.entityId ORDER BY n.entityId", id=entity_id)]
    edges = query("MATCH (p:PrincipiaProjection {id:'current'}), (s:PrincipiaEntity {snapshot:p.digest})-[r:REQUIRES {snapshot:p.digest}]->(t:PrincipiaEntity {snapshot:p.digest}) WHERE s.entityId IN $ids AND t.entityId IN $ids RETURN s.entityId,t.entityId,r.reason ORDER BY s.entityId,t.entityId", ids=ids)
    return {"target": reference, "requiredIds": ids, "requiredEdges": [{"source": row[0], "target": row[1], "reason": row[2] or ""} for row in edges]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("command", choices=["sync", "status", "graph", "semantic-audit"]); parser.add_argument("--workspace", default="")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            brain.configure_workspace(args.workspace); result = sync(brain.all_nodes(), catalog(brain.ROOT))
        elif args.command == "semantic-audit":
            brain.configure_workspace(args.workspace); result = semantic_audit(brain.all_nodes(), catalog(brain.ROOT))
        elif args.command == "graph": result = reader_graph()
        else: result = status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except ValueError as error:
        raise SystemExit(str(error)) from error
    except (HTTPError, URLError, RuntimeError) as error:
        raise SystemExit(f"Neo4j unavailable or projection invalid: {type(error).__name__}") from error


if __name__ == "__main__": main()
