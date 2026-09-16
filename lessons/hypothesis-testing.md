# Hypothesis Testing

## Meaning

A hypothesis test asks whether an observed statistic would be unusually extreme under a stated baseline, called the null hypothesis. It does not return the probability that the null is true.

## Mechanism

The null defines a [[probability-distribution]] for a statistic $S$. Before looking at the result, choose a significance level $\alpha$. The rejection region is selected so that

$$P(S\text{ is in the rejection region}\mid H_0)\le\alpha.$$

The [[conditional-probability]] is evaluated assuming the null is true. A p-value is the probability, under that same assumption, of obtaining a statistic at least as extreme as the observed one. Reject when the p-value is at most the predeclared $\alpha$.

## One example

For 100 flips of a fair coin, the null expects head counts near 50. If 65 heads is sufficiently far into the tails of the fair-coin distribution that the two-sided tail probability is below 0.05, a 5% test rejects the fair-coin null. This does not say there is a 95% probability that the coin is biased.

## Check your understanding

**Question:** Why must the threshold be chosen before searching many statistics?

**Answer:** Searching and selecting the smallest p-value changes the procedure's false-positive probability; the original $\alpha$ no longer describes the whole search.
