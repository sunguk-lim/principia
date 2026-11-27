---
id: scenario-based-agent-testing
title: "Scenario-Based Agent Testing"
summary: "Scenario-based agent testing executes bounded interactive fixtures against a versioned agent and checks both its conversation and resulting environment state."
type: concept
tags: [ml/evaluation]
prereqs: [agent-simulation-fidelity, llm-as-a-judge]
sources: [https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents, https://arxiv.org/abs/2406.12045]
status: explained
created: 2026-11-28
updated: 2026-11-28
---

# Scenario-Based Agent Testing

## Meaning

A scenario test is a repeatable interactive experiment: an initial environment, user goal, permitted actions, bounded conversation and independently specified outcome. Unlike an exact-response assertion, it can accept several valid phrasings or action sequences. Unlike an unconstrained demonstration, it has a failure oracle and a reproducible configuration.

## Mechanism

Separate the agent under test, the user driver and the graders. A user driver may replay a transcript or react to the agent according to a controlled persona. [[agent-simulation-fidelity]] concerns whether those users, tools and state transitions reproduce the properties being tested. An adapter can expose a common call interface without changing the deployed agent's decision policy; it must also preserve relevant state, errors and tool contracts.

Grade deterministic properties directly: required inputs, authorized calls, final records, duplicate side effects, deadlines and budgets. Use [[llm-as-a-judge]] for interpretation-heavy rubric dimensions only after calibration. A judge's declaration is not evidence that a database changed, nor is fluent dialogue sufficient for a pass. Keep transcript-level behavior and final-state assertions separate so a plausible claim cannot substitute for the expected effect.

## One example

A fictional itinerary test starts with a user asking for a three-day trip and a budget but no destination. The reactive driver reveals a destination only if asked. The acceptance rules require a destination before a concrete destination-specific itinerary, no booking side effects, and a plan consistent with the supplied budget. A second fixture supplies the destination initially; an agent that asks again unnecessarily should lose that dimension even if it passes the missing-input fixture.

Record the initial state and configuration afresh for each trial. Run several trials because model behavior can vary; preserve success and failure denominators. Resetting only the chat while reusing a mutated database changes the experiment.

## Boundaries and validation

Version the agent, tool implementation, simulator, rubric, prompt set and budgets. Keep critical assertions outside the repair agent's control. Maintain held-out scenario families and legitimate-action controls; a system that refuses every task should not earn a perfect safety score. Inspect judge disagreement, tool failures, timeouts and stale state separately rather than collapsing them into one success percentage.

A conventional test runner can orchestrate these fixtures, but runner success means only that its assertions passed. It does not establish production robustness beyond the modeled users and effects.

## Prerequisites

- [[agent-simulation-fidelity]]
- [[llm-as-a-judge]]

## Sources

- <https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>
- <https://arxiv.org/abs/2406.12045>
