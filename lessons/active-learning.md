# Active Learning

## Meaning

Active learning chooses which unlabeled examples to label next, trying to reach a target model quality with less total annotation and selection cost than a simpler sampling policy. A complicated acquisition score is useful only if it improves that measured objective.

## Mechanism

Maintain a labeled set, an unlabeled pool and a budget. Train a model, score candidate examples, acquire a batch of labels, update the model and repeat. Uncertainty sampling uses the model's [[probability-distribution]] to prefer uncertain examples. [[model-calibration]] checks probability-frequency agreement but does not prove that a particular acquisition rule is optimal. Evaluate with an untouched representative set rather than only the deliberately selected acquisition data.

For generated sequences, first define the labeling unit. Token predictive entropy measures spread over possible next tokens. Summing observed token entropies along one continuation is not automatically the joint entropy over every possible sequence: that quantity averages conditional uncertainty over possible prefixes. Ambiguous but valid continuations can be uncertain without being incorrect.

Selection can overrepresent duplicates, unusual inputs or labeling errors. Combine uncertainty with appropriate coverage checks and compare against random sampling at equal label and compute cost. A smaller proxy may reduce scoring expense, but its acquisition ranking needs independent validation.

## One example

Suppose a short two-token continuation has entropy 0.5 nats at each step, while a six-token continuation has 0.3. Summed scores are 1.0 and 1.8, favoring the longer item. Mean scores are 0.5 and 0.3, reversing the ranking. Neither rule is universally right: ask which predicts useful annotation gain for the actual task and budget.

## Check your understanding

Does the highest entropy example necessarily deserve the next label? No. It may be ambiguous, redundant or expensive to score. Compare learning curves, critical slices, annotation disagreement and stopping criteria; retain confident errors as a diagnostic because low entropy is not proof of correctness.
