# Quality–Cost Model Selection

## Meaning

Quality–cost model selection chooses a deployment configuration for a task and its constraints. It does not ask which checkpoint is best in the abstract. More parameters, lower training loss and a higher headline benchmark score are evidence about particular properties, not a complete deployment decision.

## Mechanism

Begin with the real acceptance rule: valid task completion, critical subgroup behavior and any hard latency, memory or budget limit. Compare models on the same held-out inputs. Preserve paired outcomes and uncertainty so a small score difference is not mistaken for a stable improvement. Examine slices because an overall gain can hide a failure on the cases with the highest error cost.

Measure the configuration you would serve: hardware, precision, batching, prompt and retry policy matter. Remove candidates that violate hard requirements. Among feasible candidates, keep quality–resource trade-offs visible. A configuration dominates another only when it is no worse on every declared objective and better on at least one; a trade-off still needs the user's priorities.

## One example

Suppose the service requires 90% valid completion and a 95th-percentile latency below 2 seconds. A measures 92%, 1.5 seconds and $0.02 per attempt. B measures 93%, 2.4 seconds and $0.04. C measures 89%, 1.2 seconds and $0.01. B misses latency and C misses quality, leaving A as the only observed feasible choice. A's quality uncertainty must still be checked before acceptance.

These invented measurements illustrate a rule, not a ranking of commercial products. Changing the allowed latency or traffic mix can change the decision.

## Rankings and combined scores

Token-volume popularity is a selected usage measure, not held-out quality: longer outputs can raise token share without more users or better answers. A composite router score also embeds priorities. If A has normalized quality 0.9 and cost 0.8, and B has quality 0.8 and cost 0.2, scoring quality minus 0.1 times cost selects A (0.82 versus 0.78). A cost weight of 0.3 instead selects B (0.66 versus 0.74). These are invented numbers demonstrating a changed objective, not changed model performance. Keep hard constraints outside compensating scores; report component metrics, workload and uncertainty.

## Count failed attempts too

A configuration costing one unit per attempt and succeeding twice in ten attempts spends ten units for two successes: five units per success. Another costing two units per attempt and succeeding eight times spends twenty units for eight successes: 2.5 units per success. These invented sample ratios include failed attempts; successful-run-only comparisons hide their cost. Report retries, infrastructure failures, latency denominators and uncertainty. Provider credits need a documented conversion before numerical comparison.

## Check your understanding

Does a lower token-level validation loss establish better deployment value? **No.** Verify the target outcomes, their uncertainty and the actual resource contract. Keep tuning data separate from final acceptance and document when the selection must be revisited.
