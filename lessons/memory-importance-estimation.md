# Write-Time Memory Importance Estimation

## Meaning

Importance estimation assigns a stored memory a salience score before the future retrieval query is known. It asks which experiences may deserve attention beyond their similarity to one immediate question. [[agent-memory]] defines the retained records; importance is additional metadata, not a truth label or a permission to retain the record.

## Mechanism

At ingestion, apply a declared rubric to the record, store its score, and retain the scoring policy or model version. The Generative Agents paper asks a language model for an integer from mundane to highly poignant at memory creation. That particular social-simulation rubric need not suit a support or engineering assistant. Operational importance may instead reflect a rare critical failure, explicit user priority, or impact under a defined task contract.

A write-time score amortizes scoring across repeated reads. It is query-independent, so it cannot perfectly anticipate future usefulness. A routine record can become decisive under a later question, and a dramatic event can remain irrelevant. Preserve query relevance and authorization as separate filters. Allow correction when the rubric changes; comparing old and new scores without version awareness can distort ranking.

## One example

An invented store receives a routine successful backup and an unusual failed restore test. A policy assigns salience 2 and 8. One hundred later searches can reuse those stored judgments rather than call a model two hundred times. If a later question asks for the last successful backup time, the routine entry can still be the right answer. High salience should not force the restore failure into every result.

Suppose a revised rubric recognizes that the backup held a uniquely required recovery point. Re-score affected records or preserve policy-specific scores; silently treating the original 2 as timeless would miss the change.

## Check your understanding

Does an importance score of 8 mean a memory is four times as valuable as one scored 2? Not without a validated ratio-scale interpretation.
