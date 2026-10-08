# Success-Filtered Self-Training

## Meaning

A model samples attempts, keeps those passing a verifier, and learns to imitate them. This is a useful starting point when it already solves some tasks; it is not a promise that every failure will teach it something.

## Mechanism

A success filter selects an offline dataset. Repeated fitting raises the probability of recorded successes, but easy tasks can dominate and reused samples can become stale. Compare this loop with fresh on-policy learning using the same rollout and compute budget. Track coverage by task difficulty, pass@1 and pass@k, diversity, and verifier gaming.

## One example

A coding agent passes 80% of easy tasks and 5% of hard ones. If it contributes every passing sample, the next training set mostly contains easy-task solutions. Sampling equally many attempts per task and monitoring accepted coverage diagnoses that bias.

## Check your understanding

**Question:** Why can the same training loss coexist with worse pass@k? **Answer:** Successful outputs may collapse to a few similar solutions; the chance that one of several diverse attempts succeeds can fall.
