---
id: mcp-apps
title: MCP Apps
summary: MCP Apps pair a tool with an interactive UI resource that an MCP host renders in an isolated conversation frame, while tool execution and permissions remain host-controlled.
type: concept
tags: [ml/agents]
prereqs: [model-context-protocol, tool-call-execution-contract]
sources: [https://modelcontextprotocol.io/extensions/apps/overview]
status: explained
created: 2026-10-04
updated: 2026-10-04
---

# MCP Apps

## Summary

An **MCP App** extends [[model-context-protocol]] by adding an interactive view to a tool result inside an MCP host. It is not simply an MCP tool that returns HTML: the tool declares a UI resource, the host loads that resource, and the view communicates with the host through a constrained message channel.

## Grounded explanation

A tool description can point to a `ui://` resource through `_meta.ui.resourceUri`. After a tool call, the host fetches the resource and can render it in a sandboxed frame. The host and view exchange defined messages for data, user interaction, and requests to call tools. The application can show a form or chart in the conversation, but the view does not gain ambient authority to call arbitrary server tools. A request to act still crosses the host's [[tool-call-execution-contract]]: tool name and arguments are validated, permissions are checked, and the result is returned through the host.

For example, a travel-search tool may return results plus a view of hotel cards. Selecting a card changes view state; making a reservation is a separate tool request that needs the user's authorization and a verified result. The view's displayed selection is not evidence that a booking succeeded. Hosts may restrict view permissions and external resource origins, so compatibility and security depend on the host implementation as well as the server.

Use an MCP App when direct manipulation of structured results materially helps the user. A plain tool response is simpler for a short answer; a standalone web app may be better when conversation context is irrelevant. Test the same task across the intended hosts, including view loading, state synchronization, denied permissions, malformed messages, tool failures, and user consent. The MCP Apps interface does not establish a product's adoption or commercial outcome.

## Prerequisites

- [[model-context-protocol]]
- [[tool-call-execution-contract]]

## Sources

- [MCP Apps overview](https://modelcontextprotocol.io/extensions/apps/overview): UI resource declaration, host rendering, messaging, and isolation model.
