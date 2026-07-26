---
id: kernel-module
title: Kernel Module
summary: A kernel module is a chunk of kernel code, packaged as a single file (by convention ending in .ko, for kernel object), that can be loaded into the already-running kernel at…
type: concept
tags: [os/kernel]
prereqs: [kernel]
sources:
  - "Linux internals study guide (etc/linux-internals-complete.html) — 'The one nuance — modules loaded later', 'Why kernel module bugs are catastrophic', 'The single sentence to remember' (§2, the kernel section), and the 'What are kernel modules?' Q&A"
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Kernel Module

## Summary

A **kernel module** is a chunk of [[kernel]] code, packaged as a single file (by
convention ending in `.ko`, for *kernel object*), that can be loaded **into the already-running
[[kernel]] at runtime** and unloaded again **without rebooting the machine**. You add one with a
loader command (`insmod` loads a file directly; `modprobe` looks the module up by name and loads
it together with anything it depends on) and remove one with `rmmod`. Most device drivers and many
filesystems ship this way rather than being built permanently into the [[kernel]]. The reason
modules exist is economy: the core [[kernel]] can stay small and boot fast, each machine loads only
the drivers its own hardware needs, and a single driver can be replaced by loading a new module
instead of rebuilding and rebooting the whole [[kernel]]. The one property that makes a module
fundamentally different from an ordinary program — and the heart of this node — is that **once
loaded, the module runs inside the [[kernel]]'s own address space at full hardware privilege; it
is not a separate, isolated process**. So a bug in a module is a bug *in the [[kernel]] itself*: it
can corrupt [[kernel]] memory and bring down the entire system, where the same bug in an ordinary
program would only crash that one program.

## Grounded explanation

### What the concept *is*: code grafted into the running kernel

Recall from [[kernel]] what the [[kernel]] is, physically. It is **one program with one address
space** — a single region of memory holding one set of code and data, all running at full hardware
privilege (the unrestricted CPU mode that ordinary programs are locked out of). At boot the
[[kernel]] is loaded once from its binary file and stays resident for the life of the machine. Its
internal parts — the scheduler, the memory manager, the filesystem code, the device drivers — are
not separate programs in separate places; after boot they sit in one continuous block of memory,
share each other's data structures, and call one another's functions directly. They are organized
into *roles*, not walled off into *compartments*.

A **kernel module** is how that single program is **extended after it is already running**. It is a
self-contained piece of [[kernel]] code — a body of functions plus their data — built into a file
(the `.ko` file). At any time after boot you can tell the [[kernel]] to take that file and weave its
code into itself. The verbs are concrete:

- **Load** — `insmod some.ko` (or `modprobe some`, which finds the right file by a short name and
  loads its dependencies too) hands the file to the [[kernel]], which places the module's code into
  memory and splices it in.
- **Unload** — `rmmod some` tells the [[kernel]] to detach that module's code and reclaim its
  memory.

Neither step reboots the machine. The [[kernel]] keeps running throughout; the module is grafted on
or pruned off underneath everything else.

The crucial word is *grafted*. A module does **not** become a new process — a separate program with
its own private slice of memory, kept at arm's length by the [[kernel]]. The [[kernel]] places the
module's code into a region of memory that is **part of the [[kernel]]'s own address space**, and
then **patches its internal function tables** so that, from that moment on, a call into the module's
code is indistinguishable from a call into the built-in scheduler. The module's functions run in the
same unrestricted CPU mode as the rest of the [[kernel]] and may touch any byte of [[kernel]] memory
and any device register. The boundary that separates an ordinary program from the [[kernel]] simply
does not exist around a module: **once loaded, the module *is* the [[kernel]].**

A useful picture: the running [[kernel]] is a building, and loading a module is building an annex
joined to it by an enclosed walkway. Physically the annex sits on a different patch of ground — and
indeed a module's code lands in a *different* region of memory than the original boot binary, with a
gap between them. But functionally the annex is part of the same building: people pass between the
two without ever stepping outside. Same address space, same privileges, same identity.

### The WHY: why graft code in at runtime instead of building it all in?

If everything a module does could simply be compiled permanently into the [[kernel]], why bother
with a separate loadable file at all? Three reasons, all flowing from the fact that a real machine
runs only a *small subset* of all the hardware and features the [[kernel]] knows how to support.

1. **Keep the core small and the boot fast.** The set of all drivers and filesystems the [[kernel]]
   can support is enormous — every brand of network card, disk, GPU, filesystem format. If all of it
   were welded into the one resident binary, that binary would be huge and slow to load at boot. By
   shipping most of it as modules, the always-resident core stays lean.
2. **Load only what *this* machine needs.** A given computer has one or two specific network cards,
   not every card ever made. With modules, the [[kernel]] loads only the drivers matching the
   hardware actually present — including automatically: plug in a USB device and the [[kernel]]
   detects it, identifies the matching module, and loads it on the spot.
