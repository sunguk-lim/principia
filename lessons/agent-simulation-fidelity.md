# Agent Simulation Fidelity

## Meaning

A simulation lets an agent interact with controlled users and tools without risking real customer effects. Fidelity asks which deployment properties it reproduces well enough for the evaluation question. Realistic dialogue alone is not sufficient if the simulated database or permission boundary behaves incorrectly.

## Mechanism

Implement a stateful sandbox with explicit initial records, tool semantics, caller identity, permissions, failures and observable outcomes. The [[tool-call-execution-contract]] defines the effect boundary: a simulated refund should change a simulated ledger only after the required checks. A user simulator can vary intent, ambiguity and adversarial pressure, while a separate evaluator inspects the resulting state through an [[evaluation-oracle-availability]] contract.

Calibrate against reviewed production traces and domain rules. Track known gaps, such as omitted asynchronous webhooks, timeouts or external consistency delays. Model-generated users and graders may share biases; independent assertions should check critical invariants. Never wire a supposed sandbox to live payment or messaging credentials merely to increase realism.

## One example

In an invented refund test, the sandbox contains invoice I1 belonging to customer A. Simulated customer B requests its refund. A fluent response saying “refunded” is not success. Assert that identity and ownership were checked, the unauthorized ledger remains unchanged and the refusal is correctly reported. A second fixture uses A with an eligible invoice and must permit exactly one refund. Testing only denials would reward an agent that refuses everything.

## Boundaries and check

Hold out scenario templates, replay real incidents and compare failure slices after deployment. Passing simulation supports only its modeled tasks and assumptions; it cannot prove that unknown production states are safe. Record model, tools, simulator, prompts and seeds so changes can be attributed. Synthetic users are useful test instruments, not representative customers by default.


## Check your understanding

Is a realistic conversation enough? No; tool permissions and resulting state must match the evaluation question.
