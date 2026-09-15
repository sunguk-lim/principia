import { useEffect, useMemo, useState } from "react";
import { GraphCanvas } from "./GraphCanvas";
import { NodePanel } from "./NodePanel";
import { loadStatuses, saveStatus } from "./status-store";
import { emptyStatus, statusLabel, type GraphData, type GraphNode, type StatusMap, type StoreMode, type StudyStatus } from "./types";
import { canonicalNodeId } from "./graph-utils";

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

  useEffect(() => {
    Promise.all([
      fetch("/api/neo4j/graph").then(response => { if (!response.ok) throw new Error("Neo4j graph unavailable"); return response.json(); }),
      loadStatuses(),
    ]).then(([graph, study]) => { setData(graph); setStatuses(study.statuses); setMode(study.mode); }).catch(error => console.error(error));
  }, []);

  const allById = useMemo(() => new Map((data?.nodes || []).map(node => [node.id, node])), [data]);
  const canonicalNodes = useMemo(() => (data?.nodes || []).filter(node => node.isCanonical !== false), [data]);
  const byId = useMemo(() => new Map(canonicalNodes.map(node => [node.id, node])), [canonicalNodes]);
  const statusFor = (node: GraphNode) => statuses[node.statusId || node.id] || emptyStatus();
  const roots = useMemo(() => [...new Set(canonicalNodes.map(node => node.root))].sort(), [canonicalNodes]);
  const visibleNodes = useMemo(() => {
    if (!data) return [];
    const needle = query.trim().toLowerCase();
    return canonicalNodes.filter(node => {
      const study = statusFor(node).status;
      return (root === "all" || node.root === root) && (statusFilter === "all" || study === statusFilter) && (!needle || `${node.title} ${node.id} ${(node.aliases || []).join(" ")} ${node.summary} ${node.tags.join(" ")}`.toLowerCase().includes(needle));
    });
  }, [canonicalNodes, query, root, statusFilter, statuses]);
  const visibleIds = useMemo(() => new Set(visibleNodes.map(node => node.id)), [visibleNodes]);
  const selected = selectedId ? byId.get(selectedId) || null : null;
  const done = canonicalNodes.filter(node => statusFor(node).status === "done").length;
  const active = canonicalNodes.filter(node => statusFor(node).status === "in_progress").length;

  const selectNode = (id: string) => { setSelectedId(canonicalNodeId(id, allById)); setMenuOpen(false); };

  useEffect(() => {
    const readHash = () => {
      const match = window.location.hash.match(/^#node=(.+)$/);
      if (match && allById.has(match[1])) selectNode(match[1]);
    };
    readHash(); window.addEventListener("hashchange", readHash);
    return () => window.removeEventListener("hashchange", readHash);
  }, [allById]);
  const save = async (id: string, value: StudyStatus) => {
    const saved = await saveStatus(id, value, statuses);
    setStatuses(current => ({ ...current, [id]: saved }));
  };

  if (!data) return <div className="loading"><div className="orb" /><strong>Assembling the knowledge graph…</strong></div>;
  return <div className="shell">
    <header className="topbar"><button className="mobile-menu" onClick={() => setMenuOpen(!menuOpen)}>Explore</button><div className="wordmark"><span className="mark">P</span><div><strong>Principia</strong><small>Neo4j learning graph</small></div></div><div className="top-stats"><span><b>{canonicalNodes.length}</b> entities</span><span><b>{data.edges.length}</b> requirements</span><span className="progress"><i style={{ width: `${Math.round(done / canonicalNodes.length * 100)}%` }} /><b>{done}</b> studied</span></div></header>
    <aside className={`explorer ${menuOpen ? "open" : ""}`}><div className="explorer-head"><span className="eyebrow">Explore</span><button className="close-mobile" onClick={() => setMenuOpen(false)}>×</button><h1>Choose what to learn next.</h1><p>Follow prerequisites from foundations to the concepts that depend on them.</p></div>
      <input className="search" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search concepts, fields, ideas…" />
      <div className="filter-row"><select value={root} onChange={e => setRoot(e.target.value)}><option value="all">All fields</option>{roots.map(value => <option key={value}>{value}</option>)}</select><select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}><option value="all">All progress</option><option value="not_started">Not started</option><option value="in_progress">In progress</option><option value="blocked">Blocked</option><option value="done">Done</option><option value="custom">Custom</option></select></div>
      <div className="study-summary"><span><b>{active}</b> in progress</span><span><b>{done}</b> done</span><span><b>{visibleNodes.length}</b> visible</span></div>
      <div className="node-list">{visibleNodes.slice(0, 160).map(node => <button key={node.id} className={`node-row ${node.id === selectedId ? "active" : ""}`} onClick={() => selectNode(node.id)}><i style={{ background: ROOT_COLORS[node.root] || "#8b9cff" }} /><span><strong>{node.title}</strong><small>{node.root} · L{node.level}</small></span><em className={statusFor(node).status}>{statusLabel(statusFor(node))}</em></button>)}</div>
    </aside>
    <main className={`graph-stage ${selected ? "panel-open" : ""}`}><GraphCanvas data={data} statuses={statuses} selectedId={selectedId} visibleIds={visibleIds} focusDepth={focusDepth} onSelect={selectNode} onClear={() => setSelectedId(null)} />
      {selected && <div className="relationship-toolbar"><div><span className="eyebrow">Relationship focus</span><strong>{selected.title}</strong></div><div className="depth-toggle"><button className={focusDepth === 1 ? "active" : ""} onClick={() => setFocusDepth(1)}>Direct</button><button className={focusDepth === 2 ? "active" : ""} onClick={() => setFocusDepth(2)}>2 steps</button><button onClick={() => setSelectedId(null)}>Overview</button></div></div>}
      <div className={`graph-hud ${selected ? "focused" : ""}`}><span>{selected ? "Arrows point from a concept to what it requires" : "Hover to preview relationships · select to focus"}</span>{selected ? <div className="relation-legend"><i className="prerequisite"/>Prerequisite <i className="dependent"/>Dependent <i className="context"/>Context</div> : <div className="legend"><i className="not_started"/>Not started<i className="in_progress"/>In progress<i className="blocked"/>Blocked<i className="done"/>Done</div>}</div>
    </main>
    {selected && <NodePanel key={selected.id + (statuses[selected.statusId || selected.id]?.updated_at || "")} node={selected} byId={byId} statuses={statuses} mode={mode} onClose={() => setSelectedId(null)} onSelect={selectNode} onSave={save} />}
    {menuOpen && <button className="scrim" aria-label="Close explorer" onClick={() => setMenuOpen(false)} />}
  </div>;
}
