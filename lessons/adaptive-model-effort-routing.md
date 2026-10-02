# Adaptive Model-and-Effort Routing

## Meaning

A routing layer can choose both *which* model handles a request and *how much* reasoning or compute budget it receives. The objective is to satisfy a task-quality target at acceptable latency and cost, not simply to select the cheapest model on every turn.

## Mechanism

A router observes permitted request features such as task type, input size, tool needs, and prior failures. A bounded decision then selects a model and effort tier. A [[decision-score-action-gate]] must convert uncertain model predictions into allowed choices and an abstain or fallback path. The routing policy should reject models lacking required modalities or tools before cost optimization.

The decision is sequential. In a continuing conversation, switching models can lose reusable prompt state and [[prefix-caching]] benefits; staying on a slightly more expensive model may cost less than a cold switch. Likewise, raising effort on the current model can improve a hard turn without a provider change. Compare expected gain against extra tokens, latency, cache loss, and the probability of retry or escalation. This is distinct from GPU model residency: routing chooses an endpoint or model policy, while residency manages loaded weights on serving hardware.

## Worked example

A support workflow contains short classification turns and occasional hard debugging turns. A fixed high-end model meets quality but costs more on routine work. A router can try a cheaper model for easy turns, increase effort for difficult ones, and stay on the same model when switching would lose a valuable cached prefix. Compare accepted-answer cost, not just nominal token prices.

**Understanding check:** When should a router stay with a more expensive model despite a cheaper alternative being available?
