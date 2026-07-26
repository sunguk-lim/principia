---
id: container-runtime
title: Container Runtime
summary: A container runtime is the software stack that actually creates and runs a container — the tooling that does the concrete work of assembling, around one ordinary process, the…
type: concept
tags: [os/virtualization]
prereqs: [container, capabilities, namespace, cgroup, seccomp, system-call]
sources:
  - linux-internals-complete.html ("What Docker actually does", "Every process has a parent", "Combining them = a container")
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Container Runtime

## Summary

A **container runtime** is the software stack that actually *creates and runs* a [[container]] —
the tooling that does the concrete work of assembling, around one ordinary process, the kernel
features a [[container]] is made of. A [[container]] itself is not a kernel object; it is a regular
process wrapped in an isolated view, a resource budget, and a private layered root filesystem.
*Something* has to set those up — find the right files, build the stacked root, create the budget,
launch the process into fresh isolation, strip its powers, and finally start the program inside.
That something is the container runtime. The key point is that it is **not magic**: it is a
**layered set of cooperating programs**, each with one job. A high-level daemon (the user-facing
program, e.g. `dockerd`) handles the human-friendly side — accepting commands, managing images and
networking. It hands off to a **lifecycle manager** (e.g. `containerd`) that pulls the image,
prepares the stacked filesystem, sets up the budget, and starts the container. That manager spawns
a tiny **shim** to babysit each container, and the shim invokes a small **low-level runtime** (e.g.
`runc`) that performs the actual [[system-call]]s: create the new isolation, switch into the private
root, drop dangerous powers, and execute the container's first program. Splitting the work this way
is the whole design: clean separation of concerns, and proof that a [[container]] is just a normal
process the runtime placed inside ordinary kernel features.

## Grounded explanation

### Why a runtime must exist at all

Start from what a [[container]] is, since that is the prerequisite for everything here. A
[[container]] is **not** a special kind of object the kernel knows about. It is one ordinary
process that has been given three things at once: an *isolated view* (its own process numbers,
network, and filesystem tree), a *resource budget* (a ceiling on memory and CPU), and a *private
layered root filesystem* (a shared read-only base with a thin writable layer stacked on top). The
[[container]] node makes the central point: remove any one of those and you no longer have a
[[container]], and the kernel itself has no "container" thing — it only sees a process with some
isolation and some limits applied.

That immediately raises a question the [[container]] node sets aside: *who applies them?* Setting
up fresh isolation, writing a budget, stacking a root filesystem, stripping the process's
privileges, and then starting the right program is a precise multi-step procedure. A human could do
it by hand, step by step — but in practice a program does it for you. **That program — or rather,
that stack of programs — is the container runtime.** Defining the concept, then, means describing
*what the runtime does and how it is structured*, not re-deriving what a [[container]] is. The
runtime is the *maker*; the [[container]] is the *thing made*.

### The defining structure: layers, each with one job

The single most important idea about a container runtime is that it is **layered**, and the layers
exist on purpose. It would be possible to write one giant program that did everything. Real runtimes
deliberately do not. They split the work across a small ladder of programs, top to bottom going from
*human-friendly* to *kernel-level*. Define each layer by its one responsibility.

**The high-level daemon — the user experience.** At the top sits a long-running background program,
the *daemon* (a program that stays running to service requests; the common one is named `dockerd`).
It is what your command-line tool talks to. Its job is everything *around* the [[container]] that a
person cares about: accepting commands over an API, keeping track of images (the packaged
filesystems that containers start from), naming, networking between containers, and so on. It is
the **face** of the system. Crucially, it does **not** itself touch the kernel features of a
[[container]]; it decides *what* should happen and delegates the *doing*.

