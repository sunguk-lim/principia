# Knowledge Distillation

## Meaning

Distillation trains a student using selected teacher behavior as supervision. The teacher may provide a distribution over alternatives or a generated answer. A smaller serving model is a common goal, not a defining requirement: student architecture and initialization are independent choices.

## Mechanism

A teacher distribution can distinguish plausible wrong alternatives. A student can minimize discrepancy from that distribution, possibly mixed with an ordinary label loss. Generated-response training instead predicts the retained answer tokens; it does not directly transmit probabilities for every token the teacher did not choose. Data, loss and sampled prefixes determine the information available for transfer.

Distillation changes weights during training. A trained student can generate without the teacher at inference. That differs from speculative decoding, whose draft proposals are checked by a target model while generating. The methods can be combined, but teacher removal and target-distribution preservation are not the same contract.

## One example

For a fictional image, the teacher predicts cat .70, fox .25 and dog .05. A one-hot cat label omits the teacher's preference between fox and dog. Students predicting (.70,.25,.05) and (.70,.05,.25) have the same top class, but only the first matches that preference. This transferred relation is not proof that the teacher's uncertainty is correct.

## Check your understanding

Does same-sized distillation compress the architecture? No. It may transfer behavior while retaining the same parameter count. Compare a fixed student trained with and without teacher supervision on independent task correctness, capability retention, calibration and serving memory, throughput and latency. Include training and teacher-feedback costs when they matter. Teacher errors can transfer; agreement alone is not success, and lower parameter count alone does not guarantee a worthwhile deployment.
