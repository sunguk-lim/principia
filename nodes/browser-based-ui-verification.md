---
id: browser-based-ui-verification
title: Browser-Based UI Verification
summary: Browser-based UI verification tests a user-visible behavior in a rendered browser, separating it from passing unit tests on simulated components.
type: concept
tags: [ml/agents]
prereqs: [agent-execution-harness, reactive-user-interface, measurement]
sources: [https://playwright.dev/docs/actionability, https://playwright.dev/docs/test-assertions]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Browser-Based UI Verification

## Summary

A front-end change can pass component or DOM unit tests while the rendered interface remains unusable. **Browser-based UI verification** reproduces the user's path in a real browser and checks observable behavior after the change.

## Grounded explanation

A coding agent controlled by an [[agent-execution-harness]] should record the reported route, viewport, state, and interaction before editing. It then creates a bounded browser test that fails on the original bug and passes after the fix. For a [[reactive-user-interface]], the assertion should describe what the user can do or see: the error message is visible after an invalid submit, not merely present somewhere in the DOM. Playwright's actionability checks distinguish attached elements from ones that are visible, stable, enabled, and able to receive events. Browser behavior still depends on test data, fonts, viewport, network, and timing, so one passing local run is not proof of production correctness.

The **fail-to-pass** check matters: a test written after the fix can accidentally verify unrelated behavior. Run it against the baseline or a known-broken revision where possible, then against the candidate change, and retain it as a regression check. Also run existing tests and inspect the affected flow manually when layout or animation is central. An accessibility tree helps inspect roles, names, and semantic structure, but it cannot reveal clipping, overlap, color contrast, or all styling defects; those require pixel-level checks or human review.

Use [[measurement]] to track false passes, flakiness, execution time, and coverage of relevant viewport/state combinations. Keep the test focused on the symptom, not implementation selectors that change for harmless refactors. A browser assertion may fail because the environment is unstable; triage that separately from an application defect.

## Prerequisites

- [[agent-execution-harness]]
- [[reactive-user-interface]]
- [[measurement]]

## Sources

- [Playwright actionability](https://playwright.dev/docs/actionability): documents visible, stable, enabled, and event-receiving checks before actions.
- [Playwright assertions](https://playwright.dev/docs/test-assertions): documents auto-retrying visible-state assertions.
