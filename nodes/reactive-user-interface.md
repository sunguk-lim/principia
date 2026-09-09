---
id: reactive-user-interface
title: Reactive User Interface
summary: A reactive user interface derives rendered output from declared state and schedules updates when that state changes instead of requiring every event handler to redraw the interface manually.
type: concept
tags: [languages/python]
prereqs: [event, python-descriptor]
sources: [https://textual.textualize.io/guide/reactivity/]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Reactive User Interface

## Summary

A **reactive user interface** associates view output with state. When declared state changes, the framework marks affected views for refresh or layout and batches work rather than requiring imperative redraw calls after each mutation.

## Grounded explanation

Suppose a view is $V=f(S)$ for application state $S$. An input [[event]] changes $S$; the runtime identifies dependent views and schedules $f$ again. This separates state transitions from rendering and can coalesce several changes into one refresh.

Textual applies this pattern to terminal interfaces. Its reactive attributes use the [[python-descriptor]] protocol, can validate or watch assignments, and automatically refresh a widget when a value changes. Multiple modifications can be combined into one refresh. State that should not redraw can be declared separately, while geometry-affecting state can request layout.

Reactivity does not remove state-management problems. Watchers that mutate each other's inputs can form cycles, expensive render functions can block responsiveness, and background tasks can race with view lifetime. Keep render functions deterministic and side-effect-light, give one component ownership of each state transition, cancel obsolete work, and separate content refresh from costly layout.

Test state transitions independently from presentation, then simulate keyboard, mouse, resize, focus, and asynchronous completion events. Check invalid values, repeated assignment, rapid updates, cancellation, terminal-size boundaries, accessibility, and deterministic snapshots. Profile event-to-render latency and refresh count rather than judging only visual appeal.

## Prerequisites

- [[event]]
- [[python-descriptor]]

## Sources

- [Textual documentation, “Reactivity”](https://textual.textualize.io/guide/reactivity/): documents descriptor-backed reactive attributes, automatic refresh, validation and watchers, batching, and layout-triggering state.
