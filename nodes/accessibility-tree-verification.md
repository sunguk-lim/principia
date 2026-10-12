---
id: accessibility-tree-verification
title: Accessibility-Tree Verification
summary: Accessibility-tree verification checks the roles, names, states, and structure exposed to assistive technologies, complementing but not replacing rendered-pixel and interaction checks.
type: concept
tags: [software/testing]
prereqs: [browser-based-ui-verification, reactive-user-interface]
sources: [https://playwright.dev/docs/aria-snapshots, https://playwright.dev/docs/locators]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Accessibility-Tree Verification

## Summary

An accessibility tree exposes semantic roles, accessible names, and states that a browser computes for assistive technologies. **Accessibility-tree verification** checks that a control has the meaning and state users need, not just a matching CSS selector.

## Grounded explanation

A [[reactive-user-interface]] may render a button that looks correct yet has no accessible name, or a validation message that is visible but not connected to its input. A [[browser-based-ui-verification]] test can locate elements by role and name, inspect enabled or disabled state, and compare an ARIA snapshot of a relevant region. Such assertions are closer to the user-facing contract than brittle DOM-class selectors. They also help a text-only agent understand interface structure without sending pixels to a vision model.

The tree is not a screenshot. It cannot establish color contrast, clipping, overlap, spatial alignment, focus-ring visibility, or whether an animation hides content. Nor does a plausible tree prove that keyboard navigation or screen-reader behavior is correct. The browser's computed semantics can vary with markup and browser version, so snapshots should be scoped to meaningful regions and reviewed when they change.

Test roles and names for key controls, error announcements, focus transitions, and keyboard operation. Pair semantic checks with rendered visibility, actual interaction, and visual inspection for layout defects. A failing snapshot is evidence of a semantic change, not automatically a defect; assess it against the intended accessible behavior.

## Prerequisites

- [[browser-based-ui-verification]]
- [[reactive-user-interface]]

## Sources

- [Playwright ARIA snapshots](https://playwright.dev/docs/aria-snapshots): documents semantic tree snapshot assertions.
- [Playwright locators](https://playwright.dev/docs/locators): documents role- and accessible-name-based locators.
