---
id: model-context-protocol
title: Model Context Protocol
summary: Model Context Protocol is a stateful client-server protocol through which an AI application can discover and invoke server capabilities using JSON-RPC messages.
type: concept
tags: [ml/ai-systems]
prereqs: []
sources: [https://modelcontextprotocol.io/specification/2025-06-18/basic/architecture, https://modelcontextprotocol.io/specification/2025-06-18/server/tools, https://modelcontextprotocol.io/specification/2025-06-18/server/resources, https://modelcontextprotocol.io/specification/2025-06-18/server/prompts]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# Model Context Protocol

## Summary

**Model Context Protocol (MCP)** defines a JSON-RPC protocol between a host application, its client connection, and a server that exposes capabilities. It standardizes the interaction boundary; it does not make a server safe, correct, or automatically compatible with every host feature.

## Grounded explanation

An MCP host creates one or more client connections to servers. During initialization, the peers negotiate protocol version and capabilities. A server advertises only the capabilities it implements, so a client must not assume that every server provides the same operations or that a named capability is available without discovery.

The server specification separates three user-facing capability families. **Tools** are model-controlled actions: a client can list their definitions and invoke one by name with structured arguments. **Resources** are application-controlled context identified by URIs: clients can list, read, and in some cases subscribe to changes. **Prompts** are user-controlled templates: clients can list them, obtain a prompt with arguments, and receive structured messages. The families differ in who selects the interaction and in the shape of their results; a server need not implement all three.

A shared protocol can reduce repeated adapter work when several hosts support the same protocol and a server exposes a stable interface. It does not collapse integration into a guaranteed $M+N$ problem: authentication, authorization, transport, lifecycle management, version support, capability differences, data schemas, and host-specific UI or policy remain integration work.

Treat a tool call as an authority boundary. Before enabling a server, identify its transport endpoint, credentials, data access, side effects, and the host’s approval behavior. Validate tool inputs and returned structured content, scope credentials to the server, and log invocations with enough context to investigate failures. A successful `tools/list` response proves discovery only; it does not prove that a call is safe or that its result is correct.

## Sources

- [Model Context Protocol specification: Architecture](https://modelcontextprotocol.io/specification/2025-06-18/basic/architecture): host, client, server roles, capability negotiation, and protocol layering.
- [Model Context Protocol specification: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools): tool discovery and invocation semantics.
- [Model Context Protocol specification: Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources): URI-identified resources, reading, and subscriptions.
- [Model Context Protocol specification: Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts): prompt discovery and retrieval with arguments.
