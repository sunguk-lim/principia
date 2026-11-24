---
id: agent-trajectory-fine-tuning
title: "Agent Trajectory Fine-Tuning"
summary: "Agent trajectory fine-tuning imitates validated next actions from the information available at each interaction step, transferring procedural behavior without turning tool observations into policy authority."
type: concept
tags: [ml/agents]
prereqs: [fine-tuning, causal-language-model-training, tool-call-execution-contract, temporal-data-leakage]
sources: [https://developers.openai.com/api/docs/guides/supervised-fine-tuning, https://huggingface.co/docs/trl/sft_trainer]
status: explained
created: 2026-11-25
updated: 2026-11-25
---

# Agent Trajectory Fine-Tuning

## Meaning

A trajectory is an ordered episode of available information, proposed actions and observed results. **Trajectory fine-tuning** converts curated episodes into examples of what the model should propose next. The objective is procedural behavior: selecting tools, constructing arguments, sequencing work and responding to failures. It is not merely copying a final answer or memorizing every document encountered during an episode.

## Mechanism

[[fine-tuning]] updates a pretrained model using task demonstrations. At each decision, serialize the permitted task, earlier actions and observations, and current tool definitions as the input prefix. The approved next assistant action is the target. Under [[causal-language-model-training]], score only designated assistant target tokens when that is the training contract; tool results can be conditioning context without being outputs the model is trained to fabricate. Preserve call identifiers, message order and schema versions. A loss mask selects training targets; an attention mask separately controls what positions can read.

The boundary established by [[temporal-data-leakage]] is essential. An action at step two cannot use a result first observed at step three. Splitting one episode into many prefixes does not produce independent tasks: keep related episodes, templates and near-duplicates together when constructing train and test splits. Generated demonstrations need an acceptance policy just as human demonstrations do.

The [[tool-call-execution-contract]] still applies after training. A well-formed call can be unauthorized or wrong. Execution code must validate identity, arguments and effects; imitation does not grant permissions. Demonstrations should distinguish a successful response, an independently verified task outcome and an unknown outcome after interruption. Do not teach unsafe retries just because the final episode eventually succeeded.

## One example

In an invented scheduling sandbox, the observed prefix says slot A is unavailable and slot B is free. The approved action proposes reserving B. A second example ends earlier, before the availability query; its target is the query, not the reservation. Supplying the future availability result to that earlier example would train a different, leaked task.

Include a recovery episode in which a reservation returns an unknown outcome. Its approved continuation checks reservation status before proposing another write. Blindly repeating the write would be an invalid demonstration even if duplicate suppression happened to hide the mistake in one run.

## Boundaries and validation

Behavioral imitation observes demonstrated states. A small earlier error may expose the deployed model to states absent from those demonstrations. Retain adjudicated recovery and refusal cases, and evaluate complete closed-loop episodes rather than only next-action token accuracy. Successful traces alone can overrepresent easy tasks; failed traces require corrected targets or explicit failure labels, not indiscriminate copying.

Compare prompting, a fixed workflow and the tuned model on held-out task families using the same tools and initial state. Measure verified completion, unauthorized effects, argument validity, recovery, total cost and broader capability retention. Tool-schema drift and changed business rules require revalidation. The primary SFT documentation grounds demonstration-based training and tool-call examples, not a guarantee that one training run will generalize to a new workflow.

## Check your understanding

If a trace ends successfully, is every earlier action a good training target? No. An unsafe, redundant or hindsight-dependent action can occur inside a successful episode.

## Sources

- <https://developers.openai.com/api/docs/guides/supervised-fine-tuning>
- <https://huggingface.co/docs/trl/sft_trainer>
