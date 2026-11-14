# Process Environment

## Meaning

An environment supplies configuration as name-value strings to a program. It belongs to a running [[process]], not to the computer as one universally synchronized dictionary. A shell can keep a variable private or export it to programs it launches. That distinction explains why a setting visible in one terminal may be absent from a worker.

## Mechanism

A launcher chooses the environment passed to the new program image. It may inherit entries, override selected names or construct a minimal environment. Existing children do not automatically receive later parent changes, and unrelated shells do not update one another. An application can implement configuration reload, but that is a separate mechanism.

Configuration files and command arguments can also supply values. Their precedence is application-defined, so checking that an environment entry exists does not prove the application used it. Check the actual launch path and consuming program.

## One example

Shell A exports `APP_REGION=east` and launches W. A then changes its own value to west and launches V. W keeps east; V begins with west. Shell B exports north, but neither worker changes. A service manager launching W could instead provide its own environment, independent of both terminals.

Test the behavior with harmless sentinel values, not live credentials. Compare an inherited launch, an explicit override and a worker already running before the change. Record only the relevant non-sensitive setting rather than dumping every environment entry. Missing and empty values also need distinct treatment when the application gives them different meanings.

## Check your understanding

Does restarting W from an unchanged service configuration import A's latest export? Not necessarily. The service manager's launch configuration, rather than A's interactive shell, may remain the source. A secret in an environment is still readable by the receiving code and potentially its descendants or diagnostics; inheritance is not encryption.
