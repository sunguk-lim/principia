# Attention Head Pruning

## Meaning

Attention head pruning removes selected head contributions from a trained layer. It asks which contributions are dispensable for a specified model and workload, not whether multiple heads are useless in general.

## Mechanism

A temporary mask can zero one head's contribution and reveal the effect on validation behavior. Candidate importance can guide a removal order, but the remaining model must be re-evaluated as removals accumulate. Heads can substitute for each other, so isolated ablations do not predict their combined effect.

A zero mask also does not guarantee less computation. If the runtime still executes every projection and attention operation, the model may run just as slowly. A structural implementation must remove real work while preserving compatible tensor shapes, and smaller shapes may use hardware less efficiently.

## One example

A four-head model scores 90%. Removing H1 alone gives 89.8%; removing H2 alone gives 89.9%. Removing both gives 84%. Each was individually dispensable because the other could compensate. A sensible iterative procedure removes one, then recomputes the evidence for removing the next.

If all masked variants still take 10 milliseconds, the ablation established only a quality observation. It did not establish faster execution. Final reporting needs a separate physically pruned implementation and measured latency, throughput and memory.

## Check your understanding

Does successful pruning prove a model trained from scratch with fewer heads would reach the same quality? **No.** Training dynamics and post-training redundancy are different questions. Validate on independent task slices and lengths, account for adaptation cost, and avoid promoting one paper's pruning percentage into a universal architecture rule.
