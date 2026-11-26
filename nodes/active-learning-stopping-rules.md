---
id: active-learning-stopping-rules
title: "Active-Learning Stopping Rules"
summary: "Active-learning stopping rules decide when to end acquisition using declared resource limits or independently monitored learning progress, without equating exhaustion with adequate quality."
type: concept
tags: [ml/training]
prereqs: [active-learning, measurement]
sources: [https://raw.githubusercontent.com/NUAA-AL/ALiPy/master/alipy/experiment/stopping_criteria.py]
status: explained
created: 2026-11-27
updated: 2026-11-27
---

# Active-Learning Stopping Rules

## Meaning

A stopping rule ends an acquisition loop according to a declared condition. It answers when further label collection should cease, not which example to choose next. A hard budget and a claim of adequate model quality are different reasons to stop [[active-learning]].

## Mechanism

Check resource feasibility before launching a batch, then record realized costs and progress after the batch completes. Fixed query count, elapsed time, labeled-pool fraction and accumulated cost are straightforward limits. An empty eligible pool is another termination condition. ALiPy's stopping implementation exposes these resource-oriented choices; it does not implement a general statistically justified performance-plateau test merely because its source comments mention that possibility.

A progress rule needs additional [[measurement]] design. Define the metric, monitored evaluation split, minimum meaningful gain, evaluation cadence and patience before watching results. Reusing one validation set for repeated stopping decisions can overfit it; retain an untouched final test and report uncertainty. Stable model predictions on the acquisition pool are not proof of correctness or adequate rare-slice coverage.

## One example

An invented labeling budget is 100 cost units. Completed rounds cost 25, 30 and 20, totaling 75. The next proposed batch has an estimated cost of 30. A pre-launch budget rule rejects or reduces that batch because only 25 remain. A purely post-batch threshold could overshoot to 105; that implementation is a reporting trigger, not strict budget enforcement.

Separately, suppose validation accuracies after three rounds are .80, .81 and .81. A predeclared rule requiring gain at least .02 for two consecutive rounds would stop under those point estimates. But small validation samples, noise and missed critical cases can make that a poor quality decision. The numbers illustrate the rule only; they are not sufficient statistical evidence of a plateau.

## Boundaries and validation

Test exact thresholds, zero remaining pool, variable batch sizes, delayed annotation, overruns and checkpoint restart. Record why the run stopped and which quality criteria remain unmet. Compare stopping policies on full learning curves reconstructed without using the final test to choose thresholds. A performance plateau can mean the current acquisition policy is unhelpful, the labels are inconsistent or the evaluation is insensitive—not that all useful knowledge has been acquired.

**Check:** Does “budget exhausted” mean the deployment target was reached? No. Report the constraint and quality outcome separately.

## Sources

- <https://raw.githubusercontent.com/NUAA-AL/ALiPy/master/alipy/experiment/stopping_criteria.py>
