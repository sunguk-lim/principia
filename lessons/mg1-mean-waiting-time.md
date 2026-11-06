# M/G/1 Mean Waiting Time

## Meaning

An M/G/1 queue has [[poisson-process|Poisson arrivals]], a general service-time distribution and one worker. For the mean waiting formula below, also assume first-come-first-served nonpreemptive service, independent identically distributed service times independent of arrivals, a work-conserving worker, an unbounded waiting room and a stationary regime. The result is about waiting before service, not a tail percentile.

## Mechanism

Let lambda be arrivals per second, S a nonnegative service time in seconds, m=E[S] its finite mean, b=E[S^2] its finite second moment, and rho=lambda m<1. [[single-server-queue-stability]] explains the load condition. Let Wq be time spent waiting before service begins. The Pollaczek–Khinchine formula is

E[Wq] = lambda b / (2(1-rho)).

Why does b appear? A service interval of duration s contributes an area s^2/2 under its remaining-service-time curve. Longer services are both more likely to be encountered at an arbitrary instant and leave more remaining work. Averaging these areas over completed jobs gives mean residual service lambda b/2. A Poisson arrival observes that time-average residual. By [[little-law]], the mean number already waiting is lambda E[Wq]; independent service requirements give mean work lambda E[Wq] m = rho E[Wq]. Adding that queued work yields E[Wq]=lambda b/2+rho E[Wq]. Rearranging gives the formula. This residual-work argument relies on the stated independence and stationarity, not just an observed average arrival rate.

## One example

Use an independently constructed rate of four jobs per second and mean service .125 seconds: rho=.5. Constant .125-second jobs have b=.015625 seconds squared and E[Wq]=4*.015625/(2*.5)=.0625 seconds. Instead, let 75% of jobs take .05 seconds and 25% take .35 seconds. Their mean is .75*.05+.25*.35=.125, but b=.75*.05^2+.25*.35^2=.0325. Mean waiting becomes .13 seconds, 2.08 times the constant-service case despite equal mean demand and load.

## Check your understanding

[[variance]] gives b=Var(S)+m^2, so equal means do not determine waiting. Total mean response is E[Wq]+m under this model; neither mean fixes p99. Infinite b can give infinite mean waiting despite rho<1. Continuous batching, multiple workers, priorities, preemption, bursty arrivals or load-dependent service require different analysis. Use this formula as an explicit idealized baseline, not an exact prediction for a shared accelerator.
