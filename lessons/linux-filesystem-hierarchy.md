# Linux Filesystem Hierarchy

## Meaning

The Linux filesystem hierarchy is a map of conventional purposes for paths beneath `/`. It helps an operator decide where to look first, but it is not a guarantee that a particular service stores a particular file there. A mount, container, distribution, or package configuration can change the effective layout.

## Mechanism

The [[vfs]] presents one path tree even when entries come from different filesystems. The Filesystem Hierarchy Standard describes common purposes: `/etc` for host-specific configuration, `/usr` for largely shareable installed software, `/var` for variable state, `/run` for runtime state, `/home` for ordinary home directories, and `/tmp` for temporary files. Paths such as `/proc` and `/sys` expose live kernel-backed information rather than ordinary persistent data.

The distinction to remember is *purpose and lifetime*. Configuration should be found from the service's actual settings, persistent data should survive a restart or reboot as required, and temporary state should not be relied on after its lifecycle ends. A directory name tells you where to investigate; observation tells you what is really happening.

## One example

A service fails after reboot. Its data is expected under `/var/lib/example`. Check the service's effective configuration and mounts, then inspect whether the data path is on a persistent volume. Seeing `/var/lib` in a path is not enough: a container could mount it differently or a package could override the location. Verify the actual files and permissions before changing anything.

## Check your understanding

**Question:** Why is `/var/log` not a complete answer to “where are this service's logs?”

**Answer:** The service may use journald, a configured alternative path, a container log driver, or remote collection. Follow its effective configuration and observe a fresh event.
