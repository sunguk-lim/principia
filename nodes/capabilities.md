---
id: capabilities
title: Capabilities
summary: Capabilities are how Linux breaks the historically all-or-nothing power of the superuser — the special user, named root and numbered user id 0, that the kernel traditionally let…
type: concept
tags: [os/virtualization]
prereqs: [process]
sources:
  - linux-internals-complete.html ("Security layers — defense in depth", "Combining them = a container", "What Docker actually does")
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Capabilities

## Summary

**Capabilities** are how Linux breaks the historically all-or-nothing power of the
superuser — the special user, named **root** and numbered **user id 0**, that the kernel
traditionally let do *anything* — into roughly **forty independent privilege bits**, each
one guarding a single class of privileged operation. A [[process]] no longer simply "is or
is not root"; instead it carries a **set** of these bits, and before allowing a privileged
action the kernel checks the *one specific capability* that governs that action rather than
asking "are you the superuser?". The point is **least privilege**: give a [[process]] only
the precise powers its job requires and withhold all the rest, so that if the [[process]]
is hijacked, the attacker inherits only those few powers — not the keys to the whole
machine. This is why containers, when they start a [[process]], deliberately **drop**
almost every capability.

## Grounded explanation

### The problem: "root" is one switch, and it's all the way on

Recall from [[process]] that the kernel records, in each process's table slot, *the
identity it runs as* — which user. Among users, one is special: the **superuser**,
conventionally named **root** and assigned the numeric user id **0**. Historically the
kernel's privilege check was brutally simple. For any sensitive operation it asked a single
yes/no question: *is this process's user id 0?* If yes, the operation was allowed —
*whatever* it was. If no, it was usually refused.

That design makes "privileged" a single switch with only two positions, fully off or fully
on. A process that needs *one* privileged power must be run as root to get it — and in
getting that one power it silently receives *every* power: it can also reboot the machine,
overwrite any file on disk, load code straight into the kernel, kill any other process, and
read any user's data. There is no way to say "you may do *this* one privileged thing and
nothing else." The grant is all-or-nothing.

This is dangerous for a reason that matters most when things go wrong. If such an
all-powerful process is compromised — say a flaw lets an attacker make it run their
instructions — the attacker now holds *all* of root's power at once. The "blast radius" (the
damage a single compromise can cause) is the entire system. The whole point of capabilities
is to shrink that blast radius.

### The mechanism: split the one power into many independent bits

Capabilities **split root's single power into about forty fine-grained bits**. Each bit is
a named, independent permission for one *class* of privileged operation. The names follow a
`CAP_` convention, and a handful make the idea concrete:

- **`CAP_NET_BIND_SERVICE`** — permission to bind a network port below 1024. (A *port* is a
  number that labels one of a machine's network endpoints; the low-numbered ports, under
  1024, are reserved for system services and were classically restricted to root.)
- **`CAP_NET_RAW`** — permission to open *raw* network sockets, the low-level kind that send
  hand-crafted packets rather than ordinary connections.
- **`CAP_CHOWN`** — permission to change which user *owns* a file.
- **`CAP_KILL`** — permission to send a termination signal to a [[process]] you do not own.
- **`CAP_SYS_ADMIN`** — a deliberately broad bit covering many heavyweight administrative
  operations, such as mounting filesystems.

These bits are **independent**: holding one says nothing about holding any other. A
[[process]] therefore no longer carries the single fact "I am root / I am not root"; it
carries a **set of capabilities** — the subset of those forty bits it currently holds,
recorded by the kernel alongside the rest of that process's bookkeeping in its table slot.
"Being root" is recovered as the *degenerate* case of holding the *whole* set; the new,
useful cases are all the proper subsets in between, which the old switch could not express.

The check changes to match. Where the kernel once asked "is your user id 0?", it now, for
each privileged action, looks up *the one capability that governs that action* and asks
only "does this process's capability set contain *that* bit?" Binding port 80 consults
`CAP_NET_BIND_SERVICE`; sending a signal to someone else's [[process]] consults `CAP_KILL`;
changing a file's owner consults `CAP_CHOWN`. A [[process]] missing the relevant bit is
refused that specific action *even though it may hold many others* — and a [[process]]
holding that bit is allowed it *even if it holds no others*. The power has gone from one
coarse switch to forty fine ones, each independently positioned.

