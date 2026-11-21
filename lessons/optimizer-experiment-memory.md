# Optimizer Experiment Memory

## Meaning

An optimizer's memory is a record of experiments about a system, not the task-solving agent's user memory. Retaining only the winning prompt or harness loses why an edit was proposed, what it was expected to repair and which failures survived. This design preserves those distinctions without assuming the recorded diagnosis is correct.

## Mechanism

For each versioned failure class, retain the candidate artifact or exact diff, parent version, proposed mechanism, predicted affected cases recorded before testing, evaluation setup, model/tool versions and observed per-case results. Keep failed and rejected attempts as well as winners. Link evidence to the exact artifact; a paraphrased rule or a changed benchmark can be a different experiment. Separate optimizer-accessible tuning results from independent promotion evidence under [[persistent-agent-improvement]].

[[score-history-prompt-optimization]] preserves candidate-score pairs. Diagnostic memory adds failure traces and falsifiable expectations: “adding a missing-field branch should repair null inputs without changing valid-field cases.” GEPA provides a primary example of reflection over trajectories and evaluated mutations; the memory schema here is an independent design rather than a claim to reproduce any named product or study.

### Prospective predictions and model transitions

Record predictions before observing results so a successful-looking story cannot silently replace the original hypothesis. Compare predicted and actual case sets, including regressions and no-change cases. A prediction makes disagreement detectable; it does not turn an uncontrolled test into causal proof. After a model swap, use [[factorial-agent-evaluation]] or held-fixed comparisons to re-evaluate inherited rules. Retain their historical scope instead of treating an old positive score as current authority.

## One example

An invented candidate B changes completion checks in harness A. Before testing, its record predicts repairs on tasks 2 and 5 and no change on task 8. Evaluation repairs 2, leaves 5 broken and regresses 8. Store all three results and the exact diff. Keeping only “task 2 fixed” would mislead the next optimizer; keeping only B's code could conceal the reason for the check entirely.

## Boundaries and check your understanding

Bound memory retrieval, preserve provenance and exclude credentials or unnecessary private traces. Stale explanations can anchor later search, and repeatedly optimizing against remembered cases can overfit them. Compare rationale-plus-outcomes memory with score-only and no-memory baselines under equal evaluation budgets, then test untouched tasks. Track repeated failed experiments, accepted changes, regressions and transfer to another model separately.

**Check:** Does a stored rationale establish why a candidate improved? No. It records a hypothesis; controlled comparisons and independent acceptance remain necessary.
