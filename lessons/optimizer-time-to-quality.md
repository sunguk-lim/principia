# Optimizer Time-to-Quality Evaluation

## Meaning

An optimizer that needs fewer updates can still be slower. Time-to-quality evaluates the complete training procedure against a declared target, including update cost, schedules, tuning and failure handling. It is not a ranking by final loss after an arbitrarily chosen number of steps.

## Mechanism

Fix the task, data/split policy, architecture, hardware, target metric and acceptance threshold. Define when timing begins and ends, which compilation, evaluation, checkpoint and data-loading work is charged, and what happens when a run never reaches the target. Give each optimizer an explicit tuning budget rather than copying one method's learning rate into another. Keep the final acceptance data independent of tuning.

[[quality-cost-model-selection]] supplies constraints and uncertainty-aware selection. [[training-memory-budget]] matters because optimizer state can change feasible batch size, accumulation or sharding, altering the entire training configuration. Report those changes rather than attributing every difference to the update formula. MLCommons AlgoPerf is a primary example of fixed-model/hardware targets and explicit tuning rules; an independent local comparison should state its own scope rather than claim benchmark equivalence.

## One example

On invented matched workloads, A reaches the target after 100 updates at 1 second each, while B needs 80 updates at 1.3 seconds each. Their training times are 100 and 104 seconds: 20% fewer steps still takes 4% longer. If an extra basis refresh costs B 6 seconds outside the measured step average, B actually takes 110 seconds. Count it once, not both in the average and again afterward.

## Check your understanding

Should a run that never reaches the quality target disappear from the average? No. Report failures, time caps and the success fraction. Repeat runs, compare task slices and memory peaks, and record tuning cost. Also report quality at a fixed compute budget: time-to-target and fixed-budget quality answer different questions and neither establishes universal optimizer superiority.
