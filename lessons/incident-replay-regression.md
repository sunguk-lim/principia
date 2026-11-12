# Incident Replay as Regression Testing

## Meaning

An incident replay preserves the conditions needed to reproduce an observed failure and checks whether a later version avoids it. It converts an anecdote into a regression fixture. It does not establish that the new system is robust on every related case.

## Mechanism

Capture the minimum relevant initial state, user inputs, identity, tool contracts, versioned configuration and observed erroneous effect. Remove private content that is unnecessary for the test. Use [[agent-simulation-fidelity]] to reconstruct safe local effects, not a live customer operation. Specify an independent expected outcome before modifying the candidate.

A fixed transcript can reproduce a parser error but may hide an interactive policy failure. Choose a recorded or reactive user model appropriate to the incident, and record that choice. For stochastic models, run multiple fresh trials with explicit success and failure denominators. The [[agent-verification-loop]] must inspect final state and permitted effects rather than trusting a statement that the issue was fixed.

## One example

An invented service refunded an invoice twice after a timeout. The fixture begins with one eligible invoice and a tool response lost after the first simulated refund commits. A retry request follows. The acceptance rule requires exactly one ledger refund and a reconciled final status. A patch that always refuses refund calls may pass the duplication assertion but fail a separate legitimate-refund control. Both fixtures are required.

## Boundaries and check

Keep the failing pre-patch result as evidence and preserve the fixture independently of the repair agent. Add neighboring cases such as an actual pre-commit failure and an unknown remote outcome. Measure recurring failures and false refusals across versions. Once developers tune repeatedly on an incident, it is development evidence; use unseen scenarios to assess generalization. Passing one historic replay means that specified failure did not recur under the tested conditions, not that the entire failure family disappeared.


## Check your understanding

Can one fixed incident prove broad robustness? No; neighboring controls and unseen scenarios are necessary.
