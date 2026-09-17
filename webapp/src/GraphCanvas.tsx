import cytoscape, { type CollectionReturnValue, type Core, type NodeSingular } from "cytoscape";
import { useEffect, useRef } from "react";
import type { GraphData, GraphEdge, GraphEdgeType, StatusMap } from "./types";
import { statusColor } from "./graph-utils";

const rootColor = (root: string) => ({ ml:"#8b9cff", math:"#f4c95d", os:"#55d6be", gpu:"#ff8a65", databases:"#d48cff", algorithms:"#65a8ff", networking:"#ff6b91", observability:"#7ee787", languages:"#c9a0ff", "parallel-computing":"#55c2ff" } as Record<string,string>)[root] || "#8b9cff";
const FOCUS_CLASSES = "focus-muted focus-context focus-selected prerequisite-node dependent-node context-node focus-edge prerequisite-edge dependent-edge context-edge labels-hidden";

interface Props {
  data: GraphData;
  statuses: StatusMap;
  selectedId: string | null;
  visibleIds: Set<string>;
  focusDepth: 1 | 2;
  onSelect: (id: string) => void;
  onClear: () => void;
}

function typeOf(edge: cytoscape.EdgeSingular): GraphEdgeType {
  return (edge.data("type") || "REQUIRES") as GraphEdgeType;
}

function directRelations(node: NodeSingular) {
  const prerequisites = node.outgoers("edge").filter(edge => typeOf(edge as cytoscape.EdgeSingular) === "REQUIRES");
  const dependents = node.incomers("edge").filter(edge => typeOf(edge as cytoscape.EdgeSingular) === "REQUIRES");
  const contextual = node.connectedEdges().filter(edge => typeOf(edge as cytoscape.EdgeSingular) !== "REQUIRES");
  return {
    prerequisiteEdges: prerequisites,
    prerequisiteNodes: prerequisites.targets(),
    dependentEdges: dependents,
    dependentNodes: dependents.sources(),
    contextEdges: contextual,
    contextNodes: contextual.connectedNodes().not(node),
  };
}

function overviewPositions(nodes: GraphData["nodes"]) {
  const groups = new Map<string, typeof nodes>();
  for (const node of nodes) groups.set(node.root, [...(groups.get(node.root) || []), node]);
  const roots = [...groups.keys()].sort();
  const grid = Math.ceil(Math.sqrt(roots.length));
  const positions = new Map<string, { x: number; y: number }>();
  roots.forEach((root, groupIndex) => {
    const group = (groups.get(root) || []).sort((a, b) => a.level - b.level || a.title.localeCompare(b.title));
    const columns = Math.max(2, Math.ceil(Math.sqrt(group.length)));
    const originX = (groupIndex % grid) * 500;
    const originY = Math.floor(groupIndex / grid) * 500;
    group.forEach((node, index) => positions.set(node.id, {
      x: originX + 48 + (index % columns) * 42,
      y: originY + 54 + Math.floor(index / columns) * 42,
    }));
  });
  return positions;
}

function contextualEdges(nodes: GraphData["nodes"], existing: GraphEdge[]) {
  const seen = new Set(existing.map(edge => `${edge.s}:${edge.t}:REQUIRES`));
  const result: GraphEdge[] = [];
  for (const node of nodes) for (const relation of node.relations || []) {
    const key = `${node.id}:${relation.t}:${relation.type}`;
    if (!seen.has(key)) { seen.add(key); result.push({ s: node.id, t: relation.t, type: relation.type, reason: relation.reason }); }
  }
  return result;
}

function focusCollection(cy: Core, selected: NodeSingular, depth: 1 | 2): CollectionReturnValue {
  const direct = directRelations(selected);
  let nodes = selected.union(direct.prerequisiteNodes).union(direct.dependentNodes);
  let edges = direct.prerequisiteEdges.union(direct.dependentEdges);
  nodes = nodes.union(direct.contextNodes);
  edges = edges.union(direct.contextEdges);
  if (depth === 2) {
    const secondEdges = nodes.connectedEdges().filter(edge => typeOf(edge as cytoscape.EdgeSingular) === "REQUIRES");
    const secondNodes = secondEdges.connectedNodes();
    nodes = nodes.union(secondNodes);
    edges = edges.union(secondEdges.filter(edge => nodes.contains((edge as cytoscape.EdgeSingular).source()) && nodes.contains((edge as cytoscape.EdgeSingular).target())));
  }
  cy.elements().removeClass(FOCUS_CLASSES);
  cy.elements().not(nodes.union(edges)).addClass("focus-muted");
  nodes.not(selected).addClass("focus-context");
  selected.addClass("focus-selected");
  edges.addClass("focus-edge");
  direct.prerequisiteNodes.addClass("prerequisite-node");
  direct.dependentNodes.addClass("dependent-node");
  direct.prerequisiteEdges.addClass("prerequisite-edge");
  direct.dependentEdges.addClass("dependent-edge");
  direct.contextNodes.addClass("context-node");
  direct.contextEdges.addClass("context-edge");
  return nodes.union(edges);
}

