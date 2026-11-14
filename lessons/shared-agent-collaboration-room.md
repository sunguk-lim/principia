# Shared Agent Collaboration Room

## Meaning

A shared room lets people address agents and inspect relevant conversation without a person relaying every terminal interaction. It exposes [[multi-agent-orchestration]] through a team interface, but the agents can still execute elsewhere. A room is neither the worker process nor the authoritative record of task completion.

## Mechanism

Distinguish the human requester, room, logical agent and execution attempt. A persistent handle identifies the agent to message; [[agent-workload-identity]] identifies the software principal that can perform resource operations. Delivery acknowledgment does not establish that the requested work succeeded.

Use a [[durable-agent-task-board]] to retain ownership, dependencies, accepted artifact revisions and evidence-backed completion outside optimistic prose. Define duplicate-message and reconnect policies. Check membership, sending permission, history visibility, attached-file access and tool authority separately. A worker present in both public and private rooms must check disclosure scope before relaying information.

Local workers can coexist with hosted message queues and file storage. Model calls and external tools add more data recipients. Therefore “runs locally” does not establish that conversations and shared artifacts stay local.

## One example

Researcher R receives task T in room A and produces artifact revision 4. Reviewer V accepts that revision. An operations agent posts an authorized summary to room B, whose audience is broader. It checks the summary's disclosure scope rather than forwarding A's whole transcript. A repeated delivery of T must not silently create a second owner.

Test wrong-room files, revoked membership, stale history permissions, worker reconnects and artifact-version mismatches. Compare with a direct single-agent interface on handoff loss, false completion, disclosure, latency and cost. Role labels alone do not create independent checking or justify more workers.

## Check your understanding

Does an inbox acknowledgment prove T completed? No. It proves a defined delivery stage. Completion needs the declared acceptance criterion and observed evidence for the relevant task attempt and revision.
