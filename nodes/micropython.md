---
id: micropython
title: MicroPython
summary: MicroPython is a compact Python implementation for microcontrollers that makes RAM, flash storage, and port-specific capabilities part of ordinary program design.
type: concept
tags: [languages/runtime]
prereqs: []
sources: [https://docs.micropython.org/en/latest/reference/constrained.html, https://docs.micropython.org/en/latest/reference/manifest.html]
status: explained
created: 2026-09-11
updated: 2026-09-11
---

# MicroPython

## Summary

**MicroPython** is an implementation of Python for microcontrollers and other constrained systems. Unlike desktop Python, its usable program design is directly constrained by the device's RAM, flash storage, hardware port, and supported modules.

## Grounded explanation

MicroPython runs on a variety of microcontroller architectures, where RAM and nonvolatile flash storage are limited. Importing a module compiles it to bytecode and executes it in the MicroPython virtual machine; the bytecode occupies RAM. Code that creates many global objects at import time therefore reduces the memory available to compile later imports.

For a memory-constrained application, first separate imports from initialization, avoid repeated allocation and destruction of temporary objects, and measure memory use on the target port. This is not merely a performance optimization: heap fragmentation and an import-time memory exception can prevent a program from starting at all.

MicroPython can also freeze Python modules or precompiled bytecode into firmware. Frozen bytecode may execute directly from flash rather than being copied into RAM, and immutable constant objects can remain in flash. The trade-off is a slower edit-test cycle because changing frozen code requires rebuilding and reflashing firmware. Use freezing for stable code or devices without a filesystem; leave rapidly changing application code in the filesystem while iterating.

**Worked decision.** A sensor controller that imports several libraries and then fails with a memory exception should not immediately be rewritten in C. First delay global initialization, precompile or freeze stable modules, and confirm the target port's available RAM. If the remaining memory or hardware API support is still inadequate, then move the constrained section to a port-specific native module or redesign the workload.

## Prerequisites

None.

## Sources

- [MicroPython on microcontrollers](https://docs.micropython.org/en/latest/reference/constrained.html): documents RAM and flash constraints, import-time compilation, heap fragmentation, precompiled modules, and frozen bytecode.
- [MicroPython manifest files](https://docs.micropython.org/en/latest/reference/manifest.html): documents frozen code, ROM execution, memory benefits, and the firmware-reflash trade-off.
