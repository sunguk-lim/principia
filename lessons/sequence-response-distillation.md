# Sequence Response Distillation

## Meaning

Sequence response distillation uses a teacher's generated output as the student's training target. It is a form of [[knowledge-distillation]] whose retained evidence can be text alone: the training set records an input and a complete teacher answer, not necessarily probabilities for every alternative token.

## Mechanism

Generate one or several teacher continuations for each permitted training prompt. Fix the teacher version and generation policy, filter or verify examples according to the task, and train the student to predict the retained answer tokens. In [[causal-language-model-training]], each token is conditioned on the earlier retained target tokens. Thus the student sees teacher-produced prefixes during training even though it will later condition on its own generated tokens.

For a prompt x and a retained answer with tokens y_1 through y_T, let q_theta be the student's conditional token probability. The response loss is minus the sum, over t from 1 to T, of log q_theta(y_t given x and y_1 through y_(t-1)). This is supervised next-token training on teacher-produced labels. It differs from matching the teacher's entire next-token distribution at each prefix. A sampled teacher answer and a beam-selected answer also induce different training datasets.

## One example

Consider an invented unit-conversion prompt whose verified teacher answer has two response tokens, “twelve” and “meters.” The student assigns .25 to the first correct token and .5 to the second given the first. The negative log likelihood is -log(.25)-log(.5)=-log(.125), about 2.079 with natural logs. The objective raises those retained-token probabilities; it supplies no direct information about the teacher's probability for “thirteen.”

## Check your understanding

Does imitating a fluent teacher answer certify the answer? No. Incorrect labels and missing task modes can transfer. Evaluate the student on independent prompts with task-specific correctness checks, compare the same student trained without teacher data, and report teacher-generation and training costs separately from inference savings. Multiple references, filtering and mixing trusted labels change coverage and cost; none guarantees universal transfer. The primary sequence-level paper establishes the method in translation, not a blanket claim about every language-model task.
