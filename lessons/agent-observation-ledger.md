# Agent Observation Ledger

## Meaning

A computer-use agent should not confuse an old screenshot with the current screen or an attempted click with a completed effect. An **observation ledger** records what the agent has tried, what was observed afterward, which subgoals are complete, and what remains uncertain. Recent pixels remain available for perception; durable progress lives in structured [[agent-session-state]].

## Mechanism

The ledger is a compact, inspectable state record, not a transcript summary claiming perfect recall. Each step has an action identifier, expected state change, observed evidence, outcome (`confirmed`, `failed`, or `unknown`), and next check. A screenshot is evidence of one moment; it should have a timestamp or step ID so a later agent cannot mistake it for the live screen. A tool result or screenshot after a click can support a transition, but neither a model's plan nor the click request alone proves the effect.

For example, an agent filling a spreadsheet might record `row 18 amount = 42.10, verified in screenshot 81` and `row 19 pending`. It can drop most earlier near-identical frames while retaining the last few for spatial continuity. If a later frame contradicts the ledger, the agent must inspect and reconcile rather than blindly trusting either. [[agent-memory]] covers general storage and retrieval; the observation ledger is narrower: it is the task-specific account of actions and current progress. [[agent-verification-loop]] decides when evidence is sufficient to commit a state transition or when to replan.

## One example

A desktop agent records a verified spreadsheet cell value and a pending next row; after compressing screenshots it can still resume from that evidence.

## Check your understanding

**Question:** Why is an attempted click insufficient as a completed ledger entry?

**Answer:** Because the action may not have changed the screen; a later observation must confirm its effect.
