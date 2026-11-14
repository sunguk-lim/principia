# Snapshot-Based Change Monitoring

## Meaning

A monitor compares captured observations under a stable policy. It does not continuously know the source's true state. A second manual capture demonstrates a comparison, not that a schedule or alerting service operated between the two observations.

## Mechanism

Keep source identity, capture time, retrieval result, extraction version and accepted evidence revision. This is [[dataset-lineage]] for observations. Normalize irrelevant presentation details, compare equivalent fields and retain the before-and-after evidence. A failed or partial fetch must not silently become an empty successful baseline.

A [[periodic-agent-workflow]] defines scheduling, missed runs and duplicate effects. Changed states at two valid capture times do not establish an exact change time. With one persistent transition, the occurrence lies between the captures. A change followed by reversal can be missed entirely. Retrieval and notification delay also add to detection time.

## One example

At 09:00 a page shows 12 units per month. At 09:15 it shows 15, plus a changed footer timestamp. The extraction policy ignores the footer but retains plan, amount, currency and billing interval. Report the observed price difference between 09:00 and 09:15, not “it changed at 09:15.” A failed 09:30 fetch records an outage and leaves the accepted 09:15 baseline intact.

If a notification response is ambiguous, reconcile its delivery identifier before retrying. Keep one comparison identity across multiple delivery attempts so a retry is not counted as a new source change. Test reordered fields, missing sections, changed units and extraction upgrades. Overbroad filters can suppress important deletions, while incomplete captures can manufacture them.

## Check your understanding

Do identical snapshots prove the source never changed between them? No. Observations bound claims; they do not fill gaps. Measure missed relevant differences, false alerts and observed delivery delay separately rather than treating one successful scheduled run as continuous coverage.
