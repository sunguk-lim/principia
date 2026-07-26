---
id: dentry
title: Dentry
summary: A dentry (short for directory entry) is the vfs object that maps a single name to a file's identity.
type: concept
tags: [os/filesystem]
prereqs: [vfs, inode]
sources: ["linux-internals-complete.html — 'Inodes and dentries — how files are tracked' (a filename is not a file; directory as a list of name→inode pairs; path resolution of /etc/hostname; hard links)"]
status: explained
created: 2026-06-23
updated: 2026-06-24
---

# Dentry

## Summary

A **dentry** (short for *directory entry*) is the [[vfs]] object that maps a single
**name** to a file's identity. The identity itself is held in an [[inode]] — the kernel
record that stores a file's real properties (its type, permissions, owner, size,
timestamps, and the pointers to where its bytes live on disk) and is referred to by an
**inode number**. The crucial fact is that the inode does *not* store the file's name; the
name lives in a dentry instead. A dentry is therefore one (name → inode-number) pair, and a
**directory is essentially just a list of dentries**. Because names are kept separate from
files, the kernel resolves a path like `/etc/hostname` by *walking* dentries — looking up
each name component in a directory's list to get the next inode — and because that walk
happens on every file access and re-reading directory data from a slow disk each time would
be ruinous, the kernel keeps recently used dentries in a fast in-memory **dentry cache** so
that resolving a path you have used before is nearly free.

## Grounded explanation

### The defining idea: a dentry names a file without being the file

