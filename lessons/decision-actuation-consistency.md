# Decision–Actuation Consistency

## Meaning

A decision is not complete when a model or rule computes a value. It is complete only under a stated policy for how the downstream system applies and exposes that value. A computed command, an accepted command, an applied effect, and a user-visible result can be different states.

## Mechanism

Track a version across proposed, accepted, applied, and observed stages. [[ml-system-freshness]] asks how old the information was when a decision was served; decision–actuation consistency asks whether that served decision matches the effect people or devices actually see. Device Shadow systems illustrate the distinction between desired and reported state. A reported state is stronger evidence than command acceptance, although even a device report may need independent checks for high-impact actions.

Set a publication rule and a failure rule. One system may stage a version until required actuators acknowledge it. Another may permit a bounded mismatch with a visible fallback. Retries should be idempotent and versioned so they do not apply the wrong decision. A fast data pipeline cannot overcome an actuator with a slow or unreliable update path.

## One example

A service computes a new public value while a downstream display is offline. Publishing the new value in one channel immediately can create inconsistent observations. Keep the old version visible, or explicitly expose the mismatch under a bounded policy, until the display reports the change. Test delayed and duplicated acknowledgments before relying on the flow.

## Check your understanding

**Question:** Does “command accepted” prove a physical change occurred?

**Answer:** No. Acceptance records intent or queueing; verify applied and observed state separately, with timeouts and recovery for missing reports.
