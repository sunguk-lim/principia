---
id: hypervisor
title: Hypervisor
summary: A hypervisor (also called a virtual machine monitor) is software that slices one physical computer into several virtual machines (VMs).
type: concept
tags: [os/virtualization]
prereqs: [kernel]
sources: ["etc/linux-internals-complete.html §10 Hypervisor & VMs"]
status: explained
created: 2026-06-23
updated: 2026-06-23
---

# Hypervisor

## Summary

A **hypervisor** (also called a **virtual machine monitor**) is software that slices one
physical computer into several **virtual machines** (VMs). Each VM is a make-believe computer:
it boots and runs its own complete operating system, including its own [[kernel]] — the
privileged resident program that manages a machine's hardware — and believes it owns real CPUs,
memory, and devices. The hypervisor sits *underneath* all those guest kernels and quietly shares
the one set of real hardware among them, while keeping each VM walled off from the others. Where
a [[kernel]] multiplexes one machine's hardware among many *processes*, a hypervisor multiplexes
hardware among many *whole machines*, each with its own kernel inside.

## Grounded explanation

**The problem.** A [[kernel]] is the program that owns a machine's hardware: it alone runs in
the CPU's privileged mode, it decides which program gets the CPU next, and it hands out memory
and mediates every device access. By design there is *one* kernel per running machine, and it is
in charge of everything on that machine. But suppose you have a single physical server and you
want to run two *different* operating systems on it at once — say a Linux system and a Windows
system — each needing its own kernel, fully isolated, so that a crash or a security break in one
cannot touch the other. One kernel cannot be two kernels. So how do you put several independent,
each-with-its-own-kernel machines onto one piece of metal?

**The idea: virtualize the machine itself.** The hypervisor's trick is to do *for whole
machines* what a [[kernel]] does *for processes*. Recall what a kernel gives each process: the
illusion of having the CPU to itself (the kernel time-shares the real CPU among processes) and
the illusion of its own private memory (the kernel maps each process's addresses onto real
memory). A hypervisor lifts that same illusion up one level. To each VM it presents a complete
*virtual computer* — virtual CPUs, a block of memory that looks like physical RAM, virtual disks
and network cards. A guest operating system installed inside the VM does exactly what an OS
always does: it boots its [[kernel]], that kernel takes the privileged mode of its (virtual) CPU,
and it proceeds to manage its (virtual) hardware — never realizing the hardware is fake. The
hypervisor is the layer that fields those illusions and maps them onto the one real machine.

**Why it works — the key insight.** A [[kernel]] keeps control because it runs in the CPU's
privileged mode and ordinary programs do not; whenever a program tries a privileged operation,
control *traps* down to the kernel. The hypervisor uses the same lever, one rung lower. Modern
CPUs add an even-more-privileged mode *below* the kernel's. The hypervisor runs there. Each
guest [[kernel]] runs in what it thinks is "the" privileged mode, but it is actually a *boxed*
privileged mode: when a guest kernel tries to touch real hardware — reprogram the memory map,
talk to a disk controller — that action traps *down to the hypervisor*, which emulates the effect
on the shared real hardware and returns control. So the invariant the hypervisor maintains is:
**every guest kernel may believe it is the most privileged thing on the machine, yet no guest
can actually reach the real hardware or another guest's memory without going through the
hypervisor.** That trap-and-mediate loop is what makes the isolation real rather than merely
promised — the same mechanism by which a [[kernel]] protects itself from its processes, applied
to protect the hypervisor (and each VM) from the guest kernels.

**Multiplexing the CPU.** The hardware has a fixed number of physical CPU cores. Each VM is
configured with some number of *virtual* CPUs. The hypervisor schedules virtual CPUs onto
physical cores in turn, just as a [[kernel]] schedules process threads onto cores — when a VM's
time slice ends, the hypervisor saves that virtual CPU's register state and runs another VM's
virtual CPU on the physical core. Memory works the analogous way: the hypervisor gives each VM a
range that *looks* like physical RAM starting at address zero, and translates those guest
"physical" addresses onto real machine addresses, so two VMs can each believe they own physical
address `0x1000` while occupying different real memory.

**Two flavors — Type 1 and Type 2.** Hypervisors differ in *what runs beneath them*.

- **Type 1 (bare-metal):** the hypervisor runs *directly on the hardware*, with no host OS under
  it — the hypervisor essentially *is* the bottom-most system program, playing the hardware-owning
  role a [[kernel]] normally plays. This is what data centers run (e.g. VMware ESXi). A
  near-relative is KVM, which makes the Linux [[kernel]] *itself* act as a bare-metal hypervisor:
  the same kernel that runs the host also uses the CPU's VM-support features to run guest VMs at
  near-native speed.