Recall from [[vfs]] the two halves of how the kernel tracks a file. The **inode** is the
file's real identity: a kernel record holding its metadata — type, permissions, owner, size,
timestamps — together with the pointers to the data blocks that hold its bytes. Each inode is
identified by an **inode number** (an integer index into the filesystem's table of inodes).
What the inode deliberately does *not* contain is the file's name. The name is stored
somewhere else entirely, and that "somewhere else" is the concept of this node: the
**dentry**.

A dentry is a single mapping from a **name** to an **inode number** — one (name → inode
number) pair. That is the whole of it. The name `hostname` and the number of the inode that
*is* the file `hostname` are bound together in a dentry; the inode sits nameless on its own.
This is the defining structure: a dentry is the thing that supplies a file with a name, kept
separate from the file's identity so that the two can vary independently.

From this one idea a directory falls out immediately. A **directory is just a list of
dentries** — a list of (name → inode-number) pairs. When you list a directory and see the
names `hostname`, `passwd`, `hosts`, you are reading the *names* out of that directory's
dentries; each of those names is paired in its dentry with the number of the inode that holds
the corresponding file's real contents and metadata. A directory, then, is not a container of
files in any literal sense. It is a name-to-inode lookup table, and the dentry is its row.

### Why separate the name from the file

Why store the name in a dentry rather than inside the inode itself? Because detaching the name
from the identity is exactly what buys three properties that a filesystem needs, and none of
them is possible if the name is welded to the file.

First, **one file can have several names.** Since a name is just a dentry pointing at an inode
number, nothing stops two different dentries — even in two different directories — from
holding the *same* inode number. Both names then refer to the one identical file; these are
called *hard links*. The file's data is not deleted when you remove one name, only when the
*last* dentry pointing at that inode is removed (the inode keeps a count of how many names
point to it). This is impossible if the name lives inside the file, because then "the file"
and "its name" would be one object and could not be many-to-one.

Second, **a directory becomes a simple, uniform structure.** Because every directory is just a
list of (name → inode-number) pairs, the kernel needs only one mechanism — "look a name up in a
list of dentries" — to handle every directory, whether it is the root, a deeply nested folder,
or a directory belonging to a completely different kind of [[vfs]] backend. The directory does
not need to know anything about the files it names beyond their inode numbers.

Third, and this is the payoff the next section makes concrete, **path traversal becomes a
repeatable, cacheable step.** Resolving any path is nothing but the same operation applied over
and over — take the current directory, look up the next name in its dentries, get an inode
number, move to that inode — so a single cached lookup table (the dentry cache) can short-circuit
the whole walk.

The invariant a dentry maintains is therefore: **a name is bound to an inode number, never to
the file's contents directly.** The name gets you to the identity; the identity (the inode)
tells [[vfs]] which backend owns the file and where its bytes are.

### How a path is resolved: a walk through dentries

A filesystem path such as `/etc/hostname` is not looked up in one shot. It is resolved one name
component at a time, and each step is a single dentry lookup. The rule, stated once and then run
on a concrete case below, is:

> Start at a known directory inode. Look up the next name component in that directory's list of
> dentries to obtain an inode number. Fetch that inode. If it is a directory and there are more
> name components left, make it the current directory and repeat; if it is the final component,
> you have found the file's inode.

Two things are worth noticing in the rule. The walk *alternates* between dentries and inodes: a
dentry gives you an inode number, the inode (if it is a directory) gives you a fresh list of
dentries to search next, and so on down the path. And the walk *only* moves forward through
directories — each intermediate inode must itself be a directory, or the path is invalid.

### A worked instance: resolving `/etc/hostname`

Take the path `/etc/hostname` and resolve it with real numbers (the inode numbers below are the
ones the source uses for this exact path). The path has two name components after the leading
slash: `etc`, then `hostname`.

1. **Start at the root.** The root directory `/` has a fixed, well-known inode — inode `2` on an
   ext-style filesystem — so the kernel begins there with no lookup needed. Inode `2` is a
   directory, so the kernel reads its list of dentries.
2. **Look up `etc` in root's dentries.** Among root's (name → inode-number) pairs is one whose
   name is `etc`. Its dentry yields inode number `131073`. The kernel fetches inode `131073` and
   checks it: it is a directory. There is still one component left (`hostname`), so `/etc`
   becomes the current directory and the kernel reads *its* list of dentries.
3. **Look up `hostname` in `/etc`'s dentries.** Among the dentries of inode `131073` is one whose
   name is `hostname`. Its dentry yields inode number `131200`. The kernel fetches inode `131200`
   and checks it: it is a regular file. `hostname` was the last component, so the walk stops —
   inode `131200` is the file the path named.

Trace the alternation explicitly: dentry `etc` → inode `131073` (a directory) → its dentries →
dentry `hostname` → inode `131200` (the file). Notice the instance is non-degenerate on purpose:
it has an intermediate directory (`/etc`) sitting *between* the root and the target, so the "if it
is a directory, recurse" branch of the rule is actually exercised rather than collapsing to a
single lookup. The name `/etc/hostname` never appears as one stored key anywhere; it exists only
as this chain of per-component dentry lookups.

### Why the dentry cache exists, and the second lookup

Every one of those lookups reads a directory's dentry list, and on a real disk that list lives in
slow storage. But path resolution is one of the most frequent things a kernel ever does — every
single file access, every `open`, walks a whole path from some directory down to the target, and
busy paths like `/etc`, the root, or a program's working directory are walked thousands of times.
If each component re-read directory data from disk, the cost would dominate everything.

So the kernel keeps recently used dentries in a fast in-memory table called the **dentry cache**.
After the walk above, the dentries for `etc` (in root) and `hostname` (in `/etc`) are held in
memory. Now run the payoff: a *second* `open("/etc/hostname")` repeats the identical walk —
look up `etc`, then `hostname` — but each lookup now finds its dentry already sitting in the
cache. The kernel obtains inode `131073` and then inode `131200` straight from memory, with **no
disk read of any directory at all**. The first resolution paid the disk cost and warmed the
cache; the second is nearly free. This is the same caching pattern [[vfs]] uses elsewhere (an
in-memory copy of slow on-disk data), applied specifically to the name-to-inode mappings that
path resolution depends on.

So the full chain a dentry sits in is: **name → dentry → inode number → inode → the file's data**
(or, for a non-disk backend, the routine that produces it). The dentry is the first link — the
one that turns a human-meaningful name into the inode number that [[vfs]] needs to find the file's
real identity and the backend that owns it. Separate the name into the dentry and the identity into
the inode, build directories out of dentries, and resolve paths by walking them: that single design
choice is what makes one file able to wear many names, makes directories uniform lookup tables, and
makes repeated path traversal cacheable and fast.

## Prerequisites

- [[vfs]]
- [[inode]]

## Sources

- `linux-internals-complete.html` — section "Inodes and dentries —
  how files are tracked": "a filename is not a file" (the inode holds size, permissions, ownership,
  timestamps and the location of the data, identified by a number; the filename is *not* in the
  inode); "the name-to-inode mapping is stored in directory entries (dentries) … a directory is just
  a list of (name → inode number) pairs"; the worked path resolution of `/etc/hostname` (root inode
  `2` → look up `etc` → inode `131073`, a directory → look up `hostname` → inode `131200`, a regular
  file); and the "why separate the name from the file data?" note (one file can have multiple names —
  hard links — and the data is freed only when the last name is removed). The in-memory dentry cache
  that makes a repeated path lookup hit memory instead of disk follows the same caching pattern the
  source applies to inodes and file data (the inode cache and page cache).
