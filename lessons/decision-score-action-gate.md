# Decision-Score Action Gate

A model's job can be a bounded judgment: “Does this ticket belong to billing, technical support, or neither?” The model may return a label and probabilities, but an application must decide what action those values warrant. This boundary is the decision-score action gate.

Define the labels and abstain state before training or prompting. Test probabilities on held-out, representative cases: among cases scored around 0.8 for billing, roughly 80% should truly belong there if the score is calibrated. Calibration alone does not choose an operating threshold. A low-cost routing mistake and an irreversible financial error require different policies. Pick thresholds from measured precision/recall and the costs of false actions and delayed review; send ambiguous cases to a human. Revisit the threshold when traffic, labels, or the model change.

For example, a support application may auto-route a ticket when a calibrated billing score is high and otherwise ask for review. A refund application cannot treat “refund eligible: 0.97” as permission to pay. It still has to check identity, account policy, amount, and whether a previous payment already happened. Those checks are application code, not model instructions. Record the score, policy version, authorization result, and final state so a later audit can distinguish a mistaken prediction from a faulty policy or a failed side effect.

A typed decision service may return yes/no, bounded-choice, or numeric answers. The application still owns arithmetic, authorization, and threshold policy. Compare specialized decision models, ordinary classifiers, rules, and constrained-output language models on the same cases. A structured JSON answer makes the interface easier to parse, not the decision safer. A purported speed advantage must be measured under a matching workload.

**Understanding check:** If a model's 0.9 scores are well calibrated, why might auto-approving every 0.9 case still be unacceptable?
