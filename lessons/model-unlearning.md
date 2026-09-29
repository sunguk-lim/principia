# Model Unlearning

## Meaning

[[model-unlearning]] tries to reduce the influence of particular training data on a trained model without repeating all training. The target could be a document, a person's records, or a category of content. A model that refuses to say the target is not automatically a model that has forgotten it.

## Mechanism

First define what “removed” means and choose a reference, ideally a model retrained without the target data. An approximate unlearning intervention may edit weights or train on counterexamples. It can lower the probability of reproducing target material, but can also harm related useful knowledge or cause excess refusal. Neither effect can be judged from a single prompt.

Use [[training-data-extraction-risk]] tests with multiple attack styles, paraphrases, and decoding settings. Compare the modified model to both its original version and the retrained reference. Also test general task quality, false refusals, and whether later tuning restores the target. State the tested attacker's budget and that the result is approximate if no formal deletion guarantee exists. Data minimization before training is often safer than trying to remove known sensitive data afterward.

## One example

Suppose a model trained on a fictional biography can answer questions about it. A refusal fine-tune may block “Who is this person?” but still allow indirect clues from other questions. An unlearning evaluation tests direct and indirect prompts, checks unrelated biography knowledge, and compares with a model never trained on the biography.

## Check your understanding

**Question:** Why is low extraction on one benchmark insufficient proof of unlearning? **Answer:** It covers only those prompts, decoding settings, and attack resources. The model may retain target influence that another attack or task exposes.
