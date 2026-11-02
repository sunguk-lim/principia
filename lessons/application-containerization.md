# Application Containerization

## Meaning

Application containerization packages a program and its runtime dependencies into an image with a declared startup command. The image is a reusable artifact. A running container is an instance of that artifact with runtime configuration and mutable state.

## Mechanism

A build recipe selects a base runtime, installs dependencies, copies source files, chooses a working directory and user, and declares how to start the program. Record exact source, dependency and base-image identities so a tested artifact can be identified later. A floating image tag alone is not an immutable identity.

Keep configuration and secrets separate from the packaged program. Do not copy a developer's home directory or credentials into an image. Durable user data belongs in a deliberately managed volume or external store, not only in the instance's disposable writable layer. Pinning dependencies improves repeatability, but rebuild and review them as security and compatibility requirements change.

Dependency-install layers can be reused when only application source changes. Put stable dependency inputs before frequently edited source files where that accurately reflects the build. Reuse is correct only when all necessary inputs are declared; caching cannot compensate for a hidden dependency.

## One example

Build a Python service image from base digest B, dependency set D and source revision C. Start two instances of that same image with different database addresses. The packaged program is identical, while each instance uses separate runtime configuration. If one writes uploaded files into its private writable layer, replacing that instance does not preserve those files as durable storage.

## Check your understanding

Does a container reaching the running state prove the service works? **No.** Test readiness and a real request with intended permissions and configuration. Verify network bindings, shutdown and persistent storage. Container packaging also does not remove host-kernel or CPU-architecture compatibility limits.