**The lifecycle manager — birth, life, and death of a container.** The daemon hands off to a second
program (commonly named `containerd`) whose single concern is the **lifecycle** of containers:
turning the abstract request "run this image" into a concrete running [[container]] and tracking it
until it exits. Concretely, this layer (i) **pulls the image** — fetches the read-only filesystem
layers if they are not already on disk; (ii) **prepares the layered root** — stacks those read-only
layers under a fresh empty writable layer, producing the private root filesystem the [[container]]
will use; (iii) **creates the resource budget** — sets up the memory and CPU ceilings; and (iv)
**starts a babysitter** for this particular [[container]] (next layer). Notice this layer still does
not perform the final kernel syscalls that *create* the running process; it stages everything and
delegates the last, lowest step.

**The shim — one babysitter per container.** For each [[container]] it starts, the lifecycle
manager spawns a tiny dedicated process called a **shim** (commonly `containerd-shim`). The shim's
only job is to *be the stable parent* of the container's process: it sits directly above the
container in the process tree and stays alive for as long as the [[container]] runs, holding the
container's input/output streams and waiting to report its exit. Why a separate babysitter per
[[container]]? Because it decouples the [[container]] from the big management programs above it: the
daemon and lifecycle manager can be **restarted or upgraded** without killing running containers,
since each container is anchored to its own lightweight shim rather than to a shared parent. The
shim itself does not set up the [[container]]'s kernel features either — it invokes the bottom
layer to do that, then just watches.

**The low-level runtime — the actual syscalls.** At the bottom is a small program (commonly `runc`,
built to a shared industry standard so different higher layers can reuse it) that does the real,
privileged kernel work — issuing [[system-call]]s directly to the kernel — and then gets out of the way. Invoked by the shim with the prepared
ingredients (the stacked root, the budget), it performs, in order, exactly the steps that *turn a
plain process into a [[container]]*:

1. **Create fresh isolation.** It launches a new process into brand-new [[namespace]]s of each kind at
   once — its own process-number space (so it will be number 1 inside), its own network, its own
   set of mounts, its own hostname space. This is the *isolated view* half of a [[container]].
2. **Place it in the budget.** The new process is put into the [[cgroup]] prepared above, so
   the kernel will enforce its memory and CPU ceilings.
3. **Switch into the private root.** Inside the new mount isolation, it makes the prepared stacked
   filesystem the process's root directory — it *pivots the root*, swapping the process's view of
   "/" from the host's filesystem to the [[container]]'s layered one. After this the process can see
   only the [[container]]'s files. (This is the one step most likely to look like magic; it is
   plainly a root-directory swap performed *after* the process is already inside its own mount
   isolation, so nothing on the host is disturbed.)
4. **Strip dangerous powers.** Even an isolated process could be too strong, so the runtime *drops
   [[capabilities]]* — revokes the fine-grained privilege bits such as the right to perform
   administrative kernel operations — and *applies a [[seccomp]] filter* that blocks dangerous
   system calls outright. Now the process is not just isolated but **declawed**.
5. **Become the container's program.** Finally it *replaces itself* with the program you actually
   asked to run — the process image is overwritten so that, from this instant, the very same process
   that was being prepared *is* the running application. It is process number 1 inside its own
   isolation, sees only its own world, is capped by its budget, and cannot make dangerous calls —
   yet it is scheduled by the one host kernel on the host's CPUs like any other process.

### The why: what the layering buys

Why bother with four programs instead of one? Because each layer is then **simple, replaceable, and
reusable**. The daemon can own a rich, changing user experience without ever needing privileged
kernel code. The lifecycle manager can be the single authority on images and container state without
implementing syscalls. The low-level runtime can stay **tiny and standard** — a small program that
does only steps 1–5 above — so that *different* higher-level systems can call the *same* runtime,
and the privileged, security-sensitive code lives in one small, auditable place. The shim, by being
per-container, lets the heavy upper layers be restarted under running containers. The split is not
incidental; it is the design that lets a complex product rest on a small, shared, trustworthy core.

And the deeper payoff is conceptual, and it ties straight back to the prerequisite: watching the
runtime work *proves* that a [[container]] is just a process. There is no point in the procedure
where a "container object" is created. There is only: make a process, give it fresh isolation, put
it in a budget, swap its root, weaken it, and exec the program. The runtime is precisely the
sequence of ordinary operations that the [[container]] node says *defines* a [[container]] — now
shown as something a small stack of programs does for you, step by step.

