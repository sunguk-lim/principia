---
id: pytorch-module-call
title: Calling a PyTorch Module
summary: Calling a PyTorch Module with module(inputs) uses the Module call path, which dispatches to forward while preserving framework-managed behavior such as registered hooks.
type: concept
tags: [ml/deep-learning]
prereqs: [neural-network, object-oriented-inheritance]
sources: [https://docs.pytorch.org/docs/2.9/generated/torch.nn.Module.html]
status: explained
created: 2026-09-10
updated: 2026-09-10
---

# Calling a PyTorch Module

## Summary

A PyTorch model is normally evaluated as `module(inputs)`: that call enters the framework's module call path, which then invokes the model's `forward` implementation.

## Grounded explanation

A model built from a [[neural-network]] is often implemented as a class derived from `torch.nn.Module`. That derived-class relationship is an instance of [[object-oriented-inheritance]]: the model supplies its own `forward` method while retaining behavior supplied by the base class.

The public invocation API is `module(inputs)`, not a direct call to `module.forward(inputs)`. `Module`'s call path dispatches to `forward` and is also where PyTorch runs registered forward and backward hooks. Calling `forward` directly can therefore bypass behavior that the module API is designed to preserve.

Implement `forward` to define the model's computation, and call the module object to execute it:

```python
output = model(inputs)
```

This distinction matters when instrumentation, monitoring, or other hooks are attached. A direct `forward` call may appear to produce the same output in a small example, but it is not the complete module invocation contract.

## Prerequisites

- [[neural-network]]
- [[object-oriented-inheritance]]

## Sources

- [PyTorch `torch.nn.Module` documentation](https://docs.pytorch.org/docs/2.9/generated/torch.nn.Module.html): documents `forward`, `__call__`, and the hook behavior preserved by the module call path.
