import { marked } from "marked";
import { useMemo, useState } from "react";
import type { GraphNode, StatusMap, StudyStatus, StoreMode } from "./types";
import { emptyStatus, statusLabel } from "./types";
import { learningRoadmap, nextStudyNode } from "./graph-utils";

interface Props {
  node: GraphNode;
  byId: Map<string, GraphNode>;
  statuses: StatusMap;
  mode: StoreMode;
  onClose: () => void;
  onSelect: (id: string) => void;
  onSave: (id: string, value: StudyStatus) => Promise<void>;
}

function markdown(body: string): string {
  const linked = body
    .replace(/\[\[([a-z0-9][a-z0-9-]*)(?:\|([^\]]+))?\]\]/g, (_m, id, label) => `[${label || id.replaceAll("-", " ")}](#node=${id})`)
    .replace(/\]\(([a-z0-9][a-z0-9-]*\.svg)\)/g, "](./node-assets/$1)");
  return marked.parse(linked, { gfm: true }) as string;
}

export function NodePanel({ node, byId, statuses, mode, onClose, onSelect, onSave }: Props) {
  const initial = statuses[node.id] || emptyStatus();
  const [draft, setDraft] = useState<StudyStatus>(initial);
  const [saving, setSaving] = useState(false);
  const roadmap = useMemo(() => learningRoadmap(node.id, byId), [node.id, byId]);
  const prerequisites = useMemo(() => node.prereqs.map(id => byId.get(id)).filter((item): item is GraphNode => Boolean(item)), [node, byId]);
  const dependents = useMemo(() => [...byId.values()].filter(item => item.prereqs.includes(node.id)).sort((a, b) => a.title.localeCompare(b.title)), [node.id, byId]);
  const next = nextStudyNode(roadmap, statuses);

  const save = async () => {
    setSaving(true);
    try { await onSave(node.id, draft); } finally { setSaving(false); }
  };
  return <aside className="node-panel">
    <header className="panel-head"><div><span className="eyebrow">{node.root} · level {node.level}</span><h2>{node.title}</h2></div><button className="icon-button" onClick={onClose} aria-label="Close">×</button></header>
    <p className="summary">{node.summary}</p>
    <section className="study-card relationship-card">
      <div className="section-heading"><div><span className="eyebrow">Direct relationships</span><strong>Arrows lead toward prerequisites</strong></div></div>
      <div className="relation-group"><span className="relation-label prerequisite">Requires · {prerequisites.length}</span><div className="relation-chips">{prerequisites.length ? prerequisites.map(item => <button key={item.id} onClick={() => onSelect(item.id)}>{item.title}</button>) : <span className="empty-relation">Foundation node</span>}</div></div>
      <div className="relation-group"><span className="relation-label dependent">Unlocks · {dependents.length}</span><div className="relation-chips">{dependents.length ? dependents.map(item => <button key={item.id} onClick={() => onSelect(item.id)}>{item.title}</button>) : <span className="empty-relation">No direct dependents</span>}</div></div>
    </section>
    <section className="study-card">
      <div className="section-heading"><div><span className="eyebrow">Learning roadmap</span><strong>{roadmap.length} concepts</strong></div>{next && <button className="next-button" onClick={() => onSelect(next.id)}>Study next</button>}</div>
      <div className="roadmap">{roadmap.map((item, index) => <button key={item.id} className={`roadmap-row ${item.id === node.id ? "current" : ""}`} onClick={() => onSelect(item.id)}><span className="roadmap-index">{index + 1}</span><span className="roadmap-title">{item.title}</span><span className={`status-pill ${statuses[item.id]?.status || "not_started"}`}>{statusLabel(statuses[item.id])}</span></button>)}</div>
    </section>
    <section className="study-card"><div className="section-heading"><div><span className="eyebrow">Private study state</span><strong>{mode === "server" ? "SQLite on this Mac" : "Stored on this device"}</strong></div></div>
      <label>Status<select value={draft.status} onChange={e => setDraft({ ...draft, status: e.target.value as StudyStatus["status"] })}><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select></label>
      {draft.status === "custom" && <label>Custom label<input value={draft.custom_label} maxLength={80} onChange={e => setDraft({ ...draft, custom_label: e.target.value })} /></label>}
      <label>Private note<textarea value={draft.note} maxLength={4000} onChange={e => setDraft({ ...draft, note: e.target.value })} /></label>
      <button className="primary-button" disabled={saving || (draft.status === "custom" && !draft.custom_label.trim())} onClick={save}>{saving ? "Saving…" : "Save progress"}</button>
    </section>
    {node.hasFigure && <img className="node-figure" src={`./node-assets/${node.id}.svg`} alt={`${node.title} diagram`} />}
    <article className="markdown" onClick={e => { const anchor=(e.target as HTMLElement).closest("a"); const match=anchor?.getAttribute("href")?.match(/^#node=(.+)$/); if(match){e.preventDefault();onSelect(match[1])}}} dangerouslySetInnerHTML={{ __html: markdown(node.body) }} />
  </aside>;
}
