# Visual Regression Testing

## Meaning

A visual regression test compares a screenshot of a controlled page state with an approved reference. It helps catch layout and style changes that an assertion about text or DOM structure might miss.

## Mechanism

Use [[browser-based-ui-verification]] to reach the same route, viewport, data, and interaction state each time. Capture an image and compare it with a reviewed baseline. [[measurement]] should include false alarms and missed defects, because pixel differences do not automatically mean a user-visible problem.

## One example

A form's error message still exists and has the right text, but a CSS change moves it behind a modal. A screenshot comparison flags that region. A reviewer confirms the defect; a semantic visibility assertion can then make the regression check more specific.

## Check your understanding

**Question:** Why not auto-accept every new screenshot? **Answer:** That would make the baseline follow regressions and remove the test's independent reference.
