---
id: in-context-learning
title: "In-Context Learning"
summary: "In-context learning conditions a fixed language model on task instructions or demonstrations in its input rather than updating its weights for that task."
type: concept
tags: [ml/llm/reasoning]
prereqs: [causal-language-model-training, context-window, measurement]
sources: [https://arxiv.org/abs/2005.14165]
status: explained
created: 2026-11-24
updated: 2026-11-24
---

# In-Context Learning

## Meaning

In-context learning changes a model's predictions through information in the current input. Examples can specify a task, label mapping or desired format without a task-time parameter update. This is different from retaining a new skill in the model's weights, and different from proving that a model inferred the intended rule.

## Mechanism

A model trained by [[causal-language-model-training]] predicts a continuation conditional on its prefix. Put task demonstrations in that prefix and then present a new input. The model can use their patterns when predicting the answer. Its parameters remain fixed during this inference call; any adaptation is represented in the computation conditioned on the input, not a separately optimized checkpoint.

The [[context-window]] bounds the demonstrations and evidence available. A later call without those examples need not reproduce their effect. Saving examples in an external store and retrieving them later is an application persistence mechanism, not automatic weight learning. Zero-shot, one-shot and few-shot name the number of task demonstrations; they do not guarantee a particular quality level.

## One example

For an invented formatting task, provide:

| Demonstration input | Desired output |
| --- | --- |
| red, blue | blue / red |
| cat, dog | dog / cat |

Then ask for the output for sun, moon. The intended answer is moon / sun. This checks a narrow order-and-separator rule. It does not show that the model learned a general sorting operation; the examples reversed order rather than sorted alphabetically. Test a new pair whose alphabetical order distinguishes these hypotheses, change the separator and reverse demonstration order.

## Validation and check

Use [[measurement]] to compare no examples, correct examples, shuffled labels and conflicting examples on held-out inputs. Control example selection, order, length and total context budget. Repeat across prompts and seeds, and check contamination or memorization where task novelty matters. More examples can improve coverage but also add distraction, cost and inconsistent instructions. A retrieved demonstration remains untrusted data under the application's authority policy.

Brown et al. evaluate few-shot tasks without gradient updates and discuss methodological limitations. Their results are evidence that the mechanism can be useful, not a universal claim that prompting matches fine-tuning or that every successful completion represents genuine rule induction.

**Check:** If a task demonstration is removed in a new request, must its effect persist? No. Persistence requires it to remain available through the input, memory or a separately trained model change.

## Prerequisites

- [[causal-language-model-training]]
- [[context-window]]
- [[measurement]]

## Sources

- <https://arxiv.org/abs/2005.14165>
