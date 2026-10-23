# Reviewed Knowledge Promotion

## Meaning

A human support reply can solve one customer's problem without being safe or general enough for every future user. Reviewed knowledge promotion separates that resolved interaction from a reusable knowledge record. The record becomes new evidence for [[retrieval-augmented-generation]], not an automatic parameter update or proof of universal correctness.

## Mechanism

Capture a candidate with its question, proposed resolution, applicability conditions, evidence, and owner. Use [[dataset-lineage]] to preserve which interaction and source versions justify it. Review correctness, sensitive details, tenant scope, effective dates, and conflicts with existing instructions. Merge a supported improvement into an existing record when appropriate; otherwise publish a separately scoped version. Keep a path to correction, expiration, or retraction.

The KCS primary materials describe integrating knowledge use, validation, improvement, and creation into operational work. The validation gates here apply that broad lifecycle to retrieval evidence; they are not a claim that one particular KCS implementation or support platform supplies these controls automatically.

Promotion must preserve a [[retrieval-authorization-boundary]]. A reply may contain a customer-specific identifier, contract exception, or internal diagnostic. Removing a name does not necessarily make the resolution public. The stored text, index metadata, cached results, and source link must retain the intended audience. A “human wrote it” flag is provenance, not blanket permission or truth.

## One example

An operator resolves a customer's upload failure by increasing a private quota from 5 to 8 units. Copying the reply into a global index would teach future customers that everyone has quota 8. A reviewed record instead says that the symptom may indicate quota exhaustion, cites the current policy, explains how an authorized operator checks the applicable quota, and excludes the customer's identifier and exceptional limit. If the policy later changes, lineage identifies the record for re-review.

A candidate can move through draft, reviewed, published, and retired states. Search should not expose a draft merely because it has an embedding. Retraction must remove or invalidate the indexed record and relevant caches, not just hide its source page. Log who approved a version and which evidence was checked while minimizing personal data in that log.

Use [[measurement]] on a held-out set to compare answer support, incorrect reuse, tenant leakage, conflicting retrieval, and correction latency before and after promotion. Keep evaluation examples separate from automatically ingested replies to avoid scoring the system on its own recycled output. More retrieved records or fewer escalations alone do not demonstrate improved support quality.

## Check your understanding

Why not index every successful reply immediately? Success on one interaction does not establish general applicability, permission for reuse, or correctness under later policy versions.

