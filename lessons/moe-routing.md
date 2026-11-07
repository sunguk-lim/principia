# MoE Routing

## Meaning

MoE routing chooses which expert transformations contribute to a token, their output weights and capacity handling. Learned token-choice top-k is common, not universal. Alternative assignment mechanisms and dropless execution exist.

## Mechanism

A common gate produces scores and normalized preferences, selects k experts and combines their outputs. Selected-weight renormalization is model-specific: selection scores may also contain balancing biases absent from the final mixing weights. Fixed k bounds selected expert evaluations, not all memory, routing or communication cost.

Count assignments, not just tokens. With T tokens each selecting k experts from E possibilities, average load is T*k/E. One illustrative cap is that average multiplied by a capacity factor and rounded upward. Real implementations can define the factor differently. A balancing objective encourages traffic distribution during training; it cannot guarantee every serving batch is balanced.

## One example

Six tokens each select two experts among four, producing twelve assignments and an average of three per expert. Requested counts [5,3,2,2] overflow a cap of three by two assignments at the first expert. Dropping removes those branch contributions; rerouting changes destinations; a dropless execution allocates or schedules the uneven work. Losing one branch does not necessarily delete a token or erase another expert's contribution and residual path.

For output weights [.50,.30,.20], top-two with renormalization uses [.625,.375], while masked-only mixing retains [.50,.30]. These yield different results; use the checkpoint's actual contract.

## Check your understanding

Are capacity limits only an inference technique, and is dropping always a small quality cost? No. Limits can be used in training or serving; some models deliberately avoid dropping. Validate per-expert load, per-token coverage, overflow, task quality and complete dispatch/compute/combine latency. Changing routing after training can change the model, so balanced counts or sparse arithmetic alone do not establish a deployment improvement.
