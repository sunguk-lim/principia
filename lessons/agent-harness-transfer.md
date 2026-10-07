# Agent Harness Transfer

## Meaning

An agent model can appear competent in one runtime yet fail in another because the runtime changes what it sees and which actions it can express. Transfer means testing whether the same weights still complete comparable tasks when the harness changes.

## Mechanism

The [[agent-execution-harness]] supplies prompts, tools, observations, and control rules. Fine-tuning on one set of trajectories teaches next-action behavior under those exact conditions. A different [[tool-call-execution-contract]] can make an otherwise sensible action invalid. If the resulting error format is also unfamiliar, later mistakes can compound.

Hold the task and weights fixed while changing one interface dimension at a time. An adapter may translate syntax, but it must preserve meaning, permissions, and side effects. Compare it with training on multiple harnesses and with keeping the original runtime. Measure valid calls and independently verified task outcomes, not training loss alone.

## One example

A model trained to call `edit_file(path, patch)` is given only `apply_patch(diff)`. A prompt describing the new tool may help, but a held-out task run tests whether it actually generates valid calls and recovers from errors.

## Check your understanding

**Question:** Does low next-action loss on one harness prove transfer? **Answer:** No; the target harness changes the input and action distribution.
