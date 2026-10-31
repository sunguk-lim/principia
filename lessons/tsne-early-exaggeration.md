# t-SNE Early Exaggeration

## Meaning

Early exaggeration temporarily strengthens attractive neighborhood forces at the start of t-SNE optimization. Later optimization restores the ordinary affinities. It is a schedule for finding a map, not proof that the resulting separated groups are distinct populations.

## Mechanism

t-SNE compares input neighbor affinities with affinities induced by the current map. In its usual force expression, an input affinity contributes attraction and the map affinity contributes repulsion. Early exaggeration multiplies the input term by a factor greater than one without renormalizing it. This shifts the relative force balance during early gradient steps.

Renormalizing immediately would undo the multiplication. The exaggerated values therefore should not be interpreted as another normalized probability distribution that all output probabilities must match.

## One example

Take one pair with input affinity 0.02 and current map affinity 0.01. Its ordinary coefficient is 0.01. With exaggeration factor four, the coefficient becomes 0.08 minus 0.01, or 0.07. Hold the current positions and distance factor fixed for this comparison.

For a weaker pair with input affinity 0.001 and the same map affinity, the exaggerated coefficient is 0.004 minus 0.01, or -0.006. It is still repulsive. Therefore multiplying all input affinities does not mean that every pair is pulled together or that every final gap scales by the exaggeration factor.

## Check your understanding

Should a larger factor always improve visualization? **No.** It interacts with learning rate, initialization and duration, and can impair optimization. Compare seeds, convergence and original-space neighborhoods. A thresholded variant that treats strong and weak pairs differently is a distinct proposed method, not a proven general improvement.
