---
id: hosted-server-tool-execution
title: Hosted Server-Tool Execution
summary: Hosted server-tool execution delegates model-requested operations to a provider-run environment, shifting execution, isolation, billing, and audit boundaries away from the client application.
type: concept
tags: [ml/agents]
prereqs: [tool-call-execution-contract, sandboxed-code-execution]
sources: [https://openrouter.ai/docs/guides/features/server-tools, https://openrouter.ai/docs/guides/features/server-tools/shell]
status: explained
created: 2026-10-03
updated: 2026-10-03
---

# Hosted Server-Tool Execution

## Summary

A user-defined tool returns a proposed call for the client application to execute. A **hosted server tool** instead runs at the model gateway during the request. That convenience changes who controls the runtime, network, credentials, logs, and charges.

## Grounded explanation

The model can request a tool, but a [[tool-call-execution-contract]] still needs a predeclared allowed tool set and bounded arguments. The gateway executes the call and returns a result to the model, so the client may see only the final response unless it asks for trace or tool events. For a shell tool, a [[sandboxed-code-execution]] boundary may isolate processes, but isolation quality depends on filesystem mounts, network policy, resource caps, lifetime, and provider operations. A hosted container is not a permission grant to run arbitrary effects on the user's systems.

Compare this with application-owned execution. Hosting can reduce client orchestration and latency, while reducing direct visibility and control. It may also create a distinct data jurisdiction from the model endpoint. Disable tools that are not needed, scope any attached resources narrowly, and treat tool output as untrusted input on the model's next step. Record tool identity, request ID, arguments within privacy limits, exit status, time, cost, and failure reason.

Test unauthorized commands, secret access, network egress, timeout, persistent-state assumptions, and retry behavior. Verify whether a failed request can leave an external side effect and whether billing includes tool runtime. A provider's product label such as “sandboxed” should be backed by current documented controls and, for sensitive workloads, independent testing.

## Prerequisites

- [[tool-call-execution-contract]]
- [[sandboxed-code-execution]]

## Sources

- [OpenRouter Server Tools](https://openrouter.ai/docs/guides/features/server-tools): provider-executed versus client-executed tool distinction.
- [OpenRouter Shell tool](https://openrouter.ai/docs/guides/features/server-tools/shell): hosted shell interface and documented constraints.
