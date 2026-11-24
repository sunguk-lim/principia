# Agent Trajectory Fine-Tuning

## Meaning

Trajectory fine-tuning teaches an agent what to propose next from curated examples of interaction. Each example contains the task and information available at a decision point, paired with an approved next action. It differs from retaining a transcript for debugging: a recorded action becomes a training target only after its intent, correctness and authority have been assessed.

## Mechanism

Start with [[fine-tuning]] and prefix-conditioned targets from [[causal-language-model-training]]. Preserve tool definitions, message order, call identifiers and the observations available so far. A loss mask can select assistant action tokens while tool results remain conditioning context. That mask does not itself prevent future information from appearing in the input.

Apply [[temporal-data-leakage]] at each decision boundary: later tool results cannot justify an earlier action. Split related tasks and templates together before evaluating. The [[tool-call-execution-contract]] remains external to learning; a plausible model proposal still needs argument validation and authorization before execution.

Training on successful episodes alone may omit hard tasks and recovery states. Conversely, copying every failed action can teach the failure. Use corrected, adjudicated targets and evaluate the resulting agent in closed-loop interaction, where its own earlier choices affect later observations.

## One example

A scheduling episode first queries availability, learns that A is occupied and B is free, then proposes B. The early prefix should target the query. Only the later prefix may use the availability result to target B. Giving both examples the future result would teach the wrong task.

If a reservation times out with an unknown outcome, an approved recovery checks status before another write. Eventual episode success does not make a blind repeated reservation a valid demonstration.

## Check your understanding

Does low next-action loss prove reliable task completion? No. The model can imitate familiar actions yet fail under its own errors, changed schemas or unfamiliar tasks. Compare verified completion, unauthorized effects, recovery and total cost on held-out episodes.
