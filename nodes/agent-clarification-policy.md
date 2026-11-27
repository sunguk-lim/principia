---
id: agent-clarification-policy
title: "Agent Clarification Policy"
summary: "An agent clarification policy requests missing decision-relevant information when acting on an assumption would materially change the permitted or useful outcome."
type: concept
tags: [ml/agents]
prereqs: [task-underspecification, tool-call-execution-contract, measurement]
sources: [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Agent Clarification Policy

## Meaning

A clarification policy determines when an agent should ask for missing information, proceed with an explicit default, or stop because it cannot safely choose. Its objective is a useful correct decision with appropriate user burden—not the maximum number of questions or the fewest turns.

## Mechanism

[[task-underspecification]] identifies outcome-relevant choices the brief leaves open. Identify which inputs are necessary for the next consequential decision. Separate absent values from conflicting values and from information that can already be retrieved within the task's permitted scope. Consider whether plausible answers would change the outcome. If all acceptable answers support the same reversible next step, a question may not be necessary yet. If the alternatives change the target, permission or effect, obtain the information before that action.

The [[tool-call-execution-contract]] still controls external effects: asking a question does not grant authority, and a model's guessed answer is not approval. A safe read or reversible draft may proceed while a question is outstanding, but an action depending on the missing input must wait. State a chosen default when it matters; silently inventing a required fact is not clarification.

## One example

For an invented request, “Plan three days away for 600 units,” the destination is missing. The agent can outline budget categories without inventing a city, then ask for a destination before presenting destination-specific travel times. If the request already says “three days in Bergen,” asking for the city repeats supplied information and adds cost without reducing uncertainty. If the next request is to purchase a ticket, destination, traveler and authorization requirements must be resolved separately; a planning answer is not purchase consent.

## Validation and boundaries

Use [[measurement]] on paired fixtures: missing critical fields, fully specified inputs, contradictory fields, safe defaults and unanswerable questions. Score task correctness, unnecessary questions, ignored answers, completion turns and premature effects. An independent rubric and explicit tool-state assertions are complementary. The evaluation reference motivates testing behavior and outcomes; this decision procedure and toy travel example are an independent design synthesis, not a claimed vendor policy.

A clarification policy cannot determine every user's preferences from context. When several valid options remain, the relevant question is which information would change the next decision enough to justify asking. Do not use an arbitrary timeout as evidence of an answer.

**Check:** Should an agent ask every missing optional preference before doing a read-only search? Not necessarily. It can often gather useful permitted evidence first, then ask only about the unresolved choice.

## Prerequisites

- [[task-underspecification]]
- [[tool-call-execution-contract]]
- [[measurement]]

## Sources

- <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
