# Secret Output Redaction

## Meaning

Redaction removes or transforms sensitive content before an output reaches an audience or store that should not receive it. It applies to credentials as well as confidential or personal information. Hiding a value in the final interface cannot undo an earlier raw export.

## Mechanism

First avoid collecting unnecessary content. Then define permitted fields before emitting each [[log-record]] and [[trace-span]]. An allowlist can retain status and correlation identifiers while dropping authentication headers. Free-form errors, subprocess output and nested bodies require their own checks; filtering one attributes dictionary does not sanitize every path.

Apply filtering before storage and before each independent exporter. Replacing a value with a marker loses diagnostic detail, while hashing preserves equality but can expose guessable low-entropy inputs. A non-sensitive reference version is often more useful than a derivative of the credential itself. Redaction does not revoke a credential or grant permission to disclose its input elsewhere.

## One example

A worker's success log includes request ID and status only. On failure, however, its HTTP exception serializes all request headers. That error path can disclose the credential despite a clean success path. The boundary instead emits `request_id=r17`, `status=403` and `credential_ref=reader-v3`, omitting raw headers and unsafe exception text before storage.

Place a fake canary in an error, nested JSON, stderr and a trace attribute. Check every exported artifact for its absence while verifying that useful status remains. Merely checking terminal display misses a trace collector that retained the original content. Pattern rules should also be tested against multiline and encoded forms, without claiming universal detection.

## Check your understanding

Can an unauthorized model receive confidential input if the final answer is filtered? No. The input already crossed the authorization boundary. Redaction complements access control and minimization rather than repairing an earlier disclosure.
