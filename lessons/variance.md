# Variance

## Meaning

Variance summarizes spread by averaging squared distances from the mean. Positive and negative deviations do not cancel after squaring, and unusually distant observations receive greater weight. Its units are squared; standard deviation takes the square root to return to the original units.

## Mechanism

For a random variable X with mean mu, population variance is the expected value of (X-mu) squared. Equivalently it is E[X²] minus the square of E[X], when these quantities exist. This identity follows by expanding the squared difference and using expectation.

For observed data, distinguish the average squared deviation of the listed values from an estimator of a population's variance. The descriptive version divides by the number of observations n. The conventional unbiased sample estimator divides by n-1 when the mean was estimated from the same independent, identically distributed sample. Neither denominator should be changed without changing the interpretation.

## One example

For 1, 3 and 5, the mean is 3. Deviations are -2, 0 and 2, whose squares add to 8. Descriptive variance is 8/3, about 2.667. Sample variance is 8/2=4. The associated standard deviations are about 1.633 and 2. These are different summaries, not two answers to an identical statistical question.

## Check your understanding

Is data variance the same as uncertainty about the average? **No.** Uncertainty of an average depends on sample size and dependence. Correlated observations cannot automatically receive the independent-sample reduction. Also inspect extreme values and sampling assumptions; one spread estimate cannot certify that a dataset represents a deployment population.
