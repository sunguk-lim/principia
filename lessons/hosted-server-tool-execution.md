# Hosted Server-Tool Execution

## Meaning

A user-defined tool returns a proposed call for the client application to execute. A **hosted server tool** instead runs at the model gateway during the request. That convenience changes who controls the runtime, network, credentials, logs, and charges.

## Mechanism

The model can request a tool, but a [[tool-call-execution-contract]] still needs a predeclared allowed tool set and bounded arguments. The gateway executes the call and returns a result to the model, so the client may see only the final response unless it asks for trace or tool events. For a shell tool, a [[sandboxed-code-execution]] boundary may isolate processes, but isolation quality depends on filesystem mounts, network policy, resource caps, lifetime, and provider operations. A hosted container is not a permission grant to run arbitrary effects on the user's systems.

Compare this with application-owned execution. Hosting can reduce client orchestration and latency, while reducing direct visibility and control. It may also create a distinct data jurisdiction from the model endpoint. Disable tools that are not needed, scope any attached resources narrowly, and treat tool output as untrusted input on the model's next step. Record tool identity, request ID, arguments within privacy limits, exit status, time, cost, and failure reason.

## Worked example

A model requests a hosted shell command to summarize local files. The gateway may run the command in its own sandbox, but the client still needs to know which files were mounted, whether networking was allowed, how output was limited, and where the execution was logged. The same tool name is not equivalent to an application-owned sandbox.

**Understanding check:** Who enforces the filesystem and network boundary for a provider-hosted tool?
