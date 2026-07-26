---
id: device-driver
title: Device Driver
summary: A device driver is the piece of kernel code that knows how to talk to one specific piece of hardware.
type: concept
tags: [os/kernel]
prereqs: [kernel, dma, interrupt]
sources:
  - "Linux internals study guide (etc/linux-internals-complete.html) — §2 'Device drivers' (bilingual-interpreter framing; the kernel-defines-an-interface / driver-fills-in function-pointer table; the three device types character/block/network), plus the 'What are kernel modules?', 'Why do drivers run in Ring 0?', and 'How does this connect' Q&A boxes."
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Device Driver

## Summary

A **device driver** is the piece of [[kernel]] code that knows how to talk to one
specific piece of hardware. The [[kernel]] wants to stay *hardware-agnostic*: it would
like to say "read this block of data" the same way to every disk, and "send these bytes"
the same way to every network card, without knowing whether the disk is an old spinning
drive or a new solid-state one. But each real device speaks its own private dialect — a
particular set of *registers* (small control slots inside the hardware that you write
numbers into to command it) and a particular protocol for using them. The driver is the
**bilingual translator** that bridges the two: on one side it speaks the [[kernel]]'s
single uniform internal interface; on the other side it speaks the exact register-pokes
that *this* device understands. It announces itself to the rest of the [[kernel]] by
handing over a set of **function pointers** — slots like "here is my code for *read*,
here is my code for *write*" — so the [[kernel]] can drive any device through the *same*
calls. The single defining idea: a driver lets the [[kernel]] add support for a new piece
of hardware by adding a driver, **not** by changing the [[kernel]]'s core.

## Grounded explanation

### What the concept *is*: a per-device translator the kernel calls through a fixed interface

Recall from [[kernel]] what kind of thing the [[kernel]] is: a resident, privileged body
of code, organized into subsystems, that mediates every program's access to the CPU,
memory, and devices. Among those subsystems is a uniform way of talking about hardware —
the [[kernel]] presents the *same* operations (open, read, write, and so on) no matter
what storage or device sits underneath. That uniformity is exactly the problem a driver
solves. Hardware is *not* uniform. Two disks that store the identical bytes for you may be
commanded in completely different ways: one expects you to write a command into one set of
registers, the other into a different set, with different meanings and a different
hand-shake. A **register**, again, is a tiny addressable control slot physically inside
the device; writing a specific number into it is how software issues an order to the
hardware. The [[kernel]] core does not want to learn every device's register layout —
there are thousands of devices, and new ones appear constantly.

So the work is split. The [[kernel]] **defines an interface**: a named list of operations
that any device of a given kind *must* be able to perform. For a disk, for instance, that
list is essentially "read a block," "write a block," "flush pending writes." A **device
driver** is a chunk of [[kernel]] code, written for *one* specific device (or one family
of nearly-identical devices), that **fills in** every slot of that interface with concrete
code for that device. The mechanism that makes "fill in the slot" literal is the
**function pointer**. A function is a named block of code; a *pointer* is a stored memory
address; a **function pointer** is therefore a variable that holds the address of a
function — a slot you can drop *any* matching function into and call later without knowing
in advance which one is there. The [[kernel]]'s interface is, concretely, a record full of
such slots: a `read_block` slot, a `write_block` slot, a `flush` slot. When a driver
*registers* itself, it writes the address of its own `read_block` code into the
`read_block` slot, its own `write_block` code into the `write_block` slot, and so on.

