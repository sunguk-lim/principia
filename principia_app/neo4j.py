"""Local Neo4j Community projection. No driver or cloud account required.

The database is a rebuildable, revisioned query index, never a second authoring
source. Every snapshot is immutable; the current pointer changes atomically.
Only the private Principia server connects to the loopback HTTP endpoint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import threading
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import brain
from principia_app.ontology import canonical_id, catalog, relations, validate

_projection_lock = threading.Lock()


def ensure_current(root) -> dict:
    """Refresh the derived index from the source when its content changes."""
    with _projection_lock:
        brain.configure_workspace(str(root))
        nodes = brain.all_nodes()
        extra = catalog(brain.ROOT)
        expected = snapshot(nodes, extra)["digest"]
        current = status()
        return current if current.get("digest") == expected else sync(nodes, extra)


def endpoint() -> str:
    value = os.environ.get("PRINCIPIA_NEO4J_URL", "http://127.0.0.1:17474").rstrip("/")
    parsed = urlparse(value)
    if (parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
            or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path):
        raise ValueError("Neo4j must be a loopback HTTP origin without embedded credentials")
    return value + "/db/neo4j/tx/commit"


def transaction(statements: list[dict]) -> list:
    request = Request(endpoint(), data=json.dumps({"statements": statements}).encode(),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=15) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("Neo4j rejected the transaction: " + "; ".join(e.get("code", "error") for e in result["errors"]))
    return result.get("results", [])


def query(statement: str, **parameters) -> list:
    results = transaction([{"statement": statement, "parameters": parameters}])
    return [entry["row"] for entry in results[0]["data"]] if results else []


def snapshot(nodes: dict, extra: dict) -> dict:
    errors = validate(nodes, extra)
    if errors:
        raise ValueError("\n".join(errors))
    concepts = [{"id": nid, "canonicalId": canonical_id(nid, nodes, extra),
                 "title": n.get("title", nid), "summary": n.get("summary", ""),
                 "domain": brain.parse_list(n.get("tags", ""))[0],
                 "aliases": extra.get("concepts", {}).get(nid, {}).get("aliases", []),
                 "sources": brain.parse_list(n.get("sources", ""))}
                for nid, n in sorted(nodes.items())]
    result = {"concepts": concepts, "relations": relations(nodes, extra)}
    result["digest"] = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
    return result


def sync(nodes: dict, extra: dict) -> dict:
    data = snapshot(nodes, extra)
    digest = data["digest"]
    query("CREATE CONSTRAINT principia_concept_key IF NOT EXISTS FOR (n:PrincipiaConcept) REQUIRE n.key IS UNIQUE")
    query("CREATE CONSTRAINT principia_projection_key IF NOT EXISTS FOR (n:PrincipiaProjection) REQUIRE n.id IS UNIQUE")
    statements = [{"statement": """UNWIND $concepts AS c
        MERGE (n:PrincipiaConcept {key: $digest + ':' + c.id})
        SET n.id=c.id, n.title=c.title, n.summary=c.summary, n.domain=c.domain,
            n.aliases=c.aliases, n.sources=c.sources, n.canonicalId=c.canonicalId, n.snapshot=$digest""",
        "parameters": {"concepts": data["concepts"], "digest": digest}}]
    statements.append({"statement": """UNWIND $concepts AS c
        WITH c WHERE c.id <> c.canonicalId
        MATCH (alias:PrincipiaConcept {key: $digest + ':' + c.id})
        MATCH (canonical:PrincipiaConcept {key: $digest + ':' + c.canonicalId})
        MERGE (alias)-[:RESOLVES_TO]->(canonical)""",
        "parameters": {"concepts": data["concepts"], "digest": digest}})
    for kind in ["REQUIRES", "ALTERNATIVE_TO", "CONTRASTS_WITH", "APPLIES_TO", "USES"]:
        statements.append({"statement": f"""UNWIND $edges AS e
            MATCH (s:PrincipiaConcept {{key: $digest + ':' + e.s}})
            MATCH (t:PrincipiaConcept {{key: $digest + ':' + e.t}})
            MERGE (s)-[r:{kind}]->(t) SET r.reason=e.reason, r.reviewed=e.reviewed""",
            "parameters": {"digest": digest, "edges": [r for r in data["relations"] if r["type"] == kind]}})
    statements.append({"statement": """MERGE (p:PrincipiaProjection {id:'current'})
        SET p.digest=$digest, p.concepts=$count, p.relations=$relations""",
        "parameters": {"digest": digest, "count": len(nodes), "relations": len(data["relations"])}})
    transaction(statements)
    return status()


def status() -> dict:
    rows = query("MATCH (p:PrincipiaProjection {id:'current'}) RETURN p.digest, p.concepts, p.relations")
    return {"available": bool(rows), "digest": rows[0][0], "concepts": rows[0][1], "relations": rows[0][2]} if rows else {"available": False}


def prerequisite_ids(target: str) -> list[str]:
    # Traverses only required learning, never comparison/application relationships.
    rows = query("""MATCH (p:PrincipiaProjection {id:'current'}),
        (requested:PrincipiaConcept {id:$target}) WHERE requested.snapshot=p.digest
        MATCH (n:PrincipiaConcept {id:requested.canonicalId, snapshot:p.digest})
        MATCH (n)-[:REQUIRES*0..]->(dependency:PrincipiaConcept)
        RETURN DISTINCT dependency.id ORDER BY dependency.id""", target=target)
    return [row[0] for row in rows]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["sync", "status", "prerequisites"])
    parser.add_argument("target", nargs="?")
    parser.add_argument("--workspace", default="")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            brain.configure_workspace(args.workspace)
            result = sync(brain.all_nodes(), catalog(brain.ROOT))
        elif args.command == "prerequisites":
            if not args.target:
                parser.error("prerequisites requires a concept ID")
            result = prerequisite_ids(args.target)
        else:
            result = status()
        print(json.dumps(result, indent=2))
    except (HTTPError, URLError, RuntimeError, ValueError) as error:
        raise SystemExit(f"Neo4j unavailable or projection invalid: {type(error).__name__}") from error


if __name__ == "__main__":
    main()