export function GraphCanvas({ data, statuses, selectedId, visibleIds, focusDepth, onSelect, onClear }: Props) {
  const host = useRef<HTMLDivElement>(null);
  const graph = useRef<Core | null>(null);
  const selectRef = useRef(onSelect);
  const clearRef = useRef(onClear);
  const selectedRef = useRef(selectedId);
  selectRef.current = onSelect;
  clearRef.current = onClear;
  selectedRef.current = selectedId;

  useEffect(() => {
    if (!host.current) return;
    const nodes = data.nodes.filter(node => node.isCanonical !== false);
    const ids = new Set(nodes.map(node => node.id));
    const requiredEdges = data.edges.filter(edge => ids.has(edge.s) && ids.has(edge.t)).map(edge => ({ ...edge, type: "REQUIRES" as const }));
    const optionalEdges = contextualEdges(nodes, requiredEdges).filter(edge => ids.has(edge.s) && ids.has(edge.t));
    const positions = overviewPositions(nodes);
    const cy = cytoscape({
      container: host.current,
      elements: [
        ...nodes.map(node => ({ data: { id: node.id, statusId: node.statusId || node.id, label: node.title, root: node.root, rootColor: rootColor(node.root), type: node.type, level: node.level }, position: positions.get(node.id) })),
        ...[...requiredEdges, ...optionalEdges].map((edge, index) => ({ data: { id: `e${index}`, source: edge.s, target: edge.t, type: edge.type, reason: edge.reason || "" } })),
      ],
      minZoom: .08, maxZoom: 3.2, wheelSensitivity: .18,
      style: [
        { selector: "node", style: { "background-color": "data(rootColor)", "border-width": 1.5, "border-color": "#667085", label: "data(label)", color: "#dce7f7", "font-size": 8, "min-zoomed-font-size": 6, "text-opacity": .68, "text-outline-width": 2, "text-outline-color": "#0b1020", "text-valign": "bottom", "text-margin-y": 6, width: 16, height: 16 } },
        { selector: 'node[type="axiom"]', style: { shape: "diamond", width: 12, height: 12 } },
        { selector: "edge", style: { width: .65, "line-color": "#344054", "target-arrow-shape": "none", "curve-style": "bezier", opacity: .16 } },
        { selector: 'edge[type="REQUIRES"]', style: { "line-color": "#42546e", opacity: .24 } },
        { selector: 'edge[type="ALTERNATIVE_TO"]', style: { "line-color": "#a58bff", "line-style": "dashed", opacity: .07 } },
        { selector: 'edge[type="CONTRASTS_WITH"]', style: { "line-color": "#ff8a65", "line-style": "dotted", opacity: .07 } },
        { selector: 'edge[type="APPLIES_TO"]', style: { "line-color": "#6f8099", "line-style": "dotted", opacity: .05 } },
        { selector: 'edge[type="USES"]', style: { "line-color": "#6f8099", "line-style": "dotted", opacity: .05 } },
        { selector: ".labels-hidden", style: { "text-opacity": 0 } },
        { selector: ".filtered", style: { opacity: .025, "text-opacity": 0 } },
        { selector: ".focus-muted", style: { opacity: .035, "text-opacity": 0 } },
        { selector: "node.focus-context", style: { opacity: .78, "text-opacity": .9 } },
        { selector: "node.prerequisite-node", style: { opacity: 1, "border-width": 4, "border-color": "#f5b942", "text-opacity": 1, "z-index": 12 } },
        { selector: "node.dependent-node", style: { opacity: 1, "border-width": 4, "border-color": "#55c2ff", "text-opacity": 1, "z-index": 12 } },
        { selector: "node.context-node", style: { opacity: .94, "border-width": 3, "border-color": "#a58bff", "text-opacity": 1, "z-index": 11 } },
        { selector: "node.focus-selected", style: { opacity: 1, "border-width": 5, "border-color": "#ffffff", width: 25, height: 25, "font-size": 11, "text-opacity": 1, "z-index": 20 } },
        { selector: "edge.focus-edge", style: { opacity: .58, width: 1.4, "line-color": "#667085", "target-arrow-color": "#667085", "target-arrow-shape": "triangle", "arrow-scale": .7, "z-index": 8 } },
        { selector: "edge.prerequisite-edge", style: { opacity: 1, width: 3, "line-color": "#f5b942", "target-arrow-color": "#f5b942", "arrow-scale": .95, "z-index": 15 } },
        { selector: "edge.dependent-edge", style: { opacity: 1, width: 3, "line-color": "#55c2ff", "target-arrow-color": "#55c2ff", "arrow-scale": .95, "z-index": 15 } },
        { selector: "edge.context-edge", style: { opacity: .82, width: 1.7, "line-color": "#a58bff", "line-style": "dashed", "target-arrow-shape": "none", "z-index": 12 } },
      ],
      // The overview is a stable domain map, not a global force simulation.
      // Physics hides the learning direction and becomes unreadable as the
      // catalog grows. A selected neighbourhood gets a directional layout.
      layout: { name: "preset", fit: true, padding: 32 },
    });
    const setLabelDensity = () => cy.nodes().toggleClass("labels-hidden", cy.zoom() < .45);
    setLabelDensity(); cy.on("zoom", setLabelDensity);
    cy.on("tap", "node", event => selectRef.current(event.target.id()));
    cy.on("tap", event => { if (event.target === cy) clearRef.current(); });
    cy.on("mouseover", "node", event => {
      if (selectedRef.current) return;
      const node = event.target as NodeSingular;
      const relations = directRelations(node);
      const related = node.union(relations.prerequisiteNodes).union(relations.dependentNodes).union(relations.prerequisiteEdges).union(relations.dependentEdges);
      cy.elements().not(related).addClass("focus-muted");
      node.addClass("focus-selected");
      relations.prerequisiteNodes.addClass("prerequisite-node");
      relations.dependentNodes.addClass("dependent-node");
      relations.prerequisiteEdges.addClass("focus-edge prerequisite-edge");
      relations.dependentEdges.addClass("focus-edge dependent-edge");
      relations.contextNodes.addClass("context-node");
      relations.contextEdges.addClass("focus-edge context-edge");
    });
    cy.on("mouseout", "node", () => { if (!selectedRef.current) cy.elements().removeClass(FOCUS_CLASSES); });
    graph.current = cy;
    return () => { cy.destroy(); graph.current = null; };
  }, [data]);

  useEffect(() => {
    const cy = graph.current; if (!cy) return;
    cy.nodes().forEach(node => {
      node.toggleClass("filtered", !visibleIds.has(node.id()));
      const status = statuses[String(node.data("statusId"))];
      node.style("border-color", statusColor(status?.status));
      node.style("border-width", status?.status && status.status !== "not_started" ? 4 : 1.5);
    });
    cy.edges().forEach(edge => { edge.toggleClass("filtered", !visibleIds.has(edge.source().id()) || !visibleIds.has(edge.target().id())); });
  }, [visibleIds, statuses]);

  useEffect(() => {
    const cy = graph.current; if (!cy) return;
    selectedRef.current = selectedId;
    cy.elements().removeClass(FOCUS_CLASSES);
    requestAnimationFrame(() => cy.resize());
    if (!selectedId) return;
    const selected = cy.getElementById(selectedId);
    if (!selected.length) return;
    const focused = focusCollection(cy, selected, focusDepth);
    requestAnimationFrame(() => {
      focused.layout({ name: "breadthfirst", roots: [selected.id()], directed: true, circle: false, grid: false, spacingFactor: 1.25, padding: 30, animate: false }).run();
      cy.resize();
      if (window.matchMedia("(max-width: 800px)").matches) {
        cy.fit(focused, 34);
        cy.zoom(Math.max(cy.minZoom(), cy.zoom() * .62));
        const box = focused.renderedBoundingBox();
        cy.panBy({ x: cy.width() / 2 - (box.x1 + box.x2) / 2, y: cy.height() * .23 - (box.y1 + box.y2) / 2 });
      } else {
        cy.animate({ fit: { eles: focused, padding: 70 }, duration: 360 });
      }
    });
  }, [selectedId, focusDepth]);

  return <div className="graph-canvas" ref={host} aria-label="Interactive Principia knowledge graph" />;
}
