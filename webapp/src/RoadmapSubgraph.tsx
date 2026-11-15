import { useMemo } from "react";
import { statusLabel, type GraphNode, type LearningRoadmap, type StatusMap } from "./types";

interface Props { roadmap: LearningRoadmap; byId: Map<string, GraphNode>; statuses: StatusMap; onSelect: (id: string) => void }
interface PositionedNode { id: string; title: string; status: string; x: number; y: number; current: boolean }

const NODE_WIDTH = 172, NODE_HEIGHT = 56, COLUMN_GAP = 54, ROW_GAP = 14, PADDING = 28;

/** A readable rank layout: goal first, then increasingly foundational concepts. */
function layoutRoadmap(roadmap: LearningRoadmap, byId: Map<string, GraphNode>, statuses: StatusMap) {
  const ids = new Set([...roadmap.requiredIds, roadmap.target]);
  const outgoing = new Map<string, string[]>();
  for (const edge of roadmap.requiredEdges) if (ids.has(edge.source) && ids.has(edge.target)) outgoing.set(edge.source, [...(outgoing.get(edge.source) || []), edge.target]);
  const rank = new Map<string, number>();
  const visit = (id: string, depth: number, path = new Set<string>()) => {
    if (path.has(id)) return;
    rank.set(id, Math.max(rank.get(id) || 0, depth));
    const nextPath = new Set(path); nextPath.add(id);
    for (const prerequisite of outgoing.get(id) || []) visit(prerequisite, depth + 1, nextPath);
  };
  visit(roadmap.target, 0);
  for (const id of ids) if (!rank.has(id)) rank.set(id, 0);
  const columns = new Map<number, string[]>();
  for (const [id, depth] of rank) columns.set(depth, [...(columns.get(depth) || []), id]);
  const maxRows = Math.max(...[...columns.values()].map(items => items.length), 1);
  const nodes: PositionedNode[] = [];
  for (const [depth, items] of [...columns.entries()].sort(([a], [b]) => a - b)) {
    items.sort((a, b) => (byId.get(a)?.title || a).localeCompare(byId.get(b)?.title || b));
    items.forEach((id, index) => {
      const node = byId.get(id);
      nodes.push({ id, title: node?.title || id, status: statusLabel(statuses[node?.statusId || id]), x: PADDING + depth * (NODE_WIDTH + COLUMN_GAP), y: PADDING + index * (NODE_HEIGHT + ROW_GAP), current: id === roadmap.target });
    });
  }
  return { nodes, width: PADDING * 2 + Math.max(...rank.values(), 0) * (NODE_WIDTH + COLUMN_GAP) + NODE_WIDTH, height: PADDING * 2 + maxRows * NODE_HEIGHT + Math.max(0, maxRows - 1) * ROW_GAP };
}

export function RoadmapSubgraph({ roadmap, byId, statuses, onSelect }: Props) {
  const graph = useMemo(() => layoutRoadmap(roadmap, byId, statuses), [roadmap, byId, statuses]);
  const position = new Map(graph.nodes.map(node => [node.id, node]));
  return <div className="roadmap-subgraph" aria-label="Learning roadmap subgraph"><svg width={graph.width} height={graph.height} viewBox={`0 0 ${graph.width} ${graph.height}`} role="img" aria-label="Goal and required foundations">
    <defs><marker id="roadmap-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#f5b942" /></marker></defs>
    {roadmap.requiredEdges.map(edge => { const source = position.get(edge.source), target = position.get(edge.target); if (!source || !target) return null; const x1 = source.x + NODE_WIDTH, y1 = source.y + NODE_HEIGHT / 2, x2 = target.x, y2 = target.y + NODE_HEIGHT / 2; return <path key={`${edge.source}:${edge.target}`} d={`M ${x1} ${y1} C ${x1 + 24} ${y1}, ${x2 - 24} ${y2}, ${x2 - 7} ${y2}`} className="roadmap-link" markerEnd="url(#roadmap-arrow)" />; })}
    {graph.nodes.map(node => <g key={node.id} className={`roadmap-node ${node.current ? "current" : ""} ${node.status.toLowerCase().replaceAll(" ", "_")}`} transform={`translate(${node.x},${node.y})`} onClick={() => onSelect(node.id)} role="button" tabIndex={0} aria-label={`Learn ${node.title}; ${node.status}`} onKeyDown={event => { if (event.key === "Enter" || event.key === " ") onSelect(node.id); }}><rect width={NODE_WIDTH} height={NODE_HEIGHT} rx="8" /><text className="roadmap-node-title" x="11" y="23">{node.title.length > 23 ? `${node.title.slice(0, 22)}…` : node.title}</text><text className="roadmap-node-status" x="11" y="43">{node.status}</text></g>)}
  </svg></div>;
}
