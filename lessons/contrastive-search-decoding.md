# Contrastive Search Decoding

## Meaning

Contrastive search chooses a next token using both probability and a hidden-state similarity penalty. It tries to avoid a plausible but repetitious continuation. The method does not simply prohibit repeated strings, and it does not require a second “amateur” model.

## Mechanism

First take the k most probable next-token candidates. For each, append it to the prefix and obtain its contextual hidden state. Compare that state with earlier token states using cosine similarity; the largest similarity is its degeneration penalty. Score a candidate by `(1-alpha) × probability - alpha × penalty`, with alpha between zero and one, then choose the largest score under a declared tie rule.

The probability term retains plausibility. The penalty encourages a distinct representation, while top-k bounds the candidate search. Static word vectors are not the same as these context-dependent states. Scores can be negative and are not a normalized probability distribution from which to sample.

## One example

Two candidates have probabilities .50 and .30, with the remaining vocabulary mass .20. Their maximum contextual similarities are .90 and .20. At alpha=.4, the first score is .6×.50-.4×.90=-.06. The second is .6×.30-.4×.20=.10, so the second candidate wins.

At alpha=.1, the scores become .36 and .25, reversing the decision. Alpha changes the balance, not the model's knowledge. A penalty can also suppress a legitimate repeated person name or technical term.

## Check your understanding

Is this identical to comparing a large model's logits with a smaller model's logits? No. The defining comparison is with earlier contextual representations. Nor does reduced repetition establish correctness. Compare coherence, required repetition, task quality and cost across k and alpha. Verify hidden-state alignment and candidate scoring against a reference calculation. The primary paper's contrastive training objective is a separate intervention from using this decoding rule.
