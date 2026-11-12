# Decision-Context-Aware Assistance

## Meaning

An assistant helps someone make a decision, not merely enumerate facts. Decision context includes the objective, available time, resources, relevant authority and current task stage. A recommendation is useful only relative to that context. Tone and factual correctness are separate dimensions.

## Mechanism

Represent the goal and constraints explicitly in the [[agent-plan-artifact]]. Read authorized current metadata when available, ask when an unknown constraint changes the decision, and distinguish stated facts from assumptions. Check freshness: yesterday's remaining budget can be wrong today. Preserve uncertainty rather than filling every missing field with a guess.

A [[decision-score-action-gate]] separates assessment from permitted action. The same evidence may justify a different feasible next step under a different time budget. This does not license changing factual claims to please the user. Explain why an option was excluded, retain serious unresolved issues and give a concrete next action rather than an unfocused critique.

## One example

An invented analysis has a suspect denominator. Reconstructing the dataset takes six hours; checking the calculation from saved counts takes twenty minutes. With one hour available, recommend the twenty-minute check and, if unresolved, qualify the claim. With two days available, recommend reconstructing the data as well. In both cases, the evidence gap remains real. The one-hour user did not receive a lower standard of truth, only a different action plan.

## Boundaries and check

Context is not always irrelevant to severity: intended deployment and potential harm can change the applicable rubric. State which variables affect truth, risk or feasibility. Evaluate matched tasks for completed useful actions, factual stability, unnecessary questions and missed constraints. Human-AI interaction guidance motivates context-sensitive assistance; the architecture here is a design synthesis, not a proven cure for every unhelpful assistant.


## Check your understanding

Why can the same correct finding yield different advice? The feasible action set can change without changing the evidence.
