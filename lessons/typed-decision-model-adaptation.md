# Typed Decision-Model Adaptation

## Meaning

A small model may learn to return one of a few decision labels. The application still decides whether that label is reliable enough to trigger an action.

## Mechanism

Define the allowed answers and an abstain option. Train a LoRA adapter or another bounded model against labeled examples. Evaluate on a held-out set that avoids duplicate entities and near-identical cases. Compare with the base model, simple rules, and a conventional classifier. Measure schema validity, per-class errors, calibration, abstention, memory, and latency. Keep authorization and policy thresholds outside the model.

## One example

A support model labels a refund request “eligible.” The action gate still checks customer identity, purchase history, amount limit, and prior refunds. A syntactically valid “eligible” output is not an authorization token.

## Check your understanding

**Question:** What does a 65% aggregate accuracy hide? **Answer:** Rare-class errors, data leakage, calibration, abstention behavior, and downstream action cost.
