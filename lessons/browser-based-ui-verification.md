# Browser-Based UI Verification

## Meaning

Browser-based UI verification checks a front-end fix through the rendered page and the user's actual interaction path. A unit test can prove component logic while missing CSS, layout, overlays, and browser event behavior.

## Mechanism

In an [[agent-execution-harness]], first record the bug's route, inputs, viewport, and expected observation. Write a browser reproduction that fails before the change and passes afterward. A [[reactive-user-interface]] may contain an error node that exists in the DOM but is hidden behind a modal; an assertion about visible state catches more than a query for existence. Playwright's actionability rules help test whether the control can receive an event.

## One example

A form says validation passed in unit tests, but the error is clipped on mobile. The browser test submits an empty field at the mobile viewport and asserts that the error is visible. Verify failure on the old revision, then success after the CSS fix. Keep other regression tests running too.

## Check your understanding

**Question:** Why should the new test fail on the original version? **Answer:** It shows that the test actually reproduces the reported defect instead of checking unrelated behavior.
