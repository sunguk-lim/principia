---
id: schema-guided-agent-memory
title: Schema-Guided Agent Memory
summary: Schema-guided agent memory constrains entity and relation extraction to a domain ontology while retaining provenance and temporal corrections.
type: concept
tags: [ml/agents]
prereqs: [graph-memory, temporal-knowledge-graph, structured-output]
sources: [https://github.com/getzep/graphiti]
status: explained
created: 2026-10-14
updated: 2026-10-14
---

# Schema-Guided Agent Memory

## Summary

Schema-guided agent memory constrains entity and relation extraction to a domain ontology while retaining provenance and temporal corrections.

## Grounded explanation

A [[graph-memory]] pipeline must decide which entities and relations deserve durable storage. **Schema-guided agent memory** declares allowed types, fields, and relation endpoints before extraction so a model cannot invent arbitrary labels that the application cannot query consistently. [[structured-output]] can enforce shape, but a well-typed graph can still contain false or missing facts.

For an incident system, a schema may admit Service, Deployment, Alert, and Team entities and relations such as Deployment affects Service. Extraction can then reject an unsupported relation or route it for review. A [[temporal-knowledge-graph]] handles corrections: an old owner relation can close at a known time while provenance remains available for historical questions. Keep raw evidence separate from derived facts and version the extraction schema so old records can be reprocessed.

A narrow schema improves query precision only if it does not exclude important facts. Start with a small ontology, then measure extraction precision and recall, relation validity, temporal update accuracy, retrieval usefulness, and missed-domain cases against unconstrained and simpler text-retrieval baselines. Product claims about a particular library's performance do not follow from the schema design.

## Prerequisites

- [[graph-memory]]
- [[temporal-knowledge-graph]]
- [[structured-output]]

## Sources

- [https://github.com/getzep/graphiti](https://github.com/getzep/graphiti)
