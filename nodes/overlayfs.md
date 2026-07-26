---
id: overlayfs
title: OverlayFS
summary: OverlayFS is a union filesystem — a filesystem that, instead of owning bytes on a disk of its own, builds one merged view by stacking other directory trees on top of each other.
type: concept
tags: [os/filesystem]
prereqs: [vfs, copy-on-write]
sources: ["linux-internals-complete.html — 'How container filesystems work — OverlayFS' (§7); glossary entry 'OverlayFS'"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# OverlayFS

## Summary

**OverlayFS** is a *union* filesystem — a filesystem that, instead of owning bytes on a
disk of its own, builds one merged view by **stacking other directory trees on top of each
other**. It plugs into the kernel through the [[vfs]] interface, so a program reading or
writing through it issues the ordinary file system calls and never sees the seam. The stack
has two kinds of layer: one or more **lower** layers, which are read-only, and a single
**upper** layer, which is writable. A read for a path is served from the upper layer if the
file is there; otherwise it "falls through" to the lower layers. A write never touches the
lower layers: changing a file that exists only below triggers a **copy-up** (the file is
copied into the upper layer and edited there), a brand-new file is created directly in the
upper layer, and deleting a lower-layer file is recorded by writing a **whiteout** marker in
the upper layer that hides the original. The reason this design matters is sharing: many
running containers can use **one** read-only image as their common lower layer while each
gets its own small, initially empty upper layer — so starting a container copies nothing,
it just hands out a fresh empty upper, which is what makes containers fast to launch and
cheap in disk space.

## Grounded explanation

### The defining idea: one filesystem that is really a stack of others

Recall from [[vfs]] what a filesystem *is* from the kernel's point of view. The [[vfs]] is
the dispatcher inside the kernel that presents one uniform set of file system calls —
`open`, `read`, `write`, and the rest — and routes each call to whichever backend owns the
file. Every concrete filesystem (a disk filesystem, a network filesystem, a pseudo-filesystem
like `/proc`) is just a backend that fills in the [[vfs]]'s operation slots with its own
routines. The program above never learns which backend it reached; it only ever issues the
same calls.

OverlayFS is one more such backend — but a peculiar one. Most backends ultimately produce
bytes from *somewhere of their own*: a disk, a remote server, the kernel's internal tables.
OverlayFS has no storage of its own at all. It is a **union** filesystem, meaning its job is
to take two or more existing directory trees — each of which already lives on some ordinary
filesystem — and **fuse them into a single tree** that it then presents through the [[vfs]]
slots. When a program calls `read` on a path inside the merged tree, the [[vfs]] routes that
call to OverlayFS's read routine, and *that* routine decides which of the stacked trees the
bytes should actually come from. So OverlayFS is a backend whose entire substance is the
*policy for combining other backends' files*. That policy is the concept of this node.

The stack is built from two roles, defined here before they are used:

- A **lower** layer is a directory tree that OverlayFS treats as **read-only**. There can be
  several of them, ordered, and they are never modified through the overlay. In a container,
  the lower layers are the image — for example, a base Ubuntu tree, a dependencies tree on
  top of it, and the application's files on top of that.
- The **upper** layer is a single directory tree that OverlayFS treats as **writable**. It
  starts empty and accumulates everything the running program changes.

OverlayFS exposes these as one **merged** view, with a fixed precedence: the upper layer
sits on top of the lower layers, and where the same path exists in more than one layer, the
*topmost* occurrence wins. Everything below follows from that single precedence rule.

### Read semantics: fall-through from top to bottom

To resolve a path in the merged view, OverlayFS searches the layers **from the top down** and
stops at the first one that has the path. Concretely: it looks in the upper layer first; if
the file is there, it serves that copy and the search ends. If the upper layer does not have
it, the request "falls through" to the highest lower layer, then the next, and so on, until
some layer supplies the file. The first hit wins; lower occurrences of the same path are
shadowed and never consulted.

This is exactly why a fresh container can read the entire image without anything being copied
into it. Its upper layer is empty, so almost every read falls straight through to the
read-only image in the lower layers and is served from there. The image is shared, untouched,
and read in place.

### Write semantics: never disturb the lower layers

The whole design rests on one **invariant: the lower layers are never modified.** They are
read-only so that they can be *shared* — and sharing is safe only if no writer can ever change
the shared bytes out from under the others. Every write operation is therefore arranged to
land in the upper layer instead, which is private to this overlay. There are three cases, and
they are the heart of the mechanism:

1. **Creating a new file.** A path that does not yet exist in any layer is simply created in
   the upper layer. Nothing needs to be consulted below; the new file lives in the upper layer
   from birth.

2. **Modifying a file that exists only in a lower layer.** This is the non-obvious,
   "magic-looking" step, and it has a name: **copy-up**. When a program opens a lower-layer
   file for writing, OverlayFS first **copies the whole file up** into the upper layer, then
   redirects the write to that upper-layer copy. From then on, the merged view's read
   precedence does the rest: because the copy now exists in the upper layer, every later read
   of that path finds the upper copy first and the lower original is shadowed. The lower file
   is never written — it is only ever read, during the one-time copy. This is precisely
   **[[copy-on-write]]**: the costly duplication happens lazily, only at the first write, and only
   for the files actually touched; everything left unmodified is still shared in place. (The
   same [[copy-on-write]] principle the kernel uses for memory pages — where a write to a shared
   page triggers a per-page copy rather than duplicating everything up front — here applied to
   whole files instead of 4 KB pages.)

3. **Deleting a lower-layer file.** Here is a subtlety the precedence rule alone cannot solve.
   OverlayFS cannot remove the file from the lower layer — the lower layer is read-only and
   shared. Nor can it leave things alone, or the deleted file would still fall through and
   reappear in the merged view. So deletion is recorded by writing a special marker called a
   **whiteout** into the upper layer at that path. A whiteout is not a file; it is a "this path
   is deleted" tombstone. When OverlayFS resolves a path during a read and encounters a whiteout
   in the upper layer, it stops the search immediately and reports the file as absent — it does
   *not* fall through to the lower layer underneath. The lower file still physically exists and
   is still shared by everyone else; this overlay has simply hidden it from its own merged view.

In all three cases the lower layers come through untouched, and everything that changed is
confined to this overlay's own upper layer. That is the invariant, maintained.

### Why it is built this way: sharing one image across many containers

Now the payoff — the reason union-with-copy-up exists rather than just giving each container
its own copy of the files. (A *container*, in plain terms, is one ordinary process the kernel
has been told to treat as if it had its own private system; one of the private things it gets
is its own root filesystem. Treat that as background; the concept here is the filesystem, not
the container machinery.)

Suppose ten containers all run from the same image. Without overlays, each would need its own
full copy of that image on disk — ten times the bytes, and a slow copy every time one launches.
With OverlayFS, the image is stored **once**, as the shared read-only lower layers. To launch a
container you create **one empty directory** to serve as its upper layer and stack it on top of
the shared image. That is the entire per-container cost: an empty directory. No image bytes are
copied. Ten containers means one image plus ten tiny uppers, and each upper holds only the
handful of files that *that* container has actually changed since it started. Reads of unchanged
files all fall through to the one shared image; writes are copied up into the private upper and
seen by no one else. This is why container images are layered, why launching a container is
nearly instant, why containers barely add to disk usage, and why one container's writes can
never corrupt the image or disturb its siblings.

### A worked instance: a base image, one container, three operations

Take a base **Ubuntu** image as the read-only lower layer, and start one container whose upper
layer is a fresh, empty directory. The merged view the container sees is, at this instant,
byte-for-byte the Ubuntu tree, because every path falls through to the lower layer. Now run
three operations that deliberately exercise all three write cases plus a plain read:

1. **`cat /etc/os-release`** — a read. OverlayFS looks in the upper layer: empty, nothing there.
   It falls through to the lower Ubuntu layer, finds `/etc/os-release`, and serves its bytes.
   No copy, no change; the file was read in place from the shared image.

2. **`echo x >> /etc/hosts`** — a modify of a file that exists only in the lower layer. This
   triggers **copy-up**: OverlayFS first copies the lower layer's `/etc/hosts` up into the
   container's upper layer, then appends `x` to *that* upper copy. The Ubuntu image's
   `/etc/hosts` is never written — only read once during the copy. From now on, any `cat
   /etc/hosts` in this container resolves to the upper copy (precedence: top layer wins) and
   shows the appended line; every *other* container still falls through to the unchanged image
   and sees the original `/etc/hosts`.

3. **`rm /usr/bin/foo`** — a delete of a file that exists only in the lower layer. OverlayFS
   cannot erase it from the read-only image, so it writes a **whiteout** marker at
   `/usr/bin/foo` in the upper layer. Afterwards, when this container resolves `/usr/bin/foo`,
   it hits the whiteout in the upper layer and reports "no such file" without falling through —
   `foo` has vanished from this container's view. The image's real `/usr/bin/foo` still exists
   and is still visible to every other container sharing that lower layer.

After all three, the shared Ubuntu image is exactly as it was. The container's once-empty upper
layer now holds two things and only two things: a modified copy of `/etc/hosts` and a whiteout
for `/usr/bin/foo`. Everything else the container "has" is still the one shared image, read in
place. That small, private, after-the-fact delta on top of a large shared base is the whole
point of OverlayFS.

## Prerequisites

- [[vfs]]
- [[copy-on-write]]

## Sources

- `linux-internals-complete.html` — section "How container
  filesystems work — OverlayFS" (§7): OverlayFS as a writable layer stacked on read-only
  layers; the merged view that "checks writable layer first, not found → checks layer 3, then
  2, then 1"; "write → goes to writable layer (copy-on-write!)"; "delete → whiteout in writable
  layer hides original"; shared read-only image layers across containers saving disk space; and
  the key takeaway "Containers use OverlayFS. Read-only image layers + a writable layer per
  container. Copy-on-write for files… Layers are shared across containers." Also the glossary
  entry: "A union filesystem that stacks read-only lower layers under a writable upper layer.
  The basis for container image layers."