### The why: least privilege and defense in depth

The justification is a security principle called **least privilege**: a [[process]] should
be granted only the powers its task actually requires, and nothing more. Capabilities are
the *machinery* that finally lets the system express least privilege for privileged
operations — before them, "needs one privileged power" forced "gets all of them," so least
privilege was simply unstatable.

Why does narrowing the grant help? Because of the blast-radius argument above, now run in
reverse. The powers a [[process]] *does not hold* are powers an attacker who hijacks it
*cannot use*. Strip a [[process]] down to the single capability it needs, and a successful
compromise yields the attacker exactly that single power — not the ability to reboot the
host, rewrite arbitrary files, or load kernel code. The damage is bounded by the size of the
capability set, so a small set means a small disaster.

This is the heart of **defense in depth** — the practice of stacking several independent
restrictions so that getting past one still leaves the attacker stopped by the next. Even a
[[process]] that the kernel still considers user id 0 (root) can be rendered nearly harmless
if its capability set has been emptied: it carries the *name* of the superuser but almost
none of the superuser's *powers*. Capabilities are one such layer. (Other layers exist
alongside them — filters that block whole categories of kernel requests, mechanisms that
narrow what a [[process]] can even see or use — and they reinforce capabilities without
replacing them; those are separate topics. The capability layer's specific job is: *can't
use most root powers.*)

This is also exactly why containers lean on capabilities. A *container* — a way of running a
[[process]] under heavy isolation, treated elsewhere — is started by, among other steps,
**dropping** almost all of its capabilities right before the program begins. A container's
main [[process]] commonly still runs as user id 0 *inside* the container, yet without
`CAP_SYS_ADMIN`, `CAP_NET_RAW`, and the rest, it cannot do much harm: it is root in name
with its powers confiscated.

### Worked instance: a web server that must bind port 80

Take a concrete [[process]]: a web server whose only privileged need is to bind **port
80**, a port below 1024 and therefore traditionally restricted to root.

The old way forced an all-or-nothing grant. To let it bind port 80 you ran the whole
[[process]] as root (user id 0). That single requirement dragged in *every* root power.
Now suppose the server has a flaw and an attacker takes it over. Because the [[process]] was
full root, the attacker can do far more than touch port 80: they can `CAP_CHOWN` any file to
themselves, `CAP_KILL` other users' processes, mount filesystems via `CAP_SYS_ADMIN`, even
load code into the kernel. One bug, total compromise.

The capability way grants exactly the one bit the job needs. You give the server
**`CAP_NET_BIND_SERVICE`** — and **drop everything else**. Its capability set is now a single
element. When it asks to bind port 80, the kernel checks `CAP_NET_BIND_SERVICE`, finds it,
and allows it; the server runs normally. Now replay the compromise. The attacker holds the
server's set, which is *only* `CAP_NET_BIND_SERVICE`. They try to change a file's owner — the
kernel consults `CAP_CHOWN`, finds it absent, and refuses. They try to load a kernel module —
the governing bit is absent, refused. They try to mount a filesystem — `CAP_SYS_ADMIN` is
absent, refused. The single power they inherited, binding a low port, is nearly useless for
escalating; the blast radius has collapsed from "the whole machine" to "one privileged
action."

To see that the bit is genuinely *specific*, contrast a different program with a different
single need: the `ping` utility, which must craft low-level network packets, needs only
**`CAP_NET_RAW`** — and *not* `CAP_NET_BIND_SERVICE`. Two programs, two different single-bit
sets, each holding precisely the one capability its task demands and no other. That is least
privilege made expressible, which is the whole contribution of capabilities.

## Prerequisites

- [[process]]

## Sources

- `linux-internals-complete.html` — sections "Security layers — defense in depth" (Linux
  splits root's power into ~40 fine-grained bits; a process may run as UID 0 inside a
  container yet be harmless without `CAP_SYS_ADMIN`, `CAP_NET_RAW`, etc.; the four-layer
  defense-in-depth stack with capabilities as "can't use most root powers"), "Combining
  them = a container", and "What Docker actually does" (a container's startup *drops
  capabilities* right before `exec`).
