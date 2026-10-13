# Schema-Guided Agent Memory

## Meaning

Schema-guided agent memory constrains entity and relation extraction to a domain ontology while retaining provenance and temporal corrections.

## Mechanism

A [[graph-memory]] pipeline must decide which entities and relations deserve durable storage. **Schema-guided agent memory** declares allowed types, fields, and relation endpoints before extraction so a model cannot invent arbitrary labels that the application cannot query consistently. [[structured-output]] can enforce shape, but a well-typed graph can still contain false or missing facts.

## One example

An incident memory allows Service, Alert, and Team nodes but rejects an untyped relation, keeping evidence for later schema review.

## Check your understanding

**Question:** Does a valid schema prove the extracted fact is true? **Answer:** No; evidence, temporal correction, and retrieval evaluation are still required.