- **Type 2 (hosted):** the hypervisor runs as an *ordinary program on top of a normal host OS*
  (e.g. VirtualBox on your laptop). There is a full host [[kernel]] underneath managing the real
  hardware, the hypervisor app sits above it, and the VMs sit above the hypervisor. This is
  convenient for desktops but adds a layer between the guests and the metal.

**The defining contrast — VM vs container.** The reason hypervisors matter is sharpest when set
against the *other* way to run isolated workloads on one machine: the **container**. (Containers
are described here only in plain prose; they are a separate topic.) A container is *not* a
virtual machine. A container is an ordinary process on the host, fenced off by host-kernel
features — "namespaces" that filter what it can see (its own view of process IDs, the
filesystem, the network) and "cgroups" that cap what it can use (so much CPU, so much memory).
Crucially, **all containers on a host share that host's single [[kernel]].** There is no second
kernel and no emulated hardware.

That single difference — *own kernel* versus *shared kernel* — drives everything else:

| | Virtual machine (hypervisor) | Container (shared host kernel) |
|---|---|---|
| What is virtualized | the **hardware** | the **OS view** (same kernel, filtered) |
| Kernel | each VM ships its **own** guest [[kernel]] + OS | all share the **one** host [[kernel]] |
| Isolation | strong — a guest kernel bug stays inside its VM | weaker — a host-kernel bug can affect every container |
| Weight / size | heavy — gigabytes (a whole OS image) | light — megabytes (just the app and its files) |
| Startup | slow — a full OS boot, seconds to minutes | fast — milliseconds (just spawn a process) |

The **why** of choosing a VM, then, is precisely the thing that makes it expensive: you get a
*different and independently isolated* [[kernel]] and operating system on the same metal — you can
run Windows beside Linux, and a total compromise of one guest kernel does not reach the host or
the neighbors — but the price is running an entire second [[kernel]] and OS, emulating hardware
for it, and waiting for it to boot. A container is cheap *because* it skips all of that and
borrows the host's [[kernel]]; that is also exactly why its isolation is thinner.

**Worked instance.** Take one physical server with **4 CPU cores** and **64 GB of RAM**, running
a Type 1 hypervisor. We host three VMs on it:

- **VM-A:** a Linux guest, configured with **2 virtual CPUs**, **16 GB**, running the Linux
  [[kernel]] version 6.x.
- **VM-B:** a Windows guest, **1 virtual CPU**, **8 GB**, running the Windows NT [[kernel]].
- **VM-C:** another Linux guest, **2 virtual CPUs**, **32 GB**, running an *older* Linux
  [[kernel]] version 5.x.

Notice this triggers the non-degenerate cases: the virtual CPUs requested total `2 + 1 + 2 = 5`,
which is *more* than the `4` physical cores — so the hypervisor genuinely must time-share, not
just hand each VM a dedicated core. Each guest boots from scratch: firmware, bootloader,
[[kernel]], first process, the works — three separate boots, three separate kernels, two of them
even *different versions of Linux*, one a completely different OS. When VM-A's Linux kernel tries
to, say, reconfigure its memory map, that privileged action traps down to the hypervisor, which
applies it only within VM-A's 16 GB slice of real RAM and resumes VM-A. Meanwhile the hypervisor
keeps rotating the five virtual CPUs across the four physical cores. If a kernel bug crashes
VM-C's old 5.x kernel, VM-A and VM-B keep running untouched, because each is a separate machine
behind the hypervisor's wall.

Now contrast the container alternative on the *same* server. Three containers would all be
ordinary processes on the host's *one* Linux [[kernel]] — no VM-A/B/C boots, no second or third
kernel, no Windows at all (you cannot run a Windows container on a Linux host, because there is
only the one Linux kernel to share). They would start in milliseconds, weigh megabytes instead of
gigabytes, and impose almost no overhead — but a flaw in that single shared host [[kernel]] would
expose all three at once. That is the trade the hypervisor exists to offer the other side of:
heavier and slower, in exchange for a genuinely separate kernel and genuine hardware-level
isolation per workload.

## Prerequisites

- [[kernel]]

## Sources

- `etc/linux-internals-complete.html` — §10 "Hypervisor & VMs": *What is a hypervisor?* (Type 1
  vs Type 2, KVM), and *Container vs VM revisited* (own kernel vs shared kernel; isolation,
  weight, and startup trade-offs).
