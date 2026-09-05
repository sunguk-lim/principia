import type { GraphNode } from "./types";

export interface CodexSession {
  threadId: string;
  name: string;
  cwd: string;
  status: string;
  source: string;
  gitBranch: string;
  updatedAt: number | null;
  canContinue: boolean;
  host: string;
}

export interface CodexCatalog {
  available: boolean;
  mode: "catalog";
  sessions: CodexSession[];
}

interface Props {
  catalog: CodexCatalog;
  selected: GraphNode | null;
  refreshing: boolean;
  onRefresh: () => void;
  onClose: () => void;
}

function relativeTime(timestamp: number | null): string {
  if (!timestamp) return "Unknown activity";
  const delta = Math.max(0, Date.now() - timestamp * 1000);
  const minutes = Math.floor(delta / 60000);
  if (minutes < 1) return "Updated just now";
  if (minutes < 60) return `Updated ${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 48) return `Updated ${hours}h ago`;
  return `Updated ${Math.floor(hours / 24)}d ago`;
}

export function CodexPanel({ catalog, selected, refreshing, onRefresh, onClose }: Props) {
  return <aside className="node-panel codex-panel">
    <header className="panel-head"><div><span className="eyebrow">Private integration</span><h2>Codex sessions</h2></div><button className="icon-button" onClick={onClose} aria-label="Close Codex sessions">×</button></header>
    <p className="summary">Principia sessions discovered through OpenClaw’s native Codex catalog.</p>
    <div className="codex-safety"><span className="codex-dot"/><div><strong>Catalog-only mode</strong><p>Session metadata stays on this Mac and is available only from localhost or your Tailscale network.</p></div></div>
    {selected && <section className="study-card codex-context"><span className="eyebrow">Current graph context</span><strong>{selected.title}</strong><p>{selected.summary}</p></section>}
    <section className="study-card">
      <div className="section-heading"><div><span className="eyebrow">Repository sessions</span><strong>{catalog.sessions.length} connected</strong></div><button className="codex-refresh" disabled={refreshing} onClick={onRefresh}>{refreshing ? "Refreshing…" : "Refresh"}</button></div>
      <div className="codex-session-list">{catalog.sessions.length ? catalog.sessions.map(session => <article className="codex-session" key={session.threadId}>
        <div className="codex-session-head"><div><strong>{session.name}</strong><small>{session.host}</small></div><span className={session.canContinue ? "ready" : "idle"}>{session.canContinue ? "Ready" : session.status}</span></div>
        <dl><div><dt>Branch</dt><dd>{session.gitBranch || "—"}</dd></div><div><dt>Source</dt><dd>{session.source}</dd></div><div><dt>Activity</dt><dd>{relativeTime(session.updatedAt)}</dd></div></dl>
        <code>{session.threadId}</code>
      </article>) : <p className="empty-codex">No Codex session is rooted in this Principia repository.</p>}</div>
    </section>
    <section className="codex-boundary"><strong>Why chat is not enabled yet</strong><p>The web-server process cannot reach Codex’s model endpoint through the Gateway proxy. Rather than bypass that protection or grant a browser full operator access, this first integration remains read-only.</p><p>A dedicated restricted agent is the safe next step if you want in-app conversation.</p></section>
  </aside>;
}
