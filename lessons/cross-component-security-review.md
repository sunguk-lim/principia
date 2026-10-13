# Cross-Component Security Review

## Meaning

Cross-component security review follows untrusted data and authority across API, state, policy, tools, and rendering boundaries instead of judging files in isolation.

## Mechanism

A component can be locally correct while an unsafe path exists through several components. **Cross-component security review** traces where data enters, how it is stored or transformed, which authority it carries, and where it is rendered or used for a side effect. This is especially important for agent-built changes that add an API, model response parser, policy, tool, and dashboard in one patch.

## One example

Incident text enters an API, is stored in shared state, and later reaches dashboard HTML; testing only the rendering file can miss the full exploit path.

## Check your understanding

**Question:** Where should an adversarial test begin? **Answer:** At the external entry point, then follow the value to the final sink or side effect.
