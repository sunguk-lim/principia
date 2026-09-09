---
id: read-eval-print-loop
title: Read–Eval–Print Loop
summary: A read–eval–print loop repeatedly accepts an interactive program fragment, evaluates it in persistent session state, displays its result, and prompts again.
type: concept
tags: [languages/runtime]
prereqs: [interpreter]
sources: [https://docs.python.org/3/tutorial/interpreter.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Read–Eval–Print Loop

## Summary

A **read–eval–print loop** (REPL) is an interactive mode of an [[interpreter]]: read one input unit, evaluate it in the current environment, print a representation of the result, and repeat.

## Grounded explanation

Python enters interactive mode when standard input is connected to a terminal. It displays a primary prompt for a new statement and a secondary prompt while a multiline construct remains incomplete. Names and imports persist for the session, making the REPL useful for exploration and diagnosis.

Interactive convenience is not reproducibility. Session state depends on execution order; redefinition can hide stale objects; sensitive values may enter history; and code pasted from an untrusted source executes with the interpreter's permissions. Move durable work into files, tests, and version control, and restart from a clean environment to confirm an explanation.

Enhanced shells may add completion, suggestions, history search, syntax highlighting, paste handling, or rewind-like features. These improve ergonomics but do not change Python semantics, and they enlarge the extension and configuration trust surface. Treat productivity claims as workload-specific.

Test interactive tools with multiline input, exceptions, user interruption, Unicode, terminal resize, history permissions, completion side effects, startup configuration, virtual environments, and clean exit. Distinguish evaluation output from explicit program output and verify that examples also run as scripts when that is the intended deployment form.

## Prerequisites

- [[interpreter]]

## Sources

- [Python Tutorial, “Using the Python Interpreter”](https://docs.python.org/3/tutorial/interpreter.html): documents terminal-connected interactive mode, prompts, multiline input, history and completion, scripts, and command-line invocation.
