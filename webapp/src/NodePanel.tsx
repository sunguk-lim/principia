import { useEffect, useMemo, useState } from "react";
import type { GraphNode, StatusMap, StudyStatus, StoreMode } from "./types";
import { emptyStatus, statusLabel } from "./types";
import { renderMarkdown } from "./markdown";

interface EntityContent { entityId: string; signature: string; explanation: string; wordCount: number; ordinal: number; segmentCount: number; reviewed: boolean }
interface Roadmap { target: string; requiredIds: string[]; requiredEdges: { source: string; target: string; reason: string }[] }
interface Props { node: GraphNode; byId: Map<string, GraphNode>; statuses: StatusMap; mode: StoreMode; onClose: () => void; onSelect: (id: string) => void; onSave: (id: string, value: StudyStatus) => Promise<void>; onOpenCopilot?: () => void }

function orderedRoadmap(result: Roadmap, byId: Map<string, GraphNode>): GraphNode[] {
  const prerequisites = new Map(result.requiredIds.map(id => [id, [] as string[]]));
  for (const edge of result.requiredEdges) prerequisites.get(edge.source)?.push(edge.target);
  const ordered: GraphNode[] = [], seen = new Set<string>(), active = new Set<string>();
  const visit = (id: string) => {
    if (seen.has(id) || active.has(id)) return;
    active.add(id); (prerequisites.get(id) || []).forEach(visit); active.delete(id); seen.add(id);
    const entity = byId.get(id); if (entity) ordered.push(entity);
  };
  visit(result.target); return ordered;
}

export function NodePanel({ node, byId, statuses, mode, onClose, onSelect, onSave, onOpenCopilot }: Props) {
  const statusId = node.statusId || node.id;
  const initial = statuses[statusId] || emptyStatus();
  const [draft, setDraft] = useState<StudyStatus>(initial), [saving, setSaving] = useState(false), [saveError, setSaveError] = useState("");
  const [content, setContent] = useState<EntityContent | null>(null), [contentError, setContentError] = useState("");
  const [roadmapData, setRoadmapData] = useState<Roadmap | null>(null), [roadmapError, setRoadmapError] = useState("");
  useEffect(() => {
    let live = true; setContent(null); setContentError(""); setRoadmapData(null); setRoadmapError("");
    fetch(`/api/neo4j/entities/${encodeURIComponent(node.id)}`).then(r => r.ok ? r.json() : Promise.reject(new Error("Explanation unavailable"))).then(value => { if (live) setContent(value); }).catch(error => { if (live) setContentError(String(error)); });
    fetch(`/api/neo4j/roadmap/${encodeURIComponent(node.id)}`).then(r => r.ok ? r.json() : Promise.reject(new Error("Roadmap unavailable"))).then(value => { if (live) setRoadmapData(value); }).catch(error => { if (live) setRoadmapError(String(error)); });
    return () => { live = false; };
  }, [node.id]);
  const roadmap = useMemo(() => roadmapData ? orderedRoadmap(roadmapData, byId) : [], [roadmapData, byId]);
  const prerequisites = useMemo(() => node.prereqs.map(id => byId.get(id)).filter((item): item is GraphNode => Boolean(item)), [node, byId]);
  const dependents = useMemo(() => [...byId.values()].filter(item => item.prereqs.includes(node.id)).sort((a, b) => a.title.localeCompare(b.title)), [node.id, byId]);
  const persist = async (value: StudyStatus) => { setSaving(true); setSaveError(""); try { await onSave(statusId, value); } catch (error) { setSaveError(error instanceof Error ? error.message : "Could not save progress."); } finally { setSaving(false); } };
  return <aside className="node-panel">
    <header className="panel-head"><div><span className="eyebrow">{node.root} · entity</span><h2>{node.title}</h2></div><div className="panel-actions">{onOpenCopilot && <button className="ask-codex" onClick={onOpenCopilot}>Ask Copilot</button>}<button className="icon-button" onClick={onClose} aria-label="Close">×</button></div></header>
    <p className="summary">{node.summary}</p>
    {!!node.aliases?.length && <p className="alias-line">Also known as: {node.aliases.join(" · ")}</p>}
    <section className="study-card explanation-card">
      <span className="eyebrow">Explanation {content ? `· ${content.wordCount} words` : "· loading"}</span>
      {contentError && <p role="alert">{contentError}</p>}
      {content && <article className="explanation-section"><div className="markdown" dangerouslySetInnerHTML={{__html: renderMarkdown(content.explanation)}} /><p className="reading-note">Portable node {content.ordinal}/{content.segmentCount} · {content.reviewed ? "reviewed" : "automatically segmented"}</p></article>}
    </section>
    <details className="study-card relationship-card"><summary>Prerequisites and connections</summary><div className="relation-group"><span className="relation-label prerequisite">Requires · {prerequisites.length}</span><div className="relation-chips">{prerequisites.length ? prerequisites.map(item => <button key={item.id} onClick={() => onSelect(item.id)}>{item.title}</button>) : <span className="empty-relation">Foundation entity</span>}</div></div><div className="relation-group"><span className="relation-label dependent">Unlocks · {dependents.length}</span><div className="relation-chips">{dependents.map(item => <button key={item.id} onClick={() => onSelect(item.id)}>{item.title}</button>)}</div></div>{!!node.relations?.length && <div className="relation-group"><span className="relation-label">Optional connections</span>{node.relations.map(r => <div key={r.type + r.t}><button onClick={() => onSelect(r.t)}>{r.type.toLowerCase().replaceAll("_", " ")} · {byId.get(r.t)?.title || r.t}</button><small className="relation-reason">{r.reason}</small></div>)}</div>}</details>
    <details className="study-card"><summary>Live learning roadmap · {roadmapData ? `${roadmap.length} entities` : "loading"}</summary>{roadmapError && <p role="alert">{roadmapError}</p>}<div className="section-heading"><div><span className="eyebrow">Neo4j Cypher traversal</span><strong>Required learning only</strong></div></div><div className="roadmap">{roadmap.map((item, index) => { const itemStatus = statuses[item.statusId || item.id]; return <button key={item.id} className={`roadmap-row ${item.id === node.id ? "current" : ""}`} onClick={() => onSelect(item.id)}><span className="roadmap-index">{index + 1}</span><span className="roadmap-title">{item.title}</span><span className={`status-pill ${itemStatus?.status || "not_started"}`}>{statusLabel(itemStatus)}</span></button>; })}</div></details>
    <details className="study-card"><summary>Notes and progress</summary><div className="section-heading"><div><span className="eyebrow">Private study state</span><strong>{mode === "server" ? "Saved privately" : "Stored on this device"}</strong></div></div>{saveError && <p role="alert">{saveError}</p>}<label>Status<select value={draft.status} onChange={e => setDraft({ ...draft, status: e.target.value as StudyStatus["status"] })}><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select></label>{draft.status === "custom" && <label>Custom label<input value={draft.custom_label} maxLength={80} onChange={e => setDraft({ ...draft, custom_label: e.target.value })} /></label>}<label>Private note<textarea value={draft.note} maxLength={4000} onChange={e => setDraft({ ...draft, note: e.target.value })} /></label><button className="primary-button" disabled={saving || (draft.status === "custom" && !draft.custom_label.trim())} onClick={() => persist(draft)}>{saving ? "Saving…" : "Save progress"}</button></details>
  </aside>;
}
