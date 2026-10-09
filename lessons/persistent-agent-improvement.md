# Persistent Agent Improvement

## Meaning

A future run improves only if a change from earlier experience survives, is used, and helps on independent tasks. Reflection inside a discarded conversation is not enough.

## Mechanism

Inspect traces and propose a specific system or model update: a new tool rule, a stored skill, a retrieval fix, or a trained checkpoint. Version the change and connect it to the execution path. Replay known failures as a smoke test, then evaluate on untouched tasks. An executable environment lets the agent try alternative actions and observe outcomes; a saved transcript only records what happened once. Keep promotion criteria independent from the task curriculum.

## One example

An agent repeatedly misuses an edit tool. A new skill describes valid patch syntax. If later runs never retrieve that skill, nothing changed. If they do, test valid edits and completed tasks on repositories excluded from skill development.

## Check your understanding

**Question:** Why is success on replayed failures insufficient? **Answer:** The update may overfit those cases and regress on new tasks.
