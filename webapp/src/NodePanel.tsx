import { useMemo, useState } from "react";
import type { GraphNode, StatusMap, StudyStatus, StoreMode } from "./types";
import { emptyStatus, statusLabel } from "./types";
import { learningRoadmap, nextStudyNode } from "./graph-utils";
import { renderMarkdown } from "./markdown";
import { lessonSteps } from "./lesson";

interface Props {
  node: GraphNode;
  byId: Map<string, GraphNode>;
  statuses: StatusMap;
  mode: StoreMode;
  onClose: () => void;
  onSelect: (id: string) => void;
  onSave: (id: string, value: StudyStatus) => Promise<void>;
  onOpenCopilot?: () => void;
}

export function NodePanel({ node, byId, statuses, mode, onClose, onSelect, onSave, onOpenCopilot }: Props) {
  const initial = statuses[node.id] || emptyStatus();
  const [draft, setDraft] = useState<StudyStatus>(initial);
  const [saving, setSaving] = useState(false);
  const [step, setStep] = useState(0);
  const steps = useMemo(() => lessonSteps(node.lesson || node.body), [node]);
  const roadmapResult = useMemo(() => {
    try { return { nodes: learningRoadmap(node.id, byId, statuses), error: "" }; }
    catch (error) { return { nodes: [], error: String(error) }; }
  }, [node.id, byId, statuses]);
  const roadmap = roadmapResult.nodes;
  const prerequisites = useMemo(() => node.prereqs.map(id => byId.get(id)).filter((item): item is GraphNode => Boolean(item)), [node, byId]);
  const dependents = useMemo(() => [...byId.values()].filter(item => item.prereqs.includes(node.id)).sort((a, b) => a.title.localeCompare(b.title)), [node.id, byId]);
  const next = nextStudyNode(roadmap, statuses);

  const save = async () => {
    setSaving(true);
    try { await onSave(node.id, draft); } finally { setSaving(false); }
  };
  return <aside className="node-panel">
    <header className="panel-head"><div><span className="eyebrow">{node.root} · level {node.level}</span><h2>{node.title}</h2></div><div className="panel-actions">{onOpenCopilot && <button className="ask-codex" onClick={onOpenCopilot}>Ask Copilot</button>}<button className="icon-button" onClick={onClose} aria-label="Close">×</button></div></header>
    <p className="summary">{node.summary}</p>
    {!!node.aliases?.length && <p className="alias-line">Also known as: {node.aliases.join(" · ")}</p>}
    <section className="study-card lesson-card">
      <span className="eyebrow">{node.lessonReviewed ? "Core lesson" : "Guided reading"} · Step {step + 1} of {steps.length} · ~{steps[step].minutes} min</span>
      <p className="lesson-objective">{node.objective || node.summary}</p>
      <progress aria-label="Reading progress" value={step + 1} max={steps.length} />
      <h3>{steps[step].title}</h3>
      <article className="markdown" onClick={e => { const anchor=(e.target as HTMLElement).closest("a"); const match=anchor?.getAttribute("href")?.match(/^#node=(.+)$/); if(match){e.preventDefault();onSelect(match[1])}}} dangerouslySetInnerHTML={{__html: renderMarkdown(steps[step].body)}} />
      <div className="lesson-navigation"><button disabled={step === 0} onClick={() => setStep(step - 1)}>Previous</button>{step < steps.length - 1 ? <button className="primary-button" onClick={() => setStep(step + 1)}>Continue</button> : <button className="primary-button" disabled={saving || initial.status === "done"} onClick={async () => { setSaving(true); try { await onSave(node.id, {...initial, status: "done", custom_label: ""}); } finally {setSaving(false);} }}>{initial.status === "done" ? "Completed" : saving ? "Saving…" : "Mark understood"}</button>}</div>
      {!node.lessonReviewed && <p className="reading-note">The existing explanation is divided into reading steps. A concise editorial review is still pending.</p>}
    </section>
    <details className="study-card relationship-card"><summary>Prerequisites and connections</summary>
      <div className="section-heading"><div><span className="eyebrow">Direct relationships</span><strong>Arrows lead toward prerequisites</strong></div></div>
      <div className="relation-group"><span className="relation-label prerequisite">Requires · {prerequisites.length}</span><div className="relation-chips">{prerequisites.length ? prerequisites.map(item => <div key={item.id}><button onClick={() => onSelect(item.id)}>{item.title}</button><small className="relation-reason">{node.prerequisiteReasons?.[item.id] || "Existing prerequisite — rationale not yet reviewed."}</small></div>) : <span className="empty-relation">Foundation node</span>}</div></div>
      <div className="relation-group"><span className="relation-label dependent">Unlocks · {dependents.length}</span><div className="relation-chips">{dependents.length ? dependents.map(item => <button key={item.id} onClick={() => onSelect(item.id)}>{item.title}</button>) : <span className="empty-relation">No direct dependents</span>}</div></div>
      {!!node.relations?.length && <div className="relation-group"><span className="relation-label">Optional connections — not prerequisites</span>{node.relations.map(r => <div key={r.type + r.t}><button onClick={() => onSelect(r.t)}>{r.type.toLowerCase().replaceAll("_", " ")} · {byId.get(r.t)?.title || r.t}</button><small className="relation-reason">{r.reason}</small></div>)}</div>}
    </details>
    <details className="study-card"><summary>Learning roadmap · {roadmap.length} steps remaining</summary>
      {roadmapResult.error && <p role="alert">This roadmap needs repair: {roadmapResult.error}</p>}
      <div className="section-heading"><div><span className="eyebrow">Required learning only</span><strong>{roadmapResult.error ? "Roadmap unavailable" : roadmap.length ? "Foundations → your goal" : "You have completed this goal"}</strong></div>{next && <button className="next-button" onClick={() => onSelect(next.id)}>Study next</button>}</div>
      <div className="roadmap">{roadmap.map((item, index) => <button key={item.id} className={`roadmap-row ${item.id === node.id ? "current" : ""}`} onClick={() => onSelect(item.id)}><span className="roadmap-index">{index + 1}</span><span className="roadmap-title">{item.title}</span><span className={`status-pill ${statuses[item.id]?.status || "not_started"}`}>{statusLabel(statuses[item.id])}</span></button>)}</div>
    </details>
    <details className="study-card"><summary>Notes and progress</summary><div className="section-heading"><div><span className="eyebrow">Private study state</span><strong>{mode === "server" ? "Saved privately" : "Stored on this device"}</strong></div></div>
      <label>Status<select value={draft.status} onChange={e => setDraft({ ...draft, status: e.target.value as StudyStatus["status"] })}><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select></label>
      {draft.status === "custom" && <label>Custom label<input value={draft.custom_label} maxLength={80} onChange={e => setDraft({ ...draft, custom_label: e.target.value })} /></label>}
      <label>Private note<textarea value={draft.note} maxLength={4000} onChange={e => setDraft({ ...draft, note: e.target.value })} /></label>
      <button className="primary-button" disabled={saving || (draft.status === "custom" && !draft.custom_label.trim())} onClick={save}>{saving ? "Saving…" : "Save progress"}</button>
    </details>
    <details className="study-card"><summary>Full reference and diagrams</summary>
    {node.hasFigure && <img className="node-figure" src={`./node-assets/${node.id}.svg`} alt={`${node.title} diagram`} />}
    <article className="markdown" onClick={e => { const anchor=(e.target as HTMLElement).closest("a"); const match=anchor?.getAttribute("href")?.match(/^#node=(.+)$/); if(match){e.preventDefault();onSelect(match[1])}}} dangerouslySetInnerHTML={{ __html: renderMarkdown(node.body) }} />
    </details>
  </aside>;
}
