# Coding-Agent Loop Ablation

## Meaning

Compare a simple one-shot code-fix pipeline with agent loops under matched conditions. The aim is to find which additional step helps or harms, not to crown one architecture from one benchmark score.

## Mechanism

Fix the tasks, model, patch format, permissions, time, and token budgets. Start with fixed localization, patch generation, and a predetermined validation check. Add model-directed inspection, feedback use, repair, and stopping one at a time. Read trajectories to classify wrong files, invalid edits, ignored failures, repeated attempts, and premature stops. A model problem, a tool interface problem, and a scoring-harness problem require different fixes.

## One example

An agent makes a good patch but sends it in a format its editor rejects. Training the model further may help, but a schema adapter is a cheaper test. Re-run the same tasks with the adapter before inferring that loops lack value.

## Context-policy example

Compare raw tool results with compacted results on the same held-out issues. Include the summarizer's cost, later recovery reads and billed failed trials. Record which evidence was present before each action. If a summary loses a previously passing result and the agent repeats that check, restore the omitted evidence in a targeted replay before attributing the extra calls to compression. More steps can be useful verification rather than wasted work. Report paired valid outcomes and total cost over repeated trials; prompt size alone is not the success metric.

## Check your understanding

**Question:** Why retain the fixed pipeline after an agent surpasses it? **Answer:** It remains a low-cost baseline and can expose future regressions in added loop steps.
