# Verbalized Sampling

## Meaning

Verbalized sampling is a prompting strategy: ask for a set of candidate answers and associated probability descriptions instead of asking for only one answer. The candidates can expose alternatives that direct prompting repeatedly misses. The written numbers are model outputs, not direct access to a normalized probability over all complete responses.

## Mechanism

[[llm-sampling-controls]] changes token selection during generation. Verbalized sampling changes what the model is asked to generate: a distribution-shaped collection of responses, possibly with instructions about the requested region of probability mass. A separate application policy can select from that collection, ask a verifier to check it or request another proposal. Do not confuse generating the collection with sampling a final answer from a specified law.

Check format, duplicate candidates, nonnegative weights and the intended normalization rule. [[model-calibration]] concerns agreement with observed outcomes; a candidate's verbalized probability is not automatically calibrated truth confidence, actual sequence likelihood or empirical human preference. The paper studies an inference-time diversity intervention. Its explanation of typicality bias and its measured gains should not be generalized into guaranteed safety or quality on another workload.

## One example

An invented prompt asks for three coffee-joke ideas and their weights. The model returns A:0.2, B:0.1 and C:0.1. If the application chooses to treat these only as relative weights over the returned set, it normalizes by 0.4, giving 0.5, 0.25 and 0.25. That is a declared conditional selection policy over three candidates; it is not proof that A has probability 0.5 among every answer the model could produce.

If A and B are paraphrases, counting three strings overstates diversity. If C contains an unsafe suggestion, a small weight does not make it acceptable. Candidate validity and final selection remain separate contracts.

## Check your understanding

Does a written 0.01 prove that a candidate is a calibrated rare but valid answer? No. It is generated metadata requiring its own interpretation and validation.
