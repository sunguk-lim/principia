import { useEffect, useMemo, useState } from "react";
import { GraphCanvas } from "./GraphCanvas";
import { NodePanel } from "./NodePanel";
import { CopilotPanel, type CopilotStatus } from "./CopilotPanel";
import { loadStatuses, saveStatus } from "./status-store";
import { emptyStatus, statusLabel, type GraphData, type GraphNode, type StatusMap, type StoreMode, type StudyStatus } from "./types";

const ROOT_COLORS: Record<string,string> = { ml:"#8b9cff", math:"#f4c95d", os:"#55d6be", gpu:"#ff8a65", databases:"#d48cff", algorithms:"#65a8ff", networking:"#ff6b91", observability:"#7ee787", languages:"#c9a0ff", "parallel-computing":"#55c2ff" };

export default function App() {
  const [data, setData] = useState<GraphData | null>(null);
  const [statuses, setStatuses] = useState<StatusMap>({});
  const [mode, setMode] = useState<StoreMode>("device");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [root, setRoot] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  const [menuOpen, setMenuOpen] = useState(false);
  const [focusDepth, setFocusDepth] = useState<1 | 2>(1);
  const [copilotStatus, setCopilotStatus] = useState<CopilotStatus | null>(null);
  const [copilotOpen, setCopilotOpen] = useState(false);

  useEffect(() => {
    fetch("/api/copilot/status").then(response => response.ok ? response.json() : null).then(status => {
      if (status?.available) setCopilotStatus(status);
    }).catch(() => { /* Static builds intentionally have no private copilot API. */ });
  }, []);

  useEffect(() => {
    Promise.all([
      fetch("./data/graph.json").then(response => { if (!response.ok) throw new Error("Graph data unavailable"); return response.json(); }),
      loadStatuses(),
    ]).then(([graph, study]) => { setData(graph); setStatuses(study.statuses); setMode(study.mode); }).catch(error => console.error(error));
  }, []);

  const byId = useMemo(() => new Map((data?.nodes || []).map(node => [node.id, node])), [data]);
  const roots = useMemo(() => [...new Set((data?.nodes || []).map(node => node.root))].sort(), [data]);
  const visibleNodes = useMemo(() => {
    if (!data) return [];
    const needle = query.trim().toLowerCase();
    return data.nodes.filter(node => {
      const study = statuses[node.id]?.status || "not_started";
      return (root === "all" || node.root === root) && (statusFilter === "all" || study === statusFilter) && (!needle || `${node.title} ${node.id} ${node.summary} ${node.tags.join(" ")}`.toLowerCase().includes(needle));
    });
  }, [data, query, root, statusFilter, statuses]);
  const visibleIds = useMemo(() => new Set(visibleNodes.map(node => node.id)), [visibleNodes]);
  const selected = selectedId ? byId.get(selectedId) || null : null;
  const done = Object.values(statuses).filter(value => value.status === "done").length;
  const active = Object.values(statuses).filter(value => value.status === "in_progress").length;

  const selectNode = (id: string) => { setSelectedId(id); setMenuOpen(false); };
  const save = async (id: string, value: StudyStatus) => {
    const saved = await saveStatus(id, value, statuses);
    setStatuses(current => ({ ...current, [id]: saved }));
  };

  if (!data) return <div className="loading"><div className="orb" /><strong>Assembling the knowledge graph…</strong></div>;
  return <div className="shell">
    <header className="topbar"><button className="mobile-menu" onClick={() => setMenuOpen(!menuOpen)}>Explore</button><div className="wordmark"><span className="mark">P</span><div><strong>Principia</strong><small>Knowledge that compounds</small></div></div><div className="top-stats"><span><b>{data.nodes.length}</b> concepts</span><span><b>{data.edges.length}</b> connections</span><span className="progress"><i style={{ width: `${Math.round(done / data.nodes.length * 100)}%` }} /><b>{done}</b> studied</span></div>{copilotStatus?.available && <button className="codex-launch" onClick={() => setCopilotOpen(true)}><i/>Copilot</button>}</header>
    <aside className={`explorer ${menuOpen ? "open" : ""}`}><div className="explorer-head"><span className="eyebrow">Explore</span><button className="close-mobile" onClick={() => setMenuOpen(false)}>×</button><h1>Choose what to learn next.</h1><p>Follow prerequisites from foundations to the concepts that depend on them.</p></div>
      <input className="search" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search concepts, fields, ideas…" />
      <div className="filter-row"><select value={root} onChange={e => setRoot(e.target.value)}><option value="all">All fields</option>{roots.map(value => <option key={value}>{value}</option>)}</select><select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}><option value="all">All progress</option><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select></div>
      <div className="study-summary"><span><b>{active}</b> in progress</span><span><b>{done}</b> done</span><span><b>{visibleNodes.length}</b> visible</span></div>
      <div className="node-list">{visibleNodes.slice(0, 160).map(node => <button key={node.id} className={`node-row ${node.id === selectedId ? "active" : ""}`} onClick={() => selectNode(node.id)}><i style={{ background: ROOT_COLORS[node.root] || "#8b9cff" }} /><span><strong>{node.title}</strong><small>{node.root} · L{node.level}</small></span><em className={statuses[node.id]?.status || "not_started"}>{statusLabel(statuses[node.id] || emptyStatus())}</em></button>)}</div>
    </aside>
    <main className={`graph-stage ${selected || copilotOpen ? "panel-open" : ""}`}><GraphCanvas data={data} statuses={statuses} selectedId={selectedId} visibleIds={visibleIds} focusDepth={focusDepth} onSelect={selectNode} onClear={() => setSelectedId(null)} />
      {selected && <div className="relationship-toolbar"><div><span className="eyebrow">Relationship focus</span><strong>{selected.title}</strong></div><div className="depth-toggle"><button className={focusDepth === 1 ? "active" : ""} onClick={() => setFocusDepth(1)}>Direct</button><button className={focusDepth === 2 ? "active" : ""} onClick={() => setFocusDepth(2)}>2 steps</button><button onClick={() => setSelectedId(null)}>Overview</button></div></div>}
      <div className={`graph-hud ${selected ? "focused" : ""}`}><span>{selected ? "Arrows point from a concept to what it requires" : "Hover to preview relationships · select to focus"}</span>{selected ? <div className="relation-legend"><i className="prerequisite"/>Prerequisite <i className="dependent"/>Dependent <i className="context"/>Context</div> : <div className="legend"><i className="not_started"/>Not started<i className="in_progress"/>In progress<i className="blocked"/>Blocked<i className="done"/>Done</div>}</div>
    </main>
    {copilotOpen && copilotStatus ? <CopilotPanel status={copilotStatus} selected={selected} onClose={() => setCopilotOpen(false)} /> : selected && <NodePanel key={selected.id + (statuses[selected.id]?.updated_at || "")} node={selected} byId={byId} statuses={statuses} mode={mode} onClose={() => setSelectedId(null)} onSelect={selectNode} onSave={save} onOpenCopilot={copilotStatus?.available ? () => setCopilotOpen(true) : undefined} />}
    {menuOpen && <button className="scrim" aria-label="Close explorer" onClick={() => setMenuOpen(false)} />}
  </div>;
}
