# Adaptive Computation Time

## Meaning

Adaptive Computation Time (ACT) learns how many internal updates to spend on an input before moving to the next output. It augments a [[recurrent-neural-network]] with a halting signal and a cost for extra updates. It is one specific adaptive-depth algorithm, not a synonym for every confidence threshold or early-exit heuristic.

## Mechanism

For one input, let $s_n$ be the state after internal update $n$, and $h_n$ a learned number in $(0,1)$ produced from that state. Choose a small tolerance $\epsilon>0$. Let $N$ be the first step where the cumulative sum of $h_n$ reaches $1-\epsilon$. Define weights $p_n=h_n$ for steps before $N$ and set the final remainder to

$$p_N=1-\sum_{n=1}^{N-1}h_n.$$

The weights sum to one. ACT forms weighted states and outputs from the internal updates, rather than sampling one update to keep. The last raw halting value need not equal its final remainder weight. The training objective adds a ponder cost, based on the number of updates and remainder, multiplied by a chosen penalty coefficient. This encourages speed but can trade away task quality. [[backpropagation-through-time]] trains the repeated shared computation and halting mechanism through the defined weighted computation.

## One example

Choose $\epsilon=0.01$ and successive halting values $0.30$, $0.40$, and $0.50$. Their cumulative sums are $0.30$, $0.70$, and $1.20$, so $N=3$. The output weights are $0.30$, $0.40$, and the remainder $0.30$, not the last raw value $0.50$. If three scalar outputs are $2$, $5$, and $9$, their weighted result is $0.3\times2+0.4\times5+0.3\times9=5.3$. Returning just the last output would be a different algorithm.

An implementation also needs a finite step cap and defined behavior when it is reached. More permissive budgets can waste work, while stronger ponder penalties can stop too early. Per-position adaptive depth may require masked execution that saves fewer device operations than its logical step count suggests. Measure real latency, active work, worst-case caps, quality by difficulty, and sensitivity to penalty and tolerance.

The original paper found gains on particular synthetic tasks and limited language-modeling improvement; neither result is a universal guarantee. Compare fixed depth with adaptive depth under the same maximum budget and data. Halting measures a learned compute decision, not proof that an answer is correct.

## Check your understanding

Why use a remainder? It makes the aggregation weights sum to one at the selected stopping step without treating an overshooting raw halting value as the final weight.
