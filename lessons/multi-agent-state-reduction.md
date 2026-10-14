# Multi-agent state reduction

Parallel workers can each return useful findings, but they may write the same shared state key. A reducer is the rule that combines those updates. Without one, a fast or late worker might overwrite another, and a replay could produce a different result.

Give workers private scratch state and require bounded, validated outputs. For a shared map keyed by finding ID, union entries and reject conflicting values for the same ID. For a list, append may preserve every item but not a stable order; sort by an explicit key before presenting it. The merge should also retain worker provenance and record partial failures.

Three algebraic questions help. Is the merge associative, so regrouping updates changes nothing? Is it commutative, so arrival order changes nothing? Is it idempotent, so replaying the same update has no extra effect? A system may not need all three for every field, but it should know when it lacks them. “Last writer wins” is a policy, not a neutral default.

Suppose worker A returns finding `f1` and worker B returns `f2`. A map union yields both regardless of order. If both return different values for `f1`, the reducer should surface a conflict for review instead of silently choosing whichever arrived last. Tests should permute order, repeat delivery, inject conflicts, and make one worker fail. Compare the result and cost with a sequential baseline.

**Check:** Why can plain list concatenation preserve content yet still fail deterministic replay?
