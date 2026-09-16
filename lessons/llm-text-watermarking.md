# LLM Text Watermarking

## Meaning

LLM text watermarking inserts a hidden statistical pattern while a model generates text. The output contains no visible label; detection depends on finding more key-selected tokens than chance predicts.

## Mechanism

At each position, a secret key and recent context select a pseudorandom green list. Before [[softmax]], the generator adds a small bias to green-list logits, making those tokens somewhat more likely without forbidding other tokens. The detector recreates every green list and counts how often the observed token is green.

For $T$ tested positions, green fraction $\gamma$, and observed green count $G$, one detector uses

$$z=\frac{G-\gamma T}{\sqrt{T\gamma(1-\gamma)}}.$$

A predeclared [[hypothesis-testing]] threshold turns this excess into a decision with a modeled false-positive rate.

## One example

With $T=100$ and $\gamma=0.5$, chance predicts 50 green tokens and the denominator is 5. Observing 65 gives $z=(65-50)/5=3$. That is evidence for the watermark under the detector's assumptions, not proof of authorship.

## Check your understanding

**Question:** Why not make the green-token bias arbitrarily large?

**Answer:** A larger bias strengthens detection but increasingly changes token choices, which can reduce quality and make the signal easier to notice or attack.
