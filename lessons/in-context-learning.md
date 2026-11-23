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

## Check your understanding

If a task demonstration is removed in a new request, must its effect persist? No. Persistence requires it to remain available through the input, memory or a separately trained model change.
