import cytoscape, { type CollectionReturnValue, type Core, type NodeSingular } from "cytoscape";
import { useEffect, useRef } from "react";
import type { GraphData, StatusMap } from "./types";
import { statusColor } from "./graph-utils";

const rootColor = (root: string) => ({ ml:"#8b9cff", math:"#f4c95d", os:"#55d6be", gpu:"#ff8a65", databases:"#d48cff", algorithms:"#65a8ff", networking:"#ff6b91", observability:"#7ee787", languages:"#c9a0ff", "parallel-computing":"#55c2ff" } as Record<string,string>)[root] || "#8b9cff";
const FOCUS_CLASSES = "focus-muted focus-context focus-selected prerequisite-node dependent-node focus-edge prerequisite-edge dependent-edge";

interface Props {
  data: GraphData;
  statuses: StatusMap;
  selectedId: string | null;
  visibleIds: Set<string>;
  focusDepth: 1 | 2;
  onSelect: (id: string) => void;
  onClear: () => void;
}

function directRelations(node: NodeSingular) {
  const prerequisites = node.outgoers("edge");
  const dependents = node.incomers("edge");
  return {
    prerequisiteEdges: prerequisites,
    prerequisiteNodes: prerequisites.targets(),
    dependentEdges: dependents,
    dependentNodes: dependents.sources(),
  };
}

function focusCollection(cy: Core, selected: NodeSingular, depth: 1 | 2): CollectionReturnValue {
  const direct = directRelations(selected);
  let nodes = selected.union(direct.prerequisiteNodes).union(direct.dependentNodes);
  let edges = direct.prerequisiteEdges.union(direct.dependentEdges);
  if (depth === 2) {
    const secondEdges = nodes.connectedEdges();
    const secondNodes = secondEdges.connectedNodes();
    nodes = nodes.union(secondNodes);
    edges = edges.union(secondEdges.filter(edge => nodes.contains(edge.source()) && nodes.contains(edge.target())));
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
    const cy = cytoscape({
      container: host.current,
      elements: [
        ...data.nodes.map(node => ({ data: { id: node.id, label: node.title, root: node.root, rootColor: rootColor(node.root), type: node.type, level: node.level } })),
        ...data.edges.map((edge, index) => ({ data: { id: `e${index}`, source: edge.s, target: edge.t } })),
      ],
      minZoom: .08, maxZoom: 3.2, wheelSensitivity: .18,
      style: [
        { selector: "node", style: { "background-color": "data(rootColor)", "border-width": 1.5, "border-color": "#667085", label: "data(label)", color: "#dce7f7", "font-size": 8, "min-zoomed-font-size": 6, "text-opacity": .68, "text-outline-width": 2, "text-outline-color": "#0b1020", "text-valign": "bottom", "text-margin-y": 6, width: 16, height: 16 } },
        { selector: 'node[type="axiom"]', style: { shape: "diamond", width: 12, height: 12 } },
        { selector: "edge", style: { width: .65, "line-color": "#344054", "target-arrow-shape": "none", "curve-style": "bezier", opacity: .22 } },
        { selector: ".filtered", style: { opacity: .025, "text-opacity": 0 } },
        { selector: ".focus-muted", style: { opacity: .035, "text-opacity": 0 } },
        { selector: "node.focus-context", style: { opacity: .78, "text-opacity": .9 } },
        { selector: "node.prerequisite-node", style: { opacity: 1, "border-width": 4, "border-color": "#f5b942", "text-opacity": 1, "z-index": 12 } },
        { selector: "node.dependent-node", style: { opacity: 1, "border-width": 4, "border-color": "#55c2ff", "text-opacity": 1, "z-index": 12 } },
        { selector: "node.focus-selected", style: { opacity: 1, "border-width": 5, "border-color": "#ffffff", width: 25, height: 25, "font-size": 11, "text-opacity": 1, "z-index": 20 } },
        { selector: "edge.focus-edge", style: { opacity: .58, width: 1.4, "line-color": "#667085", "target-arrow-color": "#667085", "target-arrow-shape": "triangle", "arrow-scale": .7, "z-index": 8 } },
        { selector: "edge.prerequisite-edge", style: { opacity: 1, width: 3, "line-color": "#f5b942", "target-arrow-color": "#f5b942", "arrow-scale": .95, "z-index": 15 } },
        { selector: "edge.dependent-edge", style: { opacity: 1, width: 3, "line-color": "#55c2ff", "target-arrow-color": "#55c2ff", "arrow-scale": .95, "z-index": 15 } },
      ],
      layout: { name: "cose", animate: false, randomize: true, nodeRepulsion: () => 5600, idealEdgeLength: () => 48, edgeElasticity: () => 80, nestingFactor: 1.2, gravity: .3, numIter: 1000, initialTemp: 180, coolingFactor: .96, minTemp: 1 },
    });
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
    });
    cy.on("mouseout", "node", () => { if (!selectedRef.current) cy.elements().removeClass(FOCUS_CLASSES); });
    graph.current = cy;
    return () => { cy.destroy(); graph.current = null; };
  }, [data]);

  useEffect(() => {
    const cy = graph.current; if (!cy) return;
    cy.nodes().forEach(node => {
      node.toggleClass("filtered", !visibleIds.has(node.id()));
      node.style("border-color", statusColor(statuses[node.id()]?.status));
      node.style("border-width", statuses[node.id()]?.status && statuses[node.id()]?.status !== "not_started" ? 4 : 1.5);
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
