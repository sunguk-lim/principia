# Accessibility-Tree Verification

## Meaning

Accessibility-tree verification checks what meaning a browser exposes for controls and content: roles, names, states, and structure. It complements checks of what a page looks like.

## Mechanism

In [[browser-based-ui-verification]], locate a button by role and accessible name instead of only a CSS class. Inspect whether it is enabled, then use a scoped semantic snapshot for a form or dialog. A [[reactive-user-interface]] can change those semantics as state changes, so test the state after the user's action.

## One example

A submit button appears visually correct but has no accessible name. A screenshot may not reveal the problem, while a role/name assertion fails. Conversely, a named button may still be hidden behind an overlay; a pixel or interaction check is also required.

## Check your understanding

**Question:** Can a correct accessibility tree prove the layout is usable? **Answer:** No. It does not show clipping, overlap, contrast, or spatial position; pair it with rendered and interaction checks.
