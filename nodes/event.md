---
id: event
title: Event
summary: An event is a discrete occurrence identified as having happened at a particular point in time, such as a request arriving or an error being raised; it is the recursion floor from which timestamped log records and span events are built.
type: axiom
tags: [observability/fundamentals]
prereqs: []
sources: [https://opentelemetry.io/docs/concepts/signals/]
status: explained
created: 2026-07-27
updated: 2026-07-27
---

# Event

## Axiom

An **event** is one distinguishable occurrence: something happened, and it can be
placed at a point in time. Examples are “a request arrived,” “a button was
pressed,” and “an exception was raised.” An event is discrete: it either occurred
or it did not. Its identity and time may later be accompanied by a name, severity,
or other fields, but those additions describe the occurrence rather than changing
what an event is.

## Why stop here

This repository treats the ability to distinguish one occurrence from another as a
recursion floor. Observability concepts build richer records from events, but
explaining the primitive idea of “this happened now” would only replace it with
synonyms. The OpenTelemetry signal model likewise treats events as point-in-time
occurrences and models them as a specialized kind of log.

## Sources

- https://opentelemetry.io/docs/concepts/signals/
