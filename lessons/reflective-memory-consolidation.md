# Reflective Memory Consolidation

## Meaning

Reflective consolidation changes the *representation* of experience: it turns selected episodes into candidate generalizations and stores those inferences alongside their evidence. It is not a better nearest-neighbor search, model-weight training, or permission to believe everything a generated summary says. [[agent-memory]] supplies the episodes and the separate decision about what may become durable state.

## Mechanism

Choose a bounded set of recent or task-relevant memories. Generate questions those records could answer; retrieve supporting and conflicting records for each question. Propose a scoped inference, attach the identifiers of the records supporting it, and apply the application's promotion checks before storing it. The Generative Agents paper describes this question–retrieval–inference loop with evidence pointers. Its simulated social-behavior evaluation does not establish universal reliability for operational agents.

The essential difference from compacting a transcript is that consolidation creates a new claim that can be retrieved independently. A concise transcript preserves an account; a reflection infers a pattern. Marking that distinction prevents the inference from masquerading as a directly observed fact. Preserve exceptions, dates and confidence where appropriate. Similarity search cannot return an inference that was never represented, but poor retrieval can still prevent consolidation from seeing the needed evidence.

## One example

An invented assistant records three job runs: two fail when a temporary mount is absent, while one succeeds with that mount present. A defensible reflection is “these failures may depend on mount availability,” linked to all three runs. “This job always fails” discards the counterexample. The reflection can guide a diagnostic check without authorizing an automatic system change.

When a later failure occurs with the mount present, revise the hypothesis rather than appending another confident repetition. Repeated reflections supported by the same three runs do not constitute additional independent observations.

## Check your understanding

Does attaching an event identifier prove a reflection is true? No. It makes the inference inspectable; the cited event may be irrelevant, contradicted, or insufficient.
