# Linux Pseudo-Filesystems

## Meaning

A pseudo-filesystem lets software inspect or control live kernel state through paths that resemble ordinary files. Its contents are generated or mediated by the kernel; copying the directory does not create a durable backup of the machine's state.

## Mechanism

The [[vfs]] supplies the familiar open-and-read interface, while the [[kernel]] implements the values. procfs, usually mounted at `/proc`, exposes process and system information. For example, a process can have a `/proc/<pid>/status` entry while it exists, and that path can disappear when it exits. sysfs, usually mounted at `/sys`, represents devices, drivers, and kernel object attributes. Some attributes are writable operations with immediate effects, not passive text documents.

These views are time- and context-dependent. Two reads can disagree because the machine changed between them. A container may see a limited or virtualized view. Permissions and mount options can hide files or prevent changes. Therefore, a path's existence is evidence about one current view, not a timeless fact about the whole host.

## One example

A diagnostic says a device is missing. Inspect the relevant `/sys` device entry and the process's namespace, then compare with kernel messages or another supported device query. Do not assume an empty `/sys` path means the physical device does not exist; the process may see a restricted mount.

## Check your understanding

**Question:** Why should a script not persist its application data in `/proc`?

**Answer:** procfs is a kernel interface to live state, not ordinary persistent storage. Its entries can be generated, restricted, or vanish with processes and kernel state.
