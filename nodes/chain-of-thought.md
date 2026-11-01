---
id: chain-of-thought
title: Chain-of-Thought
summary: Chain-of-thought prompting supplies or elicits intermediate text that later generation can condition on, without guaranteeing correct or faithful reasoning.
type: concept
tags: [ml/llm/reasoning]
prereqs: [transformer-attention]
sources: [https://arxiv.org/abs/2201.11903, https://arxiv.org/abs/2307.13702]
status: explained
created: 2026-06-23
updated: 2026-11-02
---

# Chain-of-Thought

## Meaning

Chain-of-thought prompting supplies examples of intermediate reasoning text or asks a language model to generate intermediate steps before its answer. Those steps become part of the sequence available to later generation. This is a prompting method, not proof that the text reveals the model's complete internal computation.

## Mechanism

Through [[transformer-attention]], later tokens can condition on earlier prompt and output tokens. Writing an intermediate value creates an external textual state that later generation may use. It also adds generation steps and consumes resources. Neither property guarantees an accurate answer or a faithful explanation: the model can copy an error, ignore a stated step or rationalize a conclusion reached another way.

The original prompting study found gains on its evaluated arithmetic, commonsense and symbolic tasks with particular models and demonstrations. That result does not establish a universal performance law or prove that one model pass can execute only one arithmetic operation. Attention mixes learned representations; it is not an explicit interpreter that necessarily reads a number and copies the intended calculation.

## Worked example

A customer has 7 notebooks and buys 3 packs of 4. A written decomposition can state that the packs contribute 12 and the total is 19. Later output can condition on the recorded 12 instead of relying only on an unrecorded intermediate value. This is a transparent possible solution path, not a measurement of which internal calculation caused the answer.

If the intermediate text mistakenly says the packs contribute 15, a model might answer 22, correct the mistake and answer 19, or ignore it. Intervening on the text distinguishes these observed behaviors. Merely showing a correct-looking transcript cannot tell which behavior would occur.

## Validation and boundaries

Compare direct answering and reasoning prompts on identical held-out tasks, controlling demonstrations, output budgets and scoring. Track correct final outcomes separately from intermediate-step correctness, resource use and explanation faithfulness. The faithfulness study uses interventions such as mistakes and paraphrases and finds substantial variation by model and task; more generated text alone does not explain every gain. A correct answer with a plausible rationale is not a guarantee of causal transparency. Treat intermediate text as fallible evidence, and do not use it as an authorization or correctness oracle.

## Prerequisites

- [[transformer-attention]]

## Sources

- <https://arxiv.org/abs/2201.11903>
- <https://arxiv.org/abs/2307.13702>
