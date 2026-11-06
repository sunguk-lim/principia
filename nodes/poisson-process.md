---
id: poisson-process
title: "Poisson Arrival Process"
summary: "A homogeneous Poisson arrival process counts independent stationary event increments with a constant rate, rather than assuming that equal average rates imply equal arrival patterns."
type: concept
tags: [math/probability]
prereqs: [probability-distribution, exponential-function, expectation]
sources: ["https://www.probabilitycourse.com/chapter11/11_1_2_basic_concepts_of_the_poisson_process.php"]
status: explained
created: 2026-11-07
updated: 2026-11-07
---

# Poisson Arrival Process

## Meaning

A homogeneous Poisson process models event counts over time with a constant rate and no predictive information carried between disjoint time intervals. A measured average rate alone is not enough to establish this model: periodic requests and synchronized bursts can have the same mean rate.

## Mechanism

Let N(t) count arrivals from time zero through time t, and let lambda>0 be the constant expected number of arrivals per unit time. N(0)=0. Counts in disjoint intervals are independent, and the count distribution over an interval depends only on its duration. For an interval of duration u, its count has [[probability-distribution]]

P(N(t+u)-N(t)=k) = exp(-lambda u) (lambda u)^k / k!,

for nonnegative integer k. Here exp is the [[exponential-function]], and k! means the product 1 through k, with 0!=1. The [[expectation]] of the interval count is lambda u. The parameter lambda has inverse-time units, so lambda u is dimensionless.

A further consequence is that the probability of no arrival during u is exp(-lambda u). Independent increments make the residual wait insensitive to how long an arrival-free interval already lasted. That property is not a statement that the next arrival occurs exactly after 1/lambda; event times remain random.

## One example

For an invented rate of three events per second, a half-second interval has mean count 3*.5=1.5. No arrivals has probability exp(-1.5), about .2231. Exactly two has probability exp(-1.5)*1.5^2/2, about .2510. A device emitting precisely every third of a second has the same average rate but not these count probabilities or independent increments.

## Check your understanding

Can an average of three requests per second justify a Poisson queueing formula? No. Examine rate changes, batching, bursts and dependence; choose a window and uncertainty analysis suited to the data. A time-varying Poisson model is a different model from the homogeneous process here. Neither one assumes a particular service-time distribution, queue discipline or number of workers. Those are separate assumptions in a queueing application.

## Prerequisites

- [[probability-distribution]]
- [[exponential-function]]
- [[expectation]]

## Sources

- <https://www.probabilitycourse.com/chapter11/11_1_2_basic_concepts_of_the_poisson_process.php>