3. **Replace one piece without rebuilding the whole.** Because a module is an independent file, you
   can fix or upgrade a single driver by unloading the old module and loading a new one — no need to
   recompile the entire [[kernel]] and reboot the machine.

The insight behind all three: the [[kernel]] is *one* program, but it does not have to be *born*
with all its code. Modules let that one program **grow on demand**, pulling in exactly the code a
particular machine needs, exactly when it needs it.

### The cost of that power: why a module bug is catastrophic

The same property that makes modules powerful — that a loaded module runs *as* the [[kernel]], not
*beside* it — is what makes their bugs uniquely dangerous, and this is the point the source dwells
on.

Consider what isolation normally buys an ordinary program. A process runs in the *restricted* CPU
mode and gets only its own private region of memory; the [[kernel]] guarantees it cannot name any
other process's bytes. So when a buggy program follows a **null pointer** — an address (numerically
zero) that points nowhere valid — the CPU traps into the [[kernel]], which sees a process reaching
outside its allowed memory and kills *just that process*. The fault is **contained**: your editor
crashes, nothing else does, because the program was fenced off in the first place.

A module has no such fence. It lives in the [[kernel]]'s address space at full privilege, so the
very same null-pointer bug, executing inside a module, is a stray write or read **into [[kernel]]
memory** with nothing to stop it. There is no outer authority to contain the fault, because the
faulting code *is* the authority. The [[kernel]] cannot safely kill "the module" the way it kills a
process — the module is not a separable thing; its code and the [[kernel]]'s share one address space
and one set of function tables. With its own integrity in doubt, the [[kernel]] does the only safe
thing: it **panics** — halts the entire system — taking down every process on the machine. The same
class of bug that merely segfaults one app brings down the whole computer when it lives in a module,
**precisely because, once loaded, the module is not a separate driver program — it is the
[[kernel]].**

### Worked instance: loading a network-card driver, and one bug in it

Walk one concrete module through its life, then trigger the dangerous case so no part of the
mechanism stays hidden.

Suppose your machine has an Intel gigabit network card whose driver is the module `e1000`.

1. **Load.** You run `modprobe e1000`. `modprobe` resolves the name `e1000` to its `.ko` file, and
   the [[kernel]] reads that file, places the module's code into a fresh region of its own address
   space (separate from the boot binary, but in the *same* address space), and patches its internal
   tables so calls can reach the new code.
2. **Register.** As it loads, the module runs its initialization function, which **registers its
   driver hooks with the [[kernel]]** — it hands the networking subsystem a set of functions: "to
   send a packet on this card, call *this*; when the card raises an interrupt, call *that*." From now
   on the [[kernel]]'s generic "send these bytes" requests get routed straight into the module's
   code, exactly as if those functions had been compiled in at boot.
3. **Serve.** The card starts working. When a packet arrives, the card raises a hardware interrupt;
   the [[kernel]] enters the module's interrupt hook (running at full privilege), which reads the
   card's registers and moves the data along. The module is now doing real work *as part of* the
   [[kernel]].
4. **Unload.** Done with it, you run `rmmod e1000`. The [[kernel]] detaches the module's hooks,
   removes its code, and reclaims that memory — again without a reboot. The networking subsystem
   that remains is back to the size it was before.

Now the contrast that defines the concept. Suppose the `e1000` module has a **null-pointer bug**:
on a certain malformed packet, its interrupt hook dereferences a pointer that is zero. Because that
hook runs **inside the [[kernel]]'s address space at full privilege**, the bad access is loose
inside [[kernel]] memory with nothing to contain it; the [[kernel]] cannot quarantine "the driver"
because the driver is itself, so it **panics and the whole machine goes down**. Had the *identical*
mistake instead lived in an ordinary user program parsing the same packet, the CPU would have
trapped, the [[kernel]] would have killed that one fenced-off process, and everything else would
have kept running. One bug, two outcomes — and the entire difference is that the module had no
boundary between it and the [[kernel]], while the program did. That boundary, present or absent, is
the whole concept of a kernel module.

## Prerequisites

- [[kernel]]

## Sources

- Linux internals study guide (`etc/linux-internals-complete.html`), the kernel section (§2): "The one nuance — modules loaded later" (a loaded `.ko` lands in a different memory region than the boot binary yet shares the same address space; the kernel patches its function tables; the building-annex analogy), "Why kernel module bugs are catastrophic" (once loaded the module *is* the kernel, so a faulty driver can kernel-panic the whole system), "The single sentence to remember" (modules extend the one-address-space program over time without breaking it apart), and the "What are kernel modules?" Q&A (drivers ship as loadable `.ko` files loaded/unloaded at runtime via `insmod`/`rmmod`, so the kernel loads only what it needs, including automatically on device hotplug).
