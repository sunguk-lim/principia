# Fixed-Choice Logit Scoring

## Meaning

**Goal:** rank a finite set of application-defined choices without generating an answer string.

Use fixed-choice logit scoring only when the complete choice set is known before inference. Assign each choice a verified one-token label, end the prompt immediately before that label, and read the model's next-token score for each label.

## Mechanism

If labels `A`, `B`, and `C` have logits $z_A,z_B,z_C$, apply [[softmax]] only to those three numbers:

$$p_i=\frac{e^{z_i}}{e^{z_A}+e^{z_B}+e^{z_C}}.$$

The probabilities sum to one across the offered labels. The model does not generate JSON or explanatory text; application code maps labels back to choices and decides whether to accept, abstain, or escalate.

The result is conditional on the offered set. It does not prove that the winner is correct, and it is not automatically [[model-calibration|calibrated]]. If every offered answer is wrong, normalization still gives one of them the largest score.

## One example

A support router maps `A = billing`, `B = technical`, and `C = account`. Suppose their logits are $[8.2,5.5,4.8]$. Subtracting 8.2, exponentiating, and normalizing gives approximately

$$[0.909,0.061,0.030].$$

The scorer ranks billing first. A policy might accept it only if the top score exceeds 0.8 and the offered set includes an `other` option. That policy must be validated on labeled tickets; 0.909 alone is not a measured 90.9% correctness rate.

Verify the labels in the fully rendered chat template because whitespace can change tokenization. Randomize label mappings and choice order during tests to expose token or position bias.

## Check your understanding

What happens if the true answer is `security`, but the only labels are billing, technical, and account?

**Answer:** softmax still assigns all probability mass among the three offered labels. The scorer cannot express the missing class unless the application adds `security`, `other`, or an abstention rule.
