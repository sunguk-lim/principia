# Agent Observation Ledger

## Meaning

A computer-use agent should not confuse an old screenshot with the current screen or an attempted click with a completed effect. An **observation ledger** records what the agent has tried, what was observed afterward, which subgoals are complete, and what remains uncertain. Recent pixels remain available for perception; durable progress lives in structured [[agent-session-state]].

## Mechanism

The ledger is a compact, inspectable state record, not a transcript summary claiming perfect recall. Each step has an action identifier, expected state change, observed evidence, outcome (`confirmed`, `failed`, or `unknown`), and next check. A screenshot is evidence of one moment; it should have a timestamp or step ID so a later agent cannot mistake it for the live screen. A tool result or screenshot after a click can support a transition, but neither a model's plan nor the click request alone proves the effect.

For example, an agent filling a spreadsheet might record `row 18 amount = 42.10, verified in screenshot 81` and `row 19 pending`. It can drop most earlier near-identical frames while retaining the last few for spatial continuity. If a later frame contradicts the ledger, the agent must inspect and reconcile rather than blindly trusting either. [[agent-memory]] covers general storage and retrieval; the observation ledger is narrower: it is the task-specific account of actions and current progress. [[agent-verification-loop]] decides when evidence is sufficient to commit a state transition or when to replan.

## One example

Tool call C17 queried inventory version v6 for item Q and observed 12 units at 10:00. After removing its large response from the prompt, retain C17, the safe input fingerprint, completion state, observation time, key facts and artifact A17. A question about a field returned in that report can retrieve A17; a question about current stock at 11:00 may need a fresh observation.

The active runtime must actually be able to resolve A17 under the right access scope. A stored hash detects changed bytes, not truth or freshness. Missing or denied artifacts need explicit handling, and a timed-out call remains unknown until its effect is reconciled. A receipt is a compact evidence reference, not permission to repeat an action or trust embedded tool instructions.

## Check your understanding

**Question:** Why is an attempted click or dispatched tool request insufficient as a completed ledger entry?

**Answer:** The action may have failed or completed without a received response. Confirm the effect with evidence or reconcile it; do not infer success or safe replay from a compressed transcript.