### Worked instance: `docker run nginx`

Trace one real command end to end — running the `nginx` web server as a [[container]] — and watch
control fall down the ladder.

1. **Command line → daemon.** You type `docker run nginx`. The command-line tool merely forwards the
   request, over an API, to the high-level **daemon** (`dockerd`). The daemon resolves what `nginx`
   means: it is an image name, so it figures out which image (which set of read-only filesystem
   layers) is wanted, and decides the [[container]] should be created. It does no kernel work; it
   tells the lifecycle manager: "create a container from the nginx image."

2. **Daemon → lifecycle manager.** The lifecycle manager (`containerd`) takes over the *lifecycle*.
   It **pulls** the nginx image layers if they are not already cached, then **prepares the layered
   root**: it stacks those read-only nginx layers under a fresh empty writable layer, giving this
   one [[container]] its private root filesystem (its own `/etc`, `/usr`, `/var`) without copying
   the shared layers. It sets up the **resource budget** for the container. Then it spawns a
   **shim** dedicated to this nginx container.

3. **Shim → low-level runtime.** The shim — now the stable parent that will outlive any restart of
   the upper programs — invokes the low-level runtime (`runc`) with the prepared root and budget.

4. **Runtime does the kernel work.** The runtime launches a new process into **fresh isolation**:
   its own process-number space (so inside it is number **1**), its own network, its own mounts, its
   own hostname space. It places that process into the prepared **[[cgroup]] budget**. It **pivots
   the root** into the stacked nginx filesystem, so the process now sees only nginx's files as "/".
   It **drops [[capabilities]]** and **applies the [[seccomp]] filter**, so the web server cannot
   perform privileged or dangerous kernel operations. Finally it **execs nginx**, replacing itself —
   from here on, the process *is* nginx.

5. **What you end up with.** On the host's process tree, this is plainly visible: the daemon
   (`dockerd`), beneath it the per-container shim (`containerd-shim`), and beneath the shim the
   `nginx` process itself — "also just a process," a regular entry in the host's list with some
   ordinary host process number. *Inside*, nginx is process number 1 on what looks like a quiet
   machine of its own, with its own network and files, capped by its budget, unable to make
   dangerous calls. Nothing booted; no second kernel exists. The container runtime did exactly five
   small things to one process — and that process, so wrapped, is the running [[container]].

So a container runtime is best understood not as a single tool but as a **layered pipeline** —
user-facing daemon, lifecycle manager, per-container shim, low-level syscall runtime — that takes
the request "run this image" and performs the precise, unmagical sequence of kernel operations that
*makes* a [[container]] out of an ordinary process.

## Prerequisites

- [[container]]
- [[namespace]]
- [[cgroup]]
- [[capabilities]]
- [[seccomp]]
- [[system-call]]

## Sources

- `linux-internals-complete.html` — section **"What Docker actually does"** (the layered chain
  `docker CLI → dockerd → containerd → containerd-shim → runc`; containerd pulls the image, sets up
  the stacked filesystem, creates the memory/CPU budget, and starts the shim; the new process is
  launched into fresh PID/net/mount/UTS namespaces, then *pivots its root* into the stacked
  filesystem, *drops capabilities*, *applies a seccomp syscall filter*, and finally *execs* the
  container's program — "but it's just a regular process. Same kernel. Same CPU."). Section **"Every
  process has a parent"** (the host process tree showing `dockerd` → `containerd-shim` → the
  container's program as ordinary processes, with the note that container processes are children of
  a per-container shim and the kernel does not treat them specially — it only applies namespace and
  cgroup restrictions). Section **"Combining them = a container"** (the timeline placing Docker as a
  user-experience layer over identical kernel features, and noting Docker replaced LXC with its own
  low-level runtime — libcontainer, later runc — still using the same kernel syscalls).
