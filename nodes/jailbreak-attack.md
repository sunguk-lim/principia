---
id: jailbreak-attack
title: Jailbreak Attack
summary: A jailbreak attack tries to induce a model to disregard its behavioral safeguards through adversarial prompt content; it is not the same as gaining application authority.
type: concept
tags: [ml/agents]
prereqs: [prompt-injection]
sources: [https://genai.owasp.org/llmrisk/llm01-prompt-injection/]
status: explained
created: 2026-10-17
updated: 2026-10-17
---

# Jailbreak Attack

## Summary

A **jailbreak** is a prompt strategy aimed at bypassing a model's behavioral restrictions. It is related to [[prompt-injection]], but the security question is narrower: did the model produce output it was meant to refuse or constrain? A jailbreak does not by itself confer permission to read a private file, call a privileged tool, or change an external system.

## Grounded explanation

An attacker may use role-play, reframing, multi-step decomposition, or apparent authority to make a prohibited answer seem like an ordinary task. A direct user-supplied jailbreak differs from an indirect instruction embedded in a web page: the latter also crosses a data-to-instruction boundary. Both can fail because the model responds to text patterns rather than a reliable access-control mechanism.

Separate output policy from action authority. A model that emits an unsafe answer has a content-policy failure. A model that requests a privileged action should still be stopped by application validation, regardless of whether its text sounds compliant. Conversely, a blocked tool action does not prove the model's answer remained safe. Training, input/output checks, tool permissions, and monitoring cover different failure paths; no single filter guarantees all of them.

## Validation

Use a documented test set with permitted and prohibited requests, paraphrases, benign lookalikes, and tool-enabled scenarios. Track unsafe completion rate, false refusals, unauthorized action attempts, and actual effects separately. Re-test after model or policy changes and avoid treating success on familiar attack strings as general robustness.

## Prerequisites

- [[prompt-injection]]

## Sources

- [OWASP Gen AI Security Project, Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/): distinguishes jailbreaking from broader prompt-injection behavior.
