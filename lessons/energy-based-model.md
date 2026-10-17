# Energy-Based Model

## Meaning

**Goal:** explain why ranking possible outputs need not require a normalized probability.

An energy-based model assigns a scalar cost to an input-output pair. Lower energy means a more compatible pair. Given an input, prediction searches for the candidate output with the lowest energy. The word “energy” establishes the comparison direction; it does not make the number a physical measurement or a certainty score.

## Mechanism

Let $E(x,y)$ be the energy of output $y$ for observed input $x$. Minimum-energy prediction compares these values directly. With finitely many outputs, probabilities can optionally be defined by applying [[softmax]] to their negative energies. That adds a denominator summing over all candidates. Finding the minimum does not require that sum.

Training needs a [[loss-function]] that distinguishes desirable outputs from alternatives. Merely lowering the energy of observed correct examples can allow every output to acquire the same low energy. A relative or likelihood-based training objective must prevent that trivial solution under its own assumptions. Avoiding normalization in the prediction rule does not eliminate the cost of every possible training objective.

## One example

Suppose candidate energies are $[1,3,4]$. The first candidate wins. Adding ten to all three gives $[11,13,14]$ and the same winner. The optional probabilities also remain unchanged because a common exponential factor cancels. The absolute energy value therefore cannot be interpreted as confidence without an additional measured contract.

## Check your understanding

Can any energy function over a continuous output be turned into a probability density?

**Answer:** not automatically. The integral of its negative exponential must be finite. Comparing two energies needs no such normalization, but constructing probabilities does. Search errors, ranking quality, and probability calibration are separate evaluation questions.

Reference: [LeCun's energy-based learning demonstrations](https://www.cs.nyu.edu/~yann/research/ebm/).