This is the whole trick, and it is worth saying plainly. Afterward, when the rest of the
[[kernel]] wants to read a block, it does **not** name any particular device's code. It
just calls "the `read_block` in this slot," and whatever the driver put there runs. A
solid-state-disk driver will have put its own routine there (which writes commands into
that controller's registers one way); a different disk's driver will have put a different
routine there (which writes a *different* controller's registers a different way). The
caller is identical in both cases. The [[kernel]] does not care which driver is behind the
slot — that indifference is precisely what keeps the [[kernel]] hardware-agnostic.

### The WHY: indirection is what buys hardware-independence

Here is the key insight, the non-obvious step that makes the design work. Calling hardware
*directly* would weld the [[kernel]] to that hardware: the read-a-block code would contain,
inline, the exact registers of one disk, and supporting a second disk would mean editing
that core code. Calling through a **function pointer** inserts one level of *indirection* —
the caller names a *slot*, and the slot names the code — and that indirection is exactly
the seam along which device-specific knowledge can be detached from the [[kernel]] core.
Everything that varies per device lives *inside* the driver's functions; everything the
[[kernel]] core does is phrased in terms of the *slots*, which never change. To support a
new device you write a new driver that fills the slots its own way and registers it; you
touch nothing in the core. The invariant the design maintains is: **the set of slots (the
interface) is fixed and shared; the code in the slots is per-device and swappable.** That
invariant is the entire reason a single [[kernel]] binary can run on machines with wildly
different hardware.

The same split explains the *driver's other duties*, the ones that face the hardware. The
driver is the only code that knows this device's registers, so it is also the natural place
to do the three privileged things only the [[kernel]] may do for this device. It **programs
the hardware** by writing those registers. It **handles the device's [[interrupt]]s** — an
[[interrupt]] is a device's electrical "I need attention" signal that yanks the CPU into a
registered [[kernel]] handler; for a given device, *that* handler is the driver's. And it
sets up **[[dma]]** (*Direct Memory Access*: an arrangement where the device is told a
memory address and copies a bulk of data straight to or from main memory on its own, with
the CPU only programming the transfer up front — see [[dma]]) — the driver is what hands
the device the address and arms the transfer. All three are register-level, device-specific acts, so
they belong with the only code that speaks the device's dialect. (Because all of this runs
inside the [[kernel]] with full privilege, a bug in a driver can crash the whole machine —
once loaded, a driver *is* the [[kernel]], exactly as the [[kernel]] node warns. Drivers
are usually delivered as loadable [[kernel]] *modules*: separate files the [[kernel]] can
snap into itself at runtime when a device appears, rather than code baked into the
[[kernel]] at boot — a packaging convenience, not a change to anything above.)

### The three kinds of device the kernel distinguishes

Not every device is shaped the same way, so the [[kernel]] sorts devices — and therefore
their drivers — into three classes, each with its own style of interface:

- **Character devices** handle a **byte stream**: bytes flow one at a time or in small
  chunks, in order, with no notion of jumping around. A keyboard, a serial terminal, or a
  source of random bytes is a character device — you read the next byte, then the next.
- **Block devices** handle **fixed-size blocks** (say 512-byte or 4-kilobyte chunks) and
  crucially support **random access**: you can ask for block number 500, then block
  number 3, in any order. Disks and other storage are block devices — this is the class
  whose interface is the `read_block` / `write_block` / `flush` list used above.
- **Network devices** handle **packets** — bounded bundles of bytes sent to or arriving
  from other machines. Unlike the other two, they are not addressed as named entries among
  the system's files; they are reached through the [[kernel]]'s networking subsystem.

The three differ only in the *shape* of the interface the [[kernel]] defines (a stream of
bytes, addressable blocks, or packets); the underlying bargain — fixed slots filled by
per-device function pointers — is identical across all three.

### Worked instance: a `read()` on a sensor through its driver

Take a concrete, non-degenerate case: a program issues a `read()` asking for one reading
from a temperature sensor, which is a simple character device. Trace it, leaning on the
[[kernel]]'s machinery.

1. The program executes the `read()` **system call**. As [[kernel]] explains, this is the
   front-door entry point: the CPU switches to privileged mode and jumps into the
   [[kernel]], which sees that the target is this sensor device.
2. The [[kernel]] does **not** contain any sensor-specific code. Instead it looks at the
   sensor's interface record and **dispatches through the registered `read` function
   pointer** — it calls "whatever is in the `read` slot." Because the sensor's driver
   registered itself earlier, the address sitting in that slot is the driver's own read
   routine, so *that* routine now runs.
3. The driver's routine speaks the sensor's dialect. It reads the sensor's **data
   register** — the device-specific control slot where this particular chip exposes its
   latest measurement — getting, say, the raw value `21`.
4. The driver **copies that value back** across the boundary into the program's own memory,
   exactly the kind of privileged copy [[kernel]] performs, and returns from its `read`
   routine. Control unwinds back out through the system call; the CPU returns to restricted
   mode and `read()` hands the program the value.

Notice the two-faced result, which *is* the concept. To the calling program the operation
was **uniform**: it issued the same `read()` it would issue against a keyboard, a disk
file, or any other readable thing, and got bytes back — it never learned that a temperature
sensor was involved. *Inside*, the operation was entirely **device-specific**: the only
code that knew the sensor's data register existed at all was the driver, reached purely
because its function pointer occupied the slot. Swap the sensor for a different one and only
the driver behind the slot changes; the `read()` and every layer of [[kernel]] above it
stay byte-for-byte the same. That is how a driver lets the [[kernel]] stay hardware-agnostic.

## Prerequisites

- [[kernel]]
- [[interrupt]]
- [[dma]]

## Sources

- Linux internals study guide (`etc/linux-internals-complete.html`) — §2 "Device drivers": the "translates between two languages" / **bilingual interpreter** framing and the "read 4KB from block 500" example (driver as the per-device translator between the kernel's uniform request and the hardware's registers/protocol); the "kernel defines an interface / NVMe driver fills in / SATA driver fills in" **function-pointer** table (`read_block` / `write_block` / `flush` slots filled per device, "the kernel doesn't care which driver is behind it"); the three device types — **character** (byte streams), **block** (fixed-size random-access blocks), **network** (packets); and the Q&A boxes on loadable kernel **modules**, on drivers running with full privilege (so a buggy driver can crash the machine), and on the `read()` → … → driver → DMA → hardware path.
