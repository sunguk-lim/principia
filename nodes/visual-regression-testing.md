---
id: visual-regression-testing
title: Visual Regression Testing
summary: Visual regression testing compares controlled rendered images to reveal layout and styling changes that semantic assertions may miss.
type: concept
tags: [software/testing]
prereqs: [browser-based-ui-verification, measurement]
sources: [https://playwright.dev/docs/test-snapshots]
status: explained
created: 2026-10-13
updated: 2026-10-13
---

# Visual Regression Testing

## Summary

**Visual regression testing** captures a rendered UI state and compares it with an approved reference image. It can reveal clipping, overlap, spacing, font, or styling changes that semantic browser assertions do not express.

## Grounded explanation

First use [[browser-based-ui-verification]] to reach a reproducible state. Fix the viewport, device scale, fonts, test data, animations, and network responses as much as possible; then capture a screenshot. A comparison tool reports changed pixels or regions against a reference. The expected image is a reviewed baseline, not automatically the last output. If it is blindly updated after every change, the test loses its power to detect regressions.

A pixel difference is evidence of a visual change, not proof of a defect. Browser engines, font rendering, antialiasing, asynchronous content, and legitimate design updates can produce differences. Thresholds and masked dynamic regions reduce noise but can also hide real bugs. A model-based visual judge may prioritize suspicious regions, yet its judgment is nondeterministic and should not be the only release gate for consequential visual behavior.

With [[measurement]], track both missed defects and false alarms. Review representative viewport sizes and interaction states, not one desktop screenshot. Pair image comparison with semantic assertions for keyboard use, roles, labels, and interactions; a screenshot can look correct while the UI remains inaccessible or inert.

## Prerequisites

- [[browser-based-ui-verification]]
- [[measurement]]

## Sources

- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots): documents screenshot expectations, baseline files, and rendering-environment variation.
